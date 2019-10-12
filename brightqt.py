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

    db = None # Needs to be set by user

    def __init__(self, claimnum, patient, procedures, prior_approval=None):
        self.claimnum       = claimnum
        self.patient        = patient
        self.procedures     = procedures
        self.prior_approval = prior_approval

        self.fee = sum(proc['fee'] for proc in self.procedures)

    @classmethod
    def from_claimnums(cls, claimnums, is_pa=False):
        if not Claim.db:
            raise Exception('No database connection')

        for claimnum in claimnums:
            patient = Claim.db.query('''
                SELECT p.patnum         as patnum,
                       p.fname          as first_name,
                       p.lname          as last_name,
                       p.birthdate      as birthdate,
                       p.ssn            as NHI,
                       p.gender         as gender,
                       p.address        as address,
                       p.city           as city,
                       p.schoolname     as school,
                       ins.subscriberid as sub_id
                FROM claim c
                INNER JOIN patient p ON c.patnum = p.patnum
                INNER JOIN inssub ins ON c.inssubnum = ins.inssubnum
                WHERE c.claimnum = {claimnum}
                '''.format(claimnum=claimnum))

            procedures = Claim.db.query('''
                SELECT count(*)        as quantity,
                       pl.procdate     as procedure_date,
                       pl.procfee      as fee_ea,
                       sum(pl.procfee) as fee,
                       cp.codesent     as procedure_code,
                       GROUP_CONCAT(pl.toothnum) as teeth
                FROM procedurelog pl
                INNER JOIN claimproc cp on cp.procnum = pl.procnum
                WHERE cp.claimnum = {claimnum}
                GROUP BY procedure_date, procedure_code, fee_ea
                '''.format(claimnum=claimnum))

            if is_pa:
                prior_approval = Claim.db.query('''
                    SELECT PriorAuthorizationNumber
                    FROM claim
                    WHERE claimnum = {claimnum}
                    '''.format(claimnum=claimnum))
                yield cls(claimnum, patient, procedures, prior_approval)

            yield cls(claimnum, patient, procedures)




class Summary():
    def __init__(self, claims):
        self.claims = tuple(claims)[:config.MAX_CLAIMS]
        self.total = sum(claim.fee for claim in self.claims)
        self.GST = self.total * config.GST
        self.total_inc_GST = self.total * (1 + config.GST)


if __name__ == '__main__':
    with Database() as db:
        Claim.db = db
        res = db.query("""
            SELECT claimnum
            FROM claim
            WHERE PlanNum = {plannum} and ClaimStatus = 'W' and claimform = {claimform}""".format(**SDSC))
        claims = Claim.from_claimnums(line['claimnum'] for line in res)
        s = Summary(claims)
    print(f'Patients: {len(s.claims)}',
          f'Total ext GST: {s.total}',
          f'GST: {s.GST}',
          f'Total inc GST: {s.total_inc_GST}',
          sep='\n')