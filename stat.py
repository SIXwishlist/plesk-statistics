import os
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
    def __init__(self, domainName):
        self.domainName=domainName
        self.loginName=getLoginName()
        self.ftpLoginName=self.getFtpLoginName()
        self.servicePlan=self.getServicePlan()
        self.contactName=self.getContactName()
        self.email=self.getEmail()
        self.domainList=createDomainList()
    def createDomainList(self):
        for key,value in Subscription.domainFtpLoginNameDict.items():
            if self.ftpLoginName == value:
                self.domainList.append(key)
    def countHit(self):
        for key,value in Subscription.domainHitDict.items():
            if key in self.domainList:
                self.hitNum+=value
    def isOverHit(self):
        if self.servicePlan in Subscription.servicePlanHitDict.keys():
            return self.hitNum > Subscription.servicePlanHitDict[self.servicePlan]
        else:
            return false
    def logInfo(self):
        print "domainName:", domainName
        print "contactName:", contactName
        print "loginName:", loginName
        print "ftpLoginName:", ftpLoginName
        print "servicePlan:", servicePlan
        print "email:", email
        print "hitNum:", hitNum
    def sendEmail(self):
        #
    def getLoginName(self):
        return os.popen("plesk  bin subscription --info "+self.domainName+" | grep 'Owner' | awk -F '[()]' '{print $2}'").readline()[0:-1]
    def getFtpLoginName(self):
        return os.popen("plesk bin domain --info "+x+" | grep 'FTP Login' | awk '{print $3}'").readline()[0:-1]
    def getServicePlan(self):
        return os.popen("plesk bin subscription --info "+subscription+" | tac | sed -n '5p' | awk '{print $9}'").readline()[0:-1]
    def getContactName(self):
        return os.popen("plesk bin user --info "+self.loginName+" | grep 'Contact name' | awk -F ': ' '{print $2}'").readline()[0:-1]
    def getEmail(self):
        return os.popen("plesk bin user --info "+self.domainName+" | grep 'Email' | awk -F ': ' '{print $2}'").readline()[0:-1]

def main():
    domainList=map(lambda x:x[0:-1], os.popen('plesk bin domain --list').readlines())
    domainFtpLoginNameList=map(lambda x:os.popen("plesk bin domain --info "+x+" | grep 'FTP Login' | awk '{print $3}'").readline()[0:-1], domainList)
    Subscription.domainFtpLoginNameDict=dict((x,y) for x,y in zip(domainList, domainFtpLoginNameList))
    domainHitList=map(lambda domain:os.popen("if [ -f /var/www/vhosts/system/"+domain+"/statistics/webstat/webalizer.current ];then  cat /var/www/vhosts/system/"+domain+"/statistics/webstat/webalizer.current | sed -n 3p |awk '{print $1}'; else echo '0'; fi").readline()[0:-1], domainList)
    Subscription.domainHitDict=dict((x,y) for x,y in zip(domainList,domainHitList))
    Subscription.servicePlanHitDict={'Standard':10**4, 'Professional':10**5, 'Business':10**6}
    subscriptionList=map(lambda x:x[0:-1], os.popen('plesk bin subscription --list').readlines())
    # subscriptionServicePlanList=map(lambda subscription:os.popen("plesk bin subscription --info "+subscription+" | tac | sed -n '5p' | awk '{print $9}'").readline()[0:-1], subscriptionList)
    # subscriptionServicePlanDict=dict((x,y) for x,y in zip(domainList,subscriptionServicePlanList))
    adminEmail=os.popen("plesk bin user --info admin | grep Email | awk '{print $2}'").readline()[0:-1]

if __name__ == '__main__':
    main()


