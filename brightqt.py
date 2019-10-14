# import reportlab.pdfgen
# import openpyxl
import argparse
import _secret
import config
import records
import sys

SDSC = config.SDSC
OHSA = config.OHSA
#TODO: ACC

class Database(records.Database):

    def __init__(self):
        super().__init__('mysql://{userpass}@{host}/{database}'.format(**_secret.db_login))


class Claim():
    def __init__(self, patient, procedures):
        self.patient        = patient
        self.procedures     = procedures
        self.fee = sum(proc['fee'] for proc in self.procedures)

    def __len__(self):
        return len(self.procedures)

    def __str__(self):
        return f"{self.patient['last_name']}, {self.patient['first_name']}\n\t" +\
            "\n\t".join("{code} | {quantity} | {fee}".format(**proc) for proc in self.procedures)

    @classmethod
    def from_waiting(cls, db, carrier):
        patients = db.query('''
            SELECT cw.* # claimnum, patnum, first_name, last_name, birthdate, nhi,
                        # gender, address, city, school, subscriberid, prior_approval
            FROM _claims_waiting cw
            INNER JOIN claim c ON cw.claimnum = c.claimnum
            WHERE c.plannum = {plannum}
            AND c.claimform in ({claimform}, {pa_claimform})
            '''.format(**carrier))
        procedures = db.query('''
            SELECT c.claimnum, gp.* # procnum, code, proc_date, fee, quantity, teeth
            FROM _get_procedures gp
            INNER JOIN claimproc cp on gp.procnum = cp.procnum
            INNER JOIN claim c on cp.claimnum = c.claimnum
            WHERE c.plannum = {plannum}
            AND c.claimform in ({claimform}, {pa_claimform})
            '''.format(**carrier))
        for patient in patients:
            # merge sort dual indicies merge
            yield cls(patient, tuple(procs for procs in procedures if procs['claimnum'] == patient['claimnum']))

        
class Summary():
    def __init__(self, claims):
        self.claims = tuple(claims)
        self.total = sum(claim.fee for claim in self.claims)
        self.GST = self.total * config.GST
        self.total_inc_GST = self.total + self.GST


if __name__ == '__main__':
    with Database() as db:
        for claim in (Claim.from_waiting(db, SDSC)):
            print(claim)