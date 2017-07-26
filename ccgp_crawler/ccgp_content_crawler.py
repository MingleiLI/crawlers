#coding=utf-8
from selenium import webdriver
import time
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

class crawl_ccgp(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        
    
    def crawl_list(self, target_link, outfile_table, outfile_detail):
        self.ds.get(target_link)
        time.sleep(3)
        try:
            titles = self.ds.find_elements_by_xpath('//td[@class="title"]')
            contents = self.ds.find_elements_by_xpath('//td[@class="title"]/following-sibling::td')
            for n, title in enumerate(titles):
                title = title.text.encode('utf-8')
                content = contents[n].text.encode('utf-8')
                strtmp = title + '\t' + content
                print >> outfile_table, strtmp
            button = self.ds.find_element_by_xpath('//span[@id="displayGG"]')
            button.click()
        except:
            print 'No Table!'
            
        text = self.ds.find_element_by_xpath('//div[@class="vT_detail_content w760c"]').text
        print >> outfile_detail, str(text.encode('utf-8'))
                                            
        
        


if __name__ == "__main__":
    
    #outfile = open('ccgp_list_' + str(cur_thr_index) + '.txt', 'a')
    
    count = 0
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
    
    infile = open('ccgp_list_fuwuqi_zbgg_1')
    for n, line in enumerate(infile):
        #if n < 116:
        #    continue
        outfile_table = open('./text_data_ccgp_fuwuqi_zbgg/' + str(n) + '_table', 'w')
        outfile_detail = open('./text_data_ccgp_fuwuqi_zbgg/' + str(n) + '_detail', 'w')
        title, target_link, loc = line.strip().split('|')
        
        print >> outfile_table, title
        print >> outfile_table, loc
        print >> outfile_table, '=========='
        print >> outfile_detail, title
        print >> outfile_detail, loc
        print >> outfile_detail, '=========='
        print 'Crawling Page ' + str(n) 
        print target_link
        fail_count = 0
        while(fail_count < 5):
            try:
                crawl_ccgp(phantom_driver).crawl_list(target_link, outfile_table, outfile_detail)
                break
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times at page ' + str(n)
        outfile_table.close()
        outfile_detail.close()
                
