# -*-coding:utf8 -*-

from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')

def save_info(dict_content):
    f.writelines(u'回帖人：' + str(dict_content['user_name']) + '\n')
    f.writelines(u'回帖时间：' + str(dict_content['topic_reply_time']) + '\n')
    f.writelines(u'回帖内容：' + str(dict_content['topic_reply_content']) + '\n\n')

def tieba_spider(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    content_field = selector.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    item = {}
    for each in content_field:
        reply_info = json.loads(each.xpath('@data-field')[0].replace('&quot', ''))
        author = reply_info['author']['user_name']
        reply_time = reply_info['content']['date']
        content = each.xpath('div[@class="d_post_content_main"]/div/cc/'+
                             'div[@class="d_post_content j_d_post_content  clearfix"]/text()')[0]
        item['user_name'] = author
        item['topic_reply_time'] = reply_time
        item['topic_reply_content'] = content
        save_info(item)


if __name__ == '__main__':

    print u'开始抓取...'
    time1 = time.time()
    f = open('result.txt', 'w')
    pool = ThreadPool(4)
    all_pages = []
    for i in range(1, 27):
        page = 'http://tieba.baidu.com/p/3565374963?pn=' + str(i)
        all_pages.append(page)
    results = pool.map(tieba_spider, all_pages)
    pool.close()
    pool.join()
    f.close()
    time2 = time.time()
    print u'抓取完毕...'
    print u'用时： ' + str(time2-time1) + 's'
