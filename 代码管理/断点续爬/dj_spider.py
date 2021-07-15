from requests_html import HTMLSession
import os, random, re
session = HTMLSession()


USER_AGENT = ['Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
                    ]


class DJ72(object):
    def __init__(self):
        print('开始工作==========工作使我快乐=========打工人与魂========')
        self.start_url = 'http://www.72dj.com/top/'

    def parse_start_url_response(self):
        """
        解析起始的url地址的响应
        :return:
        """
        headers = {
            'user-agent': random.choice(USER_AGENT)
        }
        response = session.get(url=self.start_url, headers=headers)
        """提取所有分类的url，返回一张列表"""
        url_classify_list = response.html.xpath('//div[@class="bangNavBd"]/ul/li/a/@href')
        """提取所有分类的标题，返回一张列表"""
        url_classify_title_list = response.html.xpath('//div[@class="bangNavBd"]/ul/li/a/text()')
        if os.path.exists('已_下_载.log'):
            with open('已_下_载.log', 'r')as f:
                data = f.read()
            list_1 = data.split(' ')
            for i in list_1:
                if i in url_classify_list:
                    url_classify_list.remove(i)
                if i in url_classify_title_list:
                    url_classify_title_list.remove(i)
        else:
            with open('已_下_载.log', 'w')as x:
                x.write('')
        self.parse_two_list(url_classify_list, url_classify_title_list)

    def parse_two_list(self, url_classify_list, url_classify_title_list):
        """
        解析两张列表数据
        :param url_classify_list: 所有分类的url
        :param url_classify_title_list: 所有分类的标题
        :return:
        """
        for url, title in zip(url_classify_list, url_classify_title_list):
            """拼接新的url"""
            next_url = 'http://www.72dj.com' + url
            """文件夹创建"""
            os_path = os.getcwd() + '/' + title + '/'
            if not os.path.exists(os_path):
                os.mkdir(os_path)
            self.parse_next_url_response(next_url, os_path, title, url)

    def parse_next_url_response(self, next_url, os_path, title, start_url):
        """
        解析分类的url，提取当前分类榜单的100首歌曲
        :param next_url: 分类的榜单url
        :param os_path: 需要保存的路径
        :return:
        """
        headers = {
            'user-agent': random.choice(USER_AGENT)
        }
        response = session.get(url=next_url, headers=headers)
        """提取出榜单页面的100首歌曲链接"""
        mp3_100_url = response.html.xpath('//*[@id="playlist"]/li/dl/dd/a/@href')
        """提取出100首歌的名称"""
        mp3_100_name = response.html.xpath('//*[@id="playlist"]/li/dl/dd/a/@title')
        """使用日志保存记录"""
        if not os.path.exists(title + '_标题.log'):
            print('无工作日志========工作日志创建中========logging==========')
            with open(title + '_标题.log', 'w', encoding='utf-8')as tf:
                tf.write(' '.join(mp3_100_name))
        else:
            with open(title + '_标题.log', 'r', encoding='utf-8')as tf_1:
                data_name = tf_1.read()
                mp3_100_name = data_name.split(' ')
        if not os.path.exists(title + '_链接.log'):
            with open(title + '_链接.log', 'w', encoding='utf-8')as lf:
                lf.write(' '.join(mp3_100_url))
        else:
            print('有工作日志========工作日志读取中========logging========')
            with open(title + '_链接.log', 'r', encoding='utf-8')as lf_1:
                data_url = lf_1.read()
                mp3_100_url = data_url.split(' ')
        self.parse_100_mp3_url_response(mp3_100_url, mp3_100_name, os_path, title, start_url)

    def parse_100_mp3_url_response(self, mp3_100_url, mp3_100_name, os_path, title, start_url):
        """
        解析100首歌曲
        :param mp3_100_url: 榜单页面的100首歌曲链接
        :param mp3_100_name: 100首歌的名称
        :return:
        """
        list_1 = ['/', '\\', '?', '？']
        for url, name in zip(mp3_100_url, mp3_100_name):
            """name判断，去除路径符号"""
            for i in list_1:
                if i in name:
                    name = name.replace(i, '')
            else:
                if name is None:
                    name = str(random.randint(1111111111, 9999999999))
                if name == '':
                    name = str(random.randint(1111111111, 9999999999))
            next_url = 'http://www.72dj.com' + url
            self.parse_url_data(next_url, name, os_path)
            """日志更新"""
            print('更新工作日志=======工作日志更新中========logging========')
            with open(title + '_标题.log', 'r', encoding='utf-8')as tf:
                tf_data = tf.read()
            mp3_classify_title_list = tf_data.split(' ')
            for title_name in mp3_classify_title_list:
                if title_name == name:
                    mp3_classify_title_list.remove(name)
                    break
            if len(mp3_classify_title_list) == 0:
                os.remove(title + '_标题.log')
            if len(mp3_classify_title_list) != 0:
                with open(title + '_标题.log', 'w', encoding='utf-8')as tf_2:
                    tf_2.write(' '.join(mp3_classify_title_list))

            """===========================分割线==========================="""
            with open(title + '_链接.log', 'r', encoding='utf-8')as lf:
                lf_data = lf.read()
            mp3_classify_url_list = lf_data.split(' ')
            for url_classify in mp3_classify_url_list:
                if url_classify == url:
                    mp3_classify_url_list.remove(url)
                    break
            if len(mp3_classify_url_list) == 0:
                os.remove(title + '_链接.log')
                os.remove(title + '_标题.log')
            if len(mp3_classify_url_list) != 0:
                with open(title + '_链接.log', 'w', encoding='utf-8')as lf_2:
                    lf_2.write(' '.join(mp3_classify_url_list))
            if (len(mp3_classify_url_list) == 0) or (len(mp3_classify_title_list) == 0):
                with open('已_下_载.log', 'a+', encoding='utf-8')as y:
                    y.write(start_url + ' ' + title + ' ')
            print('==========================logging================================')
            print()
            print()

    def parse_url_data(self, next_url, name, os_path):
        """
        解析歌曲详情页的数据
        :param next_url: 歌曲详情页地址链接
        :param name: 需要保存的歌曲名称
        :param os_path: 保存的路径
        :return:
        """
        headers = {
            'user-agent': random.choice(USER_AGENT)
        }
        response = session.get(url=next_url, headers=headers)
        file = re.findall('danceFilePath="(.*?)";', response.content.decode('gbk'))[0]
        # print(file)
        # mp3_url = 'http://p21.72djapp.cn/m4adj/2016/7201/2602/2324.m4a'
        src_url = 'http://p21.72djapp.cn/m4adj/' + file + '.m4a'
        data = session.get(url=src_url).content
        with open(os_path + '/' + name + '.m4a', 'wb')as f:
            f.write(data)
        print(f'歌曲music========={name}==========下载完成========')


if __name__ == '__main__':
    dj = DJ72()
    dj.parse_start_url_response()

