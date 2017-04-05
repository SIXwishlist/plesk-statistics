import os
class Subscription:
  domainList=[]
  loginName=''
  ftpLoginName=''
  servicePlan=''
  contactName=''
  email=''
  hitNum=0
  def countHit(self, domainHitList):
    #
  def isOverHit(self):
    #
  def sendEmail(self):
    #
def main():
  domainList=map(lambda x:x[0:-1], os.popen('plesk bin domain --list').readlines())
  domainHitList={}
  subscriptionList=map(lambda x:x[0:-1], os.popen('plesk bin subscription --list').readlines())
  servicePlanHitDic={'Standard':10**4, 'Professional':10**5, 'Business':10**6}
  adminEmail=os.popen("plesk bin user --info admin | grep Email | awk '{print $2}'").readline()[0:-1]
