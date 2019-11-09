import json
import time
import requests
import os
from flask import Flask, session, redirect, url_for, escape, request
os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

class ScheduleApiError(Exception):
    '''
    Raised if there is an error with the schedule API.
    '''
    throw Exception

# The base API endpoint
base_url = 'http://umich-schedule-api.herokuapp.com'

# the amount of time to wait for the schedule API
timeout_duration = 25

buildingLocs = {
                    "A&AB" : "Art and Architecture Building", 
                    "AH" : "Angell Hall",                   
                    "A AH" : "Angell Hall",
                    "B AH" : "Angell Hall",
                    "C AH" : "Angell Hall",
                    "D AH" : "Angell Hall",
                    "AL" : "W Walter E. Lay Automotive Lab",
                    "ALH" : "Alice Lloyd Hall",
                    "ANNEX" : "Public Policy Annex, 1015 E. Huron",
                    "ARGUS2" : "Argus Building II, Television Center, 408 S. Fourth Street",
                    "ARGUS3" : "Argust Building III, 416 S. Fourth Street",
                    "ARR" : "",
                    "BAM HALL" : "Blanch Anderson Moore Hall, School of Music",
                    "BELL POOL" : "Margaret Bell Pool, Central Campus Recreational Building",
                    "BEYST" : "Bob and Betty Beyster Building",
                    "BIOL STAT" : "Biological Station",
                    "BMT" : "Burton Memorial Tower",
                    "BOT GARD" : "Matthaei Botanical Gardens, Dixboro Road",
                    "BSRB" : "Biomedical Science Research Building",
                    "BURS" : "Bursley Hall",
                    "BUS" : "Business Administration",
                    "CAMP DAVIS" : "Camp Davis",
                    "CCL" : "Clarence Cook Little Building",
                    "CCRB" : "Central Campus Recreational Building",
                    "CHEM" : "Chemistry Building",
                    "CHRYS" : "Chrysler Center",
                    "COMM PARK" : "Commerce Park",
                    "COOL" : "Cooley Building",
                    "COUZENS" : "Couzens Hall",
                    "CPH" : "Children's Psychiatric Hospital",
                    "CRISLER" : "Crisler Arena",
                    "CCSB" : "Campus Safety Service Building, 1239 Kipke Dr.",
                    "DANA" : "Dana Building",
                    "DANCE" : "Dance Building, 1310 N University Court",
                    "DC" : "Duderstadt Center",
                    "DENN" : "David M. Dennison Building",
                    "DENT" : "Dental Building",
                    "DOW" : "Dow Engineering Building",
                    "E-BUS" : "Executive Education",
                    "EECS" : "Electrical Engineering and Computer Science Building",
                    "EH" : "East Hall",
                    "EQ" : "East Quadrangle",
                    "ERB1" : "Engineering Research Building 1",
                    "ERB2" : "Engineering Reseach Building 2",
                    "EWRE" : "Environmental and Water Resources Engineering Building", 
                    "FA CAMP" : "Fresh Air Camp, Pinckney",
                    "FORD LIB" : "Ford Library",
                    "FXB" : "Francois-Xavier Bagnoud Building",
                    "GFL" : "Gorguze Family Laboratory",
                    "GGBL" : "G. G. Brown Laboratory",
                    "GLIBN" : "Harlan Hatcher Graduate Library",
                    "HH" : "Haven Hall",
                    "HUTCH" : "Hutchins Hall",
                    "IM POOL" : "Intramural Building",
                    "IOE" : "Industrial and Operations Engineering Building",
                    "ISR" : "Institute for Social Research",
                    "K-BUS" : "Kresge Library",
                    "KEC" : "Kellogg Eye Center",
                    "KEENE THTR EQ" : "Keene Theater, Residential College",
                    "KELSEY" : "Kelsey Museum of Archaeology", 
                    "KHRI" : "Kresge Hearing Research Institute",
                    "LANE" : "Lane Hall",
                    "LBME" : "Lurie Biomedical Engineering Building",
                    "LEAG" : "Michigan League",
                    "LEC" : "Lurie Engineering Center",
                    "LLIB" : "Law Library",
                    "LORCH" : "Lorch Hall",
                    "LSA" : "Literature, Science, and the Arts Building",
                    "LSI" : "Life Sciences Institute",
                    "LSSH" : "Law School South Hall",
                    "MARKLEY" : "Mary Markley Hall",
                    "MAX KADE" : "Max Kade House, 627 Oxford Street",
                    "MH" : "Mason Hall",
                    "MHRI" : "Mental Health Research Institute",
                    "1 MLB" : "Modern Languages Building",
                    "2 MLB" : "Modern Languages Building",
                    "3 MLB" : "Modern Languages Building",
                    "4 MLB" : "Modern Languages Building",
                    "5 MLB" : "Modern Languages Building",
                    "MLB" : "Modern Languages Building",
                    "MONREOCTY HD" : "Monroe County Health Department",
                    "MOSHER" : "Mosher Jordan Hall",
                    "MOTT" : "C. S. Mott Children's Hospital",
                    "MSC1" : "Medical Science, Building I",
                    "MSC2" : "Medical Science, Building II",
                    "MSRB3" : "Medical Science Research, Building III",
                    "NAME" : "Naval Architecture Marine Engineering Building",
                    "NCRB" : "North Campus Recreational Building",
                    "NIB" : "300 North Ingalls Building",
                    "400NI" : "400 North Ingalls Building",
                    "NORTHVILLEPH" : "Northville State Hospital",
                    "NQ" : "North Quad",
                    "NS" : "Edward Henry Kraus Natural Science Building",
                    "OBL" : "Observatory Lounge, 1402 Washington Heights",
                    "PALM" : "Palmer Commons",
                    "PHOENIXLAB" : "Phoenix Memorial Laboratory",
                    "PIER" : "Pierpont Commons", 
                    "POWER CTR" : "Power Center for the Performing Arts",
                    "RACK" : "Horace H. Rackham, School of Graduate Studies",
                    "RAND" : "Randall Laboratory",
                    "R-BUS" : "Ross School of Business Building",
                    "REVELLI" : "350 HOOVER AVE",
                    "ROSS AC" : "Stephen M. Ross Academic Center",
                    "RUTHVEN" : "A. G. Ruthven Museums Building",
                    "SCHEM" : "1200 STATE ST",
                    "SEB" : "School of Education Building",
                    "SHAPIRO" : "Shapiro UnderGraduate Library", 
                    "SM" : "Earl V. Moore Building, School of Music",
                    "SNB" : "School of Nursing Building",
                    "SPH1" : "Henry Vaughan Building, School of Public Health I",
                    "SPH2" : "Thomas Francis, Jr Building, School of Public Health II",
                    "SRB" : "Space Research Building",
                    "SSWB" : "School of Social Work Building",
                    "STAMPS" : "Stamps Auditorium",
                    "STB" : "202 THAYER ST", 
                    "STJOSEPH HOSP" : "St. Joseph Mercy Hospital",
                    "STOCKWELL" : "Stockwell Hospital",
                    "STRNS" : "Sterns Building",
                    "TAP" : "Tappan Hall",
                    "TAUBL" : "1135 Catherine St",
                    "TISCH" : "Tisch Hall",
                    "TBA" : "",
                    "UM HOSP" : "University Hospital",
                    "UMMA" : "University of Michigan Museum of Art",
                    "UNION" : "Michigan Union",
                    "USB" : "Undergraduate Science Building",
                    "UTOWER" : "University Towers, 1225 S. University",
                    "VETERANSHOSP" : "Veterans Administration Hospital",
                    "WASHCTY HD" : "Washtenaw County Health Department",
                    "W-BUS" : "Wyly Hall",
                    "WDC" : "Charles R. Walgreen, Jr. Drama Center",
                    "WEILL" : "Joan and Sanford Weill Hall",
                    "WEIS" : "Weiser Hall",
                    "WEISER" : "Weiser Hall",
                    "WH" : "West Hall",
                    "WOMEN'S HOSP" : "Women's Hospital",
                    "WQ" : "West Quad"
   }

