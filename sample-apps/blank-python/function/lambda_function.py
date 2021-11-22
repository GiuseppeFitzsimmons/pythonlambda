import os
import logging
#import jsonpickle
#import boto3
import geoip2.webservice
import sys
import json

redirect = json.loads(open('./redirect.json').read().encode('ascii'))

#codicil isn't the only campaign, get a url parser and find out which one we're on and use that as the first index of redirect

def lambda_handler(event, context):
    #move this line to an outside test script, so you don't pollute this with test-specific shit
    if(type(event) is str):
        event = (json.loads(open(sys.argv[1], 'r').read()))
    response = geoip2.webservice.Client(639089, 'pKA4mu9VIQuHs7E9', host='geolite.info').country(event['requestContext']['sourceIp'])
    try:
        url_code = redirect['codicil'][response.country.iso_code]
        print('https://indie-fensible.pub/'+str(url_code)+'/googleads')
        return 'https://indie-fensible.pub/'+str(url_code)+'/googleads'
    except KeyError:
        url_code = redirect['codicil']['default']
        print('https://indie-fensible.pub/'+str(url_code)+'/googleads')
        return 'https://indie-fensible.pub/'+str(url_code)+'/googleads'

lambda_handler(sys.argv[1], sys.argv[2])