from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import time
import re
f = open("dust.csv",'wt',encoding = 'utf-8')
f.write("ZON_NM,DATE,px_mean,px_max\n")
month_list=['2018.03.','2018.04.','2018.05.','2018.06.',
            '2018.07.','2018.08.','2018.09.','2018.10.']

area=['1','2','3','4','5','6']


local_list ={'Gangwon-do':'area=2&stnId=93','Gyeonggi-do':'area=1&stnId=119',
             'Gyeongsangnam-do':'area=5&stnId=192','Gyeongsangbuk-do':'area=5&stnId=136',
             'Gwangju':'area=4&stnId=156','Daegu':'area=5&stnId=143','Daejeon':'area=3&stnId=232',
             'Busan':'area=5&stnId=160','Seoul':'area=1&stnId=108','Ulsan':'area=5&stnId=152',
             'Incheon':'area=1&stnId=201','Jeollanam-do':'area=4&stnId=146','Jeollabuk-do':'area=4&stnId=140',
             'Jeju-do':'area=6&stnId=185','Chungcheongnam-do':'area=3&stnId=232',
             'Chungcheongbuk-do':'area=3&stnId=135'}

for local_name, local_num in local_list.items():
    for month in month_list:
        url = "http://www.weather.go.kr/weather/asiandust/graph.jsp?" + local_num + "&view=2&tm=" +month
        day = 1
        if month in('2018.04.','2018.06.','2018.09.'):
            while day <31:
                try:
                    if day < 10:
                        url_day = "0"+str(day)
                        url_day = url+url_day+".&"
                        print(local_name, month,day, "진행률 : ", day,"/30")
                        url_open = urlopen(url_day)
                        soup = BeautifulSoup(url_open, "html.parser", from_encoding='utf8')

                        for px in soup.find_all("tbody"):
                            for px in px.find_all("tr"):
                                date_value = px.find(name="th", attrs={'scope': 'row'}).text
                                T_F = month+"0"+str(day)+"."
                                if date_value == T_F:
                                    sum=[]
                                    num=0
                                    for pxx in px.find_all("td", attrs={"style":"padding:2px"}):
                                        if pxx :
                                            sum.append(int(pxx.text))
                                            print(date_value,"미세먼지농도: ",pxx.text)
                                            num+=1

                                    if num != 0 :
                                        AVG = np.mean(sum)
                                        MAX = np.max(sum)
                                        print("평균 : ", AVG)
                                        print("최대값 : ", MAX)
                                        date = re.sub('[^0-9]','',T_F)
                                        f.write(local_name+','+date+',' + str(AVG) +','+ str(MAX)+ '\n')
                    else:
                        url_day = url+ str(day)+"."
                        print(local_name, month,day, "진행률 : ", day, "/30")
                        url_open = urlopen(url_day)
                        soup = BeautifulSoup(url_open, "html.parser", from_encoding='utf8')

                        for px in soup.find_all("tbody"):
                            for px in px.find_all("tr"):
                                date_value = px.find(name="th", attrs={'scope': 'row'}).text
                                T_F = month+str(day)+"."
                                if date_value == T_F:
                                    sum=[]
                                    num=0
                                    for pxx in px.find_all("td", attrs={"style":"padding:2px"}):
                                        if pxx :
                                            sum.append(int(pxx.text))
                                            print(date_value, "미세먼지농도: ", pxx.text)
                                            num += 1

                                    if num != 0:
                                        AVG = np.mean(sum)
                                        MAX = np.max(sum)
                                        print("평균 : ", AVG)
                                        print("최대값 : ", MAX)
                                        date = re.sub('[^0-9]', '', T_F)
                                        f.write(local_name + ',' + date + ',' + str(AVG) +',' + str(MAX) + '\n')
                    day+=1
                except Exception as e:
                    print(e)
        else:
            while day <32:
                try:
                    if day < 10:
                        url_day = "0" + str(day)
                        url_day = url + url_day + ".&"
                        print(local_name, month, day, "진행률 : ", day, "/30")
                        url_open = urlopen(url_day)
                        soup = BeautifulSoup(url_open, "html.parser", from_encoding='utf8')

                        for px in soup.find_all("tbody"):
                            for px in px.find_all("tr"):
                                date_value = px.find(name="th", attrs={'scope': 'row'}).text
                                T_F = month + "0" + str(day) + "."
                                if date_value == T_F:
                                    sum=[]
                                    num=0
                                    for pxx in px.find_all("td", attrs={"style": "padding:2px"}):
                                        if pxx:
                                            sum.append(int(pxx.text))
                                            print(date_value, "미세먼지농도: ", pxx.text)
                                            num += 1

                                    if num != 0:
                                        AVG = np.mean(sum)
                                        MAX = np.max(sum)
                                        print("평균 : ", AVG)
                                        print("최대값 : ", MAX)
                                        date = re.sub('[^0-9]', '', T_F)
                                        f.write(local_name + ',' + date + ',' + str(AVG) +',' + str(MAX) + '\n')
                    else:
                        url_day = url + str(day) + "."
                        print(local_name, month, day, "진행률 : ", day, "/31")
                        url_open = urlopen(url_day)
                        soup = BeautifulSoup(url_open, "html.parser", from_encoding='utf8')

                        for px in soup.find_all("tbody"):
                            for px in px.find_all("tr"):
                                date_value = px.find(name="th", attrs={'scope': 'row'}).text
                                T_F = month +  str(day) + "."
                                if date_value == T_F:
                                    sum=[]
                                    num=0
                                    for pxx in px.find_all("td", attrs={"style": "padding:2px"}):
                                        if pxx:
                                            sum.append(int(pxx.text))
                                            print(date_value, "미세먼지농도: ", pxx.text)
                                            num += 1

                                    if num != 0:
                                        AVG = np.mean(sum)
                                        MAX = np.max(sum)
                                        print("평균 : ", AVG)
                                        print("최대값 : ", MAX)
                                        date = re.sub('[^0-9]', '', T_F)
                                        f.write(local_name + ',' + date + ',' + str(AVG) +',' + str(MAX) + '\n')

                    day += 1
                except Exception as e:
                    print(e)
f.close()