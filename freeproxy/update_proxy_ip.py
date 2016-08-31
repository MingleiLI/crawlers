"""
Update Proxy List; Should be updated everyday
"""


from selenium import webdriver
import random

phantomjs_path = '/home/guan/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

#free_proxy_base_url = 'http://www.kuaidaili.com/free/intr/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outtr/'
free_proxy_base_url = 'http://www.kuaidaili.com/free/inha/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outha/'

test_url = 'http://www.baidu.com'

#Check if a proxy works
def check_proxy_validity(ip_port):
    # print ip_port
    service_args = ['--proxy=' + ip_port, '--proxy-type=socks5', ]
    # service_args = []
    ds = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    ds.set_page_load_timeout(5)
    try:
        ds.get(test_url)
        #print ip_port + ': Success'
        ds.close()
        return True
    except:
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
    #df = webdriver.Firefox()

    list_end = False
    list_num = 0

    while not list_end:
        try:
            list_num = list_num + 1
            print 'Crawling list No. ' + str(list_num)
            df.get(free_proxy_base_url + str(list_num))
            ip_list = df.find_elements_by_xpath('//div[@id="list"]/table/tbody/tr')
            for ip_element in ip_list:
                ip = ip_element.find_element_by_xpath('.//td[@data-title="IP"]').text
                port = ip_element.find_element_by_xpath('.//td[@data-title="PORT"]').text
                ip_port = str(ip).strip() + ':' + str(port).strip()
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


#Load IP Proxy List
def load_ip_proxy_list(infile_name):
    ip_list = []
    infile = open(infile_name)
    for line in infile:
        ip_list.append(line.strip())
    return ip_list

#Return a random proxy from the ip list
def get_random_proxy(ip_list):
    length = len(ip_list)
    random_num = random.ranint(0, length)
    return ip_list[random_num]


def get_driver_with_random_proxy(ip_list):
    ip_port = get_random_proxy(ip_list)
    service_args = ['--proxy=' + ip_port, '--proxy-type=socks5', ]
    ds = webdriver.PhantomJS(executable_path=phantomjs_path, service_args=service_args)
    ds.implicitly_wait(10)
    ds.set_page_load_timeout(10)
    ds.maximize_window()
    return ds

'''
if __name__ == '__main__':
	
    update_proxy_list(outfile_buffer_name = 'proxy_list_buffer',\
                      outfile_name = 'proxy_list', maxnum = 100)
'''



    
