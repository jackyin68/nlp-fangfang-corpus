# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import signal

page_limits = 10000
page_no = 0


class SospiderPipeline(object):
    def __init__(self):
        self.save_format = 'file'
        self.file = open("articles.txt", "a")

    def process_item(self, item, spider):
        global page_no, page_limits
        content = item['content']
        self.file.write(content)
        self.file.write('\n')

        print(f"======================== {page_no}")
        # print(f"{page_no}：{content}")
        if page_no > page_limits:
            self.file.close()
            os.kill(os.getpid(), signal.SIGKILL)
        page_no = page_no + 1

        return item

    def close_spider(self, spider):
        self.file.close()
