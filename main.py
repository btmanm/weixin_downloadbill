# -*- coding: utf-8 -*-

import os
import subprocess
from datetime import datetime, timedelta

from Tkinter import *

import tkFileDialog
import tkMessageBox
import tkFont

from weixin_mch_api import download_bill

import config
import csv

try:
    cur_path = os.path.dirname(os.path.abspath(__file__))
except NameError:
    import sys
    cur_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    
class Application(Frame):
    def run(self):
        appid = self.var_appid.get().strip()
        if len(appid) == 0:
            tkMessageBox.showinfo(title=u"错误", message="请输入公众账号ID")
            return

        mch_id = self.var_mch_id.get().strip()
        if len(mch_id) == 0:
            tkMessageBox.showinfo(title=u"错误", message="请输入商户号")
            return

        mch_key = self.var_mch_key.get().strip()
        if len(mch_key) == 0:
            tkMessageBox.showinfo(title=u"错误", message="请输入商户密钥")
            return

        bill_date_from = self.var_bill_date_from.get().strip()
        if len(bill_date_from) == 0:
            tkMessageBox.showinfo(title=u"错误", message="请输入开始日期")
            return
            
        path = self.var_path.get().strip()
        if len(path) == 0:
            tkMessageBox.showinfo(title=u"错误", message="请选择输出目录")
            return
            
        sub_mch_id = self.txt_sub_mch_id.get(1.0, END)
        if len(sub_mch_id) > 0:
            sub_mch_ids = list(set(sub_mch_id.split()))
        else:
            sub_mch_ids = []
        
        # save settings    
        config.save(appid, mch_id, mch_key, sub_mch_id, path)

        bill_date_to = self.var_bill_date_to.get().strip()
        if len(bill_date_to) == 0:
            bill_date_to = datetime.now().strftime("%Y%m%d")
        
        s = datetime.strptime(bill_date_from, "%Y%m%d")
        e = datetime.strptime(bill_date_to, "%Y%m%d")
        
        while s < e:
            if len(sub_mch_ids) > 0:
                for sub_mch_id in sub_mch_ids:
                    r = download_bill(mch_key, appid, mch_id, s, sub_mch_id)
                    self.save_bill(r, s, mch_id, sub_mch_id)
            
            else:
                r = download_bill(mch_key, appid, mch_id, s)
                self.save_bill(r, s, mch_id)
                
            s += timedelta(days=1)
            
        tkMessageBox.showinfo(title=u"成功", message="账单下载结束")
        subprocess.call('explorer "%s"' % path.replace('/', '\\'), shell=True)
        
    
    def save_bill(self, text, bill_date, mch_id, sub_mch_id=None):
        bill_date = bill_date.strftime("%Y%m%d")
        if text.startswith('<xml>'):
            f = '%s_%s_%s.xml' % (bill_date, mch_id, sub_mch_id) if sub_mch_id else '%s_%s_.xml' % (bill_date, mch_id)
        else:
            f = '%s_%s_%s.csv' % (bill_date, mch_id, sub_mch_id) if sub_mch_id else '%s_%s_.csv' % (bill_date, mch_id)

        fullname = os.path.join(self.var_path.get().strip(), f)
        with open(fullname, 'wb') as csv:
            csv.write(text)
            
    def select_path(self):
        self.var_path.set(tkFileDialog.askdirectory())
        
    def createWidgets(self, settings):
        row = 0
        
        # 公众号ID
        self.lbl_appid = Label(self, text=u"公众帐号ID", fg='red')
        self.lbl_appid.grid(column=0, row=row, sticky=(E, N))

        self.var_appid = StringVar(self, value=settings.get('appid')) 
        self.txt_appid = Entry(self, textvariable=self.var_appid, width=60, font=self.font)
        self.txt_appid.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        
        # 商户号
        self.lbl_mch_id = Label(self, text=u"商户号", fg='red')
        self.lbl_mch_id.grid(column=0, row=row, sticky=(E, N))

        self.var_mch_id = StringVar(self, value=settings.get('mch_id')) 
        self.txt_mch_id = Entry(self, textvariable=self.var_mch_id, width=60, font=self.font)
        self.txt_mch_id.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        # 商户密钥
        self.lbl_mch_key = Label(self, text=u"商户密钥", fg='red')
        self.lbl_mch_key.grid(column=0, row=row, sticky=(E, N))

        self.var_mch_key = StringVar(self, value=settings.get('mch_key')) 
        self.txt_mch_key = Entry(self, textvariable=self.var_mch_key, width=60, font=self.font)
        self.txt_mch_key.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        # 子商户号
        self.lbl_sub_mch_id = Label(self, text=u"子商户号")
        self.lbl_sub_mch_id.grid(column=0, row=row, sticky=(E, N))

        self.txt_sub_mch_id = Text(self, height=5, width=60, font=self.font)
        if  settings.get('sub_mch_id'):
            self.txt_sub_mch_id.insert(END, settings.get('sub_mch_id'))
        self.txt_sub_mch_id.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        # 开始日期
        self.lbl_bill_date_from = Label(self, text=u"开始日期", fg='red')
        self.lbl_bill_date_from.grid(column=0, row=row, sticky=(E, N))

        self.var_bill_date_from = StringVar() 
        self.var_bill_date_from.set((datetime.now() - timedelta(days=1)).strftime("%Y%m%d")) 
        self.txt_bill_date_from = Entry(self, width=8, textvariable=self.var_bill_date_from, font=self.font)
        self.txt_bill_date_from.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        # 结束日期
        self.lbl_bill_date_to = Label(self, text=u"结束日期")
        self.lbl_bill_date_to.grid(column=0, row=row, sticky=(E, N))

        self.var_bill_date_to = StringVar() 
        self.txt_bill_date_to = Entry(self, width=8, textvariable=self.var_bill_date_to, font=self.font)
        self.txt_bill_date_to.grid(column=1, row=row, columnspan=2, sticky=(W, N))

        row += 1
        
        # 输出目录
        self.lbl_path = Label(self, text=u"输出目录", fg='red')
        self.lbl_path.grid(column=0, row=row, sticky=(E, N))

        path = settings.get('path')
        self.var_path = StringVar(self, value=path if path else os.path.dirname(os.path.abspath(cur_path))) 
        self.txt_path = Entry(self, textvariable=self.var_path, width=55, font=self.font)
        self.txt_path.grid(column=1, row=row, sticky=(W, N, E))

        self.btn_select_path = Button(self, text=u"...", command=self.select_path)
        self.btn_select_path.grid(column=2, row=row, sticky=(E))
        
        row += 1
        
        # 执行按钮
        self.btn_run = Button(self, width=20, text=u"下载", fg='blue', command=self.run)
        self.btn_run.grid(column=1, row=row, pady=(15, 0))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.font = tkFont.nametofont("TkDefaultFont")
        self.font.configure(family='MS Gothic', size=9)

        self.grid(column=0, row=0, sticky=(N, W, E, S), padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure (0, weight=1)

        settings = config.load()
        self.createWidgets(settings)

root = Tk()
root.title(u"微信商户平台对账单下载")
root.rowconfigure(0, weight=1)
root.columnconfigure (0, weight=1)

root.resizable(width=False, height=False)
app = Application(master=root)
root.mainloop()
