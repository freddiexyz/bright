GST = 0.15

MAX_CLAIMS = 1

# for reportlabs default A4 page
left_margin_1 = 36
left_margin_2 = 310

proc_line_height = 280
proc_line_height_pa = 168
proc_line_step = 18

proc_date_width = 36
proc_code_width = 90
proc_quantity_width = 320
proc_teeth_width = 360
proc_fee_width = 445

SDSC_form_coords = {
    'patient' : {
        'NHI' : (left_margin_1, 717, {'charSpace' : 11}),
        'birthdate' : (left_margin_1, 678, {'charSpace' : 11}),
        'school' : (left_margin_1, 590,),
        'city' : (left_margin_1, 550),
        'last_name' : (left_margin_2, 717),
        'first_name' : (left_margin_2, 678),
        'address' : (left_margin_2, 630),
        # 'provider' : (),
        'prov_city' : (left_margin_2, 550)
    },
    'procedures' : {
        'date' : (proc_date_width, proc_line_height),
        'code' : (proc_code_width, proc_line_height),
        'quantity' : (proc_quantity_width, proc_line_height),
        'teeth' : (proc_teeth_width, proc_line_height),
        'fee' : (proc_fee_width, proc_line_height,)
    },
    'procedures_pa' : {
        'date' : (proc_date_width, proc_line_height_pa),
        'code' : (proc_code_width, proc_line_height_pa),
        'quantity' : (proc_quantity_width, proc_line_height_pa),
        'teeth' : (proc_teeth_width, proc_line_height_pa),
        'fee' : (proc_fee_width, proc_line_height_pa)
    },
    'prior_approval' : (),
    'total' : (proc_fee_width, 80)
}

OHSA_form_coords = {
    'patient' : {

    },
    'capitated' : {

    },
    'procedures' : {

    },
    'procedures_pa' : {
    
    },
    'prior_approval' : (),
    'total' : ()
}

SDSC = {
    'name' : 'SDSC',
    'plannum' : 1,
    'claimform' : 32,
    'pa_claimform' : 21,
    'form_img' : 'resources\\SDSC_claimform.jpg',
    'form_length' : 5,
    'form_length_pa' : 5,
    'form_coords' : SDSC_form_coords
}

OHSA = {
    'name' : 'OHSA',
    'plannum' : 7,
    'claimform' : 33,
    'pa_claimform' : 35,
    'form_img' : 'resources\\OHSA_claimform.jpg',
    'form_length' : 8,
    'form_length_pa': 6,
    'form_coords' : OHSA_form_coords
}

schools = {
    #CDC
    (".*CDC", ".*CLINIC", ".*CDS", ".*CC$", "REFER FROM SELF") : 0,
    #Aidanfield Christian School
    ("AIDANFIELD",) : 8,
    #Akaroa Area School
    ("AKAROA",) : 8,
    #Allencale Special School and Res Centre
    ("ALLENVALE",) : 6,
    #Amuri Area School
    ("AMURI",) : 8,
    #Ao Tawhiti Unlimited Discovery
    ("AO TAWHITI", "DISCOVERY", "UNLIMITED") : 7,
    #Ashburton Christian School
    ("ASHBURTON\s+CHRISTIAN",) : 6,
    #Ashburton College
    ("ASHBURTON\sCOLLEGE",) : 6,
    #Avonside GHS
    ("AVONSIDE",) : 6,
    #Burnside High School
    ("BURNSIDE",) : 8,
    #Cashmere High School
    ("CASHMERE",) : 8,
    #Cathedral College
    ("CATHEDRAL", "CATHOLIC\sCATHEDRAL") : 4,
    #Christs College
    ("CHRIST('?S)?(\sCOLLEGE)?", "CHRISTS$", "SYRUPS") : 10,
    #Christchurch Boys High School
    ("CBHS", "CHRISTCHURCH\sBOY", "BOYS\sHIGH", "CH.*CH\sBOY") : 10,
    #Christchurch Girls High School
    ("CGHS", "CHRISTCHURCH\sGIRL", "GIRLS\sHIGH", "CH.*CH\sGIRL") : 9,
    #CPIT
    ("CPIT", "ARA$") : 5,
    #Craighead
    ("CRAIGHEAD",) : 9,
    #Darfield High School
    ("DARFIELD",) : 9,
    #Ellesmere College
    ("ELLESMERE",) : 8,
    #Ferndale School
    ("FERNDALE",) :4,
    #Greymouth High School
    ("GREYMOUTH",) : 4,
    #Haeata Community Campus
    ("HAEATA",) : 1,
    #Hagley Community College
    ("HAGLEY",) : 6,
    #Halswell Residential College
    ("HALSWELL\sRES",) : 2,
    #Hillmorton High School
    ("HILL?MORTON",) : 4,
    #Hillview Christian School
    ("HILLVIEW",) : 7,
    #Home Schooled
    ("HOME",) : 5,
    #Hornby High School
    ("HORNBY",) : 3,
    #Hurunui College
    ("HURUNUI",) : 7,
    #Kaiapoi High School
    ("KAIAPOI",) : 7,
    #Kaikoura High School
    ("KAIKOURA",) : 4,
    #Kimihia Parent's College
    ("KIMIHIA",) : 1,
    #Lincoln High School
    ("LINCOLN",) : 10,
    #Linwood College
    ("LINWOOD",) : 3,
    #Mairehau High School
    ("MAIREHAU",) : 4,
    #Marian College
    ("MARIAN",) : 8,
    #Middleton Grange School
    ("MIDDLETON",) : 9,
    #Mount Hutt College
    ("MOUNT\sHUTT", "MT\sHUTT") : 9,
    #None/Unknown
    ("N/?A",) : 5,
    #Oxford Area School
    ("OXFORD AREA",) : 7,
    #Papanui High School
    ("PAPANUI",) : 7,
    #Rangi Ruru Girls' School
    ("RANGI\s",) : 10,
    #Rangiora High School
    ("RANGIORA\sHIGH", "RANGIORA\sHS") : 9,
    #Rangiora New Life School
    ("RANGIORA\sNEW",) : 9,
    #Riccarton High School
    ("RICCARTON",) : 6,
    #Rolleston College
    ("ROLLESTON",) : 10,
    #Rudolf Steiner
    ("RUDOLF",) : 8,
    #Shirley High School
    ("SHIRLEY", "SHIRELY") : 6,
    #St Andrews College
    ("STAC", "ST\sANDREW") : 10,
    #St Bedes College
    ("ST\sBEDE",) : 9,
    #St Margarets
    ("ST\sMARG",) : 10,
    #St Thomas
    ("ST\sTHOMAS",) : 8,
    #Te Kura Correspondance School
    ("TE\sKURA",) : 4,
    #University
    (".*UNIVERSITY",) : 5,
    #Villa Maria
    ("VILLA\sMARIA",) : 9,
    #Vision College
    ("VISION",) : 5,
    #Working
    ("WORKING",) : 5
}

