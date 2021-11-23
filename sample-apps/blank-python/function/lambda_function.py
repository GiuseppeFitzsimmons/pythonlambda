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
        print('error, probably failed to parse url')
        return (
                    {
        "statusCode": 502,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": error_object
    }
        )
    try:
        response = geoip2.webservice.Client(639089, 'pKA4mu9VIQuHs7E9', host='geolite.info').country(event['requestContext']['sourceIp'])
        json_log = {"country":response.country.iso_code.encode('ascii'), "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) }
        print(json_log)
        try:
            redirect_url = redirect[book_campaign][response.country.iso_code]
        except KeyError:
            redirect_url = redirect[book_campaign]['default']
    except:
        print('Cannot parse IP, setting to default')
        json_log = {"country":"invalid", "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) }
        print(json_log)
        redirect_url = redirect[book_campaign]['default']
    return({
            "statusCode": 307,
            "headers": {
                "Content-Type": "application/json",
                "location":str(redirect_url)
            },
            "body": ''
        })

lambda_handler(sys.argv[1], sys.argv[2])