from MeroShareAPI import MeroShare
from env import *

def searchBank(code):
    for i in MeroShare.getBankInfo():
        if i['code'] == str(code):
            return i['id']


def apply(id, bankCode, pinCode, password, kitta):
    bankId = searchBank(bankCode)
    meroShare = MeroShare(id, password, bankId)
    boid = meroShare.getOwnDetails()['demat']
    applyForIPO = meroShare.getOpenedIPO()['object']

    for i in applyForIPO:
        if(i['shareGroupName'] == 'Ordinary Shares'):
            print(i['companyName'])
            shareId = i['companyShareId']
            applied = meroShare.applyIPO(shareId, pinCode, kitta)
            print(applied)

            if('errorCode' not in applied.keys()):
                print(applied['message'])
            else:
                print('Error while applying')

for i in all:
    apply(i['id'], i['bankCode'], i['pinCode'], i['password'], kitta)
    print()


