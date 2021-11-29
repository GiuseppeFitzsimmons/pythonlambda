import geoip2.webservice
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

geoip2_account = int(os.getenv('GEOIP2_ACCOUNT'))
geoip2_key = str(os.getenv('GEOIP2_KEY'))
redirect = json.loads(open('./redirect.json').read().encode('ascii'))
error_object={'error':'error, probably failed to parse path'}

def lambda_handler(event, context):
    json_log = {"country":'', "platform":'', "book_campaign": '', "date":str(date.today()) }
    try:
        book_campaign = event['pathParameters']['campaign']
        json_log['book_campaign']=book_campaign
        try:
            platform = event['pathParameters']['platform']
            json_log['platform']=platform
        except:
            print('Exception, platform not present')
    except:
        print('Exception, probably failed to parse url', event)
        try:
            ip = event['requestContext']['identity']['sourceIp']
            country=geoip2.webservice.Client(geoip2_account, geoip2_key, host='geolite.info').country(ip)
            json_log['country']=country
        except:
            print('Exception, cannot parse IP')
        print(json_log)
        return (
            {
                "statusCode": 307,
                "headers": {
                    "location":str(redirect['default']['default'])
                }
            }
        )
    try:
        ip = event['requestContext']['identity']['sourceIp']
        response = {}
        response = geoip2.webservice.Client(639089, 'pKA4mu9VIQuHs7E9', host='geolite.info').country(ip)
        try:
            redirect_url = redirect[book_campaign][response.country.iso_code.encode('ascii').decode()]
            json_log['book_campaign']=book_campaign
            json_log['country']=str(response.country.iso_code.encode('ascii').decode())
        except Exception as e:
            print('Exception, probably just a country not included in the redirect JSON', e)
            try:
                redirect_url = redirect[book_campaign]['default']
                json_log['country']=response.country.iso_code.encode('ascii').decode()
            except:
                redirect_url = redirect['default']['default']
                json_log['country']='default'
        print(json_log)
    except:
        print('Cannot parse IP, setting to default', response)
        json_log = {"country":"invalid", "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) }
        print(json_log)
        redirect_url = redirect[book_campaign]['default']
    return({
            "statusCode": 307,
            "headers": {
                "location":str(redirect_url)
            }
        })