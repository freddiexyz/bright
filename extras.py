import bright
from bright import config, A4, draw, _secret

lvl3 = 'level_three'
lvl4 = 'level_four'

GET_PROCS = '''
SELECT
    c.claimnum as claimnum,
    pl.procnum AS procnum,
    cp.codesent as code,
    pl.ProcDate as proc_date,
    sum(pl.ProcFee) as fee,
    count(*) as quantity,
    GROUP_CONCAT(pl.ToothNum) as teeth
FROM procedurelog pl
INNER JOIN claimproc cp on pl.procnum = cp.procnum
INNER JOIN claim c on cp.claimnum = c.claimnum
WHERE c.claimnum in (SELECT claimnum from {})
GROUP BY c.claimnum, pl.procdate, cp.codesent, pl.procfee
ORDER BY c.patnum
'''

GET_PATS = '''
SELECT *
FROM {}
ORDER BY patnum
'''

form_coords_comment = (140, 280)
fcc = form_coords_comment

msg1 = 'Emergency Care'
msg2 = 'COVID-19 Prep and clean-up'

class Claim(bright.Claim):

    @classmethod
    def level4(cls, db, carrier):
        patients = db.query(GET_PATS.format(lvl4)).all(as_dict=True)
        procedures = db.query(GET_PROCS.format(lvl4)).all(as_dict=True)

        return cls.merge(patients, procedures, carrier)

    @classmethod
    def level3(cls, db, carrier):
        patients = db.query(GET_PATS.format(lvl3)).all(as_dict=True)
        procedures = db.query(GET_PROCS.format(lvl3)).all(as_dict=True)

        return cls.merge(patients, procedures, carrier)

    def to_page(self, cvs, procs):
        # TODO: tickboxes
        width, height = A4
        cvs.drawImage(self.carrier['form_img'], 0,0, width=width, height=height) # fullpage image
        pat_coords = self.carrier['form_coords']['patient']
        if self.is_pa:
            proc_coords = self.carrier['form_coords']['procedures_pa']
            draw(cvs, self.patient['prior_approval'],
                *self.carrier['form_coords']['prior_approval'])
        else:
            proc_coords = self.carrier['form_coords']['procedures']

        cvs.setFont('Courier', 12) # courier since monospaced
        for field, coords in pat_coords.items():
            draw(cvs, self.patient[field], *coords)

        cvs.setFont('Courier', 10) # so it will fit
        for num, proc in enumerate(procs):
            for field, coords in proc_coords.items():
                # lowers height of each line by set amount each procedure
                draw(cvs, str(proc[field]), coords[0], coords[1]-(num*config.proc_line_step))
                if proc['code'] == 'CON4':
                    draw(cvs, msg1, fcc[0],fcc[1]-(num*config.proc_line_step))
                elif proc['code'] in ('MS01','MS02'):
                    draw(cvs, msg2, fcc[0],fcc[1]-(num*config.proc_line_step))

        draw(cvs, self.patient['fee'], *self.carrier['form_coords']['total'])
        cvs.setFont('Courier', 50)
        draw(cvs, '.', *(18, 458))
        cvs.showPage()

class Summary(bright.Summary):

    @classmethod
    def level4(cls, db, carrier):
        cls.db = db
        claims = list(Claim.level4(cls.db, carrier))

        return cls(claims, carrier, 'BSCOVID1')

    @classmethod
    def level3(cls, db, carrier):
        cls.db = db
        claims = list(Claim.level3(cls.db, carrier))

        return cls(claims, carrier, 'BSCOVID1')

    def to_summary(self, cvs):
        width, height = A4
        cvs.drawImage(self.carrier['summary_img'], 0,0, width=width, height=height)
        cvs.setFont('Courier', 12)

        for field, value in _secret.practice_details.items():
            draw(cvs, value, *config.summary_coords[field])

        draw(cvs, 'BSCOVID2',         *config.summary_coords['claim_reference'])
        draw(cvs, len(self),          *config.summary_coords['num_patients'])
        draw(cvs, self.total_inc_GST, *config.summary_coords['fee_inc'])
        draw(cvs, self.total,         *config.summary_coords['fee_ex'])
        draw(cvs, self.GST,           *config.summary_coords['GST'])
        cvs.drawImage('D:\\jo_sig.jpg',75, 75, 250, 75)
        
        date_coords = (350, 115, {'charSpace' : 17})
        date = '14032021'
        draw(cvs, date, *date_coords)

        cvs.showPage()
        # cvs.save()
        return cvs

if __name__ == '__main__':
    with bright.Database() as db:
        test = Summary.level4(db, config.SDSC)
        claim_ref = 'BSCOVID1'
        filename = config.FILENAME_FORMAT.format(
            payee_num = _secret.practice_details['payee_number'],
            claim_ref = claim_ref,
            claim_type = 'SDSC',
            num_patients = len(test))
        cvs = bright.canvas.Canvas(f'.\\test_output\\{filename}.pdf', pagesize=bright.A4)
        test.to_forms(cvs)
        cvs.save()
