# -*- coding: utf8 -*-
import glob
files = glob.glob('./text_data_ccgp/*')
#items = set()
bgpc_it = set()
infile = open('ccgp_list_it')
for line in infile:
    bgpc_it.add(line.strip())

    
jiafang = ['采购人', '采购单位', '招标人', '招标单位']
shijian = ['招标公告日期', '定标日期', '磋商公告及磋商文件发布日期', '确定成交的日期', '谈判公告及谈判文件发布日期', '合同履行日期', '确定成交日期']
zhongbiaochangshang = ['中标人', '中标供应商', '成交供应商', '中标单位', '中标候选人']
jine = ['金额', '价']
zhaobiaoneirong = ['项目名称', '招标内容', '采购项目性质或用途', '招标货物名称及数量', '采购货物或服务名称及数量']


def get_info(titles, line):
    for item in titles:
        if item in line[0]:
            if line[1].strip() != '':
                return line[1]
    return 'NA'

def get_info_v2(titles, line, next_line):
    for title in titles:
        for n, item in enumerate(line):
            if title in item:
                return next_line[n]
    return 'NA'

def get_info_list(line, next_line):
    line = line.strip().split()
    if len(line) > 3:
        next_line = next_line.strip().split()
        if len(line) == len(next_line):
            jf = get_info_v2(jiafang, line, next_line)
            sj = get_info_v2(shijian, line, next_line)
            zb = get_info_v2(zhongbiaochangshang, line, next_line)
            je = get_info_v2(jine, line, next_line)
            nr = get_info_v2(zhaobiaoneirong, line, next_line)
            return [jf, sj, zb, je, nr]
        else:
            return 0
    else:
        return 0
def merge_info(list1, list2):
    new_list = []
    for n, item in enumerate(list1):
        if item == 'NA' and list2[n] != 'NA':
            new_list.append(list2[n])
        else:
            new_list.append(item)
    return new_list
            

outfile = open('ccgp_it_result.csv', 'w')
print >> outfile, '标题' + '\t' + '甲方' + '\t' + '时间' + '\t' + '中标厂商' + '\t' + '金额' + '\t' + '招标内容'


for file_name in files:
    #info = open('./text_data_bgpc/' + file_name)
    info = open(file_name)
    #print info
    company_info = {}
    company_info['title'] = 'NA'
    company_info['jf'] = 'NA'
    company_info['sj'] = 'NA'
    company_info['zb'] = 'NA'
    company_info['je'] = 'NA'
    company_info['nr'] = 'NA'
    
    for n, line in enumerate(info):
        if n == 0:
            company_info['title'] = line.strip()
            continue
        if ':' in line:
            line = line.strip().split(':', 1)
        elif '：'in line:
            line = line.strip().split('：', 1)
        else:
            continue
            
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        
        jf = get_info(jiafang, line)
        if jf != 'NA':
            company_info['jf'] = jf
            #print jf
            continue
        
        sj = get_info(shijian, line)
        if sj != 'NA':
            company_info['sj'] = sj
            continue
            
        zb = get_info(zhongbiaochangshang, line)
        if zb != 'NA':
            company_info['zb'] = zb
            continue
            
        je = get_info(jine, line)
        if je != 'NA':
            company_info['je'] = je
            continue
            
        nr = get_info(zhaobiaoneirong, line)
        if nr != 'NA':
            company_info['nr'] = nr
            continue
    
    info.close()
    info = open(file_name)
    final_list = [company_info['jf'],company_info['sj'],company_info['zb'],company_info['je'],company_info['nr']]
    changed = False
    for n, line in enumerate(info):
        try:
            next_line = next(info)
        except:
            break
        info_list = get_info_list(line, next_line)
        if info_list != 0:
            final_list = merge_info(final_list, info_list)
            changed = True
            break
    
    if changed:
        #print 'changed'
        company_info['jf']=final_list[0]
        company_info['sj']=final_list[1]
        company_info['zb']=final_list[2]
        company_info['je']=final_list[3]
        company_info['nr']=final_list[4]
    
    
            
        
    
    strtmp = company_info['title'] + '\t' + company_info['jf'] + '\t' + company_info['sj'] + '\t' + company_info['zb'] + '\t' + company_info['je'] + '\t' + company_info['nr']
    if company_info['title'] != 'NA':
        line = company_info['title']
        #if '电脑' in line or '服务器' in line or '笔记本' in line or '软件' in line or '机房' in line:
        print >>outfile, strtmp
