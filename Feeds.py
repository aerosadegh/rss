# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 16:48:30 2017

@author: Sadegh
"""


import feedparser as fp
import jdatetime, dateparser
import persian as pr
from emoji import emojize
from time import strftime, sleep

config = {}
exec(compile(open("RSSF.py").read(), "RSSF.py", 'exec'),config)
RSSFLink = config['RSSFLink']

#em = lambda x: emojize(x, use_aliases=True)

def cdp(st):    
    #dat_time = dateparser.parse(u'Sun, 11 Mar 2017 10:22:50')
    dat_time = dateparser.parse(st)
    pdt = jdatetime.datetime.fromgregorian(datetime = dat_time)
    pds = pr.enWeekdayToPersian(pr.enMonthToPersian(pr.enToPersianNumb(pdt.strftime("%H:%M:%S ,%a %d %b %Y"))),full=True)
    return pds

while 1:
    st = ''
    sd = ''
    print('Updating...')
    for cat,u in RSSFLink:
        fd = fp.parse(u)
        print(u.split('/')[-1], end=' ')
        st += ':arrow_down:' + 'بروز شده در\n {:}'.format(cdp(fd['feed']['updated']))+'\n'
        st += '\n.|.\n'
        for c in fd['entries']:
            st += '{:} [{:}]({:})\n\n{:}\n\n`{:}`\n{:}\n'.format(':arrow_left:',
                                                               c['title'],
    												                  c['link'],                                 
                                                               c['summary'],
                                                               cdp(c['published']),
                                                               ':heavy_check_mark: @FarsRssBot'
                                                               )
#        sd += '{:}\n'.format(cdp(c['published']))
    
            st += '\n.|.\n'
        st += '\n..|..\n'

    with open('FD.txt','w') as f:
        f.write(str(st.encode('utf8')))
    print(strftime('%H:%m:%S'),'\nSleep...')
    sleep(540)
    
    
