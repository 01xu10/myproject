#scrapy爬虫基础

###一.创建项目

输入命令创建普通scrapy爬虫

第一步：爬虫项目创建
    scrapy startproject 爬虫项目名
第二步：
    cd 爬虫项目名文件夹
第三步：爬虫文件的创建
    scrapy genspider 爬虫名  爬虫域
第四步：运行爬虫
    scrapy crawl 爬虫名

###二.创建替换ua中间件

1.在middlewares文件中创建类

```python
class RandomAgentMiddleware(object):    
    def process_request(self, request, spider):        
        ua = choice(USER_AGENT_LIST)        			               request.headers['user-agent'] = ua
```

2.在settings配置文件中，添加UA中间件

```python
SPIDER_MIDDLEWARES = {  
    'jdspider.middlewares.RandomAgentMiddleware': 543,
}
```

### 三.执行代码

修改在爬虫文件同级下的init.py文件

```python
from scrapy import cmdline
	cmdline.execute('scrapy crawl 爬虫文件名称'.split(' '))
```