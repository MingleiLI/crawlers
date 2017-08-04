# -*- coding: utf-8 -*-

"""
Update Proxy List; Should be updated everyday
"""


from selenium import webdriver
import random
import requests
import time

phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
#phantomjs_path = '/home/gwang3/software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/intr/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outtr/'
free_proxy_base_url = 'http://www.kuaidaili.com/free/inha/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outha/'

test_url = 'http://icanhazip.com/'
#test_url = 'http://www.baidu.com'
#test_url = 'http://gsxt.saic.gov.cn/'
#test_url = 'http://gsxt.gdgs.gov.cn/'

#Check if a proxy works
def check_proxy_validity(ip_port):
    print ip_port
    #Set Headers
    headers = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
               }

    for key, value in enumerate(headers):
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    #service_args = ['--proxy=' + ip_port, '--proxy-type=socks5', ]
    service_args = ['--proxy=' + ip_port, '--proxy-type=http', ]
    # service_args = []
    ds = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    #ds.implicitly_wait(10)
    ds.set_page_load_timeout(5)
    ds.maximize_window()

    try:
        ds.get(test_url)
        time.sleep(5)
        
        print ds.page_source
       
        if ds.find_element_by_xpath('//body/pre').text == ip_port.split(':')[0]:
            print ip_port + ': Success'
            ds.close()
            return True
        else:
            ds.close()
            return False
    except Exception as e:
        print e
        #print ip_port + ': Fail'
        ds.close()
        return False

#Update proxy list
def update_proxy_list(outfile_buffer_name = 'proxy_list_buffer',\
                      outfile_name = 'proxy_list', maxnum = 100):
    ip_proxy_set = set()
    outfile_buffer = open(outfile_buffer_name, 'w')
    outfile = open(outfile_name, 'w')

    df = webdriver.PhantomJS(executable_path=phantomjs_path)

   #list_end = False
    list_num = 0

    while 1:
        try:
            list_num = list_num + 1
            print 'Crawling list No. ' + str(list_num)
            df.get(free_proxy_base_url + str(list_num))
            ip_list = df.find_elements_by_xpath('//div[@id="list"]/table/tbody/tr')
            for ip_element in ip_list:
                ip = ip_element.find_element_by_xpath('.//td[@data-title="IP"]').text
                port = ip_element.find_element_by_xpath('.//td[@data-title="PORT"]').text
                ip_port = str(ip).strip() + ':' + str(port).strip()
                #print ip_port
                if check_proxy_validity(ip_port) == True:
                    print ip_port + ' Success'
                    ip_proxy_set.add(ip_port)
                    print >> outfile_buffer, ip_port

            #If enough proxies are found then break
            if len(ip_proxy_set) > maxnum:
                break
                
        except Exception as e:
            print str(e)
            print "List End! Crawled " + str(len(ip_proxy_set)) + "free proxies!"
            break

    for ip_port in ip_proxy_set:
        print >> outfile, ip_port

    return list(ip_proxy_set)

#Update proxy list from kuaidaili api
def update_proxy_list_api(outfile_name = 'proxy_list'):
    r = requests.get('http://dps.kuaidaili.com/api/getdps/?orderid=997633218150329&num=20&ut=1&sep=2')
    ip_list = r.text.split()
    outfile = open(outfile_name, 'w')
    ip_final_list = []
    for ip_port in ip_list:
        if check_proxy_validity(ip_port) == True:
            #print ip_port + ' Success'
            print >> outfile, ip_port
            ip_final_list.append(ip_port)
    return ip_final_list



#Load IP Proxy List
def load_ip_proxy_list(infile_name):
    ip_list = []
    try:
        infile = open(infile_name)
        for line in infile:
            ip_list.append(line.strip())
    except:
        pass
    return ip_list

#Return a random proxy from the ip list
def get_random_proxy(ip_list):
    length = len(ip_list)
    random_num = random.randint(0, length-1)
    return ip_list[random_num]


def get_phantomjs_with_random_proxy(ip_list):
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
    if len(ip_list) != 0:
        ip_port = get_random_proxy(ip_list)
        print ip_port
        service_args = ['--proxy=' + ip_port, '--proxy-type=http', ]
    ds = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(10)
    ds.maximize_window()
    return ds

def get_chrome_with_random_proxy(ip_list):
    #PROXY = "120.199.224.78:80"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1904x950')
    chrome_options.add_argument('disable-gpu')
    if len(ip_list) > 0:
        ip_port = get_random_proxy(ip_list)
        chrome_options.add_argument('--proxy-server=%s' % ip_port)
    driver = webdriver.Chrome("/home/gwang3/software/chromedriver",chrome_options = chrome_options)
    return driver


#Get ip from abuyun
def get_chrome_with_abuyun_proxy():
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "xxxxxxxxxxxxxxx"
    proxyPass = "xxxxxxxxxxxxxxx"

    service_args = [
        "--proxy-type=http",
        "--proxy=%(host)s:%(port)s" % {
            "host" : proxyHost,
            "port" : proxyPort,
        },
        "--proxy-auth=%(user)s:%(pass)s" % {
            "user" : proxyUser,
            "pass" : proxyPass,
        },
    ]
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('/home/gwang3/software/chromedriver',chrome_options = chrome_options, service_args=service_args)
    return driver



if __name__ == '__main__':
    update_proxy_list_api()
