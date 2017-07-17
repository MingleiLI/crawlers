# -*- coding: utf8 -*-
import glob
import os
#files = glob.glob('./text_data_bgpc_20170713/*')
files = glob.glob('./bgpc_raw_txt/*')
#items = set()
#bgpc_it = set()
#infile = open('ccgp_list_it')
#for line in infile:
#    bgpc_it.add(line.strip())


jiafang = ['采购人', '采购单位', '招标人', '招标单位', '委托单位', '采购机构']
shijian = ['招标公告日期', '定标日期', '磋商公告及磋商文件发布日期', '确定成交的日期', '谈判公告及谈判文件发布日期', '合同履行日期', '确定成交日期']
zhongbiaochangshang = ['中标人', '中标供应商', '成交供应商', '中标单位', '中标候选人']
jine = ['金额', '价', '资金']
zhaobiaoneirong = ['项目名称', '招标内容', '采购项目性质或用途', '招标货物名称及数量', '采购货物或服务名称及数量']

institute = ['局','中心', '小学','中学','大学','学校','学院','公司','处', '法院','处','医院','银行','所', '海关']

provinces = ['北京', '天津市', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西','甘肃','青海','台湾','内蒙','广西','西藏','宁夏','新疆']


#zbgg = ['招标编号', '采购编号','项目名称', '委托单位', '集中采购机构全称', '集中采购机构地址', '采购人地址', '项目负责人' ,'招标范围及形式', '简要技术要求 /招标项目的性质', '评标方法和标准',   '招标货物名称及数量' , '价格', '预算资金',  '采购方式', '采购用途', '询标时间', '询标内容', '询标地点', '投标截止时间、开标时间', '投标、开标地点',   ]

zbgg = ['招标公告编号', '招标编号', '采购编号','项目名称', '集中采购机构全称', '集中采购机构地址','采购人名称', '采购人地址', '招标货物名称及数量', '采购用途', '采购方式', '招标范围及形式' , '招标公告日期' , '定标日期','合同履行日期', '预算资金', '中标供应商名称', '中标供应商地址', '中标金额', '评标委员会成员名单','项目负责人']

#gg_types = ['需求', '招标', '更正', '中标', '废标']
gg_item_dic = {}
#for item in gg_types:
#    gg_item_dic[item] = set()
#gg_item_dic['其它'] = set()

item_count = {}

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


def change_amount(input_str):
    strtmp = ''
    for loc in input_str:
        if loc.isdigit() or loc == '.':
            strtmp = strtmp + loc
    try:
        strtmp = float(strtmp)
        if strtmp < 1000:
            strtmp = strtmp * 10000
        return strtmp
    except:
        return 0

def get_year(input_str):
    input_str = input_str.strip().split('年')
    try:
        return int(input_str[0].strip())
    except:
        return 0

def get_province(input_str):
    for item in provinces:
        if item in input_str:
            return item
    return 0

def get_consumer(input_str):
    for item in institute:
        if item in input_str:
            input_str = input_str.strip().split(item)
            return input_str[0].strip() + item       
    return 'NA'

outfile = open('old', 'w')
outfileee = open('bgpc_中标记录.csv', 'w')
#print >> outfile, '标题' + '\t' + '甲方' + '\t' + '时间' + '\t' + '中标厂商' + '\t' + '金额' + '\t' + '招标内容'
strtmp = '标题' + '\t'
for item in zbgg:
    strtmp = strtmp + item + '\t'
print >> outfileee, strtmp.strip()

for file_name in files:
    list_len = len(zbgg) + 1
    gg_info = ['NA'] * list_len
    info = open(file_name)
    #print file_name
    file_name_items = os.path.basename(file_name).strip().strip('.txt').split('_')
    gg_cur_type = file_name_items[0]
    #if gg_cur_type != '招标公告':
    if gg_cur_type != '中标公告':
        continue
    title = file_name_items[2]
    gg_info[0] = title
    for n, line in enumerate(info):
        if ':' in line:
            line = line.strip().split(':', 1)
        elif '：'in line:
            line = line.strip().split('：', 1)
        else:
            continue
            
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        for n, item in enumerate(zbgg):
            if line[0] == item:
                if line[1] != '':
                    gg_info[n+1] = line[1]
                break
    strtmp = ''
    for item in gg_info:
        strtmp = strtmp + item + '\t'
    print >> outfileee, strtmp.strip()
        



for file_name in files:
    #info = open('./text_data_bgpc/' + file_name)
    info = open(file_name)
    print file_name
    file_name_items = os.path.basename(file_name).strip().split('_')
    gg_cur_type = file_name_items[0]
    title = file_name_items[2]
    
    #print info
    company_info = {}
    company_info['title'] = 'NA'
    company_info['jf'] = 'NA'
    company_info['sj'] = file_name_items[1]
    company_info['zb'] = 'NA'
    company_info['je'] = 'NA'
    company_info['nr'] = 'NA'
    
    for n, line in enumerate(info):
        '''
        if n == 0:
            company_info['title'] = line.strip()
            for item in gg_types:
                if item in line:
                    gg_cur_type = item
            if gg_cur_type == '':
                gg_cur_type = '其它'
            continue
        '''
        if ':' in line:
            line = line.strip().split(':', 1)
        elif '：'in line:
            line = line.strip().split('：', 1)
        else:
            continue
            
        line[0] = line[0].strip()
        line[1] = line[1].strip()
        if line[0] not in item_count:
            item_count[line[0]] = 1
        else:
            item_count[line[0]] += 1
        if gg_cur_type != '':
            if gg_cur_type not in gg_item_dic:
                gg_item_dic[gg_cur_type] = set()
            gg_item_dic[gg_cur_type].add(line[0])
        
        jf = get_info(jiafang, line)
        if jf != 'NA':
            company_info['jf'] = jf
            #print jf
            continue
        
        '''
        sj = get_info(shijian, line)
        if sj != 'NA':
            company_info['sj'] = sj
            continue
        '''
        
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
    
    
    if company_info['jf'] == 'NA':
        company_info['jf'] = get_consumer(company_info['title'])
    company_info['je'] = str(change_amount(company_info['je']))
        
    
    strtmp = company_info['title'] + '\t' + company_info['jf'] + '\t' + company_info['sj'] + '\t' + company_info['zb'] + '\t' + company_info['je'] + '\t' + company_info['nr']
    if company_info['title'] != 'NA':
        line = company_info['title']
        #if '电脑' in line or '服务器' in line or '笔记本' in line or '软件' in line or '机房' in line:
        print >>outfile, strtmp
outfile.close()

#Get possible items
outfile = open('items', 'w')
for item in gg_item_dic:
    print >> outfile, '===================='
    print >> outfile, item
    strtmp = ''
    for itemm in gg_item_dic[item]:
        if item_count[itemm] > 100:
            strtmp = strtmp + itemm + '|'
    print >> outfile, strtmp.strip('|')
 
