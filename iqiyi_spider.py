import requests,re
import pandas as pd
from bs4 import BeautifulSoup
from sys import argv
datalist=[]
#爬取多少页改动下一行的range中的数字
fzdyurls=['http://list.iqiyi.com/www/1/291-------------11-{}-1-iqiyi--.html'.format(str(i)) for i in range(1,int(argv[1])+1)]
def getHtmlText(url):   #获取网页内容
    try:
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""

def get_data(url):  #解析网页,获取电影详细信息,并整理数据
    try:
        soup= BeautifulSoup(getHtmlText(url),"html5lib")
        title=soup.find("span",attrs={"class":"title-txt","id":"widget-videotitle"}).text
        time = soup.find("span",attrs={"class":"qy-mod-label"}).text
        score1=soup.find("div",attrs={"id":"iqiyi-main"})
        score2=str(score1)
        score3=re.findall('"score"\:\d\.\d',score2)
        score4=re.findall('\d\.\d',str(score3[0]))
        score=str(score4[0])
        actors1=soup.find_all("a",attrs={"class":"name-link","itemprop":"actor"})
        actors=[]
        for actor in actors1:
            actors.append(actor.string)
        a=str(actors)   
        dict={'[':'',']':'',"'":''}
        for key,value in dict.items():
            a=a.replace(key,value)
        data=[title,url,time,score,a]    #单个电影数据
        print('------------------------------------------------')
        print('------------------单个电影数据------------------')
        print(data)
        print('------------------------------------------------')
        return data
    except:
        return ""

def getdatalist(fzdyurl):
    soup = BeautifulSoup(getHtmlText(fzdyurl),"html5lib")
    dytitle=soup.find_all(class_='qy-mod-link') #获取电影列表
    
    for info in  dytitle:
        url = "http:"+info.get('href')
        # name = info.get('title')
        data=get_data(url)
        datalist.append(data)       #多电影数据
    # print('------------------------------------------------')
    # print('------------------多电影数据------------------')
    # print(datalist)
    # print('------------------------------------------------')

    return datalist
        
def writedata(datalist):
    df = pd.DataFrame(datalist, columns=['影名', '链接', '时长', '评分' ,'演员'])
    df = df.dropna()#去掉空行
    df.to_excel("Movies.xlsx", index=False)


def main():
    i=0
    print('---------------------开始-----------------------')
    for fzdyurl in fzdyurls:
        i=i+1
        print("---------------------第"+str(i)+"页----------------------")
        datalist=getdatalist(fzdyurl)
    print("---------------完成，共爬取"+str(i)+"页---------------")
    writedata(datalist)
    

if __name__ == '__main__':    
    main()


    
