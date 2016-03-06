# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 17:21:00 2015

@author: jayantsahewal
"""

"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

OSMFILE = "orlando_florida.osm"
street_type_suffix = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_prefix = re.compile(r'^\b\S+\.?', re.IGNORECASE)

expected_suffix = ["Avenue", "Boulevard", "Broadway", "Circle", "Court", "Drive", "Lane", "North", "Parkway",
            "Place", "Plaza", "Road", "Row", "Street", "Trail", "Turnpike", "Way"]

expected_prefix = []
# Mapping variable for updating the street names
mapping_suffix = {
            "St.": "Street",
            "St": "Street",
            "Rd" : "Road",
            "Blvd" : "Boulevard",
            "blvd." : "Boulevard",
            "Dr" : "Drive",
            "Ave" : "Avenue"}


mapping_prefix = {
            "N" : "North",
            "N." : "North",
            "S" : "South",
            "S." : "South",
            "E" : "East",
            "E." : "East",
            "W" : "West",
            "W." : "West"}

# Return Street Types which are not present in expected or mapping
def audit_street_type(street_types, street_name):
    m = street_type_suffix.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_suffix:
            street_types[street_type].add(street_name)

# Check if the element being parsed is a street or not
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Audit an OSMFILE using helper functions
def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    street_names = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    street_names.add(tag.attrib['v'])
                    audit_street_type(street_types, tag.attrib['v'])
 
    return street_types

# Update the name using the mapping defined
def update_name(name):

    # YOUR CODE HERE
    m = street_type_prefix.search(name)
    better_name = name
    if m:
        if m.group() in mapping_prefix:
            better_street_type = mapping_prefix[m.group()]
            better_name = street_type_prefix.sub(better_street_type, name)

    m = street_type_suffix.search(better_name)
    if m:
        if m.group() in mapping_suffix:
            better_street_type = mapping_suffix[m.group()]
            better_name = street_type_suffix.sub(better_street_type, better_name)
    
    # Extra cleaning based upon manual observations
    # These were very few, so I didn't spend much time to come up with better functions
    better_name = re.sub("Rd", "Road", better_name)
    better_name = re.sub("Ste", "Suite", better_name)
    better_name = re.sub("-", " ", better_name)
    better_name = re.sub(" E ", " East ", better_name)
    better_name = re.sub(r"\s+", " ", better_name, flags=re.UNICODE)
    better_name = string.capwords(better_name)

    return better_name

def update_postcode(zipcode):
    zipcode = re.sub("FL", "", zipcode)
    zipcode = re.sub(r"\s+", "", zipcode)
    zipcode = zipcode[:5]
    return zipcode

def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))
    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping_prefix)
            print name, "=>", better_name
    print update_postcode('32821')
    print update_postcode('FL 32801')
    print update_postcode('32819-7827')        

if __name__ == '__main__':

    test()