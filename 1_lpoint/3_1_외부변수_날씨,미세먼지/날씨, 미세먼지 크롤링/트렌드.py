import urllib.request
import datetime
import json
from naver.config import *


import os
import sys
import urllib.request
client_id = 'zMsen_PxGP6b8a9NsMPH'
client_secret = 'gdRjWdf3oD'
url = "https://openapi.naver.com/v1/datalab/shopping/categories"

body = "{\"startDate\":\"2017-08-01\"," \
       "\"endDate\":\"2019-01-07\"," \
       "\"timeUnit\":\"day\"," \
       "\"category\":[{\"name\":\"패션의류\",\"param\":[\"50000000\"]}," \
       "{\"name\":\"화장품/미용\",\"param\":[\"50000002\"]}]," \
       "\"device\":\"pc\",\"ages\":[\"20\",\"30\"],\"gender\":\"f\"}";

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")
response = urllib.request.urlopen(request, data=body.encode("utf-8"))
rescode = response.getcode()


if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)

''''''


def get_request_url(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200: # 정상적으로 잘 수행 되었을 때
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))

        return None

def getNaverSearchResult(sNode, search_text, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % sNode
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(search_text), page_start, display)
    url = base + node + parameters

    print("==============================================================")
    print('url = ', url)
    print("==============================================================")
    retData = get_request_url(url)
    # print("retData = ", retData)
    if (retData == None):
        return None
    else:
        print(retData)
        return json.loads(str(retData))

# [CODE 3]
def getPostData(post, jsonResult):
    print()
    title = post['title']
    description = post['description']
    link = post['link']

    # blog 용 링크 => org_link = post['bloggerlink']
    org_link = post['originallink']

    # Tue, 14 Feb 2017 18:46:00 +0900
    # blog 용 시간 => pDate = post['postdate']
    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900') # 뉴스용
    pDate = pDate.strftime('%Y-%m-%d %H:%M:%S') # 뉴스용
    jsonResult.append({'title':title, 'description':description, 'org_link':org_link,
                       'link':link, 'pDate':pDate})
    return

def main():
    jsonResult = []
    sNode = 'news' # 'news', 'blog', 'cafearticle' sNode = 'news'
    search_text = '세종특별자치시'
    display_count = 5
    jsonSearch = getNaverSearchResult(sNode, search_text, 1, display_count)
    print("jsonSearch =",jsonSearch)
    print("----------------------------------------------------------------")

    while ((jsonSearch != None) and (jsonSearch['display'] != 0)):
        for post in jsonSearch['items']: # 'item' key에 기사가 저장되어 있음
            print("####################################################################")
            print(post)
            print("####################################################################")
            getPostData(post, jsonResult)
        nStart = jsonSearch['start'] + jsonSearch['display']
        jsonSearch = getNaverSearchResult(sNode, search_text, nStart, display_count)
    with open('%s_naver_%s.json' % (search_text, sNode), 'w', encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)
    print("%s_naver_%s.json SAVED" % (search_text,sNode))

if __name__ == '__main__':
    main()




import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from itertools import count

def get_request_url(url,enc = 'utf-8'):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')
            return ret
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getKyochonAddress(sido1, result):
    for sido2 in count():
        Kyochon_URL = "http://www.kyochon.com/shop/domestic.asp?sido1=%s&sido2=%s&txtsearch=" % \
                      (str(sido1), str(sido2 + 1))
        print(Kyochon_URL)

        try:
            rcv_data = get_request_url(Kyochon_URL)
            soupData = BeautifulSoup(rcv_data, 'html.parser')
            ul_tag = soupData.find('ul', attrs={'class':'list'})

            for store_data in ul_tag.findAll('a', href = True):
                store_name = store_data.find('dt').get_text()
                store_address = store_data.find('dd').get_text()
                store_sido_gu = store_address.split()[:2]
                result.append([store_name] + store_sido_gu + [store_address])

        except:
            break
    return

def main():
    result = []
    print("Kyochon ADDRESS CRAWLING START")
    for sido1 in range(1,18):
        getKyochonAddress(sido1, result)
    Kyochon_table = pd.DataFrame(result, columns=("store", 'sido', 'gungu', 'store_address'))
    Kyochon_table.to_csv('Kyochon_ans.csv', encoding='utf-8', mode='w', index=True)
    del result[:]
    print('FINISHED')


if __name__ == '__main__':
    main()