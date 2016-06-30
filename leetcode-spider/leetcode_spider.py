# -*-coding:utf-8-*-

import re
import requests
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Spider:
    def __init__(self):
        pass

    def get_source(self, url):
        html = requests.get(url)
        return html.text

    def get_body(self, source):
        """

        :param source: url对应html文本信息
        :return: 题目所在范围
        """
        topic_body = re.findall('<tbody>(.*?)</tbody>', source, re.S)
        return topic_body[1]  # topic_body包含两个元素，且topic_body内容为空

    def get_all_subjects(self, topic_body):
        """

        :param topic_body: 题目所在范围
        :return: 所有题目范围列表
        """
        all_subjects = re.findall('<tr>(.*?)</tr>', topic_body, re.S)
        return all_subjects

    def get_content(self, each_subject):
        """

        :param each_subject: 每个题目的范围
        :return: 题目信息(编号，题名，准确率，难度)
        """
        subject_info = []
        contents = re.findall('<td>(.*?)</td>', each_subject, re.S)
        subject_no = contents[1]
        subject_name = re.search('>(.*?)</a>', contents[2], re.S).group(1)
        subject_acceptance = contents[3]
        subject_difficulty = re.search('\'>(.*?)</td>', each_subject, re.S).group(1)
        subject_info.append(subject_no)
        subject_info.append(subject_name)
        subject_info.append(subject_acceptance)
        subject_info.append(subject_difficulty)
        return subject_info

    def save_info(self, all_subjects):
        f_easy = open('easy.txt', 'w')
        f_medium = open('medium.txt', 'w')
        f_hard = open('hard.txt', 'w')
        f_easy.writelines('No\tName\tAcceptance\tDifficulty\n')
        f_medium.writelines('No\tName\tAcceptance\tDifficulty\n')
        f_hard.writelines('No\tName\tAcceptance\tDifficulty\n')
        for each_subject in all_subjects:
            result = leetcode_spider.get_content(each_subject)
            if result[3] == 'Easy':
                f_easy.writelines(result[0]+'\t'+result[1]+'\t'+result[2]+'\t'+result[3]+'\n')
            elif result[3] == 'Medium':
                f_medium.writelines(result[0]+'\t'+result[1]+'\t'+result[2]+'\t'+result[3]+'\n')
            else:
                f_hard.writelines(result[0]+'\t'+result[1]+'\t'+result[2]+'\t'+result[3]+'\n')
        f_easy.close()
        f_medium.close()
        f_hard.close()


if __name__ == '__main__':

    print u'开始抓取...'
    time1 = time.time()
    url = 'https://leetcode.com/problemset/algorithms/'
    leetcode_spider = Spider()
    source = leetcode_spider.get_source(url)
    topic_body = leetcode_spider.get_body(source)
    all_subjects = leetcode_spider.get_all_subjects(topic_body)
    leetcode_spider.save_info(all_subjects)
    time2 = time.time()
    print u'抓取完毕...'
    print u'用时: ' + str(time2-time1) + 's'
