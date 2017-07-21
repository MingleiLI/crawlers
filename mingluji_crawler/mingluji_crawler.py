#coding=utf-8
from selenium import webdriver
import sys
phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
target_link = 'https://shanghai.mingluji.com/%E5%88%86%E7%B1%BB:%E4%B8%8A%E6%B5%B7%E5%B8%82'
thread_num = 1


class crawl_mingluji(object):
    def __init__(self, phantom_driver):
        self.ds = phantom_driver
        self.ds.set_page_load_timeout(8)
    
    def find_next_page(self):
        try:
            items = self.ds.find_elements_by_xpath('//a[@title="分类:上海市"]')
            return items[1].get_attribute('href')
        except:
            return -1
    
    
    def crawl_list(self, target_link, outfile):
        self.ds.get(target_link)
        items = self.ds.find_elements_by_xpath('//div[@class="mw-content-ltr"]/div/div/ul/li/a')
        for item in items:
            link = item.get_attribute('href')
            text = item.text.strip()
            print >> outfile, str(text.encode('utf-8')) + '|' + str(link)
        next_page = self.find_next_page()
        fail_count = 0
        while next_page == -1 and fail_count < 50:
            fail_count += 1
            print "Cannot find next page, try again..."
            self.ds.get(target_link)
            next_page = self.find_next_page()
        return next_page



if __name__ == "__main__":
    outfile = open('./data/mingluji_list', 'w')
    phantom_driver = webdriver.PhantomJS(executable_path=phantomjs_path)
    while target_link != -1:
        print 'Crawling Page ' + str(target_link)
        next_link = target_link
        fail_count = 0
        while(fail_count < 10):
            try:
                next_link = crawl_mingluji(phantom_driver).crawl_list(target_link, outfile)
                break
            except Exception as e:
                print e
                fail_count += 1
                print 'Fail ' + str(fail_count) + ' times'
        target_link = next_link
                
