#!/usr/local/bin/python
import requests
import keyring 
from bs4 import BeautifulSoup as bs

# pull the taz homepage in order to determine the name of the
# most recent epub file
# result is saved in variable 'id' 

# added a comment here

r = requests.get("https://dl.taz.de/ipaper") 
content = r.content
soup = bs(content, "html.parser")
option= soup.find_all('option')[0]
id = format(option['value'])

# login to homepage and request epub file

login_items = {'name':'117600', 'password':keyring.get_password("taz_download", "117600"),'id': id,'Laden':' Laden '}
url = 'https://dl.taz.de/ipaper'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
headers = { 'User-Agent' : user_agent }
r = requests.post(url, data=login_items, headers = headers)

# write file to disk
with open("/Users/jplenge/Downloads/" + login_items['id'], 'wb') as output:
    output.write(r.content)
