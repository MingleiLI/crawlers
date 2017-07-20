# -*- coding: utf-8 -*-
#infile = open('ccgp_list')
#outfile = open('ccgp_list_it', 'w')
infile = open('bgpc_list_all')
outfile = open('bgpc_list_it_new', 'w')
for n, line in enumerate(infile):
    #if n % 1000 == 0:
    #    print n
    if '电脑' in line or '服务器' in line or '笔记本' in line or '软件' in line or '机房' in line or '计算' in line or '信息' in line or '数据' in line or '系统' in line or '网络' in line:
        #print >> outfile, n
        print >> outfile, line.strip()