#!/user/bin/env python
# coding:utf-8
from cfuzzyset import cFuzzySet as FuzzySet
import re
ceo_list = []
ceo_edu_dic = {}
a = FuzzySet()
count = 0
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
    
def clean_name(name):
    
    todel = [ i.start() for i in re.finditer('"', name)]
    if len(todel) == 2:
        myString = name[0:todel[0]] + name[todel[1]+2:-1]
        #print name + ' --->  ' +  myString 
        return myString
   
    return name

def clean_sin_charac(name):
    name = name.strip().split()
    final_name = ""
    for item in name:
        item = item.strip(".")
        if len(item) >1:
            final_name = final_name+" "+item
    return final_name.strip()

#Import Existing Info
infile = open('ceo_crawled_education.csv')
for n, line in enumerate(infile):
    if n == 0:
        continue
    line = line.strip().split(',')
    name = clean_name(line[0].upper())
    if check_name(name):
        education = line[3]
        #ceo_list.append(name)
        a.add(name)
        ceo_edu_dic[name] = education

infile.close()    


target_edu_dic = {}
#Read Target File and Fuzzy Wuzzy
infile = open('1996-2006.csv')
outfile = open('1996-2006_edu_test.csv', 'w')
#infile = open('2007-2017.csv')
#outfile = open('2007-2017_edu_test.csv', 'w')
for n, orgline in enumerate(infile):
    if n == 0:
        continue
    #if n > 100:
    #    break
    if n % 1000 == 0:
        print n
    line = orgline.strip().split(',')
    fullname = line[-1]
    #fullname = line[1]
    if fullname not in target_edu_dic:
        target_edu_dic[fullname] = 'None'
        try:
            #result = process.extractOne(fullname, ceo_list, scorer=fuzz.token_set_ratio)
            result = a.get(clean_sin_charac(fullname))[0]
            #print fullname
            #print result
        except:
            pass
        if result == None:
            continue
        if result[0] > 0.5:
            print fullname
            print result
            count += 1
            target_edu_dic[fullname] = ceo_edu_dic[result[1]]
    print >> outfile, orgline.strip() + ',' + target_edu_dic[fullname]

    
print "#########################"
print count
        
        
        
    
    