# -*- coding: UTF-8 -*-
import re
import urllib.parse
from bs4 import BeautifulSoup

class HtmlParser(object):

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_datas(page_url, soup)
        return new_data

    def _get_new_datas(self, page_url, soup):
        res_dates = []
        # 查看所有div中类为list_title的对象
        houseList = soup.find_all('div', class_='list_title')
        for house in houseList:
            res_date = {}
            _price = house.find('div', class_='the_price').get_text()
            _area = house.find('div', class_='the_area').get_text()
            _house_info = house.find('p', class_='house_info').get_text()
            _house_hot = house.find('p', class_='house_hot').get_text()
            # 总价
            _priceTotal = re.findall('.*?(?=万)', _price)
            # 均价
            _priceAvg = re.findall('(?<=元).*?(?=元)', _price)
            # 面积
            _newArea = re.findall('.*?(?=㎡)', _area)
            # 区域
            _zone = re.findall('(?<=\[).*?(?=\])', _house_info)
            # 楼盘名称
            result = {}
            result = re.split(',',_house_info)
            _houseName = result[len(result)-1].strip()

            resultTmp = {}
            _houseHotTmp = _house_hot.replace(' ','').replace('\r\n','').replace(' ','')
            resultTmp = re.split('\|',_houseHotTmp)
            #楼层
            _houseFloor = re.findall('(?<=\/).*?(?=层)', resultTmp[0])
            #户型
            _houseType = resultTmp[1]
            # 朝向
            _houseWay = resultTmp[2]

            res_date['priceTotal'] = _priceTotal[0]
            res_date['priceAvg'] = _priceAvg[0]
            res_date['area'] = _newArea[0]
            res_date['zone'] = _zone[0]
            res_date['houseName'] = _houseName
            if _houseFloor is not None:
                fCount = len(_houseFloor)
                if fCount > 0:
                    res_date['houseFloor'] = _houseFloor[0]
                else:
                    res_date['houseFloor'] = ""
            else:
                res_date['houseFloor'] = ""
            res_date['houseType'] = _houseType
            res_date['houseWay'] = _houseWay

            res_dates.append(res_date)
            #print('总价：%s, 均价(元/㎡):%s, 面积(㎡):%s， 区域：%s, 楼盘名称: %s ' % (_priceTotal[0],_priceAvg[0],_newArea[0],_zone[0],_houseName))
            #print('楼层：%s, 户型:%s, 朝向:%s' % (_houseFloor[0],_houseType,_houseWay))

        return res_dates