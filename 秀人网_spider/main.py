#encoding:utf-8
import  requests
import time
from lxml import etree
import os
from urllib import request

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Referer":"https://cjhd.mediav.com/games/hang.html?&si=UFzPo0&containerID=QIHOO__INTERACTIVE_PLUGIN1545570742629&t=1545570743078"
}

rooturl="https://www.meitulu.com/t/dachidu/"#此处放爬取连接，按照浏览器中进行粘贴
targetpages=range(1,30)#爬取页码，从第几页开始，到第几页结束
savepath=".\\"#保存地址，会在保存地址路径下生成图集文件夹，每个图集一个文件夹

#生成指定类别的url，秀人网的url比较简单，类别为拼音
def UrlProduct():
    ans=[]
    for i in targetpages:#控制生成页码
        if i==1:
            temp=rooturl
        else:
            temp=rooturl+'%d.html'%i
        ans.append(temp)
    #ans.append(rooturl)
    return ans

#将每页的内容生成一个字典，字典的内容为｛题目：url｝
def Getsubpage(url):
    ditilrespon = requests.get(url, headers=headers)
    dititext = ditilrespon.content.decode('utf-8', errors='ignore')
    ditihtml = etree.HTML(dititext)
    titleulr = ditihtml.xpath('//li/a[@target="_blank"]/@href')
    titlename=ditihtml.xpath('//li/a[@target="_blank"]/img/@alt')
    ans=dict(zip(titlename, titleulr))
    return ans

#将每一页的内容生成一个字典，字典格式为｛‘名字’：‘所有页面url’｝
def Getallpageurls(dict):
    for key in dict:
        ans = {}
        name=key
        url=dict[key]
        baseurl='https://www.meitulu.com/'
        ditilrespon = requests.get(url, headers=headers)
        dititext = ditilrespon.content.decode('utf-8', errors='ignore')
        ditihtml = etree.HTML(dititext)
        temppages=ditihtml.xpath('//div[@id="pages"]/a/@href')
        finalpage=[]
        for page in temppages:
            page=baseurl+page
            if page not in finalpage:
                finalpage.append(page)
        #需调整如果大于11的，要重新遍历添加新值
        if len(finalpage)>10:
            lastpage=finalpage[len(finalpage)-1]
            ditilrespon = requests.get(lastpage, headers=headers)
            dititext = ditilrespon.content.decode('utf-8', errors='ignore')
            ditihtml = etree.HTML(dititext)
            temppages = ditihtml.xpath('//div[@id="pages"]/a/@href')
            for page in temppages:
                page=baseurl+page
                if page not in finalpage:
                    finalpage.append(page)
        ans[name]=finalpage
        Getallphotourl(ans)
    return ans

#分析｛‘名字’：‘所有页面url’｝字典，并将页面url替换为对应图片url
def Getallphotourl(dict):
    for key in dict:
        ans = {}
        pages=dict[key]
        allptoto={}
        for page in pages:
            ditilrespon = requests.get(page, headers=headers)
            dititext = ditilrespon.content.decode('utf-8', errors='ignore')
            ditihtml = etree.HTML(dititext)
            photourls = ditihtml.xpath('//center/img/@src')
            allptoto[page]=photourls
        ans[key]=allptoto
        #print(ans)此处最后得出的结构为｛图集名：｛来源：[连接],来源，[连接]....｝｝
        Downloadpotos(ans)
    return ans
#下载图片到指定文件夹，并将文件夹名命名为其key
def Downloadpotos(photodict):
    for key in photodict:
        path = Mkdir(key)
        if path=='completed':
            print("%s 已经爬取过，跳过！"%key)
            return 0
        name=key
        urldict=photodict[key]
        i=1
        for key in urldict:
            #print("referer in %s"%key)
            #print("url is %s"%urldict[key])
            headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Referer":key,
}
            for url in urldict[key]:
                img = requests.get(url, headers=headers)
                imgname=url[-10:]
                imgname=imgname.replace("/","_")
                #print(imgname)
                with open(os.path.join(path,imgname), 'ab') as f:
                    f.write(img.content)
                    f.close()
                    i+=1
                time.sleep(0.05)
        print("%s 爬取完毕！"%name)

    '''
    opener=request.build_opener()
    opener.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36')]
    request.install_opener(opener)
    for key in dict:
        path=Mkdir(key)
        photourls=dict[key]
        for photo in photourls:
            print(photo)
            request.urlretrieve(photo,path)
    print("%s 下载完成！"%key)
'''
#创建文件夹
def Mkdir(path):
# 引入模块去除首位空格
    path = path.strip()
# 去除尾部 \ 符号
    path = path.rstrip("\\")
    finalpath=os.path.join(savepath,path)
# 判断路径是否存在存在     True 不存在   False
    isExists = os.path.exists(finalpath)
# 判断结果
    if not isExists:
# 如果不存在则创建目录,创建目录操作函数
        os.makedirs(finalpath)
        print(finalpath + ' 创建成功')
        return finalpath
    else:
# 如果目录存在则不创建，并提示目录已存在
        #print(finalpath + ' 目录已存在')
        return 'completed'


pages=UrlProduct()
i=0
for page in pages:
    i+=1
    pagedict=Getsubpage(page)
    Getallpageurls(pagedict)
    with open(os.path.join(savepath,'状态.txt'),"a+") as fp:
        fp.write("第%s页爬取完毕！"%i)
        fp.close()
    print("第%s页爬取完毕！"%i)
