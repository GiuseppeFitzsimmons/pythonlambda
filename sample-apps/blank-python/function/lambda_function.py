import os
import logging
#import jsonpickle
#import boto3
import geoip2.webservice
import sys
import json
from datetime import date

redirect = json.loads(open('./redirect.json').read().encode('ascii'))
error_object={'error':'error, probably failed to parse path'}

def lambda_handler(event, context):
    #move this line to an outside test script, so you don't pollute this with test-specific shit
    try:
        if(type(event) is str):
            event = (json.loads(open(sys.argv[1], 'r').read()))
        response = {}
        event_path = str(event['requestContext']['path'])
        book_campaign = str(event_path).split('/')[3]
        platform = str(event_path).split('/')[4]
    except:
        print(error_object)
        return error_object
    try:
        response = geoip2.webservice.Client(639089, 'pKA4mu9VIQuHs7E9', host='geolite.info').country(event['requestContext']['sourceIp'])
        json_log = json.dumps({"country":response.country.iso_code, "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) })
        try:
            redirect_url = redirect[book_campaign][response.country.iso_code]
            print(str(redirect_url))
            return str(redirect_url)
        except KeyError:
            redirect_url = redirect[book_campaign]['default']
            print(str(redirect_url))
            return str(redirect_url)
    except:
        print('Cannot parse IP, setting to default')
        json_log = json.dumps({"country":"invalid", "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) })
        redirect_url = redirect[book_campaign]['default']
        print(str(redirect_url))
        return str(redirect_url)
    print('json_log', json_log)

lambda_handler(sys.argv[1], sys.argv[2])