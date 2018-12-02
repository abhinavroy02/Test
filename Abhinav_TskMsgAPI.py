import requests
from requests.auth import HTTPBasicAuth

""" The authorization credentials and the URL """

auth_id = "MAODUZYTQ0Y2FMYJBLOW"
auth_token = "ODgyYmQxYTQ2N2FkNDFiZTNhZWY4MDAwYWY4NzY0"
url = 'https://api.plivo.com/v1/Account/'

""" Get the souce and destination phone numbers using Numbers API """

get_response1 = requests.get(url + auth_id + '/Number', auth=HTTPBasicAuth(auth_id, auth_token))
jsonObj = get_response1.json()
src = jsonObj["objects"][0]["number"]                                                # Take the first number from the response list as source
dest = jsonObj["objects"][1]["number"]                                               # Take the second number from the response list as destination
print " The source phone number is " + src + "\n Destination Phone number is " + dest

""" Get the cash credits from the account before sending a message using Account API """

get_response2 = requests.get(url + auth_id + '/', auth=HTTPBasicAuth(auth_id, auth_token))
cash_credits_start = float(get_response2.json()["cash_credits"])                     # Convert the unicode response in float and store
print "\n Cash credits beofre sending the sms is " + str(cash_credits_start)

""" Send sms from souce to destination using Message API """

txt = "hello sir how are you"
post_response1 = requests.post(url + auth_id + '/Message/', auth=HTTPBasicAuth(auth_id, auth_token), json = {"src" : src, "dst" : dest, "text" : txt})
uuid = post_response1.json()["message_uuid"]                                         # Get the message uuid  
uuid = '\''.join(uuid)                                                               # Convert the unicode uuid to string


""" Get message details using Message API """

get_response3 = requests.get(url + auth_id + '/Message/' + uuid + '/' , auth=HTTPBasicAuth(auth_id, auth_token))
amt_charged = float(get_response3.json()["total_amount"])                            # Get the amount charged for sms and convert to float
print "\n Amount charged for sending the sms is " + str(amt_charged)

""" Get the pricing details for sending a sms in US using Pricing API """

params = {'country_iso' : 'US'}
get_response4 = requests.get(url + auth_id + '/Pricing/' , params , auth=HTTPBasicAuth(auth_id, auth_token))
outbound_rate = float(get_response4.json()["message"]["outbound"]["rate"])           # Get the outbound sms rate and convert to float
print "\n Outbound rate for sms is " + str(outbound_rate)

""" Compare the amount charged and outbound rate """

if amt_charged == outbound_rate:
    print "\n...................Amount charged is same as Outbound rate.............."
else :
    print "\n Amount charged is not the same as outbound rate, please check "
    
""" Get the cash credits from the account after sending a message using Account API """

get_response5 = requests.get(url + auth_id + '/', auth=HTTPBasicAuth(auth_id, auth_token))
cash_credits_end = float(get_response5.json()["cash_credits"])                        # Convert the unicode response in float and store
print "\n Cash credits after sending the sms is " + str(cash_credits_end)

""" Compare the cash credits before and after sending the sms """

if cash_credits_end == cash_credits_start - amt_charged:
    print "\n...................TASK COMPLETED..............\n"
else :
    print "\n.............TASK FAILED............\n"
