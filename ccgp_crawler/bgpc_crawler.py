#encoding = utf-8
from selenium import webdriver
import sys
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
target_link_1 = 'http://www.bgpc.gov.cn/defaults/news/news/page/'
target_link_2 ='%2Ftid%2F9'
index_range = 509
thread_num = 1


class crawl_ccgp(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        self.ds.set_page_load_timeout(8)
    
    def crawl_list(self, target_link, outfile):
        self.ds.get(target_link)
        items = self.ds.find_elements_by_xpath('//div[@class="content-right-content-center"]/li/a')
        for item in items:
            link = item.get_attribute('href')
            text = item.text.strip()
            print >> outfile, str(text.encode('utf-8')) + '|' + str(link)
                                            
        
        


if __name__ == "__main__":
    cur_thr_index = int(sys.argv[1])
    start_index = (cur_thr_index-1) * index_range + 1
    end_index = cur_thr_index * index_range
    outfile = open('bgpc_list_all_' + str(cur_thr_index) + '.txt', 'a')
    i = start_index
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    while i <= end_index:
        print 'Crawling Page ' + str(i) 
        target_link = target_link_1 + str(i) + target_link_2
        fail_count = 0
        while(fail_count < 10):
            try:
                crawl_ccgp(phantom_driver).crawl_list(target_link, outfile)
                break
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times at page ' + str(i)
        i += 1
                
