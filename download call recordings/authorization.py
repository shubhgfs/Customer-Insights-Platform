import requests
import hashlib
import hmac
import base64
import re
import os
import random
import json
from urllib.parse import urlparse
from datetime import datetime
import pandas as pd


APIKeyId = "q64eqHNP"
APIKey = "NB5dduSmQL8_ye0NALLuq_O-yyoTXFAWLvlzfNiCTVs"
SERVER = "wfo.mt3.verintcloudservices.com"

def base64url(input):
    base64String = base64.b64encode(input).decode('utf-8')
    return urlConvertBase64(base64String)

def debase64url(str):
    str += '==='.lstrip(str[-1])
    str = str.replace('-', '+').replace('_', '/')
    return str

def generate_canonicalizedHeader():
    # generate canonicalizedHeader
    ref = dict(pm.request.headers)
    canonicalizedHeader = ""

    for key, value in ref.items():
        if key[:7].lower() != "verint-":
            continue
        canonicalizedHeader += (key + ":")
        canonicalizedHeader += value
        canonicalizedHeader += "\n"

    # make canonicalizedHeader lowercase
    canonicalizedHeader = canonicalizedHeader.lower()

    return

def urlConvertBase64(input):
    output = input.rstrip('=').replace('+','-').replace('/','_')
    return output

def replaceVars(string):
    def replaceFunc(match):
        varName = match.group()[2:-2]
        varValue = pm.environment[varName] or pm.globals[varName]
        return varValue and replaceVars(varValue) or match.group()
    return re.sub('{{.+?}}', replaceFunc, string)

def getAuthHeader(url, method):
    random = os.urandom(16)
    path = urlparse(url).path
    salt = base64url(random)
    issuedAt = datetime.utcnow().isoformat()[:19] + "Z"
    stringToSign = '{}\n{}\n{}\n{}\n{}\n'.format(salt, method, path, issuedAt, "")
    hash = hmac.new(base64.b64decode(debase64url(APIKey)), stringToSign.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(hash.digest()).decode('utf-8')
    verintAuthId = "Vrnt-1-HMAC-SHA256"
    authHeaderValue = '{} salt={},iat={},kid={},sig={}'.format(verintAuthId, salt, issuedAt, APIKeyId, urlConvertBase64(signature))
    # print(authHeaderValue)
    return authHeaderValue

def check_auth():
    #Simple check if API point is up and running
    URL = "https://wfo.mt3.verintcloudservices.com/api/recording/locator/v1/export/interactions/2024041213182346982908600089234705".format(SERVER)
    method = "POST"

    HEADERS = {'Authorization' : getAuthHeader(URL, method)}
    r = requests.head(url = URL, headers = HEADERS)
    if r.status_code == 200:
        print('IngestionWS is up and running, auth OK')
    return

# check_auth()
