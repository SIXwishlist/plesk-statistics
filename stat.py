import os
domainList=map(lambda x:x[0:-1], os.popen('plesk bin domain --list').readlines())
subscriptionList=map(lambda x:x[0:-1], os.popen('plesk bin subscription --list').readlines())
class Subscription:
