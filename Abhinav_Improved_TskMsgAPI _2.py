# -*- coding: utf-8 -*-

"""
This script is about using the Plivo API and
plivo automation framework to send a sms from
one number to another and check whether the
sms is charged correctly or not
"""

import plivo
from plivo.resources import (accounts, numbers, messages, pricings)

auth_id = "MAODUZYTQ0Y2FMYJBLOW"
auth_token = "ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0"


""" Create a RestClient Object for the Account """
p = plivo.RestClient(auth_id, auth_token)


""" Get the souce and destination phone numbers using list method in numbers module """
def get_numbers():
    numList= p.numbers.list()
    src = numList[0]["number"]
    dest = numList[1]["number"]
    print " The source phone number is " + src + "\n Destination Phone number is " + dest
    return src,dest

""" Get the cash credits from the account before sending a message using get method from accounts module """
def get_account_details():
    accDetails = p.account.get()
    startCredit = float(accDetails["cash_credits"])
    return startCredit

""" Send sms from souce to destination using create method of messages module
    Then use the sms uuid to get the amount charged
"""
def send_sms():
    txt = "hello sir how are you"
    src,dest = get_numbers()
    msg = p.messages.create(dest,txt,src)
    uuid = msg["message_uuid"]
    uuid = '\''.join(uuid)
    listMsg = p.messages.get(uuid)
    amtCharged = float(listMsg["total_amount"])                           
    print "\n Amount charged for sending the sms is " + str(amtCharged)
    return amtCharged

""" Get pricing details using get method of pricings module API """
def get_pricing():
    countryIso = "US"
    price = p.pricing.get(countryIso)
    outRate = float(price["message"]["outbound"]["rate"])           
    print "\n Outbound rate for sms is " + str(outRate)
    return outRate

startCredit = get_account_details()
print "\n\nCash credit at the start is " + str(startCredit)
amtCharged = send_sms()
outRate = get_pricing()
endCredit = get_account_details()
print "\n\nCash credit at the end is " + str(endCredit)

""" Compare the amount charged and outbound rate """
if amtCharged == outRate:
    print "\n...................Amount charged is same as Outbound rate.............."
else :
    print "\n Amount charged is not the same as outbound rate, please check "
    
""" Compare the cash credits before and after sending the sms """
if endCredit == startCredit - amtCharged:
    print "\n...................TASK COMPLETED..............\n"
else :
    print "\n.............TASK FAILED............\n"
