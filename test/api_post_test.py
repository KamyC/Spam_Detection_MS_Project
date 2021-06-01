import requests,json
# this is a post test to report spam
url = 'http://localhost:5000/detect_api/post_report'
data = {
    'tweet':'this is a tweet for report',
    'label':'True'
}
r = requests.post(url,json.dumps(data))
print(r.json())

# this is a post test to detect spam
url =  'http://localhost:5000/detect_api/post_detect'
data = {
    'tweet':'this is a tweet for detect',
    'label':'Unknown'
}
r = requests.post(url,json.dumps(data))
print(r.json())
