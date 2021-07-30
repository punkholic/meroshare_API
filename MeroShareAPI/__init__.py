import requests, json
from datetime import date

class MeroShare:

    def __init__(self, username, password, bankID):
        self.username = username
        self.password = password
        self.token = self.getAuthToken(bankID)
        self.toCheck = ['branchName', 'accountNumber', 'bankCode', 'accountType', 'accountBranch', 'customerId', 'boid', 'branchCode', 'branchId', 'applyBoid', 'bankId', 'clientCode', 'branchName', 'bankName']
        for i in self.toCheck:
            setattr(self, i, None)
        self.checkRequired()

    def checkRequired(self):
        for i in self.toCheck:
            if not getattr(self, i):
                ownDetail = self.getOwnDetails()
                self.boid = ownDetail['demat']

                myDetails = self.getMyDetails()
                self.branchName = myDetails['bankName']
                self.accountNumber = myDetails['accountNumber']
                self.bankCode = myDetails['bankCode']
                self.accountType = myDetails['accountType']


                bankDetails = self.getBankRequestDetails()
                self.accountBranch = bankDetails['accountBranch']['id']
                self.customerId = bankDetails['id']
                self.branchCode = bankDetails['branch']['code']
                self.branchId = bankDetails['branch']['id']
                self.applyBoid = bankDetails['boid']
                self.bankId = bankDetails['bank']['id']
                self.clientCode = bankDetails['capital']['code']
                self.branchName = bankDetails['branch']['name']
                self.bankName = bankDetails['bank']['name']
                break
    

    @staticmethod
    def getBankInfo():
        return json.loads(requests.get("https://webbackend.cdsc.com.np/api/meroShare/capital/").text)


    @staticmethod
    def getCompany():
        return json.loads(requests.get("https://iporesult.cdsc.com.np/result/companyShares/fileUploaded").text)

    @staticmethod
    def checkIPOResult(companyId, boid):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'null',
            'Content-Type': 'application/json',
        }

        data = {"companyShareId": companyId, "boid": boid}

        response = requests.post('https://iporesult.cdsc.com.np/result/result/check', headers=headers, data=json.dumps(data))
        return json.loads(response.text)


    def getAuthToken(self, bankId):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'null',
            'Content-Type': 'application/json',
        }

        data = {"clientId":bankId,"username":self.username,"password":self.password}


        response = requests.post('https://webbackend.cdsc.com.np/api/meroShare/auth/', headers=headers, data=json.dumps(data))
        if 'Authorization' not in response.headers:
            print("Invalid username or password!!")
            exit(1)

        self.token = response.headers['Authorization']
        return self.token

    def sendAuthorizedRequest(self, url, type = 'get', data = None, parse = True):
        if not self.token:
            print("Please authorized first with getAuthToken method!!")

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }
        if parse:
            data = json.dumps(data)
        
        if type == 'get':
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, data=data)

        return json.loads(response.text)
    
    def getOwnDetails(self):
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/ownDetail/")

    def getMyDetails(self):
        return self.sendAuthorizedRequest(f"https://webbackend.cdsc.com.np/api/meroShareView/myDetail/{self.boid}")

    def getAccountType(self):
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/bankRequest/accountType/")

    def getBankRequestBanks(self):
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/bankRequest/bank/")

    def getBankRequestDetails(self):
        return self.sendAuthorizedRequest(f"https://webbackend.cdsc.com.np/api/bankRequest/{self.bankCode}")

    def getBranchCode(self):
        return self.sendAuthorizedRequest(f"https://webbackend.cdsc.com.np/api/bankRequest/branch/{self.bankCode}")

    def getEDISStatusType(self):
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/EDIS/statusName/")
    
    def getBankDetail(self):
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/bank/")
    

        # 

    def getMyShares(self):
        data = {
            "sortBy":"CCY_SHORT_NAME",
            "demat":[self.boid],
            "clientCode": self.clientCode,
            "page":1,
            "size":200,
            "sortAsc": True
            }
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShareView/myShare/", "post", data)
    
    def getMyTransaction(self):
        data = {
            "boid": self.boid,
            "clientCode": self.clientCode,
            "script": None,
            "fromDate": None,
            "toDate": None,
            "requestTypeScript": False,
            "page": 1,
            "size": 200
        }

        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShareView/myTransaction/", "post", data)
    
    def getMyPortfolio(self):
        data = {
            "sortBy" : "script",
            "demat" : [self.boid],
            "clientCode" : self.clientCode,
            "page" : 1,
            "size" : 200,
            "sortAsc" : True
            }

        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShareView/myPortfolio/", "post", data)
   
    def getMyPledgor(self):
        data = {
            "page": 1,
            "size": 200,
            "sortAsc": True,
            "boid": self.boid
        }

        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShareView/myPledgor/", "post", data)
    

    def sendBankRequest(self):
        #not working    
        data = {
            "accountNumber": self.boid,
            "bankCode": self.bankCode,
            "bankName": self.bankName,
            "branchId": self.branchCode,
            "branchName": self.branchName,
            "branchCode" : self.branchCode,
            "accountType" : self.accountType
        }
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/bankRequest/", "post", data)

    def searchMyPurchase(self, text):
        data = {
            "demat": self.boid,
            "scrip": text
            }

        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/myPurchase/search/", "post", data)

    def searchMyPurchase(self, text):
        data = {
            "demat": self.boid,
            "scrip": text
            }

        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/myPurchase/search/", "post", data)

    def getOpenedIPO(self):
        data = {
            "filterFieldParams":[
                    {"key":"companyIssue.companyISIN.script","alias":"Scrip"},
                    {"key":"companyIssue.companyISIN.company.name","alias":"Company Name"},
                    {"key":"companyIssue.assignedToClient.name","value":"","alias":"Issue Manager"}
                ],
            "page":1,
            "size":10,
            "searchRoleViewConstants":"VIEW_APPLICABLE_SHARE",
            "filterDateParams":[
                {"key":"minIssueOpenDate","condition":"","alias":"","value":""},
                {"key":"maxIssueCloseDate","condition":"","alias":"","value":""}
            ]
        }
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/companyShare/applicableIssue/", "post", data)

    def getIPODetail(self, id):
        return self.sendAuthorizedRequest(f"https://webbackend.cdsc.com.np/api/meroShare/active/{id}")

    def getCurrentIssue(self):
        data = {
            "filterFieldParams": [
                    {
                    "key": "companyIssue.companyISIN.script",
                    "alias": "Scrip"
                    },
                    {
                    "key": "companyIssue.companyISIN.company.name",
                    "alias": "Company Name"
                    },
                    {
                    "key": "companyIssue.assignedToClient.name",
                    "value": "",
                    "alias": "Issue Manager"
                    }
                ],
                "page": 1,
                "size": 10,
                "searchRoleViewConstants": "VIEW_OPEN_SHARE",
                "filterDateParams": [
                    {
                    "key": "minIssueOpenDate",
                    "condition": "",
                    "alias": "",
                    "value": ""
                    },
                    {
                    "key": "maxIssueCloseDate",
                    "condition": "",
                    "alias": "",
                    "value": ""
                    }
                ]
            }


        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/companyShare/currentIssue", "post", data)

    def searchApplicationReport(self, script = "", companyName = "", fromDate = "", toDate = ""):
        if fromDate != "" and toDate != "":
            toDate = date.today().strftime("%d-%m-%Y")
        data = '{"filterFieldParams":[{"key":"companyShare.companyIssue.companyISIN.script","value":"' + script + '","alias":"Scrip"},{"key":"companyShare.companyIssue.companyISIN.company.name", "value":"'+companyName+'","alias":"Company Name"}],"page":1,"size":10,"searchRoleViewConstants":"VIEW_APPLICANT_FORM_COMPLETE","filterDateParams":[{"key":"appliedDate","condition":"","alias":"","value":null},{"key":"appliedDate","condition":"BETWEEN \''+ fromDate +'\' AND \''+ toDate +'\'","alias":"","value":""}]}'
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/applicantForm/active/search/", "post", data, False)


    def searchOldReport(self, script = "", companyName = "", fromDate = "", toDate = ""):
        if fromDate != "" and toDate != "":
            toDate = date.today().strftime("%d-%m-%Y")
        data = '{"filterFieldParams":[{"key":"companyShare.companyIssue.companyISIN.script", "value":"' + script + '", "alias":"Scrip"},{"key":"companyShare.companyIssue.companyISIN.company.name", "value":"'+companyName+'" ,"alias":"Company Name"}],"page":1,"size":200,"searchRoleViewConstants":"VIEW","filterDateParams":[{"key":"appliedDate","condition":"","alias":"","value":""},{"key":"appliedDate","condition":"BETWEEN \''+ fromDate +'\' AND \''+ toDate +'\'","alias":"","value":""}]}'
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/migrated/applicantForm/search/", "post", data, False)

    def canApply(self, ipoId):
        return self.sendAuthorizedRequest(f"https://webbackend.cdsc.com.np/api/meroShare/applicantForm/customerType/{ipoId}/{self.boid}")
        
    def applyIPO(self, ipoId, pin, crnNumber, kitta):

        if 'Customer can apply.' != self.canApply(ipoId)['message']:
            print("Cannot apply this share")
            return

        ipoDetails = self.getIPODetail(ipoId)
        maxKitta = ipoDetails['maxUnit']
        if(maxKitta < kitta):
            print(f"Max kitta is {maxKitta}")
            return
        
        data = {
            "demat": self.boid,
            "boid": self.applyBoid,
            "accountNumber": self.accountNumber,
            "customerId": self.customerId,
            "accountBranchId": self.branchId,
            "appliedKitta": kitta,
            "crnNumber": crnNumber,
            "transactionPIN": pin,
            "companyShareId": ipoId,
            "bankId": self.bankId
        }
        return self.sendAuthorizedRequest("https://webbackend.cdsc.com.np/api/meroShare/applicantForm/share/apply/", "post", data)
