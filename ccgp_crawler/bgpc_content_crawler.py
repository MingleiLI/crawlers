# -*- coding: utf8 -*-
from selenium import webdriver
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

class crawl_ccgp(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        self.ds.set_page_load_timeout(8)
    
    def crawl_list(self, title, target_link):
        file_name = ''
        '''
        gg_types = ['需求', '招标', '更正', '中标', '废标']
        gg_cur_type = '其它'
        for item in gg_types:
            if item in title:
                gg_cur_type = item
                break
        '''
        
        
        self.ds.get(target_link)
        gg_cur_type = self.ds.find_element_by_xpath('//a[@class="current"]').text.strip().encode('utf-8')
        text1 = self.ds.find_element_by_xpath('//div[@class="content-right-details-top"]/p').text
        date = text1.strip().split()[0].strip()
        if u'：' in date:
            date = date.split(u'：')[1].strip()
        elif ':' in date:
            date = date.split(':')[1].strip()
        file_name = gg_cur_type
        file_name = file_name + '_' + date.encode('utf-8')
        file_name = file_name + '_' + title
        print file_name
        text2 = self.ds.find_element_by_xpath('//div[@class="content-right-details-content"]').get_attribute('innerHTML')
        text2text = self.ds.find_element_by_xpath('//div[@class="content-right-details-content"]').text
        outfile = open('./bgpc_raw_html/' + file_name, 'w')
        print >> outfile, str(text2.encode('utf-8'))
        outfile.close()
        outfile = open('./bgpc_raw_txt/' + file_name + '.txt', 'w')
        print >> outfile, str(text2text.encode('utf-8'))
        outfile.close()
        self.ds.get('www.google.com')
                                            
        
        


if __name__ == "__main__":
    
    #outfile = open('ccgp_list_' + str(cur_thr_index) + '.txt', 'a')
    
    count = 0
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    infile = open('bgpc_list_it_new')
    for n, line in enumerate(infile):
        #if n < 837:
        #    continue
        
        #outfile = open('./text_data_bgpc_20170713/' + str(n), 'w')
        fail_count = 0
        while(fail_count < 5):
            try:
                title, target_link = line.strip().split('|')
                #print >> outfile, title
                #print >> outfile, '=========='
                print 'Crawling Page ' + str(n) 
                crawl_ccgp(phantom_driver).crawl_list(title, target_link)
                break
            
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times at page ' + str(n)