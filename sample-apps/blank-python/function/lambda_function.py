import geoip2.webservice
import json
from datetime import date

redirect = json.loads(open('./redirect.json').read().encode('ascii'))
error_object={'error':'error, probably failed to parse path'}

def lambda_handler(event, context):
    try:
        response = {}
        event_path = str(event['requestContext']['path'])
        book_campaign = str(event_path).split('/')[3]
        platform = str(event_path).split('/')[4]
    except:
        print('error, probably failed to parse url')
        return (
                    {
            "statusCode": 307,
            "headers": {
                "Content-Type": "application/json",
                "location":str(redirect['default']['default'])
            },
            "body": ''
        }
        )
    try:
        response = geoip2.webservice.Client(639089, 'pKA4mu9VIQuHs7E9', host='geolite.info').country(event['requestContext']['sourceIp'])
        json_log = {"country":response.country.iso_code.encode('ascii'), "platform":platform, "book_campaign": book_campaign, "date":str(date.today()) }
        print(json_log)
        try:
            redirect_url = redirect[book_campaign][response.country.iso_code]
        except:
            try:
                redirect_url = redirect[book_campaign]['default']
            except:
                redirect_url = redirect['default']['default']
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