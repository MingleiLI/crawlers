# -*- coding: utf-8 -*-
infile = open('ccgp_list')
outfile = open('ccgp_list_it', 'w')
for n, line in enumerate(infile):
    #if n % 1000 == 0:
    #    print n
    if '电脑' in line or '服务器' in line or '笔记本' in line:
        print >> outfile, line.strip()