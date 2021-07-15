# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
# @project : Py_Project
# @File    : 携程酒店id获取.py
# @Software: PyCharm
# @Author  : Xu
# @Time    : 2021/4/11 16:09
# ------------------------------

from requests_html import HTMLSession
from pprint import pprint
from fake_useragent import UserAgent
from jsonpath import jsonpath
import json, js2py
session = HTMLSession()
ua = UserAgent()

if __name__ == '__main__':
    js = js2py.EvalJs()
    with open('xiecheng_houtel_id.js', 'r')as f:
        js.execute(f.read())
        r = js.gencb()
    start_url = 'https://m.ctrip.com/restapi/soa2/16709/json/HotelSearch?testab={}'.format(r)
    headers = {
        'user-agent': ua.chrome,
        'content-type': 'application/json;charset=UTF-8',
        'referer': 'https://hotels.ctrip.com/',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"'
    }
    data_1 = {"meta":{"fgt":"","hotelId":"","priceToleranceData":"","priceToleranceDataValidationCode":"","mpRoom":[],"hotelUniqueKey":"","shoppingid":"","minPrice":"","minCurr":""},"seqid":"","deduplication":[427151,374791,19635743,429044,375126,56796268,71403045,4536895,700672,473871,18460327],"filterCondition":{"star":[],"rate":"","rateCount":[],"priceRange":{"lowPrice":0,"highPrice":-1},"priceType":"","breakfast":[],"payType":[],"bedType":[],"bookPolicy":[],"bookable":[],"discount":[],"zone":[],"landmark":[],"metro":[],"airportTrainstation":[],"location":[],"cityId":[],"amenty":[],"promotion":[],"category":[],"feature":[],"brand":[],"popularFilters":[],"hotArea":[],"ctripService":[],"priceQuickFilters":[],"applicablePeople":[]},"searchCondition":{"sortType":"1","adult":1,"child":0,"age":"","pageNo":2,"optionType":"City","optionId":"1","lat":0,"destination":"","keyword":"","cityName":"北京","lng":0,"cityId":1,"checkIn":"2021-04-22","checkOut":"2021-04-23","roomNum":1,"mapType":"gd","travelPurpose":0,"countryId":1,"url":"https://hotels.ctrip.com/hotels/list?city=1&checkin=2021/04/22&checkout=2021/04/23&optionId=1&optionType=City&directSearch=0&display=%E5%8C%97%E4%BA%AC&crn=1&adult=1&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=1&","pageSize":10,"timeOffset":28800,"radius":0,"directSearch":0,"signInHotelId":0,"signInType":0,"hotelIdList":[]},"queryTag":"NORMAL","genk":True,"genKeyParam":{"a":0,"b":"2021-04-22","c":"2021-04-23","d":"zh-cn","e":2},"webpSupport":True,"platform":"online","pageID":"102002","head":{"Version":"","userRegion":"CN","Locale":"zh-CN","LocaleController":"zh-CN","TimeZone":"8","Currency":"CNY","PageId":"102002","webpSupport":True,"userIP":"","P":"84362864210","ticket":"","clientID":"1618114092608.33n7u4","group":"ctrip","Frontend":{"vid":"1618114092608.33n7u4","sessionID":15,"pvid":100},"Union":{"AllianceID":"","SID":"","Ouid":""},"HotelExtension":{"group":"CTRIP","hasAidInUrl":False,"Qid":"384345819233","WebpSupport":True,"hotelUuidKey":"fO1xkgKt1eFME6MY0YqUYO7E4YpOeSMELQjkoWhYgMj6kenHvdNjmYoTjBcxzNvZ8j4Y8ziLHxbSv9Fr4YA8J8kwpNy5TILbvDbWtOYQkjMcynYqcvHfYTGYNHwQ9jBteGziXDYDYHYNlvF9e4cEgHipDYtY5YQ6EG4KDaw4PeL7RONjorZFYtcJB0ymr3FYglWZqvq5x49eD9YPZxH4x9BYbHikzwcljG9EobJBAWaSjSr3AJ4GicUwZQvGqRBnjMqYknjGrt0ygaiHdwXfRfZE9QjadxzZxn9EGBEDsEm0WMQefswSlEskj9beLFi8dYfNrG3eD9eqAxO8i9Di5pxpZWazjcZeB1wnPKk8wtcilARF3jn3eo4Edcy1SvfZigFEQ0yHTvLLKkfEtFKSDwGmiOoRPTj7r1fY90JhOyXrfdjcMe1OjNFKM0jspwc7xsSxozx30x3kEqlEb3E1SWmaeLawlQE1mj7feFhi3gYqkrUAEsty5Hv3GiQzEZby6qvkkKmfWOSE78jcSeUGxacjor80EBnWbDe5Sj48YngjdcxgbxaQxzlxcZE79EThEUGWapeF5w3pEH8jXde70igQYUfr56ecMez7YgaEU9wDLWgHiPPK4FEOkEMBElgWs9eNtwQ0EqTj5FekdiTqYU5razeQSeOaEdsY3MEN9w6TW74iAYfqYM8ibZi7ZiBTjdYzLwH7EzMYS5wMhEcpJn9Y5Tw1Yh3RmZwTzRUXvB8RqSWtpRshRZmwptWmbJG7jcoyXYsFJtOi9GemGRQ3vqqxscJzLrBhyDTYhNY98jQPEO1xafEtfIUY8SRPAwqfRfhj3FRk0R9kE7PW9BvAtYUBwF4WmZj9Y4gjzPwc0vtGjbYoLRpZJQHiFMwcQeA3jL7w97EQYMoRXDJ68i7dwUneN0j6hil1EmY6pRB5wpQRa3vsFR1fWbORfcRP4wtNW5MJdtRmfR9YDlEQpjUkWt1WAgWAtY6sYX1Y9zRkaY9FWMGYUgYDaYN6jcQeAsEfqWF8eDUwUBePnjhHYFGyDHEPQjB5E8QrOajUFwFP"}}}
    play_load = json.dumps(data_1)
    response = session.post(start_url,headers=headers,data=play_load)
    # pprint(response.json())
    hotelList = jsonpath(response.json(), '$..hotelList')
    hotelList_1 = jsonpath(hotelList,'$..hotelName')
    pprint(hotelList_1)

