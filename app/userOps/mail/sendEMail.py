#! /usr/bin/env python

import requests

# simple mail using POST

def send_message(to, message):
    return requests.post(
        "https://api.mailgun.net/v2/benchcare.co",
        auth=("api", "key-8-5nfh4jvinhqtv2ww-0htrmgopbwue6"),
        data={"from": "LinkUs" + "<email@benchcare.co>",
              "to": [to],
              "subject": "LinkUs",
              "text": message})


def get_domains():
	return requests.get(
        "https://api.mailgun.net/v2/domains",
        auth=("api", "key-8-5nfh4jvinhqtv2ww-0htrmgopbwue6"),
        params={"skip": 0,
                "limit": 3})

