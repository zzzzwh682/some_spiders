#encoding:utf-8

import  requests
import time
from lxml import etree
import csv



header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        #"Referer":"http://dytt8.net/"
        }

def parse_info(info,rule):
    return info.replace(rule,"").strip()
movies = []
for i in range(1,100):
    url="http://dytt8.net/html/gndy/dyzz/list_23_%d.html"%i
    respon=requests.get(url,headers=header)
    #print(respon.content.decode('gbk'))
    try:
        text=respon.content.decode('gbk',errors='ignore')#第4页后会有解码错误
    except UnicodeDecodeError:
        #print(text)
        pass
    html = etree.HTML(text)
    tbodys=html.xpath("//table[@class='tbspan']")
    for tbody in tbodys:
        movie = {}
        suburl=tbody.xpath(".//a/@href")
        finalurl='http://dytt8.net/'+suburl[0]
        ditilheader={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
            "Referer":url
        }
        ditilrespon=requests.get(finalurl,headers=ditilheader)
        #print(ditilrespon.content.decode('gbk'))
        #time.sleep(5)
        dititext=ditilrespon.content.decode('gbk',errors='ignore')
        ditihtml=etree.HTML(dititext)
        try:
            titlename=ditihtml.xpath('//div[@class="title_all"]//font[@color="#07519a"]/text()')[0]
        except IndexError:
            continue
        movie['name']=titlename
        movie['filecover'] = ' '
        movie['screenshot'] = ' '


        zoom=ditihtml.xpath('//div[@id="Zoom"]')[0]
        cover=zoom.xpath(".//img/@src")
        #print(cover)
        try:
            movie['filecover'] =cover[0]
            movie['screenshot']=cover[1]
        except IndexError:
            pass
        infors=zoom.xpath(".//text()")

        for index,infor in enumerate(infors):
            movie['writor'] = ' '
            movie['douban_marks'] = ' '
            movie['duration'] = ' '
            movie['category'] = ' '
            movie['downloadurl'] = ' '
            movie['director'] = ' '
            movie['actors'] = ' '
            movie['localtion'] = ' '
            movie['year'] = ' '
            movie['contain'] = ' '
            if infor.startswith("◎年　　代"):
                info=parse_info(infor,"◎年　　代")
                movie['year']=info
            elif infor.startswith("◎产　　地"):
                info = parse_info(infor, "◎产　　地")
                movie['localtion']=info
            elif infor.startswith("◎类　　别"):
                info = parse_info(infor, "◎类　　别")
                movie['category']=info
            elif infor.startswith("◎豆瓣评分"):
                info = parse_info(infor, "◎豆瓣评分")
                movie['douban_marks'] = info
            elif infor.startswith("◎片　　长"):
                info = parse_info(infor, "◎片　　长")
                movie['duration'] = info
            elif infor.startswith("◎导　　演"):
                director=[]
                for x in range(index,len(infors)):
                    if infors[x].startswith("◎编　　剧") or infors[x].startswith("◎主　　演"):
                        break
                    #print(infors[x])
                    info=parse_info(infors[x],"◎导　　演")
                    director.append(info)
                movie['director']=director

            elif infor.startswith("◎编　　剧"):
                writor=[]
                for x in range(index,len(infors)):
                    if infors[x].startswith("◎主　　演"):
                        break
                    #print(infors[x])
                    info=parse_info(infors[x],"◎编　　剧")
                    writor.append(info)
                movie['writor']=writor

            elif infor.startswith("◎主　　演"):
                actors=[]
                for x in range(index,len(infors)):
                    if infors[x].startswith("◎简　　介 ") or infors[x].startswith("◎标　　签") :
                        break
                    #print(infors[x])
                    info=parse_info(infors[x],"◎主　　演")
                    actors.append(info)
                movie['actors']=actors

            elif infor.startswith("◎简　　介"):
                contain=''
                for x in range(index+1,len(infors)):
                    if(len(infors[x])<10):
                        break
                    contain=contain+infors[x].strip()

                movie['contain']=contain
        try:
            downloadurl=ditihtml.xpath("//td[@style='WORD-WRAP: break-word']/a/text()")[0]
        except IndexError:
            pass
        #downloadurl=ditihtml.xpath("//a/@opdrttxi")
        #print(type(downloadurl))
        #print(downloadurl)
        movie['downloadurl']=downloadurl
        movies.append(movie)
    print("第%d页爬取完毕！"%i)

with open("ddtt_newly.csv","w",newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['片名','封面链接','剧照链接','年份','地区','类型','豆瓣评分','时长','导演','编剧','主演','简介','下载地址'])
    for movie in movies:
        #print(movie)
        try:
            writer.writerow([movie['name'],movie['filecover'],movie['screenshot'],movie['year'],movie['localtion'],
                            movie['category'],movie['douban_marks'],movie['duration'],movie['director'],movie['writor'],movie['actors'],
                            movie['contain'],movie['downloadurl']])
        except UnicodeEncodeError:
            continue
    print("写出完毕！！")
        #writer.writerow(["name", "name", "name", "name"])


