from flask import render_template, request
from app import app
from schedule_api import *

@app.route('/')
def index():
    options = {}

    options['terms'] = get_terms()

    return render_template('index.html', **options)

@app.route('/')
def indexLogin():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/<term_code>')
def school_index(term_code):
    options = {}
    options['schools'] = get_schools(term_code)
    options['term_descr'] = get_term_descr(term_code)
    options['term_code'] = term_code

    return render_template('school_index.html', **options)

@app.route('/<term_code>/<school_code>')
def subject_index(term_code, school_code):
	options = {}

	options['subjects'] = get_subjects(term_code, school_code)
	options['term_code'] = term_code
	options['school_code'] = school_code
	options['school_descr'] = get_school_descr(term_code, school_code)
	

	return render_template('subject_index.html', **options)


@app.route('/<term_code>/<school_code>/<subject_code>')
def catalog_index(term_code, school_code, subject_code):
	options = {}
	temp_list = {}

	options['catalogs'] = get_catalog_numbers(term_code, school_code, subject_code) 
	options['term_code'] = term_code
	options['school_code'] = school_code
	options['subject_code']	= subject_code
	options['subject_descr'] = get_subject_descr(term_code, school_code, subject_code)

	return render_template('catalog_index.html', **options)

@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>')
def course_description_index(term_code, school_code, subject_code, catalog_number):
	options = {}
	options['Description'] = get_course_description(term_code, school_code, subject_code, catalog_number)
	options['catalogs'] = get_catalog_numbers(term_code, school_code, subject_code) 
	options['term_code'] = term_code
	options['school_code'] = school_code
	options['subject_code'] = subject_code
	options['catalog_number'] = catalog_number
	options['Course_Title'] = get_course_title(term_code, school_code, subject_code, catalog_number)

	temp_meetings = []
	options['meetings'] = {}
	options['sectionDetails'] = {}
	sectionNums = get_section_nums(term_code, school_code, subject_code, catalog_number)
	for i in sectionNums:
		options['sectionDetails'][i] = get_section_details(term_code, school_code, subject_code, catalog_number, i)
		temp_meetings = get_meetings(term_code, school_code, subject_code, catalog_number, i)
		options['meetings'][i] = temp_meetings[0]
	options['sections'] = get_section_nums(term_code, school_code, subject_code, catalog_number)


	return render_template('course_description.html', **options)


@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/sections')
def course_sections_display(term_code, school_code, subject_code, catalog_number):
	options = {}

	options['sections'] = get_section_nums(term_code, school_code, subject_code, catalog_number)

	return render_template('section.html', **options)


@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/<section_number>')
def section_details_index(term_code, school_code, subject_code, catalog_number, section_number):
	options = {}

	options['sectionDetails'] = get_section_details(term_code, school_code, subject_code, catalog_number, section_number)
	options['sections'] = get_section_nums(term_code, school_code, subject_code, catalog_number)

	return render_template('section_details_index.html', **options)

@app.route('/<term_code>/<school_code>/<subject_code>/<catalog_number>/<section_number>/meetings')
def meetings_index(term_code, school_code, subject_code, catalog_number, section_number):
	options = {}
	options['lecType'] = ""
	temp_meetings = []
	temp_meetings = get_meetings(term_code, school_code, subject_code, catalog_number, section_number)
	options['meetings'] =  temp_meetings[0]

	temp_instructors = {}
	temp_instructors = get_instructors(term_code, school_code, subject_code, catalog_number, section_number)
	options["Instructors"] = {}
	for i in range(len(temp_instructors)):
		options["Instructors"][i] = temp_instructors[i]

	options['section'] = section_number
	options['subject_code'] = subject_code
	options['catalog_number'] = catalog_number
	options['course_title'] = get_course_title(term_code, school_code, subject_code, catalog_number)


	locToBeParsed = str(options['meetings']["Location"])
	parsedLocation = locToBeParsed[locToBeParsed.find(' ') + 1: len(locToBeParsed)]


	options['Location'] = get_location_info(parsedLocation)


	sectDetails = get_section_details(term_code, school_code, subject_code, catalog_number, section_number) 

	options['lecType'] = sectDetails.get('SectionTypeDescr')

	return render_template('meetings.html', **options)


