# -*- coding: utf8 -*-
import glob
#files = glob.glob('../text_data_ccgp_fuwuqi_gkzb/*_table')
files = glob.glob('../text_data_ccgp_fuwuqi_zbgg/*_table')
#item_list = ["采购人联系方式","采购人","采购项目名称","采购单位","获取招标文件时间","行政区域","采购单位联系方式","品目","获取招标文件的地点","项目联系人","公告时间","代理机构地址","预算金额","采购单位地址","采购人地址","开标时间","项目联系电话","代理机构名称","代理机构联系方式","开标地点","招标文件售价"]
item_list = ["中标日期","采购人联系方式","采购人","评标委员会成员名单","采购项目名称","总成交金额","采购单位","行政区域","采购单位联系方式","谈判小组、询价小组成员名单及单一来源采购人员名单","成交日期","品目","项目联系人","公告时间","代理机构地址","评审专家名单","总中标金额","采购单位地址","采购人地址","本项目招标公告日期","项目联系电话","代理机构名称","定标日期","代理机构联系方式"]
#outfile = open('ccgp_fuwuqi_gkzb.csv', 'w')
outfile = open('ccgp_fuwuqi_zbgg.csv', 'w')

strtmp = '中标题目' + '\t' + '地域'
for item in item_list:
    strtmp = strtmp + '\t' + item
print >> outfile, strtmp

for _, file in enumerate(files):
    #if _ > 10:
    #    break
    title_list = []
    content_list = []
    infile = open(file)
    titleee = ''
    location = ''
    
    for n, line in enumerate(infile):
        if n == 0:
            titleee = line.strip()
            continue
        if n == 1:
            location = line.strip()
            continue
        if n == 2: #======
            continue
        line = line.strip().split('\t', 1)
        if "货物" in line or "服务" in line or "附件" in line:
            continue
        if len(line) < 2:
            continue
        title_list.append(line[0].strip())
        if line[1].strip() != '公告时间' and line[1].strip() != '中标日期' and line[1].strip() != '定标日期':
            content_list.append(line[1].strip())
    content_len = len(content_list)
    com_dic = {}
    for n, title in enumerate(title_list):
        if n < content_len:
            if title in item_list:
                if content_list[n] != '详见公告正文':
                    com_dic[title] = content_list[n]
    if len(com_dic) < 3:
        continue
    strtmp = titleee + '\t' + location
    for item in item_list:
        if item in com_dic:
            strtmp = strtmp + '\t' + com_dic[item].strip()
        else:
            strtmp = strtmp + '\t' + 'NA'
    print >> outfile, strtmp.strip()
        