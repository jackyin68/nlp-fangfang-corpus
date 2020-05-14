import urllib.request
import urllib.error
import http.cookiejar
from urllib import parse

start_urls = []
params = {"q": "方方汪芳武汉"}
wd = parse.urlencode(params)
query_url = 'https://www.so.com/s?' + wd

cookie_filename = '../cookie/cookie.txt'
cookie = http.cookiejar.LWPCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

get_url = query_url
get_request = urllib.request.Request(get_url)
get_response = opener.open(get_request)
print(get_response.read().decode())