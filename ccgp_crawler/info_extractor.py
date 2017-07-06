#encoding = utf-8
import glob
files = glob.glob('./text_data/*')
for file_name in files:
    info = open(file_name)#2068
    found = False
    for n, line in enumerate(info):
        line = line.strip.split(':')
        if "采购人" in line[0]:
            if len(line) > 1:
                print line[1]
            else:
                print info[n+1]
            found = True
            break
    if found == False:
        print 'fail'