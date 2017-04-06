#coding=utf-8
import os
import string
import datetime
class Subscription:
    domainFtpLoginNameDict={}
    servicePlanHitDict={}
    domainHitDict={}
    domainName=''
    loginName=''
    ftpLoginName=''
    servicePlan=''
    contactName=''
    email=''
    hitNum=0
    month=''
    def __init__(self, domainName):
        self.domainName=domainName
        self.loginName=self.getLoginName()
        self.ftpLoginName=self.getFtpLoginName()
        self.servicePlan=self.getServicePlan()
        self.contactName=self.getContactName()
        self.email=self.getEmail()
        self.createDomainList()
        tmp=datetime.datetime.now()
        month=tmp.year+'年'+tmp.month+'月'
    def createDomainList(self):
        tmpList=[]
        for key,value in Subscription.domainFtpLoginNameDict.items():
            if self.ftpLoginName == value:
                tmpList.append(key)
        self.domainList=tmpList
    def countHit(self):
        print self.domainList
        # print Subscription.domainFtpLoginNameDict
        for key,value in Subscription.domainHitDict.items():
            if key in self.domainList:
                self.hitNum+=value
    def isOverHit(self):
        if self.servicePlan in Subscription.servicePlanHitDict.keys():
            return self.hitNum > Subscription.servicePlanHitDict[self.servicePlan]
        else:
            return False
    def logInfo(self):
        print "domainName:",   self.domainName
        print "contactName:",  self.contactName
        print "loginName:",    self.loginName
        print "ftpLoginName:", self.ftpLoginName
        print "servicePlan:",  self.servicePlan
        print "email:",        self.email
        print "hitNum:",       self.hitNum
    def logout(self):
        return "domainName:"+self.domainName \
        +";contactName:"+self.contactName \
        +";loginName:"+self.loginName \
        +";ftpLoginName:"+self.ftpLoginName \
        +";servicePlan:"+self.servicePlan \
        +";email:"+self.email \
        +";hitNum:"+self.hitNum \
        +";hitNumLimit"+Subscription.servicePlanHitDict[self.servicePlan] \
        +";"
    def getLoginName(self):
        return os.popen("plesk  bin subscription --info "+self.domainName+" | grep 'Owner' | awk -F '[()]' '{print $2}'").readline()[0:-1]
    def getFtpLoginName(self):
        return os.popen("plesk bin subscription --info "+self.domainName+" | grep 'FTP Login' | awk '{print $3}'").readline()[0:-1]
    def getServicePlan(self):
        return os.popen("plesk bin subscription --info "+self.domainName+" | tac | sed -n '5p' | awk '{print $9}'").readline()[1:-2]
    def getContactName(self):
        return os.popen("plesk bin user --info "+self.loginName+" | grep 'Contact name' | awk -F ': ' '{print $2}'").readline()[0:-1]
    def getEmail(self):
        return os.popen("plesk bin user --info "+self.loginName+" | grep 'Email' | awk -F ': ' '{print $2}'").readline()[0:-2]
    def sendMail(self):
        try:
            os.popen('''curl -d 'apiUser=hkmars&apiKey=mOd5WW9D5cSvNbPK&from=hkmars@bisend.cn&fromName=必盛互联&subject=点击数超过限制&templateInvokeName=hit_num_over_limit' --data-urlencode 'xsmtpapi={"to": ["'''+self.email+'''"],"sub":{"%name%": ["'''+self.contactName+'''"],"%subscription%":["'''+self.domainName+'''"],"%year_month%":["'''+self.month+'''"],"%hit_num%":["'''+str(self.hitNum)+'''"],"%hit_num_limit%":["'''+str(Subscription.servicePlanHitDict[self.servicePlan])+'''"]}}' http://api.sendcloud.net/apiv2/mail/sendtemplate''')
        except Exception as e:
            print "sendMail error:",e

def main():
    domainList=map(lambda x:x[0:-1], os.popen('plesk bin domain --list').readlines())
    domainFtpLoginNameList=map(lambda x:os.popen("plesk bin domain --info "+x+" | grep 'FTP Login' | awk '{print $3}'").readline()[0:-1], domainList)
    Subscription.domainFtpLoginNameDict=dict((x,y) for x,y in zip(domainList, domainFtpLoginNameList))
    domainHitList=map(lambda domain:string.atoi(os.popen("if [ -f /var/www/vhosts/system/"+domain+"/statistics/webstat/webalizer.current ];then  cat /var/www/vhosts/system/"+domain+"/statistics/webstat/webalizer.current | sed -n 3p |awk '{print $1}'; else echo '0'; fi").readline()[0:-1]), domainList)
    domainSslHitList=map(lambda domain:string.atoi(os.popen("if [ -f /var/www/vhosts/system/"+domain+"/statistics/webstat-ssl/webalizer.current ];then  cat /var/www/vhosts/system/"+domain+"/statistics/webstat-ssl/webalizer.current | sed -n 3p |awk '{print $1}'; else echo '0'; fi").readline()[0:-1]), domainList)
    domainHitList=[domainHitList[i]+domainSslHitList[i] for i in range(len(domainHitList))]
    Subscription.domainHitDict=dict((x,y) for x,y in zip(domainList,domainHitList))
    Subscription.servicePlanHitDict={'Standard':10**4, 'Professional':2*10**4, 'Business':5*10**4}
    subscriptionList=map(lambda x:x[0:-1], os.popen('plesk bin subscription --list').readlines())
    # subscriptionServicePlanList=map(lambda subscription:os.popen("plesk bin subscription --info "+subscription+" | tac | sed -n '5p' | awk '{print $9}'").readline()[0:-1], subscriptionList)
    # subscriptionServicePlanDict=dict((x,y) for x,y in zip(domainList,subscriptionServicePlanList))
    adminEmail=os.popen("plesk bin user --info admin | grep Email | awk '{print $2}'").readline()[0:-1]
    content=''
    for ss in subscriptionList:
        obj=Subscription(ss)
        obj.countHit()
        if obj.isOverHit():
            content+=obj.logout()
            # obj.sendMail()
    try:
        os.popen('''curl -d 'apiUser=hkmars&apiKey=mOd5WW9D5cSvNbPK&from=hkmars@bisend.cn&fromName=必盛互联&subject=点击数超过限制的报告&templateInvokeName=admin_hit_num_over_limit' --data-urlencode 'xsmtpapi={"to": ["'''+adminEmail+'''"],"sub":{"%content%": ["'''+content+'''"]}}' http://api.sendcloud.net/apiv2/mail/sendtemplate''')
    except Exception as e:
        print "sendMail error:",e
if __name__ == '__main__':
    main()


