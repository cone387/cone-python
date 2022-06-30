# -*- coding:utf-8 -*-

# author: Cone
# datetime: 2022/3/20 上午11:19
# software: PyCharm
import requests
from pyquery import PyQuery
from lxml.html import etree
from cone.hooks import lib
from cone.utils.functional import cached_property


class Response(requests.Response):

    @cached_property
    def doc(self):
        return PyQuery(self.text)

    @cached_property
    def etree(self) -> etree._Element:
        return self.doc[0]

    def xpath(self, path):
        return self.etree.xpath(path)

# lib.hook_model_object('requests.Response', Response)
# #
#
# response: Response = requests.get(
#     'https://www.chinanews.com.cn/gn/2022/03-18/9706104.shtml',
# )
# response.encoding = 'utf8'
# print(response.doc("h1:first").text())
# print(response.xpath('//h1/text()')[0].strip())

# str.b = 1

print.a = 1

a = str(4)

print(a.b)


# print(requests.Response.doc)