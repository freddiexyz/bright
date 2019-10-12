GST = 0.15

MAX_CLAIMS = 50

SDSC = {'name' : 'SDSC',
        'plannum'      : 1,
        'claimform'    : 32,
        'pa_claimform' : 21}

OHSA = {'name' : 'OHSA',
        'plannum'       : 7,
        'claimform'    : 33,
        'pa_claimform' : 35}

deciles = {
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

teeth = {'1': '18', '10': '22', '11': '23', '12': '24', '13': '25', '14': '26', '15': '27', '16': '28', '17': '38', '18': '37', '19': '36', '2': '17', '20': '35', '21': '34', '22': '33',
        '23': '32', '24': '31', '25': '41', '26': '42', '27': '43', '28': '44', '29': '45', '3': '16', '30': '46', '31': '47', '32': '48', '4': '15', '5': '14', '6': '13', '7': '12', '8': '11',
        '9': '21', 'A': '55', 'B': '54', 'C': '53', 'D': '52', 'E': '51', 'F': '61', 'G': '62', 'H': '63', 'I': '64', 'J': '65', 'K': '75', 'L': '74', 'M': '73', 'N': '72', 'O': '71', 'P': '81',
        'Q': '82', 'R': '83', 'S': '84', 'T': '85'}

create_view_claims_waiting = '''
CREATE VIEW _claims_waiting AS
SELECT
    c.claimnum AS claimnum,
    p.patnum AS patnum,
    p.fname AS first_name,
    p.lname AS last_name,
    p.birthdate AS birthdate,
    p.ssn AS NHI,
    p.gender AS gender,
    p.address AS address,
    p.city AS city,
    p.schoolname AS school,
    ins.subscriberid,
    c.priorauthorizationnumber AS prior_approval
FROM claim c
INNER JOIN patient p ON c.patnum = p.patnum
INNER JOIN inssub ins ON c.inssubnum = ins.inssubnum
WHERE c.claimstatus = 'W'
'''

create_view_get_procedures = '''
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