# -*- coding: UTF-8 -*-
import pymysql.cursors

class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_date(self, data):
        if data is None:
            return
        self.datas.append(data)

    def collect_dates(self, datas):
        if datas is None:
            return
        for data in datas:
            self.datas.append(data)

    def clear_dates(self):
        if self.datas is None:
            return
        self.datas = []

    def print_date(self):
        for data in self.datas:
            print('%s' % data)

    def delDB(self):
        connection = pymysql.connect(host='localhost',user='root',password='root',db='seckill',charset='utf8mb4')
        try:
            with connection.cursor() as cursor:
                # 删除麦田今日的数据
                sqlDel = "delete from seckill.houseinfo where date_format(createTime,'%Y-%m-%d')= date_format(now(),'%Y-%m-%d') and copyType = '麦田'"
                result = cursor.execute(sqlDel)
                connection.commit()
        finally:
            connection.close()

    def insertDB(self):
        connection = pymysql.connect(host='localhost',user='root',password='root',db='seckill',charset='utf8mb4')
        if len(self.datas) <= 0:
            return
        try:
            with connection.cursor() as cursor:
                # 添加新数据
                #sqlIns = 'insert into 'seckill.houseinfo'(priceTotal,priceAvg,area,zone,houseName,houseFloor,houseType,houseWay,copyType) values (%s,%s,'3','4','5','6','7','8','麦田')"
                for data in self.datas:
                    sqlIns = 'insert into seckill.houseinfo(priceTotal,priceAvg,area,zone,houseName,houseFloor,houseType,houseWay,copyType) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sqlIns, (data['priceTotal'] , data['priceAvg'], data['area'], data['zone'], data['houseName'], data['houseFloor'], data['houseType'], data['houseWay'], '麦田'))

                connection.commit()
        finally:
            connection.close()

    def output_html(self):
        fout = open('output.html','w')
        fout.write("<html>")
        fout.write("<head>")
        fout.write("<title>福州购房指导交流群</title>")
        fout.write('<meta name="viewport" content="width=device-width, initial-scale=1">')
        fout.write('<link rel="stylesheet" href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css">')
        fout.write('<script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>')
        fout.write('<script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>')
        fout.write("</head>")
        fout.write("<body>")
        fout.write('<table class="table">')
        fout.write("<tr>")
        fout.write("<th>区域</th>")
        fout.write("<th>小区名称</th>")
        fout.write("<th>户型</th>")
        fout.write("<th>楼层</th>")
        fout.write("<th>朝向</th>")
        fout.write("<th>面积</th>")
        fout.write("<th>总价</th>")
        fout.write("<th>均价</th>")
        fout.write("</tr>")
        # ascii
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['zone'])
            fout.write("<td>%s</td>" % data['houseName'])
            fout.write("<td>%s</td>" % data['houseType'])
            fout.write("<td>%s层</td>" % data['houseFloor'])
            fout.write("<td>%s</td>" % data['houseWay'])
            fout.write("<td>%s</td>" % data['area'])
            fout.write("<td>%s万</td>" % data['priceTotal'])
            fout.write("<td>%s元/㎡</td>" % data['priceAvg'])
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()