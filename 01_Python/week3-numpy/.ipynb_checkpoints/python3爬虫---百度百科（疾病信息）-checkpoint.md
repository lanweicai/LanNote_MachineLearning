## 一、问题描述

之前爬虫过程主要存在两个个问题：
（1）爬取到网页源码之后，没有解析，直接利用正则表达式抓取信息，这样做起来比较费劲，容易造成信息抓取不全面，同时，所有页面链接都是根据链接规律自建的，没有做到自动爬取。
（2）代码未做模块化处理，检查错误比较难。
在改善了上述两个问题之后，重新爬取了百度百科中疾病信息库，并保存在.xlsx文件中

## 二、网页分析及爬虫结构

**1、网页分析**

爬虫入口链接：root_url="http://baike.baidu.com/fenlei/%E7%96%BE%E7%97%85"
爬虫入口页面：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190830160333998.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xJVkVBRA==,size_16,color_FFFFFF,t_70)
红圈对应源码位置为该疾病链接，蓝圈对应位置为每个分页链接
因此本次爬虫的过程为：依次爬取每页所有疾病链接，进而根据疾病链接爬取疾病信息

**2、爬虫结构**

**（1）url 集合**
urls_0=set()：主页链接集合（未爬取）
urls_1=set()：疾病页面链接集合（未爬取）
new_url_0：主页链接（即将爬取）
new_url_1：疾病链接（即将爬取）
old_urls=set()：所有已爬取链接集合（防止重复爬取）

**（2）模块**
main: 主程序（调度，保存数据）
url_manager ：url管理器（url保存，提取，查空）
html_downloader ：html下载器（下载HTML）
html_parser ：html解析器（提取主页内疾病链接和疾病页面内所需信息）

**（3）爬取过程**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190830170953905.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xJVkVBRA==,size_16,color_FFFFFF,t_70)

## 三、具体模块代码

为方便查看，将主模块放在最后

**1、url_manager ：url管理器**（url保存，提取，查空）

    class UrlManager(object):
        def __init__(self):
            self.new_urls_0=set()#主页链接集合（未爬取）
            self.new_urls_1=set()#疾病链接集合（未爬取）
            self.old_urls=set()#已爬取链接集合
    
        #单一url添加到url_set中  
        def add_new_url(self,url,url_set):
            if url is None:
                return 
            if url not in url_set and url not in self.old_urls:
                url_set.add(url)
    
        #多个url添加到url_set中     
        def add_new_urls(self,urls,url_set):
            if urls is None or len(urls)==0:
                return
            for url in urls:
                self.add_new_url(url,url_set)
    
        #从url_set中获取一个url ，同时将该url添加到old_url集合中      
        def get_new_url(self,url_set):
            new_url=url_set.pop()
            self.old_urls.add(new_url)
            return new_url
    
        #判断url_set中是否还有未爬取的url  
        def has_new_url(self,url_set):
            return len(url_set)!=0

**2、html_downloader** ：html下载器（下载HTML）

    import urllib.request
    import urllib
    
    class HtmlDownloader(object):
        def __init__(self):
            pass
        #下载html
        def download(self,url):
            if url is None:
                return None
            print ("html downloading")
            i=1 
            #设置开关，报错时继续下载该HTML，配合urlop.close()主要为了解决10054（拒绝访问）报错
            #如果报错信息不是10054，Ctrl+C终止循环，改错后继续
            while i==1:
                i=0
                try:
                    urlop=urllib.request.urlopen(url,timeout=100)
                    data=urlop.read().decode('utf-8')
                    urlop.close()
                except Exception as e:
                    print(e)
                    i=1
            return data

**3、html_parser ：html解析器**（提取主页内疾病链接和疾病页面内所需信息）

    from bs4 import BeautifulSoup
    import re
    class HtmlParser(object):
        
        #返回页面中的所有链接
        def parse_url(self,url_r,html_cont):
            soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
            new_urls_0=self._get_new_urls_0(url_r,soup)
            new_urls_1=self._get_new_urls_1(soup)
            return new_urls_0,new_urls_1
        
        #返回页面中爬取的数据信息
        def parse_data(self,html_cont):
            soup=BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
            new_data=self._get_new_data(soup)
            return new_data
    
        #解析得到html中的所有疾病链接 
        def _get_new_urls_1(self,soup):
            new_urls_1=set()
            #获取本页疾病链接
            #例：<a href="/view/124636.htm" class="pic-content nslog:7450" title="骨髓瘤" target="_blank">
            links_1=soup.find_all('a',href=re.compile(r"/view/\d+\.htm"))
            for link in links_1:
                new_url=link['href']
                new_full_url='http://baike.baidu.com'+new_url
                new_urls_1.add(new_full_url)
            return new_urls_1
        
        #解析得到html中的页面链接
        def _get_new_urls_0(self,url_r,soup):
            new_urls_0=set()
            #获取更多页面链接
            #例：<a href="疾病?limit=30&index=2&offset=30#gotoList" class="nslog:7453">
            links_0=soup.find_all('a',href=re.compile(r"\?limit=\d+&index=\d+&offset=\d+\#gotoList"))
            for link in links_0:
                new_url=link['href']
                new_full_url=url_r+new_url[2::]#构造完整链接
                new_urls_0.add(new_full_url)
            return new_urls_0
    
        #解析得到疾病页面中的标题(title)、简介(summary)    、基本信息
        def _get_new_data(self,soup):
            res_data={}
           
            #title 示例
            #<dd class="lemmaWgt-lemmaTitle-title">
            #<h1 >骨关节炎</h1>
            title_node=soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
            res_data['疾病名']=str(title_node.string)
           
            #summer示例
            #<div class="lemma-summary" label-module="lemmaSummary">
            #<div class="para" label-module="para">骨<a target=_blank。。。关节畸形等。</div>
            summary_node=soup.find_all('div',class_="lemma-summary")
            soup_summary=BeautifulSoup(str(summary_node), 'lxml')
            
            #简介
            res_data['简介']=str(soup_summary.div.text)
            #<div class="dl-baseinfo">
            #base_inf=soup.find_all('div',attrs={"class":"dl-baseinfo"})[0].find_all('dd')
            for i in soup.find_all('div',attrs={"class":"dl-baseinfo"}):
                item=i.find_all('dt')
                inf=i.find_all('dd')
                for j,x in enumerate(item):
                    try:
                        res_data[x.string]=','.join(re.findall('\S+',inf[j].string))   
                    except Exception as e:
                        print(e)
                        res_data[x.string]=None
            return res_data

