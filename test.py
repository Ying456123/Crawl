import requests
from lxml import etree
from Weibo import Weibo
import json
weibos = []
userId = 6067213401
url = 'https://weibo.cn/u/%d?page=1' % userId
#please type your own cookie
cookie = {"Cookie":""}
print('prepared to crawl')
html = requests.get(url,cookies = cookie).content
selector = etree.HTML(html)
print('get the page number')
pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
#crawl every page of this user
for page in range(1,pageNum+1):
    url = 'http://weibo.cn/u/%d?page=%d' % (userId, page)
    lxml = requests.get(url, cookies=cookie).content
    selector = etree.HTML(lxml)
    weiboitems = selector.xpath('//div[@class="c"][@id]')
    #parse every weibo
    for item in weiboitems:
        weibo = Weibo()
        weibo.id = item.xpath('./@id')[0]
        cmt = item.xpath('./div/span[@class="cmt"]')
        if len(cmt) != 0:
            weibo.isrepost = True
            weibo.content = cmt[0].text
        else:
            weibo.isrepost = False
        ctt = item.xpath('./div/span[@class="ctt"]')[0]
        if ctt.text is not None:
            weibo.content += ctt.text
        for a in ctt.xpath('./a'):
            if a.text is not None:
                weibo.content += a.text
            if a.tail is not None:
                weibo.content += a.tail
        if len(cmt) != 0:
            reason = cmt[1].text.split(u'\xa0')
            if len(reason) != 1:
                weibo.repostreason = reason[0]
        ct = item.xpath('./div/span[@class="ct"]')[0]
        time = ct.text.split(u'\xa0')[0]
        weibo.time = time
        weibos.append(weibo)

#save weibos to a doc
fo = open("E:/spider_test/%s" % userId, "w", encoding="utf-8")
for weibo in weibos:
    fo.write(weibo.time+'\t'+weibo.content+'\n')
fo.close()







