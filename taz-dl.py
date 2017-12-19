#!/usr/local/bin/python3
import settings
import requests
import sys
import getopt
from bs4 import BeautifulSoup as bs


'''

-pull the taz homepage in order to determine the name of the most recent taz issue
-download the latest issue as pdf, epub, or mobi format and save it to disk

'''

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:d:")
    except getopt.GetoptError:
        print('usage: taz-dl -f <format> -d <destination>')
        sys.exit(2)

    # parse command line paramter
    destination = ''
    fileforamt = ''

    for opt, arg in opts:
        if opt == '-h':
            print('usage: taz-dl.py -f <format> -d <destination> ')
            print('available formats: epub, pdf, mobi')
            sys.exit()
        elif opt == '-f':
            if arg in ['pdf', 'epub', 'mobi']:
                fileformat = arg
            else:
                print(arg)
                print('wrong format, available formats: epub, pdf, mobi')
                sys.exit(2)
        elif opt == '-d':
            destination = arg

    # determine the name of the most recent issue 
    r = requests.get("https://dl.taz.de/{0}".format(fileformat))
    content = r.content
    soup = bs(content, "html.parser")
    option= soup.find_all('option')[0]
    id = format(option['value'])

    # login to homepage and request file
    login_items = {'name': settings.AboId, 'password': settings.password, 'id': id, 'Laden':' Laden '}
    url = 'https://dl.taz.de/{0}'.format(fileformat)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
    headers = { 'User-Agent' : user_agent }
    r = requests.post(url, data=login_items, headers = headers)

    # write file to disk
    with open(destination + login_items['id'], 'wb') as output:
        output.write(r.content)


if __name__ == "__main__":
    main(sys.argv[1:])
