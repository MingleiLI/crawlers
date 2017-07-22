# -*- coding: utf8 -*-
from selenium import webdriver
import sys
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

class crawl_mingluji(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        self.ds.set_page_load_timeout(8)
        self.item_header = ['机构名称', '机构类型', '经营范围', '经济类型', '注册日期', '办证日期', '办证机构', '注册资金', '职工人数', '经济行业', '门类', '大类', '中类', '小类', '法人代表', '长途区号', '电话号码', '中国行政区号', '省份', '地市', '区县', '机构地址', '邮政编码']
    
    def crawl_list(self, title, target_link, outfile):
        self.ds.get(target_link)
        try:
            description = self.ds.find_element_by_xpath('//span[@itemprop="description"]').text.encode('utf-8')
        except:
            description = 'NA'
        items = self.ds.find_elements_by_xpath('//ul/li')
        item_dic = {}
        for item in items:
            strtmp = item.text.encode('utf-8')
            if '：' in strtmp:
                strtmp = strtmp.split('：')
            else:
                continue
            if strtmp[1].strip() != "":
                item_dic[strtmp[0]] = strtmp[1].strip()
        strtmp = ""
        for item in self.item_header:
            if item in item_dic:
                strtmp = strtmp + '\t' + item_dic[item]
            else:
                strtmp = strtmp + '\t' + 'NA'
        strtmp = strtmp + '\t' + description
        print>> outfile, strtmp.strip()
            

if __name__ == "__main__":
    
    
    count = 0
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    file_name = sys.argv[1]
    infile = open('./data/' + file_name )
    outfile = open('./data/' + file_name + '_content', 'w')
    for n, line in enumerate(infile):
        #if n < 837:
        #    continue
        fail_count = 0
        while(fail_count < 5):
            try:
                title, target_link = line.strip().split('|')
                #print >> outfile, title
                #print >> outfile, '=========='
                print 'Crawling Page ' + str(n) 
                crawl_mingluji(phantom_driver).crawl_list(title, target_link, outfile)
                break
            
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times at page ' + str(n)
                
                
                
