#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 00:13:20 2017

@author: msadegh
"""

config = {}
exec(compile(open("RSSF.py").read(), "RSSF.py", 'exec'),config)
RSSFLink = config['RSSFLink']

Feeds = []
with open('FD.txt','r') as f:
    p = eval(f.read()).decode('utf8')
    lst = p.split('\n..|..\n')
    Feeds = [c.split('\n.|.\n') for c in lst]
    
