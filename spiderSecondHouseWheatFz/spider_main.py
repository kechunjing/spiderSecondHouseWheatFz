# -*- coding: UTF-8 -*-
import time

from spiderSecondHouseWheatFz import url_manager, html_downloader, html_parser, html_outputer
import traceback

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        # 爬虫
        self.action()
        # 输出
        #self.outputer.output_html()
        self.outputer.insertDB()
    def action(self):
        # 删除今日的数据
        self.outputer.delDB()
        count = 1
        self.urls.add_new_url(root_url+str(count))
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print('craw : %s' % new_url)
                # 获取html信息
                html_cont = self.downloader.downloader(new_url)
                # 解析获取的html，并保存数据
                new_data = self.parser.parse(new_url,html_cont)
                # 收集数据
                self.outputer.collect_dates(new_data)
                # 保存数据
                self.outputer.insertDB()
                # 清空临时数据
                self.outputer.clear_dates()
                #最多限制3000页
                if count == 3000:
                    break
                if count % 100 == 0:
                    #睡眠100秒
                    print("睡眠100秒")
                    time.sleep(100)
                _dateLen = len(new_data)
                if _dateLen == 10:
                    count = count + 1
                    self.urls.add_new_url(root_url+str(count))
            except:
                traceback.print_exc()
                print('craw fail')
if __name__ == "__main__":
    root_url = "http://fz.maitian.cn/esfall/PG"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)