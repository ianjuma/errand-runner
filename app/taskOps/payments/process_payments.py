import urllib2
import pesapal


pesapal.consumer_key = 'CkTmeBHciLM07WG0ltwGu8fklRSKdEqd'
pesapal.consumer_secret = 'X6mK+tUOne8tHbIZvETFjDvuDz0='
pesapal.testing = False

# sample request data - dummy
request_data = {
    'Amount': '100',
    'Description': 'Task Sample',
    'Type': 'MERCHANT',
    'Reference': '12erwe',
    'PhoneNumber': '0701435178'
}


def postOrder(request_data):
    """
        build url to redirect user to confirm payment
    """
    post_params = {
        'oauth_callback': 'http://127.0.0.1/post_payment/'
    }

    url = pesapal.postDirectOrder(post_params, request_data)
    return url


def queryPaymentByRef(post_params):
    # post_params are from url post
    url = pesapal.queryPaymentStatusByMerchantRef(post_params)
    response = urllib2.urlopen(url)
    return response.read()


def queryPayment(post_params):
    """
        Get order status
    """
    url = pesapal.queryPaymentStatus(post_params)
    response = urllib2.urlopen(url)
    return response.read()


def queryPamentDetails(post_params):
    """
        Get detailed order status
    """
    url = pesapal.queryPaymentDetails(post_params)
    response = urllib2.urlopen(url)
    return response.read()


# req 2 on -> POST
post_params = {
  'pesapal_merchant_reference': '000',
  'pesapal_transaction_tracking_id': '000'
}