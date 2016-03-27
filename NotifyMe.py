
#Created By Syed Ahmed - Dang team - Wear hacks TO 2016
#
import time
from yahoo_finance import Share
from mailjet_rest import Client
from pprint import pprint
import os


API_KEY = '03a06c90a7e8aedb43b63ec8150641ab'
API_SECRET = '439c5c01dc8c6e421df099e2ef6b1c0a'
invalid = 'invalid Stock Ticker; YHOO is automatically chosen'
valid = False
strCompany = ''
count = 0
mailjet = Client(auth=(API_KEY, API_SECRET))


strCompany = raw_input("Enter the company Stock Ticker; example: YHOO for Yahoo:      ")
if strCompany == '':
    print invalid
    strCompany = 'YHOO'
elif len(strCompany) > 5:
    print invalid
    strCompany = 'YHOO'
else:
    valid = True

company = Share(strCompany)
price = str(company.get_price())
#historical = str(company.get_historical('2016-03-22', '2016-03-27'))
historical = company.get_historical('2016-03-22', '2016-03-27')
historical_string = ""

for item in (historical):
    for key in item.keys():
        if (str(key) == "Volume"): historical_string = historical_string + str(key) + str(item[key])+ "<br/>"
        else: historical_string = historical_string + str(key) + ": $" + str(item[key])+ "<br/>"
        historical_string  = historical_string+"<br/><br/>"

print(historical_string)

print company.get_price()

#Send email
while count < 49:
    company.refresh
    price = str(company.get_price())

    data = {
        'FromEmail': 'stoks@niotic.com',
        'FromName': 'Stock Partner',
        'Subject': 'There has been a change in prices!',
        'Text-part': 'We do not use text!',
        'Html-part': '<h3>Here is the stock update for: ' + strCompany +' </h3><br/><H1> Current Price: $' + price + ' </H1> <p> here is some other relevant information </p> <br/> <p> ' + historical_string + '</p> ',
        'Recipients': [{'Email':'dangnitish31@gmail.com'}] # change email
        }
    result = mailjet.send.create(data=data)
    print result.status_code
    print result.json()
    count = count + 1
    time.sleep(60*30)
