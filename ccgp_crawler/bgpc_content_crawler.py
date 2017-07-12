#encoding = utf-8
from selenium import webdriver
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

class crawl_ccgp(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        self.ds.set_page_load_timeout(8)
    
    def crawl_list(self, target_link, outfile):
        self.ds.get(target_link)
        text = self.ds.find_element_by_xpath('//div[@class="content-right-details-content"]').text
        print >> outfile, str(text.encode('utf-8'))
        self.ds.get('www.google.com')
                                            
        
        


if __name__ == "__main__":
    
    #outfile = open('ccgp_list_' + str(cur_thr_index) + '.txt', 'a')
    
    count = 0
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    infile = open('bgpc_list_it')
    for n, line in enumerate(infile):
        #if n < 837:
        #    continue
        
        outfile = open('./text_data_bgpc/' + str(n), 'w')
        fail_count = 0
        while(fail_count < 5):
            try:  
                title, target_link = line.strip().split('|')
                print >> outfile, title
                print >> outfile, '=========='
                print 'Crawling Page ' + str(n) 
                crawl_ccgp(phantom_driver).crawl_list(target_link, outfile)
                break
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times at page ' + str(n)
        outfile.close()
                
