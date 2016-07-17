# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeatherPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        with open('result.txt', 'w+') as file:
            city = item['city'][0].encode('utf-8')
            date = item['date']
            desc = item['dayDesc']
            dayTemp = item['dayTemp']

            file.write('city:' + str(city) + '\n\n')
            dayDesc = desc[1::2]
            nightDesc = desc[0::2]
            wea_item = zip(date, dayDesc, nightDesc, dayTemp)

            for i in range(len(wea_item)):
                item = wea_item[i]
                d = item[0]    # 日期
                dd = item[1]   # 白天天气
                nd = item[2]   # 夜晚天气
                ta = item[3].split('/')
                dt = ta[0]     # 白天气温
                nt = ta[1]     # 夜晚气温
                txt = 'date:{0}\t\tday:{1}({2})\t\tnight:{3}({4})\n\n'.format(
                        d,
                        dd.encode('utf-8'),
                        dt.encode('utf-8'),
                        nd.encode('utf-8'),
                        nt.encode('utf-8')
                )
                file.write(txt)

        return item