def get_data(relative_path):
    '''
    Gets data from the schedule API at the specified path.
    Will raise a ScheduleApiError if unsuccessful.
    Assumes API will return JSON, returns as a dictionary.
    '''

    timeout_at = time.time() + timeout_duration

    while time.time() < timeout_at:
        r = requests.get(base_url + relative_path)
        if r.status_code == 200:
            return json.loads(r.text)
        if r.status_code == 400:
            break

    raise ScheduleApiError('error for url: {0} message: "{1}" code: {2}' \
        .format(relative_path, r.text, r.status_code))


def get_terms():
    '''
    Returns a list of valid terms.
    Each item in the list is a dictionary containing:
        ('TermCode', 'TermDescr', 'TermShortDescr')
    '''
    return get_data('/get_terms')


def get_schools(TermCode):
    term_code = str(TermCode)
    urlBeg = '/get_schools?term_code='
    return get_data(urlBeg + term_code)


def get_subjects(TermCode, SchoolCode):
    term_code = str(TermCode)
    urlPrefix = '/get_subjects?term_code='
    urlSchool = '&school='
    return get_data(urlPrefix + term_code + urlSchool + SchoolCode)

def get_catalog_numbers(TermCode, SchoolCode, SubjectCode):
    term_code = str(TermCode)
    urlPrefix = '/get_catalog_numbers?term_code='
    urlSchool = '&school='
    urlSubject = '&subject='
    return get_data(urlPrefix + TermCode + urlSchool + SchoolCode + urlSubject + SubjectCode)



