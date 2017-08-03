import geetest_cract_gsxt_v2 as geetest
import update_proxy_ip_kuaidaili as driver_util

##Shanghai Gongshang Crawler
target_link = "http://sh.gsxt.gov.cn/notice"


def crawl_company(company_name)
    #ip_list = driver_util.update_proxy_list_api()
    ip_list = driver_util.load_ip_proxy_list("proxy_list")
    fail_count = 0
    while fail_count < 5:
        try:
            driver = driver_util.get_chrome_with_random_proxy([])
            #for i in [u'招商银行', u'交通银行', u'中国银行']:
            #############First Page, Input keyword and get list
            #driver.get("http://www.gsxt.gov.cn/index")
            driver.get(target_link)
            wait = WebDriverWait(driver, 10, 1.0)
            element = wait.until(EC.presence_of_element_located((By.ID, "keyword")))
            element.send_keys(company_name)
            time.sleep(1.1)
            #element = wait.until(EC.presence_of_element_located((By.ID, "btn_query")))
            element = wait.until(EC.presence_of_element_located((By.ID, "buttonSearch")))
            element.click()
            time.sleep(1.1)
            geetest.geetest_go(driver)
            time.sleep(1)
            
            #############Second Page, Get list and click first page
            element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'blue1bg')))
            if len(element) >= 1:
                element[0].click()
            else:
                return -1
            driver.switch_to_window(driver.window_handles[-1])
            wait = WebDriverWait(driver, 8)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'printInfo')))
            element.click()
            time.sleep(1.1)
            geetest.geetest_go(driver)
            time.sleep(1)
            
            #############Third Page, Save print-page source
            driver.switch_to_window(driver.window_handles[-1])
            wait = WebDriverWait(driver, 8)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'printInfo')))
            print >> outfile, driver.page_source.encode('utf-8')
            driver.close()
    
        except Exception as e:
            fail_count += 1
            print e
            #call("kill $(ps ax | grep chromedriver | awk '{print $1}')", shell=True)
            #call("kill $(ps ax | grep chromium | awk '{print $1}')", shell=True)
            time.sleep(5)
            continue
            

if __name__ == '__main__':
    infile = open('shanghai_company_list')
    for line in infile:
        crawl_company(line)