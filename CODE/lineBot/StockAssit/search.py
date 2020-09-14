# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:38:09 2019

@author: yeh
"""

from bs4 import BeautifulSoup
import requests

def get_webservice(url):
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content)
    r = soup.find('string').text
    return r
def getPrice(stock):
    url = "http://61.220.30.176/WebOrder/GVETransacs.asmx/QueryQuote5Price?compcode=" + stock
    client = get_webservice(url)
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
        
    #price = client.service.QueryQuote5Price(stock, )
    r = ET.fromstring(client)
    r_new = "<您查詢的股價>\n"+"成交價: "+str(r[0][0].text)+\
                                "\n"+"成交量: "+str(r[0][1].text)+\
                                "\n"+"委買價: "+str(r[0][2].text)+\
                                "\n"+"委買量: "+str(r[0][22].text)+\
                                "\n"+"委賣價: "+str(r[0][12].text)+\
                                "\n"+"委賣量: "+str(r[0][23].text)+\
                                "\n"+"昨收價: "+str(r[0][24].text)+\
                                "\n"+"漲停價: "+str(r[0][25].text)+\
                                "\n"+"跌停價: "+str(r[0][26].text)
    return r_new

def getOrder():
    url = "http://61.220.30.176/WebOrder/GVETransacs.asmx/QueryWaitingOrderListGVE3XML_NS?TokenString=143986D99078C7FA6A0B5BCD8C00ACA4A1DB04385D50EFF4682053C7A0AA4979D7B81BE534ECF4C969E3EA65DFF55137F00EEF9BA3C9FF02C78BA63C37C6202EA694BE201140613AF586FADA1560C84FD5517892C838E79199922D9DDF92DE7626D7BE97ADF465278B4ABD03F7CDF9573B578E7BA64604142854EF2CF90DE997F75D73B2D6499FB20F6841F13751C5C906CB71B300D30C76&Language=TC"
    client = get_webservice(url)
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
        
    #price = client.service.QueryQuote5Price(stock, )
    r = ET.fromstring(client)
    arr = []
    for country in r.findall('Order'):
            #i=i+1
            OrderTime = country.get('OrderTime')
            OrderID = country.get('OrderID')
            AssetID = country.get('AssetID')
            CompName = country.get('CompName')
            Price = country.get('Price')
            Volume = country.get('Volume')
            BSAction = country.get('BSAction')
            OrderType = country.get('OrderType')
            output ="<<成交資訊>>\n" +"委託時間: " + OrderTime + \
                            "\n"+ "委託ID: " + OrderID + \
                            "\n"+ "股票代碼: " + AssetID + \
                            "\n"+ "公司名稱: " + CompName + \
                            "\n"+ "委託價格: " + Price + \
                            "\n"+ "委託數量: " + Volume + \
                            "\n"+ "買賣類型: " + BSAction + \
                            "\n"+ "掛單類型: " + OrderType+"\n"\
                    +"----------------------"
            arr.append(output)
    if len(arr):
        a = "\n".join(arr)
    else:
        a = "目前沒有委託資訊"
    return a

def getInStock():
    url = "http://61.220.30.176/WebOrder/GVEAccount.asmx/QueryTodayPositionGve3XML_NS?TokenString=143986D99078C7FA6A0B5BCD8C00ACA4A1DB04385D50EFF4682053C7A0AA4979D7B81BE534ECF4C969E3EA65DFF55137F00EEF9BA3C9FF02C78BA63C37C6202EA694BE201140613AF586FADA1560C84FD5517892C838E79199922D9DDF92DE7626D7BE97ADF465278B4ABD03F7CDF9573B578E7BA64604142854EF2CF90DE997F75D73B2D6499FB20F6841F13751C5C906CB71B300D30C76&Language=TC&SubTotalItem=&SortItem=AssetCode%20Asc"
    client = get_webservice(url)
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
        
        #price = client.service.QueryQuote5Price(stock, )
    r = ET.fromstring(client)
    arr = []
    for country in r.findall('PortfolioAsset'):
        AssetCode = country.get('AssetCode')
        CompName = country.get('CompName')
        Hold = country.get('Hold')
        Cost = country.get('Cost')
        QuotePrice = country.get('QuotePrice')
        UpDown = country.get('UpDown')
        PL = country.get('PL')
        UnRealizedPL = country.get('UnRealizedPL')
        output = "<<庫存資訊>>\n" + "股票代碼: " + AssetCode + \
                                "\n"+ "公司名稱: " + CompName + \
                                "\n"+ "持有數量: " + Hold + \
                                "\n"+ "持有成本: " + Cost + \
                                "\n"+ "現價: " + QuotePrice + \
                                "\n"+ "漲跌: " + UpDown + \
                                "\n"+ "盈虧 " + PL + \
                                "\n"+ "累積未實現損益: " + UnRealizedPL +"\n"\
                                +"----------------------"
        arr.append(output)
    
    if len(arr):
        a = "\n".join(arr)
    else:
        a = "目前沒有庫存資訊"
    return a
def getDeal():
    url = "http://61.220.30.176/WebOrder/GVETransacs.asmx/QueryDealLogGVE3ByGMRDayRangeLiteXML_NS?GMRID=1111708496&StartDate=2019/01/02&EndDate=2019/12/20&Language=TC"
    client = get_webservice(url)
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
        
        #price = client.service.QueryQuote5Price(stock, )
    r = ET.fromstring(client)
    arr = []
    for country in r.findall('GVEUserLog'):
        LogTime = country.get('LogTime')
        AssetCode = country.get('AssetCode')
        CompName = country.get('CompName')
        BSAction = country.get('BSAction')
        OrderType = country.get('OrderType')
        Price = country.get('Price')
        Volume = country.get('Volume')
        fee = country.get('fee')
        logdesc = country.get('logdesc')
        output = "<<成交資訊>>\n" + "交易時間: " + LogTime + \
                                "\n"+ "股票代碼: " + AssetCode + \
                                "\n"+ "公司名稱: " + CompName + \
                                "\n"+ "買賣類型: " + BSAction + \
                                "\n"+ "掛單類型: " + OrderType + \
                                "\n"+ "成交價: " + Price + \
                                "\n"+ "成交量 " + Volume + \
                                "\n"+ "手續費 " + fee + \
                                "\n"+ "交易訊息: " + logdesc+"\n"\
                                +"----------------------"
        arr.append(output)
    if len(arr):
        a = "\n".join(arr)
    else:
        a = "目前沒有成交資訊"
    
    return a