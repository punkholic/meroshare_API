from MeroShareAPI import MeroShare 
from env import password, details

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

applyForIPO = meroShare.getOpenedIPO()['object']

for i in applyForIPO:
    if(i['shareGroupName'] == 'Ordinary Shares'):
        shareId = i['companyShareId']
        applied = meroShare.applyIPO(shareId, details['pinCode'], details['crn'], details['kitta'])
        
        if('errorCode' not in applied.keys()):
            print(f"Done applying {i['companyName']}")
        else:
            print('Error while applying')

    else:
        print('Nothing to apply')





