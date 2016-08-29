import selenium

start_link = 'http://www.aastocks.com/tc/ipo/ListedIPO.aspx'

def crawl_hk_ipo():
    ds = selenium.webdriver(phantomjs)
    ds.get(start_link)
    ds.find_element_by_xpath('//body/div[@class = "xxx"]/dic[@class = 'yyy']')


    return 0