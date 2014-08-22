import urllib2
import pesapal


pesapal.consumer_key = 'CkTmeBHciLM07WG0ltwGu8fklRSKdEqd'
pesapal.consumer_secret = 'X6mK+tUOne8tHbIZvETFjDvuDz0='
pesapal.testing = False


def postOrder(request_data):
    """
        build url to redirect user to confirm payment
    """
    post_params = {
        'oauth_callback': 'http://188.226.195.158/billing/'
    }

    url = pesapal.postDirectOrder(post_params, request_data)


def queryPayment(post_params):
    """ 
        Get order status
    """
    url = pesapal.queryPaymentStatus(post_params)


def queryPamentDetails(post_params):
    """
        Get detailed order status
    """


response = urllib2.urlopen(url)
print response.read()


### get order status by ref

post_params = {
  'pesapal_merchant_reference': '000'
}
url = pesapal.queryPaymentStatusByMerchantRef(post_params)
response = urllib2.urlopen(url)
print response.read()



post_params = {
  'pesapal_merchant_reference': '000',
  'pesapal_transaction_tracking_id': '000'
}
url = pesapal.queryPaymentDetails(post_params)
response = urllib2.urlopen(url)
print response.read()