def get_course_description(TermCode, SchoolCode, Subject, CatalogNum):
    term_code = str(TermCode)
    urlTerm = '/get_course_description?term_code=' + TermCode
    urlSchool = '&school=' + SchoolCode
    urlSubject = '&subject=' + Subject
    urlCatalog = '&catalog_num=' + CatalogNum
    urlTotal = urlTerm + urlSchool + urlSubject + urlCatalog
    return get_data(urlTotal)

def get_section_nums(TermCode, SchoolCode, Subject, CatalogNum):
    urlTerm = '/get_section_nums?term_code=' + str(TermCode)
    urlSchool = '&school=' + SchoolCode
    urlSubject = '&subject=' + Subject
    urlCatalog = '&catalog_num=' + str(CatalogNum)
    urlTotal = urlTerm + urlSchool + urlSubject + urlCatalog
    return get_data(urlTotal)

def get_section_details(TermCode, SchoolCode, Subject, CatalogNum, SectionNum):
    urlTerm = '/get_section_details?term_code=' + str(TermCode)
    urlSchool = '&school=' + SchoolCode
    urlSubject = '&subject=' + Subject
    urlCatalog = '&catalog_num=' + CatalogNum
    urlSection = '&section_num=' + str(SectionNum)
    urlTotal = urlTerm + urlSchool + urlSubject + urlCatalog + urlSection
    return get_data(urlTotal)

def get_meetings(TermCode, SchoolCode, Subject, CatalogNum, SectionNum): 
    urlTerm = '/get_meetings?term_code=' + str(TermCode)
    urlSchool = '&school=' + SchoolCode
    urlSubject = '&subject=' + Subject
    urlCatalog = '&catalog_num=' + CatalogNum
    urlSection = '&section_num=' + str(SectionNum)
    urlTotal = urlTerm + urlSchool + urlSubject + urlCatalog + urlSection    

    return get_data(urlTotal)

def get_instructors(TermCode, SchoolCode, Subject, CatalogNum, SectionNum): 
    urlTerm = '/get_instructors?term_code=' + str(TermCode)
    urlSchool = '&school=' + SchoolCode
    urlSubject = '&subject=' + Subject
    urlCatalog = '&catalog_num=' + CatalogNum
    urlSection = '&section_num=' + str(SectionNum)
    urlTotal = urlTerm + urlSchool + urlSubject + urlCatalog + urlSection

    return get_data(urlTotal)

def get_course_title(TermCode, SchoolCode, SubjectCode, CatalogNum):
    #FIX THIS STRING
    title_course = 'Oops'
    catalog_list = {}
    catalog_list = get_catalog_numbers(TermCode, SchoolCode, SubjectCode)
    for i in catalog_list:
        if str(i["CatalogNumber"]) == CatalogNum:
            title_course = i["CourseTitle"]
    return title_course

def get_subject_descr(TermCode, SchoolCode, SubjectCode):
    subject_descr = "It didn't work"
    subject_list = {}
    subject_list = get_subjects(TermCode, SchoolCode)
    for i in subject_list:
        if i["SubjectCode"] == SubjectCode:
            subject_descr = i["SubjectDescr"]
    return subject_descr

def get_school_descr(TermCode, SchoolCode):
    school_descr = "It didn't work"
    school_list = {}
    school_list = get_schools(TermCode)
    for i in school_list:
        if i["SchoolCode"] == SchoolCode:
            school_descr = i["SchoolDescr"]
    return school_descr

def get_location_info(locAbbrev):
    location = buildingLocs.get(locAbbrev)
    if not location:
        location = "University of Michigan"
    return location

''' In Construction: '''
'''
def teacher_info(): 
    teacherInfo = {}
    url = 'http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Michigan&schoolID=1258&queryoption=TEACHER'
    *** tutorial courtesy of docs.python-guide.org ***
    page = requests.get(url)
    tree = html.fromstring(page.content)
    teacherInfo['TeacherRatings'] = tree.xpath('//span[@class="rating"]/text()').extract()
    
    return teacherInfo
    '''

def get_term_descr(TermCode):

    term_descr = 'It did not work'
    term_list = {}
    term_list = get_terms()
    for i in term_list:
        if i['TermCode'] == int(TermCode):
            term_descr = i['TermDescr']
    return term_descr