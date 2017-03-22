#!/usr/bin/python

import bs4
import requests

URL = 'http://www.farsnews.com'
page = requests.get(URL + '/RSSLinks')

soup = bs4.BeautifulSoup(page.content,'lxml')

names = soup.find_all(attrs={'class': 'centercolumn'})[0].contents

rss = []
for name in names:
    try:
        if name.attrs['class'][0].startswith('rsslinks'):
            rss.append(name.find('a'))
    except:
        pass


RSSLinks = [(r.text.encode('utf8'), r.attrs['href']) for r in rss]
RSSFLink = [(r.text.encode('utf8'), URL + r.attrs['href']) for r in rss]

with open('RSSF.py', 'w') as f:
    f.write('RSSLinks={:}\nRSSFLink={:}\n'.format(RSSLinks,RSSFLink))
    f.write('''
RSSLinks = [(t.decode('utf8'),u) for t,u in RSSLinks]
RSSFLink = [(t.decode('utf8'),u) for t,u in RSSFLink]''')
    