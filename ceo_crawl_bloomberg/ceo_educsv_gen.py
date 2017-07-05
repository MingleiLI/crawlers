#!/user/bin/env python
# coding:utf-8
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import collections

infile = open('ceo_dicts_all')
outfile = open('ceo_crawled_education.csv', 'w')
item_list = ['name','title','company','Career History','Corporate Information','Personal Information','Awards & Publications','Memberships']
#print >> outfile, 'name,title,company,Career History,Corporate Information,Personal Information,Awards & Publications,Memberships'
print >> outfile, 'name,title,company,education(University;Degree;Major;Year|University2...)'
#edu_dic = {}
#ceo_edu_list = []
major_set = set()

for n, line in enumerate(infile):
    #if n > 50:
    #    break
    if n % 10000 == 0:
        print n
    ceo_info = json.loads(line)
    ceo_dict = {}
    for item in ceo_info:
        ceo_dict[item[0]] = item[1] 
    
    if 'Personal Information' in ceo_dict:
        if 'Education' in ceo_dict['Personal Information'][0]:
            edu_str = '' #University;Degree;Major;Year|University...
            try:
                edu_info = ceo_dict['Personal Information'][0].split('\n\n\n\n')[1]
            except Exception as e:
                #print ceo_dict['Personal Information'][0]
                #print e
                continue
            edu_info = edu_info.split('\n\n\n')
            for item in edu_info:
                #Each item is an education info
                if 'Show More' not in item:
                    university = ''
                    degree = ''
                    major = ''
                    year = ''
                    item = item.split('\n')
                    university = item[0]
                    if len(item) > 1:
                        details = item[1].split(',')
                        for detail in details:
                            detail = detail.strip()
                            if '19' in detail or '20' in detail or '16' in detail or 'PRESENT' == detail:
                                year = detail
                            elif 'Degree' in detail or 'PhD' in detail or 'Graduated' in detail or 'MBA' in detail \
                            or 'JD' == detail or 'MASTER' in detail or 'DOCTOR' in detail or 'Diploma' in detail \
                            or 'DOCTORATE' in detail or 'BACHELOR' in detail or 'MD' == detail or 'Masters' in detail\
                            or 'Post-Graduate' in detail:
                                degree = detail
                            else:
                                major = detail
                                major_set.add(major)
                edu_str = edu_str + university + ';' + degree + ';' + major + ';' + year + '|'
                                
                        
                        
                    
            try:
                print >> outfile, ceo_dict['name'] + ',' + ceo_dict['title'] + ',' + ceo_dict['company'] + ',' + edu_str.strip('|')
            except Exception as e:
                #print e
                pass
                                           
                                              
for item in major_set:
    print item
    
            