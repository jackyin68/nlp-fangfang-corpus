# -*- coding: utf-8 -*-
# Copyright 2020 yinzhiwu@126.com.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import http.cookiejar
import re
import urllib.error
import urllib.request
from urllib import parse
import scrapy

from scrapy.http import Request
from sospider.items import SospiderItem

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.LWPCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {
    'User-Agent': user_agent
}


class A360spiderSpider(scrapy.Spider):
    name = '360spider'
    allowed_domains = ['so.com']

    start_urls = []
    params = {"q": "方方汪芳武汉联系"}
    wd = parse.urlencode(params)
    query_url = 'https://www.so.com/s?' + wd
    start_urls.append(query_url)

    def parse(self, response):
        urls = response.xpath("//li[@class='res-list']/h3[@class='res-title ' or @class='res-title']/a/@href").getall()
        for url in urls:
            yield Request(url, callback=self.parse_details)

        next_url = response.xpath("//a[@id='snext']/@href").get()
        if next_url:
            next_url = parse.urljoin(response.url, next_url)
            yield Request(url=next_url, callback=self.parse)

    def min_len(self, item):
        if len(item.strip()) > 5:
            return True

    def parse_details(self, response):
        content = response.body.decode(response.encoding)
        result = re.search('(方方)', content)
        if result:
            rst = re.findall('<div.*?class=".*?content.*?">(.*?)</div>', content, re.S)
            article = "\\n".join(rst)
            if len(article) < 10:
                return
            spider_item = SospiderItem(content=article)
            yield spider_item
        else:
            pattern = re.compile(r'.*URL=\'(.*http.*)\'\">')
            match_url_object = pattern.search(content)
            if match_url_object:
                url = match_url_object.group(1)
                print(url)
                so_rst = re.findall('.*?(so.com).*', url, re.S)
                if so_rst:
                    get_url = url
                    get_request = urllib.request.Request(get_url)
                    get_response = opener.open(get_request)
                    article = get_response.read().decode()
                    # print(article)
                else:
                    req = urllib.request.Request(url, headers=headers)
                    get_response = urllib.request.urlopen(req, timeout=10)
                    article = get_response.read().decode('utf-8', 'ignore')

                rst = re.findall('<div.*?class=".*?content.*?">(.*?)</div>', article, re.S)
                article = "".join(rst)
                if len(article) < 10:
                    return
                spider_item = SospiderItem(content=article)
                yield spider_item