**4、main: 主程序**（调度，保存数据）
为方便对照，将爬虫结构图再次放置
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190830180147680.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xJVkVBRA==,size_16,color_FFFFFF,t_70)

    #上述模块保存后调用
    import url_manager,html_downloader,html_parser
    import openpyxl
    class Main(object):
        def __init__(self):
            self.urls=url_manager.UrlManager()#url管理器
            self.downloader=html_downloader.HtmlDownloader()#html下载器
            self.parser=html_parser.HtmlParser()#html解析器
            self.sheet=sheet
        def craw(self,root_url):
        
            urls_0=self.urls.new_urls_0#新页面url集合
            urls_1=self.urls.new_urls_1#新疾病url集合
            self.urls.add_new_url(root_url,urls_0)#将爬虫入口添加到新页面url集合
            count=0#页面数目
            row=1#数据总条目
            while self.urls.has_new_url(urls_0):#爬完所有页面时停止
                i=0#同一页面下，所爬取疾病数目
                count+=1
                new_url_0=self.urls.get_new_url(urls_0)#从页面url集合获取一个url，并将其放入old_urls中
                print ("页面 %d: %s"%(count,new_url_0))
                html_cont=self.downloader.download(new_url_0)#下载html
                new_urls_0,new_urls_1=self.parser.parse_url(root_url,html_cont)#获取页面html中的新页面链接和疾病链接
                self.urls.add_new_urls(new_urls_0,urls_0)#保存新页面链接
                self.urls.add_new_urls(new_urls_1,urls_1)#保存疾病链接
                #print(urls_0)
                while self.urls.has_new_url(urls_1):#爬完本页所有疾病时停止
                    i+=1
                    new_url_1=self.urls.get_new_url(urls_1)#获取一个疾病链接，并添加到old_urls中
                    print('页面 %d 疾病 %d: %s'%(count,i,new_url_1))
                    html_cont=self.downloader.download(new_url_1)#下载疾病页面html
                    new_data=self.parser.parse_data(html_cont) #提取所需信息
                    row+=1#每爬取一个疾病信息，数据总数加一
                    print(row)#输入已爬取总数
                    #print(new_data['疾病名'])
                    #print(new_data)
                    #return new_data
                    #写入表格
                    for data in new_data:
                        if data in items:
                            sheet.cell(row,items.index(data)+1,new_data[data])
                            
    
    if __name__=="__main__":
        #表头内容
        items= ['疾病名', '英文名称', '就诊科室', '常见发病', '常见病因', '常见症状', '简介']
        #爬虫入口
        root_url="http://baike.baidu.com/fenlei/%E7%96%BE%E7%97%85"
        #载入表格
        workbook=openpyxl.load_workbook(r'C:\Users\Administrator\Desktop\jibing2.xlsx')
        #获取sheet
        sheet=workbook.worksheets[0]
        #添加表头
        for i,x in enumerate(items):
            sheet.cell(1,i+1,x)
        obj_spider=Main()
        #调用爬虫调度程序
        obj_spider.craw(root_url)
        #保存数据
        workbook.save(r'C:\Users\Administrator\Desktop\jibing2.xlsx')

## 四、报错及结果

**1、报错信息**

（1）  
  `TypeError: 'str' object is not callable`
原因是定义了一个str变量，但是该变量名是系统本身的函数或者自定义函数，发生冲突，更改该变量名即可
（2）

    openpyxl
    sheet.cell(0,0,x)
    ValueError: Row or column values must be at least 1

报错原因：
openpyxl表格位置计数从1开始，并非从0开始
（3）

    save_workbook(self, filename)
    PermissionError: [Errno 13] Permission denied: 'C:\\Users\\Administrator\\Desktop\\jibing2.xlsx'

错误原因：
当前表格处于打开状态，关闭表格后重试
**2、运行过程**
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190830181401868.?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0xJVkVBRA==,size_16,color_FFFFFF,t_70)
