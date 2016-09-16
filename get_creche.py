# -*- coding: utf-8 -*-
"""
***************************************************************************
    get_creche_adresse.py
    ---------------------
    Date                 : 2016-04-08 15:11:10
    Copyright            : (C) 2016 by ASTER
    Email                : ddtm-sctsrd-aster@eure.gouv.fr
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'ASTER'
__date__ = '2016-04-08 15:11:10'
__copyright__ = '(C) 2016, ASTER'


import urllib2
from bs4 import BeautifulSoup
import csv

# proxy handeler
proxy_support = urllib2.ProxyHandler({"http":"http://direct.proxy.i2:8080"})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)


_CSVFILE_=r'C:/creches_eure.csv'
_URL_ =ur'http://lescreches.fr/eure-27/'
page = 1
continue_request = True
url = _URL_

with open(_CSVFILE_, 'wb') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    hearders = [u'nom_creche',u'type_creche',u'commune',u'information',u'adresse',u'horaire']
    csv_writer.writerow([header.encode('utf-8') for header in hearders])
    while continue_request:
        print(u'traitement page {}'.format(page))
        try:
            req = urllib2.Request(url, None, headers={'User-Agent' : "New Browser"})
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            # <div class="item ev">
            # <h4><a href="/evreux-27000/halte-garderie-la-madeleine-1px.html">Halte garderie la Madeleine</a></h4>
            # <p><em>Halte-garderie</em> à <em>Évreux</em> (27000)</p>
            # <p>Rue Joliot Curie 27000 Évreux</p>
            # <p>Lundi, mardi, mercredi et vendredi de 8h30 à 12h30 et 13h30 à 17h - jeudi de 8h30 à 17h</p>
            # </div>
            soup.find_all('div')
            creches = soup.find_all('div', 'item')
            for creche in creches:
                info_creche = []
                info_creche.append(creche.h4.text)
                info_creche += [ elem.text for elem in creche.p.find_all('em')]
                info_creche += [ elem.text for elem in creche.find_all('p') if elem.text is not None]
                csv_writer.writerow([info.encode('utf-8') for info in info_creche])
            page += 1
            url = "{}page{}.html".format(_URL_,str(page)) #http://lescreches.fr/eure-27/page2.html
        except urllib2.HTTPError :
            continue_request = False