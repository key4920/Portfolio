import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv

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



def main():


    url = 'https://search.shopping.naver.com/search/category.nhn?cat_id=50000167'
    rcv_data = get_request_url(url)
    soupData = BeautifulSoup(rcv_data, 'html.parser')

    ctg1 = []

    ctg1_tag = soupData.select('a._category1 em')
    for i in range(len(ctg1_tag)):
        ctg1.append(ctg1_tag[i].text)
    ctg1_url = [50000000+i for i in range(11)]
    #ctg1_dict = {i: 50000000 + ind for ind, i in enumerate(ctg1)}

    ctg2 = []
    ctg2_url = []

    ctg3 = []
    ctg3_url = []

    for i in range(10):
        url = 'https://search.shopping.naver.com/category/category.nhn?cat_id='

        url = url + str(50000000+i)
        print(url)
        rcv_data = get_request_url(url)
        soupData = BeautifulSoup(rcv_data, 'html.parser')


        ctg2_tag = soupData.select('div.category_cell h3 strong')
        for j in ctg2_tag:
            ctg2.append(j.text)
        ctg2_tag2 = soupData.select('div.category_cell h3 a')
        for i in ctg2_tag2:
            ctg2_url.append(i.get('href')[-8:])


        ctg3_tag = soupData.select('div.category_cell > ul.category_list > li > a')

        for i in ctg3_tag:
            if i.text=='더보기':
                continue
            else:
                ctg3.append(i.text)
                ctg3_url.append(i.get('href')[-8:])


    #ctg2_dict = {a: b for a, b in zip(ctg2, ctg2_url)}
    #print(ctg2_dict)

    #ctg3_dict = {a: b for a, b in zip(ctg3, ctg3_url)}
    #print(ctg3_dict)


    dfctg1 = pd.DataFrame([(a,b) for a,b in zip(ctg1,ctg1_url)],columns=['ctg1','id'])
    dfctg2 = pd.DataFrame([(a,b) for a,b in zip(ctg2,ctg2_url)],columns=['ctg2','id'])
    dfctg3 = pd.DataFrame([(a, b) for a, b in zip(ctg3, ctg3_url)], columns=['ctg3', 'id'])

    dfctg1.to_csv('ctg1_2.csv',index=False,index_label=False)
    dfctg2.to_csv('ctg2_2.csv', index=False, index_label=False)
    dfctg3.to_csv('ctg3_2.csv', index=False, index_label=False)


    # ctg3_dict = {a: b for a, b in zip(ctg3, ctg3_url)}



if __name__ == '__main__':
    main()
