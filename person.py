import random
import time
import re
from datetime import datetime  
from datetime import timedelta
from random import randint
from selenium.webdriver.common.keys import Keys

def random_with_n_digits(n=9):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def wait(s=3):
    time.sleep(s)

class register:
    def __init__(self,datalist,br,tag):
        self.datalist = datalist
        self.prefix = ''
        self.sno,self.id,self.date,self.name,self.age,self.gender,self.address,self.mobile,self.result,self.tested,self.srf,self.kit,self.ng,self.rdrp = map(str,datalist)
        print('Inside Class Register')
        self.br = br
        if not tag:
            self.dataValidation()
            self.validateSample()
            self.datalist = [self.sno,self.id,self.date,self.name,self.age,self.gender,self.address,self.mobile,self.result,self.tested,self.srf,self.kit,self.ng,self.rdrp]
        self.received = self.dateGenerator(self.date,rhr=True)

    def dataValidation(self):
        sampleName = ['Ravi','Ram Kumar','Vijay','Surya','Mathu','Harshit']
        rand = random.randrange(0,6)
        # name
        name = str(self.name).split('(')
        name = name[0]
        if len(name)==0:
            name = sampleName[rand]
        elif len(name)<4:
            name = name+'    '
        if name.find('.')>=0:
            name = ' '.join(name.split('.'))
        self.name = name
        # age
        rand = random.randrange(35,65)
        try:
            self.age = int(self.age)
        except:
            self.age = rand
        # gender
        gender = self.gender
        if len(gender)==0 or gender[0]=='M' or gender[0]=='m': self.gender = 'Male'
        elif gender[0]=='F' or gender[0]=='f': self.gender = 'Female'
        else: self.gender = 'Transgender'
        # mobile
        mobile = self.mobile
        if len(mobile)<10:
            self.mobile = '9'+str(random_with_n_digits())
        #address
        add = self.address.rstrip()
        if len(add)==0:
            add = 'NAMAKKAL'
        add = add.replace(';','')
        add = add.replace('\n',' ')
        add = add.replace('\t',' ')
        self.address = add.upper()
        #srf
        srf = str(self.srf)
        if srf!='':
            try:
                srf = ''.join(srf.split())
                n = int(srf)
                prefix = '33580000'
                l = len(srf)
                if l<13 and l>=10:srf=''
                elif l<13:
                    if len(prefix+srf)>13:
                        diff = 13-len(prefix+srf)
                        prefix = prefix[:diff]
                    srf = prefix+srf
            except:
                srf = ''
        self.srf = srf
        if self.kit=='':
            self.kit = "LABGUN"
        self.kit = str(self.kit).lower()

    def validateSample(self):
        # date
        date = self.date
        if date=='':
            if self.tested=='':
                date = self.dateGenerator(datetime.today().strftime('%d-%m-%y %H:%M:%S'),day=-2)
            else : 
                data = self.dateGenerator(self.tested,day=-1) 
        if len(str(date))!=19:
            date = '-'.join(date.split('.'))
            date += ' '+str(datetime.today().strftime('%H:%M:%S'))
            date = self.dateGenerator(date,rhr=True)
        self.date = date
        # tested
        testdate= self.tested
        if testdate=='':
            testdate = self.dateGenerator(self.date,day=1,rhr=True)
        if len(str(testdate))!=19:
            testdate = '-'.join(testdate.split('.'))
            testdate += ' '+str(datetime.today().strftime('%H:%M:%S'))
            testdate = self.dateGenerator(testdate,rhr=True)
        self.tested = testdate
        # result
        result = (self.result).lower()
        if result=='':
            result = 'negative'
        self.result = result   
        
        ng = self.ng
        if ng!='':
            ng = ng.split()
            ng = ng[-1]
        self.ng = ng

        rdrp = self.rdrp
        if rdrp!='':
            rdrp = rdrp.split()
            rdrp = rdrp[-1]
        self.rdrp = rdrp
            
    def dateGenerator(self,date,day=0,hour=0,rhr=False):
        # print('Generate Date ',date)
        randhr = 1
        if rhr:
            randhr = random.randint(1,3)
        randsec = random.randrange(1,60)
        randmin = random.randrange(1,60)
        date = date.split()
        date,time = date[0],date[1]
        date = list(map(int,date.split('-')))
        time = list(map(int,time.split(':')))
        d = datetime(date[-1],date[1],date[0],time[0],time[1],second=time[2])+timedelta(days=day,hours=hour+randhr,minutes=randmin,seconds=randsec)
        dt = list(map(str,str(d).split()))
        dt[0] = str(d.day)+'-'+str(d.month)+'-'+str(d.year)
        return (' '.join(dt))
    

    def enterValues(self):
        print('EnterValue of ',self.sno)
        wait()
        try:
            if self.srf!='':
                srf = self.browserActivityBySrf()
                if srf=="err":
                    return False
                elif srf=="exist":
                    return True
            else:
                self.br.execute_script('window.location.href = "https://cvstatus.icmr.gov.in/add_record.php"')
            return (self.browserActivityByAdd())
        except Exception as e: 
            print(e)
            self.br.refresh()
            return False


    def browserActivityByAdd(self):
        print('Enter Into browserActivityByAdd:')
        br = self.br
        try:
            wait()
            # /html/body/div[3]/div[3]/div/button  /html/body/div[3]/div[1]/button/span[1]
            # br.find_element_by_xpath('/html/body/div[3]/div[1]/button/span[1]').click()
            br.execute_script("document.getElementsByClassName('ui-button ui-corner-all ui-widget')[0].click()")
            br.find_element_by_xpath('//*[@id="state"]/option[33]').click()   
            br.find_element_by_xpath('//*[@id="patient_id"]').send_keys(self.prefix+self.id)
            br.find_element_by_xpath('//*[@id="patient_id"]').send_keys(Keys.TAB)
            
            if self.waitForAlert(br): return True
            br.execute_script("document.getElementById('patient_name').value=''")
            br.find_element_by_xpath('//*[@id="patient_name"]').send_keys(self.name.upper())
            br.execute_script('document.getElementById("age").value=arguments[0]',self.age)
            br.find_element_by_xpath('//*[@id="gender"]/option[text()="'+self.gender+'"]').click()
            br.execute_script('document.getElementById("contact_number").value=arguments[0]',self.mobile)
            # br.find_element_by_xpath('//*[@id="contact_number"]').send_keys(self.mobile)
            br.execute_script("document.getElementById('contact_number_belongs_to').value = 'patient'")
            br.find_element_by_xpath('//*[@id="nationality"]/option[100]').click()
            br.find_element_by_xpath('//*[@id="aarogya_setu_app_downloaded"]/option[3]').click()
            br.find_element_by_xpath('//*[@id="quarantined"]/option[3]').click()
            self.address = ',\n'.join(str(self.address).split(','))
            br.execute_script('document.getElementById("address").value=arguments[0]',self.address)
            # br.find_element_by_xpath('//*[@id="address"]').send_keys(self.address)
            br.find_element_by_xpath('//*[@id="ncat17"]').click()
            br.execute_script("document.getElementById('district').value = 580")
        except Exception as e:
            print(e)
        return self.sample_execute(br)


    def browserActivityBySrf(self):
        print('Enter Into browserActivityBySrf:')
        try:
            br = self.br
            br.execute_script('window.location.href = "https://cvstatus.icmr.gov.in/fetch_srf_record.php"')
            # br.find_element_by_xpath('/html/body/div[1]/aside[1]/section/ul/li[4]/a').click()            
            wait()
            br.find_element_by_xpath('//*[@id="srf_id"]').send_keys(self.srf)
            br.find_element_by_xpath('//*[@id="btn"]').click()

            if self.waitForAlert(br):
                return "exist"
            return "Not exist"
        except:
            return "err"
            

    def sample_execute(self,br):
        try:
            res = self.sample()
            if res == "Success":
                br.find_element_by_xpath('//*[@id="btn"]').click()
                if not self.waitForAlert(br):
                    return True
            return False
        except:
            return False


    def sample(self):
        try:
            br = self.br
            res = (self.result.lower()).split()
            # elem = br.find_element_by_xpath('//*[@id="sample_cdate"]')
            # br.execute_script("arguments[0].setAttribute('value',arguments[1])",elem, self.date)
            try:
                br.execute_script("document.getElementById('sample_cdate').value=arguments[0]",self.date)
            except:
                print('no sample_cdate for diff case')
            br.execute_script("document.getElementById('sample_rdate').value=arguments[0]",self.received)
            br.execute_script("document.getElementById('date_of_onset_of_symptoms').value=''")
            br.execute_script("document.getElementById('hospitalization_date').value=''")
            br.find_element_by_xpath('//*[@id="hospitalized"]/option[3]').click()
            elem = br.find_element_by_xpath('//*[@id="sample_tdate"]')
            br.execute_script("arguments[0].setAttribute('value',arguments[1])",elem, self.tested)
            br.find_element_by_xpath('//*[@id="sample_type"]/option[2]').click()
            postFix = '/'+self.sno
            br.find_element_by_xpath('//*[@id="sample_id"]').send_keys(self.id+postFix)
            if self.kit=="cbnaat":
                br.execute_script("document.getElementById('testing_kit_used').value='Cepheid'")
            else:
                br.execute_script("document.getElementById('testing_kit_used').value='Labgun'")
            # br.find_element_by_xpath('//*[@id="testing_kit_used"]/optgroup[2]/option[64]').click()
            # br.find_element_by_xpath('//*[@id="covid19_result_egene"]/option[3]').click()
            
            
            if res[0]=='positive' or res[-1]=="positive":
                br.execute_script("document.getElementById('covid19_result_egene').value='Positive'")
                br.execute_script("document.getElementById('ct_value_screening').removeAttribute('readonly')")
                br.execute_script("document.getElementById('ct_value_screening').value = arguments[0]",self.ng)
                br.execute_script("document.getElementById('rdrp_confirmatory').value='Positive'")
                br.execute_script("document.getElementById('ct_value_rdrp').removeAttribute('readonly')")
                br.execute_script("document.getElementById('ct_value_rdrp').value = arguments[0]",self.rdrp)
                br.execute_script("document.getElementById('final_result_of_sample').value='Positive'")
            elif res[0]=="rejected" or res[0]=="resample": 
                br.execute_script("document.getElementById('final_result_of_sample').value='Sample Rejected'")
                br.execute_script("document.getElementById('covid19_result_egene').value='Inconclusive_Spillage_Rejected'")
                br.execute_script("document.getElementById('orf1b_confirmatory').value='Inconclusive_Spillage_Rejected'")
                br.execute_script("document.getElementById('rdrp_confirmatory').value='Inconclusive_Spillage_Rejected'")
            elif res[0]=='negative':
                br.execute_script("document.getElementById('covid19_result_egene').value='Negative'")
                br.execute_script("document.getElementById('orf1b_confirmatory').value='Negative'")
                br.execute_script("document.getElementById('final_result_of_sample').value='Negative'")
                
            wait(1)
            return "Success"
        except Exception as e:
            br.refresh()
            print(e)
            return "Failed"
    
    def waitForAlert(self,br):
        try:
            wait(2)
            alert = br.switch_to.alert
            alert_text = alert.text
            alert.accept()
            print(alert_text,' Failed !!!!!!!!!:( ')
            br.refresh()
            return True
        except:
            return False
    
    def getDataList(self):
        return self.datalist
    def show(self):
        # data = [str(self.id),str(self.date),str(self.name),str(self.age),str(self.gender),str(self.address),str(self.mobile),str(self.result),str(self.tested)]
        return ';'.join([str(j) for j in self.datalist])+'\n'
        # self.test.show()