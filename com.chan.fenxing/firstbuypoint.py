#coding=utf-8
import tushare as ts
import pymongo

from multiprocessing.pool import ThreadPool

class fenxing:
    """分型的判断及属性的填充"""

    #分型类型：low——底分型  high——顶分型
    fenxingtype ='low'
    maxprice=100
    conn = pymongo.MongoClient('192.168.222.188', port=27017)
    #是否笔结束的分型
    isok = 0

    def __init__(self,type,isok):
        self.fenxingtype = type
        self.isok = isok


    #判断分型的方法
    def check(self,df,code,day):
        #底分型判断条件
        if (df['high'][day]>df['high'][day+1]<df['high'][day+2])&(df['low'][day] > df['low'][day+1] < df['low'][day+2]):
            # print '底分型成立', code
            lowcount = 0
            #前面（day-3/-2/-1）是下降趋势
            for item in range(1,10):

                itemcount = self.trend(df,item+day)
                if itemcount > 0:
                    lowcount+=1
                    if lowcount >4:
                        print code,'向下成笔!'
                        print item
                        print '当前价格',df['high'][0]
                        break



        #顶分型判断条件
        if(df['high'][day] < df['high'][day+1] > df['high'][day+2])&(df['low'][day] < df['low'][day+1] > df['low'][day+2]):
            # print '顶分型成立',code
            return fenxing('high',1)

        # print '趋势段',code


    #判断两根K线的权重
    def trend(self,df,day):
        #如果是下降趋势的，返回1
        if (df['high'][day] < df['high'][day+1])&(df['low'][day] < df['low'][day+1]):
            return 1

        if (df['high'][day] > df['high'][day + 1]) & (df['low'][day] > df['low'][day + 1]):
            return -1


    def monitor(self,code):
        try:
            df = ts.get_hist_data(code).head(15)
            #以下方法输入1表示从今天前一天算起，输入0表示从今天算起
            self.check(df,code,1)

            #如果是底分型，判断前面是否为下降趋势段

            #如果是下降趋势，则可以买入
        except Exception as e:
            print e



    def monitorthread(self):
        stock_codes = []
        for item in self.conn.mystock.todaydata.find():
            stock_codes.append(item['code'])
        pool = ThreadPool(60)
        pool.map(self.monitor, stock_codes)

# fenxing('',0).monitor('600616')
fenxing('',0).monitorthread()

