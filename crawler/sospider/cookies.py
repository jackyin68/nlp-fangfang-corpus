import urllib.request, urllib.parse, urllib.error
import http.cookiejar
from urllib import parse

start_urls = []
params = {"q": "方方汪芳武汉"}
wd = parse.urlencode(params)
query_url = 'https://www.so.com/s?' + wd


URL_ROOT = query_url
values = {'name': '******', 'password': '******'}
postdata = urllib.parse.urlencode(values).encode()
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
headers = {'User-Agent': user_agent}

cookie_filename = '../cookie/cookie.txt'
cookie = http.cookiejar.LWPCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(URL_ROOT, postdata, headers)
try:
    response = opener.open(request)
except urllib.error.URLError as e:
    print(e.reason)

cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中
for item in cookie:
    print('Name = ' + item.name)
    print('Value = ' + item.value)
