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

from RocketGate import *

request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

#
#	Setup the Purchase request.
#
request.Set(GatewayRequest.MERCHANT_ID, 1)
request.Set(GatewayRequest.MERCHANT_PASSWORD, "testpassword")
request.Set(GatewayRequest.CARDNO, "4111-1111-1111-1111")

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, "Customer-1")

request.Set(GatewayRequest.BILLING_ADDRESS, "317 Clydesdale Drive")
request.Set(GatewayRequest.BILLING_CITY, "Stephens City")
request.Set(GatewayRequest.BILLING_STATE, "Virginia")
request.Set(GatewayRequest.BILLING_ZIPCODE, "22655")
request.Set(GatewayRequest.BILLING_COUNTRY, "US")

request.Set(GatewayRequest.EMAIL, "darcy@rocketgate.com")
request.Set(GatewayRequest.IPADDRESS, "68.224.133.117")

#
#      Setup test parameters in the service.
#
service.SetTestMode(1)

#
#      Perform the scrub transaction.
#
status = service.PerformCardScrub(request, response)
if (status):
    print ("CardScrub succeeded")
    print ("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print ("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print ("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))
else:
    print ("CardScrub failed")
    print ("Response Code: ", response.Get(GatewayResponse.RESPONSE_CODE))
    print ("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print ("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))
    print ("Exception: ", response.Get(GatewayResponse.EXCEPTION))

