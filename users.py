# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 17:20:55 2015

@author: jayantsahewal
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

OSMFILE = "orlando_florida.osm"

def get_user(element):
    return


def process_map(filename):
    users = []
    for event, element in ET.iterparse(filename):
        if 'uid' in element.attrib.keys():
            if element.attrib['uid'] not in users:
                users.append(element.attrib['uid'])       

    return users


def test():
    users = process_map(OSMFILE)
    pprint.pprint(users)


if __name__ == "__main__":
    test()