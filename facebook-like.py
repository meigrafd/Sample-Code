#Tutorial : http://www.idiotinside.com/2015/02/13/get-number-of-likes-of-a-facebook-page-using-graph-api-in-python/
import urllib2
import json

def getPageData(page_id):
    api_endpoint = "https://graph.facebook.com"
    fb_graph_url = api_endpoint+"/"+page_id
    try:
        api_request = urllib2.Request(fb_graph_url)
        api_response = urllib2.urlopen(api_request)
        try:
            return json.loads(api_response.read())
        except (ValueError, KeyError, TypeError):
            return "JSON error"

except IOError, e:
    if hasattr(e, 'code'):
        return e.code
        elif hasattr(e, 'reason'):
            return e.reason

page_id = "idiotinside" # username or id

data = getPageData(page_id)
print "Page Name:"+ data['name']
print "Likes:"+ str(data['likes'])
print "Website:"+ data['link']
