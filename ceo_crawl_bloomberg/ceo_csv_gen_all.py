#!/user/bin/env python
# coding:utf-8
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import collections

infile = open('ceo_dicts_all')
outfile = open('ceo_crawled_all_cleaned.csv', 'w')
item_list = ['name','title','company','Career History','Corporate Information','Personal Information','Awards & Publications','Memberships']
print >> outfile, 'name,title,company,Career History,Corporate Information,Personal Information,Awards & Publications,Memberships'
#print >> outfile, 'name,title,company,education(University;Degree;Major;Year|University2...)'


for n, line in enumerate(infile):
    #if n > 50:
    #    break
    if n % 10000 == 0:
        print n
    ceo_info = json.loads(line)
    #print ceo_info
    ceo_dict = {}
    for item in item_list:
        ceo_dict[item] = ''
    try:
        for item in ceo_info:
            ceo_dict[item[0]] = str(item[1]).replace("Show More", "").replace("Address:',", "Address:'").replace("',", "';").replace('u', '').replace('[', '').replace(']', '').replace(',', ' ').replace('\\n\\n\\n\\n', '|').replace("'", "").replace('\\n', ' ').strip('"')
      
        strtmp = ''
        for item in item_list:
            strtmp = strtmp + ceo_dict[item] + ','
        print >> outfile, strtmp.strip(',')
    except Exception as e:
        #print e
        pass
                                           
                                             
    
            