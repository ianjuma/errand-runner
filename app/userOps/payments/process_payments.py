import urllib2
import pesapal


pesapal.consumer_key = 'CkTmeBHciLM07WG0ltwGu8fklRSKdEqd'
pesapal.consumer_secret = 'X6mK+tUOne8tHbIZvETFjDvuDz0='
pesapal.testing = False


### post a direct order
post_params = {
    'oauth_callback': 'http://taskwetu.com/payments_pesapal'
}
request_data = {
    'Amount': '100',
    'Description': 'E-book purchase', # task_cat
    'Type': 'MERCHANT',
    'Reference': '12erwe', # rand no - stored - task_id
    'PhoneNumber': '0701435178'
}
# build url to redirect user to confirm payment
# place url in view
url = pesapal.postDirectOrder(post_params, request_data)


### get order status
### get from url
post_params = {
    'pesapal_merchant_reference': '000',
    'pesapal_transaction_tracking_id': '000'
}
url = pesapal.queryPaymentStatus(post_params)
response = urllib2.urlopen(url)
print response.read()


### get order status by ref

post_params = {
    'pesapal_merchant_reference': '000'
}
url = pesapal.queryPaymentStatusByMerchantRef(post_params)
response = urllib2.urlopen(url)
print response.read()


### get detailed order status

post_params = {
    'pesapal_merchant_reference': '000',
    'pesapal_transaction_tracking_id': '000'
}
url = pesapal.queryPaymentDetails(post_params)
response = urllib2.urlopen(url)
print response.read()
