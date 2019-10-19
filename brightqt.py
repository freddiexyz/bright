from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
# import openpyxl
# import argparse
import _secret
import config
import records
# import sys
# import os
import re


class Database(records.Database):

    def __init__(self):
        super().__init__('mysql://{userpass}@{host}/{database}'.format(**_secret.db_login))


class Claim():

    def __init__(self, patient, procedures, carrier):
        self.patient = patient
        self.patient['birthdate'] = self.patient['birthdate'].strftime("%d%m%Y")
        self.patient['prov_city'] = 'Christchurch'
        self.procedures = procedures
        self.carrier = carrier
        self.missing_info = []
        self.is_pa = (self.patient['claimform'] == self.carrier['pa_claimform'])


        if self.carrier['name'] == 'OHSA':
            #TODO: deal with capitated procedures
            self.patient['decile'] = get_decile(self.patient['school'])

        self.fee = 0
        for proc in self.procedures:
            self.fee += proc['fee']
            proc['fee'] = f"{proc['fee']:.2f}"
            proc['date'] = proc['proc_date'].strftime("%d.%m.%y")
            if proc['teeth']:
                proc['teeth'] = ','.join(config.teeth[tooth] for tooth in proc['teeth'].split(',')\
                 if tooth.isalnum())

    def __len__(self):
        return len(self.procedures)

    def __str__(self):
        return f"{self.patient['last_name']}, {self.patient['first_name']}\n\t" +\
            "\n\t".join("{proc_date} | {code} | {quantity} | {fee:>6.2f} | {teeth}".format(
                **proc) for proc in self.procedures)

    @classmethod
    def gen_from_waiting(cls, db, carrier):
        # claimnum, claimform, patnum, first_name, last_name, birthdate, NHI,
        # gender, address, city, school, subnum, prior_approval
        patients = db.query(config.SELECT_PATIENTS.format(**carrier)).all(as_dict=True)
        # procnum, code, proc_date, fee, quantity, teeth
        procedures = db.query(config.SELECT_PROCEDURES.format(**carrier)).all(as_dict=True)

        # merge sort dual indicies, requires lists sorted by claimnum
        proc_index = 0
        for patient in patients:
            patient_procs = [procedures[proc_index]]
            proc_index += 1
            try:
                while procedures[proc_index]['claimnum'] == patient['claimnum']:
                    patient_procs.append(procedures[proc_index])
                    proc_index += 1
            except IndexError: # exhausted all procedures
                pass
            yield cls(patient, patient_procs, carrier)

    def validate(self):
        # prior approval claims need prior approval numbers
        if self.is_pa and not self.patient['prior_approval']:
            self.missing_info.append('prior_approval')
        # all claims need valid NHIs
        if not check_nhi(self.patient['NHI']):
            self.missing_info.append('NHI')
        # SDSC claims need referral numbers
        if self.carrier['name'] == 'SDSC' and not check_cds_ref(self.patient['subnum']):
            self.missing_info.append('subnum')
        # check for presence of required fields
        for field in ('first_name', 'last_name', 'birthdate', 'address', 'city', 'school'):
            if not self.patient[field]:
                self.missing_info.append(field)
        # OHSA claims need deciles
        if self.carrier['name'] == 'OHSA' and not self.patient['decile']:
            self.missing_info.append('decile')
            # TODO: match decile to DBCON code/fee to ensure correct decile band being claimed
        return not self.missing_info

    def to_form(self, cvs):
        form_length = self.carrier['form_length_pa'] if self.is_pa else self.carrier['form_length']
        for page_num in range(((len(self) - 1) // form_length) + 1):
            procs = self.procedures[page_num*form_length:(page_num+1)*form_length] #what
            self.to_page(cvs, procs)

    def to_page(self, cvs, procs):
        width, height = A4
        cvs.drawImage(self.carrier['form_img'], 0,0, width=width, height=height) # fullpage image
        cvs.setFont('Courier', 12)
        for field, coords in self.carrier['form_coords']['patient'].items():
            cvs.drawString(coords[0], coords[1], self.patient[field], **coords[2])
        cvs.setFont('Courier', 10) # so it will fit
        proc_coords = 'procedures_pa' if self.is_pa else 'procedures'
        for num, proc in enumerate(procs):
            for field, coords in self.carrier['form_coords'][proc_coords].items():
                cvs.drawString(coords[0], coords[1]-(num*config.proc_line_step), str(proc[field]))

        if self.is_pa:
            coords = self.carrier['form_coords']['prior_approval']
            cvs.drawString(coords[0], coords[1], self.patient.prior_approval)
        coords = self.carrier['form_coords']['total']
        cvs.drawString(coords[0], coords[1], str(self.fee))
        cvs.showPage()


        
class Summary():
    def __init__(self, claims):
        self.claims = tuple(claims)
        self.total = sum(claim.fee for claim in self.claims)
        self.GST = self.total * config.GST
        self.total_inc_GST = self.total + self.GST

    def __len__(self):
        return len(self.claims)

    def __str__(self):
        return f'Number of Patients: {len(self)}' +\
            f'\nTotal: {self.total:>8.2f}' +\
            f'\nGST: {self.GST:>8.2f}' +\
            f'\nTotal inc GST: {self.total_inc_GST:>8.2f}'

    @classmethod
    def from_waiting(cls, db, carrier):
        claims = []
        gen = Claim.gen_from_waiting(db, carrier)
        while len(claims) < config.MAX_CLAIMS:
            claim = next(gen)
            if claim.validate():
                claims.append(claim)
        return cls(claims)

    def to_forms(self, filename):
        cvs = canvas.Canvas(f'.\\test_output\\{filename}.pdf', pagesize=A4)
        for claim in self.claims:
            claim.to_form(cvs)
        cvs.save()
        return cvs


def check_nhi(nhi):
    '''Uses the check digit to verify that NHI is valid'''
    alpha = 'ABCDEFGHJKLMNPQRSTUVWXYZ' # does not contain 'I' or 'O'
    nhi = str(nhi).upper().strip()
    if not re.fullmatch(f'^[{alpha}]{{3}}[\d]{{4}}$', nhi): # matches pattern AAANNNN
        return False
    # Parity check maths
    sum_letters = sum((str.find(alpha, str(nhi[i])) + 1) * (7-i) for i in range(3))
    sum_numbers = sum(int(nhi[i]) * (7-i) for i in range(3,6))
    total = sum_letters + sum_numbers
    check = 11 - (total % 11)
    if check == 11 or check % 10 != int(nhi[6]):
        return False
    return True

def check_cds_ref(ref_num):
    '''Matches referral number to known patterns
    ######-[SED/SBD] or SED-049-#### or SED17[NHI]'''
    ref_num = ref_num.strip().upper()
    if ref_num == '.':
        return True
    if re.fullmatch('^\d{6}[-|\s]?[A-Z]{3}.*', ref_num):
        return True
    if re.fullmatch('^SED-\d{3}-\d{4}$', ref_num):
        return True
    if re.fullmatch('^(SED|SDB)\d{2}[-|\s]?[A-Z]{3}\d{4}$', ref_num):
        return True
    return False

def get_decile(pat_school):
    '''Attempts to match a given school to know schools'''
    for school in config.schools:
        if any(re.fullmatch(f"^{pattern}.*$", pat_school.upper().strip()) for pattern in school):
            return config.schools[school]
    return 0 # placeholder for not found or N/A


if __name__ == '__main__':
    with Database() as db:
        Summary.from_waiting(db, config.SDSC).to_forms('test')
