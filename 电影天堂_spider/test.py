import requests
url = "http://dytt8.net/html/gndy/dyzz/list_23_4.html"
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        #"Referer":"http://dytt8.net/"
        }
respon = requests.get(url, headers=header)
text=respon.content.decode('gbk',errors='ignore')