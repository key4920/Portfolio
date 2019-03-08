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


    ctg3 = pd.read_csv('ctg3_2.csv')

    parent_id=[]
    for i in range(len(ctg3)):
        url = 'https://search.shopping.naver.com/search/category.nhn?cat_id='
        url = url + str(ctg3['id'].iloc[i])
        rcv_data = get_request_url(url)
        soupData = BeautifulSoup(rcv_data, 'html.parser')

        parent_tag = soupData.select('div.finder_cell ul.finder_list a')
        parent_id_var = parent_tag[0].get('data-parent-id')[-8:]

        print(parent_id_var)
        parent_id.append(parent_id_var)

    ctg3['parent_id'] = parent_id
    print(ctg3.head())

    ctg3.to_csv('parent_ctg3_2.csv', index=False, index_label=False)



if __name__ == '__main__':
    main()
