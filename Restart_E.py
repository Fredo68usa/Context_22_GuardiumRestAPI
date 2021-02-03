#!/usr/bin/python

import requests
import sys
import json
import getpass

class Report_E:

  def __init__(self,param_json):

    self.report = str(sys.argv[1])
    self.client = str(sys.argv[2])

    with open(param_json) as f:
         self.param_data = json.load(f)

    self.RO_user = self.param_data["RO_user"]
    self.RO_pwd = self.param_data["RO_pwd"]
    self.client_id = self.param_data["client_id"]
    self.client_secret = self.param_data["client_secret"]
    self.appliance = self.param_data["Appliance"]

    self.token_url = "https://" + self.appliance + ":8443/oauth/token"

    self.param_api_url = "https://" + self.appliance + ":8443/restAPI/gim_client_params" # Setting up gim param
    self.push_api_url = "https://" +self.appliance + ":8443/restAPI/gim_schedule_install" # Setting up gim param

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

      report_data['clientIP']=p1.client
      dataReport = str(report_data)
      print (type(dataReport))
      print (dataReport)

      print (type(dataReport))
      print (dataReport)
      api_call_response = requests.put(p1.param_api_url, headers=api_call_headers, verify=False, data=dataReport)
      print(api_call_response.json())

      dataPushT={"clientIP":"x.x.x.x","date":"NOW" }
      dataPushT['clientIP']=p1.client
      dataPush=str(dataPushT)
      api_call_response = requests.put(p1.push_api_url, headers=api_call_headers, verify=False, data=dataPush)
      print(api_call_response.json())



if __name__ == '__main__':
    print("Start Gim Params:")


    p1 = Report_E("param_data.json")

    result = p1.Report()
