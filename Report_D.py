#  -------------------------
#      Open Source Project Context 22
#      Autor  : Frederic Petit 
#      with a BIG help from :  https://docs.sparkflows.io/en/latest/rest-api-python/python-token.html
# 
#      Execute a Guardium RestAPI on a report
#      Update :
#         - Written in OO
#         - Parameterized :
#              - param file for accessing the 
#              - param file for report parameters
#  -------------------------


#!/usr/bin/python
import requests
import sys
import json
import getpass

class Report_D:

  def __init__(self,param_json):

    self.report = str(sys.argv[1])

    with open(param_json) as f:
         self.param_data = json.load(f)

    self.RO_user = self.param_data["RO_user"]
    self.RO_pwd = self.param_data["RO_pwd"]
    self.client_id = self.param_data["client_id"]
    self.client_secret = self.param_data["client_secret"]
    self.Appliance = self.param_data["Appliance"]
    print ( " on : " , self.Appliance )
    self.token_url = "https://" + self.Appliance + ":8443/oauth/token"

    self.processor_count_api_url = "https://" + self.Appliance + ":8443/restAPI/online_report" # Running a Guardium Report

    #Step A - resource owner supplies credentials
    #Resource owner (enduser) credentials

    #client (application) credentials

    #step B, C - single call with resource owner credentials in the body and client credentials as the basic auth header will return #access_token

    self.data = {'grant_type': 'password','username': self.RO_user, 'password': self.RO_pwd}

    self.access_token_response = requests.post(self.token_url, data=self.data, verify=False, allow_redirects=False, auth=(self.client_id, self.client_secret))

    print(self.access_token_response.headers)
    print(self.access_token_response.text)

    self.tokens = json.loads(self.access_token_response.text)
    print( "access token: " + self.tokens['access_token'])


  def Report(self):
      # Step C - now we can use the access_token to make as many calls as we want.
      api_call_headers = {
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + p1.tokens['access_token']}

      print( api_call_headers)

      with open(p1.report) as f2:
         report_data = json.load(f2)

      dataReport = str(report_data)
      print (type(dataReport))
      print (dataReport)

      print (type(dataReport))
      print (dataReport)
      api_call_response = requests.post(p1.processor_count_api_url, headers=api_call_headers, verify=False, data=dataReport)

      print(len(api_call_response.json()))

      for i in range(0,len(api_call_response.json())) :
          print (api_call_response.json()[i])

if __name__ == '__main__':
    print("Start RestAPI Report:")


    p1 = Report_D("param_data.json")

    result = p1.Report()

