from MeroShareAPI import MeroShare 
from env import password

def searchBank(code):
    for i in MeroShare.getBankInfo():
        if i['code'] == str(code):
            return i['id']

def checkForIPOResult(boid):
    for i in MeroShare.getCompany()['body']:
        result = MeroShare.checkIPOResult(i['id'], boid)
        if(result['success']):
            print(result['message'], " for ", i['name'])

bankId = searchBank(password['bankCode'])

meroShare = MeroShare(password['id'], password['pass'], bankId)

boid = meroShare.getOwnDetails()['demat']

checkForIPOResult(boid)


shareId = meroShare.getOpenedIPO()['object'][0]['companyShareId']

shareDetails = meroShare.getIPODetail(shareId)

applied = meroShare.applyIPO(shareId, 1234, 1234, 12)

