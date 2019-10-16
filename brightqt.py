# import reportlab.pdfgen
# import openpyxl
import argparse
import _secret
import config
import records
import sys
import re

class Database(records.Database):

    def __init__(self):
        super().__init__('mysql://{userpass}@{host}/{database}'.format(**_secret.db_login))


class Claim():

    def __init__(self, patient, procedures, carrier):
        self.patient = patient
        self.procedures = procedures
        self.carrier = carrier
        self.fee = 0
        self.missing_info = []

        for proc in self.procedures:
            self.fee += proc['fee']
            proc['date'] = proc['proc_date'].strftime("%d.%m.%y")
            # if teeth := proc['teeth']: 3.8 when
            if proc['teeth']:
                proc['teeth'] = ','.join(config.teeth[tooth] for tooth in proc['teeth'].split(',') if tooth.isalnum())

    def __len__(self):
        return len(self.procedures)

    def __str__(self):
        return f"{self.patient['last_name']}, {self.patient['first_name']}\n\t" +\
            "\n\t".join("{proc_date} | {code} | {quantity} | {fee:>6.2f} | {teeth}".format(**proc) for proc in self.procedures)

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
        if self.patient['claimform'] == self.carrier['pa_claimform'] and not self.patient['prior_approval']:
            self.missing_info.append('prior_approval')
        if not check_nhi(self.patient['NHI']):
            self.missing_info.append('NHI')
        if not check_cds_ref(self.patient['subnum']):
            self.missing_info.append('subnum')
        return not self.missing_info

        
class Summary():
    def __init__(self, claims):
        self.claims = tuple(claims)
        self.total = sum(claim.fee for claim in self.claims)
        self.GST = self.total * config.GST
        self.total_inc_GST = self.total + self.GST

    def __str__(self):
        return f'Number of Patients: {len(self.claims)}' +\
            f'\nTotal: {self.total:>8.2f}' +\
            f'\nGST: {self.GST:>8.2f}' +\
            f'\nTotal inc GST: {self.total_inc_GST:>8.2f}'

def check_nhi(nhi):
    '''Uses the check digit to verify that NHI is valid'''
    alpha = 'ABCDEFGHJKLMNPQRSTUVWXYZ' #does not contain 'I' and 'O'
    nhi = str(nhi).upper().strip()
    if not re.fullmatch('^[A-H|J-N|P-Z]{3}[\d]{4}$', nhi):
        return False
    sum_letters = sum((str.find(alpha, str(nhi[i])) + 1) * (7-i) for i in range(3))
    sum_numbers = sum(int(nhi[i]) * (7-i) for i in range(3,6))
    total = sum_letters + sum_numbers
    check = 11 - (total % 11)
    if check == 11 or check % 10 != int(nhi[6]):
        return False
    return True

def check_cds_ref(ref_num):
    '''######-[SED/SBD] or SED-049-#### or SED17[NHI]'''
    ref_num = ref_num.strip().upper()
    if ref_num == '.':
        return True
    if re.fullmatch('^\d{6}[-|\s]?(SED|SDB|SED/SDB|SDB/SED|ACC)$', ref_num):
        return True
    if re.fullmatch('^SED-\d{3}-\d{4}$', ref_num):
        return True
    if re.fullmatch('^(SED|SDB)\d{2}[-|\s]?[A-H|J-N|P-Z]{3}\d{4}$', ref_num):
        return True
    return False


if __name__ == '__main__':
    with Database() as db:
        print(Summary(Claim.gen_from_waiting(db, config.SDSC)))

        # for claim in (Claim.gen_from_waiting(db, config.SDSC)):
        #     print(claim.validate())