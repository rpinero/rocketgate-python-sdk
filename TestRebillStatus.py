#! /usr/bin/env python
#
# Copyright notice:
# (c) Copyright 2020 RocketGate
# All rights reserved.
#
# The copyright notice must not be removed without specific, prior
# written permission from RocketGate.
#
# This software is protected as an unpublished work under the U.S. copyright
# laws. The above copyright notice is not intended to effect a publication of
# this work.
# This software is the confidential and proprietary information of RocketGate.
# Neither the binaries nor the source code may be redistributed without prior
# written permission from RocketGate.
#
# The software is provided "as-is" and without warranty of any kind, express, implied
# or otherwise, including without limitation, any warranty of merchantability or fitness
# for a particular purpose.  In no event shall RocketGate be liable for any direct,
# special, incidental, indirect, consequential or other damages of any kind, or any damages
# whatsoever arising out of or in connection with the use or performance of this software,
# including, without limitation, damages resulting from loss of use, data or profits, and
# whether or not advised of the possibility of damage, regardless of the theory of liability.
#

#
# Example $9.99 USD monthly subscription purchase.
# Subsequently, Check the status of the subscription
#

import datetime
from RocketGate import *

request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

merchID = "1";
merchPassword = "testpassword";

# For example/testing, we set the order id and customer as the unix timestamp as a convienent sequencing value
# appending a test name to the order id to facilitate some clarity when reviewing the tests
theTime = datetime.datetime.now().strftime("%s")
custID = theTime + ".PythonTest";
invID = theTime + ".RebillStatusTest";

#
#	Setup the nly request.
#
request.Set(GatewayRequest.MERCHANT_ID, merchID)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merchPassword)

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, custID)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, invID)

# $9.99/month subscription
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.AMOUNT, 9.99)
request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

request.Set(GatewayRequest.CARDNO, "4111-1111-1111-1111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.EMAIL, "Pythontest@fakedomain.com")
request.Set(GatewayRequest.IPADDRESS, "68.224.133.117")

request.Set(GatewayRequest.BILLING_ADDRESS, "123 Main St.")
request.Set(GatewayRequest.BILLING_CITY, "Las Vegas")
request.Set(GatewayRequest.BILLING_STATE, "NV")
request.Set(GatewayRequest.BILLING_ZIPCODE, "89141")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

# Risk/Scrub Request Setting
request.Set(GatewayRequest.AVS_CHECK, "IGNORE")
request.Set(GatewayRequest.CVV2_CHECK, "IGNORE")
request.Set(GatewayRequest.SCRUB, "IGNORE")

#
#      Setup test parameters in the service.
#
service.SetTestMode(1)

#
#      Perform the Purchase transaction.
#
status = service.PerformPurchase(request, response)
if (status):
    print ("Purchase succeeded")
    print ("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))
    print ("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print ("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print ("AuthNo: ", response.Get(GatewayResponse.AUTH_NO))
    print ("AVS: ", response.Get(GatewayResponse.AVS_RESPONSE))
    print ("CVV2: ", response.Get(GatewayResponse.CVV2_CODE))
    print ("CardHash: ", response.Get(GatewayResponse.CARD_HASH))
    print ("Account: ", response.Get(GatewayResponse.MERCHANT_ACCOUNT))
    print ("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))

    # Check Rebill Status
    ##
    ##  This would normally be two separate processes, 
    ##  but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
    ##  The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID.
    ## 
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, merchID)
    request.Set(GatewayRequest.MERCHANT_PASSWORD, merchPassword)

    request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, custID)
    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, invID)

    status = service.PerformRebillUpdate(request, response)
    if (status):
        print ("\nStatus Check succeeded")

        rebill_end_date = response.Get(GatewayResponse.REBILL_END_DATE)

        if (rebill_end_date == None):
            print ("  User is Active and Set to Rebill")

        elif  (datetime.datetime.strptime(rebill_end_date,"%Y-%m-%d") > time):
            print ("  User is Active and Set to Cancel")
        
        else:
            print ("  User is Canceled")

        print ("  Rebill Amount: ", response.Get(GatewayResponse.REBILL_AMOUNT))
        print ("  Rebill Date: ", response.Get(GatewayResponse.REBILL_DATE))
        print ("  Cancel Date: ", response.Get(GatewayResponse.REBILL_END_DATE))

    else:
        print ("\nStatus Check failed")
        print ("  Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
        print ("  Reason Code: ", response.Get(GatewayResponse.REASON_CODE))

else:
    print ("Purchase failed\n")
    print ("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))
    print ("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print ("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print ("Exception: ", response.Get(GatewayResponse.EXCEPTION))
    print ("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))
    exit()