# conversion from american notation to normal one
teeth = {
    '1': '18', '10': '22', '11': '23', '12': '24', '13': '25', '14': '26',
    '15': '27', '16': '28', '17': '38', '18': '37', '19': '36', '2': '17',
    '20': '35', '21': '34', '22': '33', '23': '32', '24': '31', '25': '41',
    '26': '42', '27': '43', '28': '44', '29': '45', '3': '16', '30': '46',
    '31': '47', '32': '48', '4': '15', '5': '14', '6': '13', '7': '12', '8': '11',
    '9': '21', 'A': '55', 'B': '54', 'C': '53', 'D': '52', 'E': '51', 'F': '61', 
    'G': '62', 'H': '63', 'I': '64', 'J': '65', 'K': '75', 'L': '74', 'M': '73',
    'N': '72', 'O': '71', 'P': '81', 'Q': '82', 'R': '83', 'S': '84', 'T': '85'
        }

create_view_claims_waiting = '''
DROP VIEW _claims_waiting;\n''' +\
'''
CREATE VIEW _claims_waiting AS
SELECT
    c.claimnum AS claimnum,
    c.claimform AS claimform,
    p.patnum AS patnum,
    p.fname AS first_name,
    p.lname AS last_name,
    p.birthdate AS birthdate,
    p.ssn AS NHI,
    p.gender AS gender,
    p.address AS address,
    p.city AS city,
    p.schoolname AS school,
    ins.subscriberid AS subnum,
    c.priorauthorizationnumber AS prior_approval
FROM claim c
INNER JOIN patient p ON c.patnum = p.patnum
INNER JOIN inssub ins ON c.inssubnum = ins.inssubnum
WHERE c.claimstatus = 'W';
'''

create_view_get_procedures = '''
DROP VIEW _get_procedures;\n''' +\
'''
CREATE VIEW _get_procedures AS
SELECT
    pl.procnum AS procnum,
    cp.codesent as code,
    pl.ProcDate as proc_date,
    sum(pl.ProcFee) as fee,
    count(*) as quantity,
    GROUP_CONCAT(pl.ToothNum) as teeth
FROM procedurelog pl
INNER JOIN claimproc cp on pl.procnum = cp.procnum
INNER JOIN claim c on cp.claimnum = c.claimnum
WHERE c.claimstatus = 'W'
GROUP BY c.claimnum, pl.procdate, cp.codesent, pl.procfee
'''

SELECT_PATIENTS = '''
SELECT cw.* # claimnum, patnum, first_name, last_name, birthdate, nhi,
            # gender, address, city, school, subscriberid, prior_approval
FROM _claims_waiting cw
INNER JOIN claim c ON cw.claimnum = c.claimnum
WHERE c.plannum = {plannum}
AND c.claimform in ({claimform}, {pa_claimform})
ORDER BY claimnum;
'''

SELECT_PROCEDURES = '''
SELECT c.claimnum, gp.* # procnum, code, proc_date, fee, quantity, teeth
FROM _get_procedures gp
INNER JOIN claimproc cp on gp.procnum = cp.procnum
INNER JOIN claim c on cp.claimnum = c.claimnum
WHERE c.plannum = {plannum}
AND c.claimform in ({claimform}, {pa_claimform})
ORDER BY c.claimnum;
'''
