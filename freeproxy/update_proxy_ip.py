from selenium import webdriver

phantomjs_path = '/home/guan/Software/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'

#free_proxy_base_url = 'http://www.kuaidaili.com/free/intr/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outtr/'
free_proxy_base_url = 'http://www.kuaidaili.com/free/inha/'
#free_proxy_base_url = 'http://www.kuaidaili.com/free/outha/'

test_url = 'http://www.baidu.com'
ip_proxy_set = set()


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

def update_proxy_list(outfile_buffer_name, outfile_name):

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

                
        except Exception as e:
            print str(e)
            print "List End! Crawled " + str(len(ip_proxy_set)) + "free proxies!"
            break

    for ip_port in ip_proxy_set:
        print >> outfile, ip_port
         

if __name__ == '__main__':
	
    update_proxy_list('proxy_list_20160831_buffer', 'proxy_list_20160831')



    
