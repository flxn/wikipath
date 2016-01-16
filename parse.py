# -*- coding: utf-8 -*-
#!/usr/bin/env python

from xml.etree import ElementTree as ET
import re
import csv
import sys

filename = sys.argv[1]

wikitext_link_re = re.compile(ur'\[\[(.*?)\]\]')

nodenames = dict()
with open('nodes.txt', 'wb') as nnf:
    with open('graph_out.csv', 'wb') as f:
        #writer = csv.writer(f)
        pagecount = 0
        for event, elem in ET.iterparse(filename):
            if event == "end":
                elem.tag = elem.tag.split('}', 1)[1]
                links = []
                if elem.tag == "page":
                    pagecount += 1
                    sys.stdout.write("\rArticles parsed: %i" % pagecount)
                    sys.stdout.flush()
                if elem.tag == "title":
                     title = elem.text.replace('"','\\"')
                if elem.tag == "text":
                    if isinstance(elem.text, basestring):
                        matches = re.findall(wikitext_link_re, elem.text)
                        for match in matches:
                            if '|' in match:
                                match = match.split('|')[0]
                            if '#' in match:
                                match = match.split('#')[0]
                            match = match.replace('"','\\"')
                            links.append(match)

                if len(links) > 0:
                    output = []
                    output.append(title.encode('utf-8'))
                    output.append('|'.join([link.encode('utf-8') for link in links]))

                    try:
                        t = nodenames[title]
                    except KeyError as e:
                        nodenames[title] = len(nodenames)
                        nnf.write(str(nodenames[title]) + '|' + title.encode('utf-8') + '\n')
                        pass

                    for link in links:
                        try:
                            t = nodenames[link]
                        except KeyError as e:
                            nodenames[link] = len(nodenames)
                            nnf.write(str(nodenames[link]) + '|' + link.encode('utf-8') + '\n')
                            pass

                    f.write(str(nodenames[title]) + ';' + '|'.join([str(nodenames[link]) for link in links]) + '\n')

                    #f.write(str(nodenames.index(title)) + ';' + '|'.join([str(nodenames.index(link)) for link in links]) + '\n')
                    #f.write('"' + title.encode('utf-8') + '";"' + '|'.join([link.encode('utf-8') for link in links]) + '"\n')
                    #writer.writerow(output)
                #print '"' + title.encode('utf-8') + '";"' + '|'.join([link.encode('utf-8') for link in links]) + '"'

            elem.clear()
