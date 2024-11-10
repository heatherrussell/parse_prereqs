import requests                                
import json

calendar_url = 'https://uvic.kuali.co/api/v1/catalog/courses/65eb47906641d7001c157bc4'

response = requests.get(calendar_url)
calendar = json.loads(response.text)

phys_data = [x for x in calendar if x['subjectCode']['name'] == 'PHYS']
#print( phys_data )

phys_pid = [x['pid'] for x in phys_data]

course_url = 'https://uvic.kuali.co/api/v1/catalog/course/65eb47906641d7001c157bc4/'

all_courses = []
for pid in phys_pid:
    response = requests.get(course_url + pid)
    course = json.loads(response.text)
    course_skim = {}
    course_skim['name'] = course['__catalogCourseId']
    course_skim['title'] = course['title']
    if 'preOrCorequisites' in course:
        course_skim['coreqs'] = course['preOrCorequisites']
    else:
        course_skim['coreqs'] = ''
    if 'preAndCorequisites' in course:
        course_skim['prereqs'] = course['preAndCorequisites']
    else:
        course_skim['prereqs'] = ''
    all_courses+=[course_skim]

with open('phys_courses.txt', 'w') as out_file:
     json.dump(all_courses, out_file,indent = 4)