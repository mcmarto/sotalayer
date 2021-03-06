#!/usr/bin/env python3

# Python program to extract country-specific SOTA peaks from "summitslist.csv"
# and write out a GPX file, "favourites.gpx".  This can be copied directly
# to the OsmAnd file directory on an Android phone.  OsmAnd will import and
# merge the peaks with existing favourites so that SOTA peaks can be viewed
# on the OsmAnd screen.

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('region',
                    nargs='?',
                    help='SOTA region to extract, e.g. G/ or G/CE')

args = parser.parse_args()

if args.region is None:
    print("Region must be specified.")
    sys.exit()

key = args.region       # First part of SOTA ref. to match (can be as long as you like)
print("Extracting '%s'."%key)

id = 0     # Internal counter

# Colours for each point level.  Gradient from green to red.
colours = {'1':'00FF00', '2':'65FF00', '4':'CCFF00', '6':'FFCC00', '8':'FF6600', '10':'FF0000'}

with open('favourites.gpx', 'w', encoding='utf-8') as o:

    o.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
    o.write('<gpx version="1.1" creator="sotagpx.py" xmlns="http://www.topografix.com/GPX/1/1"\n')
    o.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
    o.write('xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')

    with open("summitslist.csv", encoding='utf-8') as f:
        for line in f:
            if line[:len(key)] == key:
                
                id -= 1

                fields = line.split(',')

                # Name is "SOTA ref. Name [Points]"
                name = fields[0] + ' ' + fields[3] + ' [' + fields[10] + ']'

                # Activations go in 'desc', with URL.
                activations = fields[14] + ' activation' + ('.' if int(fields[14])==1 else 's.')
                if int(fields[14]) > 0:
                    activations += '\nLast ' + fields[16] + ' (' + fields[15] + ').'
                    
                o.write('  <wpt lat="%s" lon="%s">\n'%( fields[9],fields[8]))
                o.write('    <ele>%s</ele>\n'%(fields[4]))
                o.write('    <name>%s</name>\n'%(name))
                o.write('    <desc>%s\nhttp://www.sota.org.uk/Summit/%s</desc>\n'%(activations,fields[0]))
                o.write('    <type>SOTA %s</type>\n'%fields[0].split('-')[0])   # SOTA + Association + Region
                o.write('    <extensions>\n')
                o.write('        <color>#%s</color>\n'%colours[fields[10]])
                o.write('    </extensions>\n')
                o.write('  </wpt>\n')

    o.write("</gpx>\n")

print("%s POIs extracted."%abs(id))
