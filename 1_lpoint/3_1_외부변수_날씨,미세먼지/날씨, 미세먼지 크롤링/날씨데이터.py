from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import re
''' 01:강원도 02:경기도 03:경상남도 04:경상북도 05:광주광역시 06:대구광역시 07:대전광역시
08:부산광역시, 09:서울특별시. 17: 세종특별자치시, 10: 울산광역시,
11: 인천광역시, 12: 전라남도, 13:전라북도, 14: 제주도, 15: 충청남도, 16: 충청북도 

여기서 소분류를 가장 인구가 많은 시/구로 정함 
강원도(01) : 원주(130) --> 01130
경기도(02) : 수원시권선구(113) --> 02113
경상남도(03) : 창원시의창구(121) --> 03121
경상북도(04) : 포항시북구(113) --> 04113
광주광역시(05) : 북구(170) --> 05170
대구광역시(06) : 달서구(290) --> 06290
대전광역시(07) : 서구(170) --> 07170
부산광역시(08) : 해운대구(350) --> 08350
서울특별시(09) : 송파구(710) --> 09710
울산광역시(10) : 남구(140) --> 10140
인천광역시(11) : 남동구(200) --> 11200
전라남도(12) : 여수시(130) --> 12130
전라북도(13) : 전주시완산구(111) --> 13111
제주도(14) : 제주시(110) --> 14110
충청남도(15) : 천안시 서북구(133) --> 15133
충청북도(16) : 청주시(113) --> 16113
세종특별자치시(17110)  --> 17110
'''
local_list ={'Gangwon-do':'01130','Gyeonggi-do':'02113','Gyeongsangnam-do':'03121','Gyeongsangbuk-do':'04113',
             'Gwangju':'05170','Daegu':'06290','Daejeon':'07170',
             'Busan':'08350','Seoul':'09710','Ulsan':'10140',
             'Incheon':'11200','Jeollanam-do':'12130','Jeollabuk-do':'13111',
             'Jeju-do':'14110','Chungcheongnam-do':'15133','Chungcheongbuk-do':'16113','Sejong':'17110'}
# csv 파일 형식 --> 지역, 월, 일, 날씨 이렇게 합시다
f = open("L_point_weather.csv",'wt',encoding = 'utf-8')
f.write("ZON_NM,DATE,WEATHER,T_MAX,T_MIN\n")
month_list =['201803','201804','201805','201806','201807','201808','201809','201810']
pattern = re.compile(r'\s+')
for local_name, local_num in local_list.items():

    for month in month_list:
        url = "https://weather.naver.com/period/pastWetrMain.nhn?ym=" + month
        url= url + "&naverRgnCd=" + local_num
        print(local_name, url)
        url = urlopen(url)
        soup = BeautifulSoup(url, "html.parser", from_encoding='utf8')
        time.sleep(0.2)
        try:
            day = 1
            for weather_1 in soup.find_all("td"):
                weather = weather_1.find(name = "p", attrs={'class':'icon'})
                temp_mn = weather_1.find(name="span", attrs={'class': "temp_mn"})
                temp_mx = weather_1.find(name="span", attrs={'class': "temp_mx"})
                if weather :
                    print(month,"월",str(day),"일 날씨 :",weather.img['alt'])
                    temp_mn_re = re.sub(pattern, '', temp_mn.strong.string)
                    temp_mx_re = re.sub(pattern, '', temp_mx.strong.string)
                    print("최저기온", temp_mn_re)
                    print("최고기온", temp_mx_re)
                    if day <10 :
                        f.write(local_name+','+month+'0'+str(day)
                            +','+weather.img['alt']+','+temp_mn_re+','+temp_mx_re+'\n')
                    else:
                        f.write(local_name + ',' + month + str(day)
                                + ',' + weather.img['alt'] + ',' + temp_mn_re + ',' + temp_mx_re + '\n')
                    day += 1
                if month in ('201804','201806','201809'):
                    if day == 31 :
                        break
                elif day == 32 :
                    break

        except Exception as e:
            print(e)



f.close()