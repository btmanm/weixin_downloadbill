# -*- coding: utf-8 -*-

import cgi
import json
import logging
import random
import string
import urllib2

from hashlib import md5

from datetime import datetime, date

def dict2xml(params):
    xml = "<xml>"
    for k, v in params.items():
        v = v.encode("utf8")
        k = k.encode("utf8")
        xml += "<" + k + ">" + cgi.escape(v) + "</" + k + ">"
            
    xml += "</xml>"
    return xml

def get_nonce_str(length=32):
    rule = string.letters + string.digits
    str = random.sample(rule, length)

    return "".join(str)

def sign(params, key=None):
    """
    md5签名
    https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_3
    """
    l = ['%s=%s' % (k, params.get(k, '').strip()) for k in sorted(params.keys())]
    s = '&'.join(l)
    if key:
        s += '&key=' + key

    return md5(s.encode('utf-8')).hexdigest().upper()
    
def download_bill(key, appid, mch_id, bill_date, sub_mch_id=None):
    """
    下载对账单
    :param bill_date: 下载对账单的日期
    :return: 返回的结果数据
    """
    while True:
        try:
            if isinstance(bill_date, (datetime, date)):
                bill_date = bill_date.strftime('%Y%m%d')
        
            data = {
                'appid': appid,
                'mch_id': mch_id,
                'bill_date': bill_date,
                'nonce_str': get_nonce_str(),
                'bill_type': 'ALL',
            }
            
            if sub_mch_id:
                data['sub_mch_id'] = sub_mch_id
                
            data["sign"] = sign(data, key)
            
            url = 'https://api.mch.weixin.qq.com/pay/downloadbill'
            
            req = urllib2.Request(url)
            req.add_data(dict2xml(data))
            
            r = urllib2.urlopen(req)
            
            logging.debug('downloaded.')
            return r.read()
        except Exception as e:
            import sys
            import traceback
            
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
