import person
import time
import xlrd
import threading
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join

resultData = 'DataRemains\ResultData.txt'

def readFile():
    f = open(resultData,'r')
    fout = f.read()
    f.close()
    return fout

def writeFile(outStr):
    f = open(resultData,'w')
    f.write(outStr)
    f.close()


class icmrProcess():
    def __init__(self,datadict,tag):
        self.datadict = datadict
        self.uname = "GDHHNKTN"
        self.pas = "GDHHNKTN@icmr"
        self.br = webdriver.Chrome(executable_path="C:\Program Files\chromedriver")
        self.personObject = []
        self.tag = tag
        self.createEntries()

    def webCreation(self):
        self.br.get("https://cvstatus.icmr.gov.in/")
        person.wait()
        self.br.find_element_by_xpath('//*[@id="username"]').send_keys(self.uname)
        self.br.find_element_by_xpath('//*[@id="passwd"]').send_keys(self.pas)
        self.br.find_element_by_xpath('//*[@id="login_btn"]').click()
    
    def createEntries(self):
        print('createEntries')
        outStr = ''
        try:
            templist = []
            for j in self.datadict:
                print(j)
                p = person.register(j,self.br,self.tag)
                self.personObject.append(p)
                if not self.tag:
                    templist.append(p.getDataList())
                    outStr+=p.show()
            if not self.tag:
                self.datadict=templist
                writeFile(outStr)
            print('Finished')
        except Exception as e:
            print(e)
            
    #  def fileAppend(self,outStr):
        #     f = open(resultData,'a')
        #     f.write(outStr)
        #     f.close()
    
    # def fileEnter(self,outStr):
        # fdata = ''
        # j=0
        # for i in datadict:
        #     line=';'.join(i)+'\n'
        #     if outStr[j]!=line:
        #         fdata+=line
        #     elif outStr[j]==line:
        #         j+=1
        # if fdata=='':
        #     # print(outStr,'==',fdata)
        #     if(path.exists(resultData)):
        #         os.remove(resultData)
        # else:
        #     # outStr = fdata.replace(outStr,'')
        #     f = open(resultData,'w')
        #     f.write(fdata)
        #     f.close()

    def enterAllData(self):
        fout = readFile()
        for p in self.personObject:
            if p.enterValues():
                fout = fout.replace(p.show(),'')
                writeFile(fout)

    # def enterDataOf(self,start,end):
        # flag = False
        # outStr = self.personObject[0]
        # print(self.personObject)
        # for p in self.personObject:
        #     outStr = p
        #     # print(p.id,start,end,p.id==start or p.id==end)
        #     if p.id==start:
        #         flag=True
        #     if flag and not p.enterValues():
        #         self.fileAppend(p.show())
        #     if p.id==end:
        #         break
            
            
            # if ev:
            #     try:
            #         outStr=';'.join(j)+'\n'
            #         print('Remove: ',outStr)
            #         f = open('DataRemains\\'+self.fname,'r')
            #         fout = f.read()
            #         f.close()
            #         f = open('DataRemains\\'+self.fname,'w')
            #         # print('file: ',fout)
            #         if fout==outStr:
            #             f.close()
            #             os.remove('DataRemains\\'+self.fname)
            #         else:
            #             fout = str(fout).replace(outStr,'')
            #             # print('After Process: ',fout)
            #             f.write(fout)
            #             f.close()
            #     except:
            #         f.close()


def getIndex(header,req):
    arr = []
    l = len(header)
    for i in req:
        try:
            elem = header.index(i) 
            arr.append(elem)  
        except:
            arr.append(l)
            l+=1
    return arr



def getXlData(fname,start=0,end=''):
    work = xlrd.open_workbook(fname)
    worksheet = work.sheet_by_index(0)
    cols = worksheet.ncols
    rows = worksheet.nrows
    itr = 0
    while (worksheet.cell(itr,0).value!='S.NO'):itr+=1
    table = []
    cols = getIndex([str(worksheet.cell(itr,i).value).strip() for i in range(cols)],['S.NO','COVID NUMBER','SAMPLE DATE','NAME',
    'AGE','SEX','COMPLETE ADDRESS','MOBILE NUMBER','RESULT','DATE OF RESULT','SRF ID','KIT USED','NG VALUE','RDRP VALUE'])
    print(cols)
    flag = False
    for i in range(itr+1,rows):
        rowval = []
        cno = str(worksheet.cell(i,1).value)
        if start==cno or start=='0': 
            flag = True
        if cno=='' or len(cno)==0 or not flag: continue
        else:
            for j in cols:
                try:
                    data = worksheet.cell(i,j).value
                except: data=''
                if isinstance(data,float): data = int(data)
                rowval.append(str(data).rstrip().strip())
            table.append(rowval)
            # outStr+=';'.join(rowval)+'\n'
        if end==cno:
            flag = False
            break
    # writeFile(outStr)
    return(table)



datadict = []
if(path.exists(resultData) and readFile()==''):
    os.remove(resultData)
    
tag = False
if not (path.exists(resultData)):
    mypath = 'DataFolder'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and not(f[0]=='~')]
    for file in onlyfiles:
        print('File Name: ', file)
        start = input('Enter start : ')
        end = input('Enter end : ')
        datadict.append(getXlData('DataFolder\\'+file,start,end))
    datadict = [i for j in datadict for i in j]
else:
    for file in listdir('DataRemains'):
        outStr = readFile()
        datadict=[[dt for dt in txt.split(';')] for txt in outStr.split('\n')]
        datadict.pop()
        tag = True
        
print(datadict)
icmr = icmrProcess(datadict,tag)
icmr.webCreation()
icmr.enterAllData()


# end  C73637
