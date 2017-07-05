#!/user/bin/env python
# coding:utf-8
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
ceo_list = []
ceo_edu_dic = {}

def check_name(name):
    name_tmp = name.strip().split()
    if len(name) <= 5:
        return False
    if len(name_tmp) == 1:
        return False
    if name_tmp[0] == name_tmp[1]:
        return False
    
    else:
        return True


#Import Existing Info
infile = open('ceo_crawled_education.csv')
for n, line in enumerate(infile):
    if n == 0:
        continue
    line = line.strip().split(',')
    name = line[0].upper()
    if check_name(name):
        education = line[3]
        ceo_list.append(name)
        ceo_edu_dic[name] = education

infile.close()    


target_edu_dic = {}
#Read Target File and Fuzzy Wuzzy
infile = open('1996-2006.csv')
outfile = open('1996-2006_edu.csv', 'w')
#infile = open('2007-2017.csv')
#outfile = open('2007-2017_edu.csv', 'w')
for n, orgline in enumerate(infile):
    if n == 0:
        continue
    #if n > 100:
    #    break
    if n % 100 == 0:
        print n
    line = orgline.strip().split(',')
    fullname = line[-1]
    #fullname = line[1]
    if fullname not in target_edu_dic:
        target_edu_dic[fullname] = 'None'
        result = process.extractOne(fullname, ceo_list, scorer=fuzz.token_set_ratio)
        print fullname
        print result
        if result == None:
            continue
        if result[1] > 95:
            target_edu_dic[fullname] = ceo_edu_dic[result[0]]
    print >> outfile, orgline.strip() + ',' + target_edu_dic[fullname]
        
        
        
    
    