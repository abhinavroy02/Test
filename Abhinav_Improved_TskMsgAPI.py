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
numList= p.numbers.list()
src = numList[0]["number"]
dest = numList[1]["number"]
print " The source phone number is " + src + "\n Destination Phone number is " + dest


""" Get the cash credits from the account before sending a message using get method from accounts module """
accDetails = p.account.get()
startCredit = float(accDetails["cash_credits"])
print "\n Cash credits beofre sending the sms is " + str(startCredit)


""" Send sms from souce to destination using create method of messages module """
txt = "hello sir how are you"
msg = p.messages.create(dest,txt,src)
uuid = msg["message_uuid"]
uuid = '\''.join(uuid)


""" Get the amount from the account after sending a message using Account API """
listMsg = p.messages.get(uuid)
amtCharged = float(listMsg["total_amount"])                           
print "\n Amount charged for sending the sms is " + str(amtCharged)


""" Get pricing details using get method of pricings module API """
countryIso = "US"
price = p.pricing.get(countryIso)
outRate = float(price["message"]["outbound"]["rate"])           
print "\n Outbound rate for sms is " + str(outRate)


""" Compare the amount charged and outbound rate """

if amtCharged == outRate:
    print "\n...................Amount charged is same as Outbound rate.............."
else :
    print "\n Amount charged is not the same as outbound rate, please check "
    

""" Get the cash credits from the account after sending a message using Account API """
accDetails = p.account.get()
endCredit = float(accDetails["cash_credits"])
print "\n Cash credits after sending the sms is " + str(endCredit)


""" Compare the cash credits before and after sending the sms """

if endCredit == startCredit - amtCharged:
    print "\n...................TASK COMPLETED..............\n"
else :
    print "\n.............TASK FAILED............\n"
