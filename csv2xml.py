#!/usr/bin/python -u

# Installation (for detailed instruction see - https://github.com/amardeshbd/android-resource-converter/blob/master/README.md

# usage: $ python csv2xml.py <file_with_translations>.csv

import csv
from lxml import etree
import sys

reader = csv.reader(open(sys.argv[1], "rb"), delimiter='\t', quotechar='',
                    skipinitialspace=False, quoting=csv.QUOTE_NONE)
translations = []
roots = []
resourceKey = "Key"
resourceNameKey = "name"

for row in reader:
    if row[0] == resourceKey:
        translations = row
        translations.pop(0)
        break

for translation in translations:
    roots.append(etree.Element("resources"))

for row in reader:
    if row[0] != resourceKey:
        number_of_translations = len(row) - 1
        for i in range(0, number_of_translations):
            string_resource = etree.SubElement(roots[i], "string")
            string_resource.set(resourceNameKey, row[0])
            string_resource.text = row[i + 1].decode('utf-8').replace("'", "\\'")
            if number_of_translations == 1:
                string_resource.set("translatable", "false")

# Function to sort the keys
def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))


#
# Prepare the XML document with all the collected nodes
#

xml_file_header = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

for i in range(0, len(translations)):
    xml_string = etree.tostring(roots[i], encoding='unicode', method='xml', pretty_print=True, xml_declaration=False)
    pretty_xml_string = xml_file_header
    pretty_xml_string += xml_string 
    xml_file = open(translations[i], "w")
    xml_file.write(pretty_xml_string.encode('utf-8'))
    xml_file.close()

# Make another copy of XML with sorted keys
for i in range(0, len(translations)):
    tree = etree.parse(translations[i])
    root = tree.getroot()
    sortchildrenby(root, resourceNameKey)
    tree.write(translations[i] + '_sorted.xml')
