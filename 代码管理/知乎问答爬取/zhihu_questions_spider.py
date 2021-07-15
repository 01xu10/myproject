# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : zhihu_comment_spider.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/10 16:26
# ------------------------------
'''
    https://www.zhihu.com/api/v4/questions/453629553/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=5&platform=desktop&sort_by=default

'''
from requests_html import HTMLSession
from fake_useragent import UserAgent
from pprint import pprint
from jsonpath import jsonpath
import re, os, pdfkit, time
ua = UserAgent()
session = HTMLSession()

class zhihu_comment(object):
    def __init__(self):
        self.url = input('请输入知乎问答链接：')+' '
        self.start_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset={}&platform=desktop&sort_by=default'
        self.hearders= {
            'user-agent': ua.chrome,
            'referer': self.url.replace(' ', '')
        }
        self.html = '''
                   <!DOCTYPE html>
                   <html lang="en">
                   <head>
                       <meta charset="UTF-8">
                       <title>{}</title>
                   </head>
                   <body>
                   <h1>{}</h1>
        '''
        self.num = 1

    def parse_start_url(self):
        print('*********正在访问**********')
        time.sleep(2)
        i = 0
        question_id = re.findall('question/(.*?) ', self.url)[0]
        while True:
            start_url = self.start_url.format(question_id, i*5)
            response = session.get(start_url, headers=self.hearders)
            # print(is_end)
            self.title = jsonpath(jsonpath(response.json(), '$..question'), '$..title')[0]
            # pprint(self.title)
            self.html = self.html.format(self.title, self.title)
            is_end = jsonpath(response.json(),'$..is_end')[0]
            print('*********logging********关于{}的解答*******'.format(self.title))
            if is_end is False:
                # pprint(response.json()['data'])
                data_list = response.json()['data']
                for data in data_list:
                    self.parse_comment_data(data)

            else:
                data_list = response.json()['data']
                for data in data_list:
                    self.parse_comment_data(data)
                break
            i += 1

    def parse_comment_data(self, data):
        voteup_count = jsonpath(data,'$..voteup_count')[0]
        name = jsonpath(data, '$..name')[0]
        headline = ''.join(jsonpath(data, '$..headline'))
        content = ''.join(jsonpath(data, '$..content'))
        # print(name, headline, voteup_count, content)
        self.create_html_info(name, headline, voteup_count, content)

    def create_html_info(self,name, headline, voteup_count, content):
        title = '''
            <div>
                <h2 style="color:#8800ff">用户：{} - {}</h2>
                <span style="color: #888888">{}人赞同了该回答</span>
            </div><br>
        '''.format(name,headline,voteup_count)
        self.html += title + content + '<br><hr>'
        print('========第{}回答下载完成========='.format(self.num))
        self.num += 1
        # time.sleep(0.2)

    def save_question_info(self,html_content):
        os_path = os.getcwd()+'/知乎/'
        os.makedirs(os_path, exist_ok=True)
        with open(os_path+'{}.html'.format(self.title), 'w', encoding='utf-8') as f:
            f.write(html_content)
        try:
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_file(r'./知乎/{}.html'.format(self.title), r'./知乎/{}.pdf'.format(self.title), configuration=config)
            print("文件下载成功：{}".format(self.title))
        except Exception as e:
            print("文件转换失败")


    def main(self):
        self.parse_start_url()
        self.html = re.sub('<noscript>|</noscript>.*?/>',  '', self.html)
        self.html += '</body></html>'
        self.save_question_info(self.html)
        print('下载完成！！！共{}个回答'.format(self.num-1))

if __name__ == '__main__':
    comment = zhihu_comment()
    comment.main()
