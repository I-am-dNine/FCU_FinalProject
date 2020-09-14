# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:41:34 2019

@author: Admin
"""
from bs4 import BeautifulSoup
import requests

def get_webservice(url):
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content)
    r = soup.find('string').text
    return r
#取消委託功能
def cancelOrder(orderid):
        url = "http://61.220.30.176/WebOrder/GVETransacs.asmx/CancelOrderStr_NS?TokenString=143986D99078C7FA6A0B5BCD8C00ACA4A1DB04385D50EFF4682053C7A0AA4979D7B81BE534ECF4C969E3EA65DFF55137F00EEF9BA3C9FF02C78BA63C37C6202EA694BE201140613AF586FADA1560C84FD5517892C838E79199922D9DDF92DE7626D7BE97ADF465278B4ABD03F7CDF9573B578E7BA64604142854EF2CF90DE997F75D73B2D6499FB20F6841F13751C5C906CB71B300D30C76&OrderID=" + orderid
        #get_webservice(url)
        client = get_webservice(url)
        
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        r = ET.fromstring(client)
        
        for neighbor in r.iter('Column1'):
            x = neighbor.text
        
        if x =='fail':
            return x
        else:
            return x
    
#手動委託下單功能
def putOrder(bsaction, stockid,  ordertype, volume, price):
        url = "http://61.220.30.176/WebOrder/GVETransacs.asmx/PutOrderXML3?GMRIDStr=BCSP&CompCode="+stockid+"&Price="+price+"&Volume="+volume+"&BSAction="+bsaction+"&OrderType="+ordertype+"&IsOddLot=0&Currency=TWD&OrderNote=ROD&OCType=0&CombineNo=&OrderParameter=0&Lang=TC&str_ip=127.0.0.1"
        client = get_webservice(url)
        
        """try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        r = ET.fromstring(client)
        """
        r = client.split("\"")
        if r[1] == "Success":
            return "委託下單成功"
            #tk.messagebox.showinfo(title='回報', message='Success')
        elif r[1] == "Failure":
            return "委託下單失敗"+'原因:'+r[5]
            #tk.messagebox.showinfo(title='回報',message = 'Failure\n'+'原因:'+new[5])
        else:
            return "委託下單失敗"+'原因:格式輸入錯誤'
            #tk.messagebox.showinfo(title='回報',message = 'Failure\n'+'原因:格式輸入錯誤')