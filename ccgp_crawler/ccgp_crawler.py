#coding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import time
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
target_link_1 = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index='
#bidType=1 招标公告
#bigType=7 中标公告
target_link_2 ='&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=1&dbselect=bidx&kw=%E6%9C%8D%E5%8A%A1%E5%99%A8&start_time=2013%3A01%3A01&end_time=2017%3A07%3A05&timeType=6'
index_range = 204
thread_num = 1


class crawl_ccgp(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        
    def crawl_list(self, target_link, outfile):
        print target_link
        self.ds.get(target_link)
        #time.sleep(3)
        #outfileee = open('test.html', 'w')
        #print >> outfileee, self.ds.page_source.encode('utf-8')
        items = self.ds.find_elements_by_xpath('//ul[@class="vT-srch-result-list-bid"]/li/a')
        locs = self.ds.find_elements_by_xpath('//ul[@class="vT-srch-result-list-bid"]/li/span/a')
        #print items
        for n, item in enumerate(items):
            #print item
            link = item.get_attribute('href')
            text = item.text.strip()
            loc = locs[n].text.strip()
            #print loc
            print >> outfile, str(text.encode('utf-8')) + '|' + str(link.encode('utf-8')) + '|' + str(loc.encode('utf-8'))
                                            
        
        


if __name__ == "__main__":
    cur_thr_index = int(sys.argv[1])
    start_index = (cur_thr_index-1) * index_range + 1
    end_index = cur_thr_index * index_range
    outfile = open('ccgp_list_fuwuqi_gkzb_' + str(cur_thr_index) , 'a')
    i = start_index
    
    #Set Headers
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
               }

    for key, value in enumerate(headers):
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    service_args = []
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    phantom_driver.implicitly_wait(10)
    phantom_driver.set_page_load_timeout(8)
    phantom_driver.maximize_window()
    
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
                
