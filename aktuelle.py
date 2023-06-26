import requests
import bs4
import logging
import html5lib
#import lxml
import traceback
from datetime import datetime
import pandas as pd
import time
timestr = time.strftime("%Y%m%d")
print (timestr)
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re

def schnell_kurs(ISIN):
    firmenname = 0
    e_geldkurs = 0
    e_briefkurs = 0
    e_andvortag = 0
    e_tageshoch = 0
    e_tagestief = 0
    e_umsatz = 0
    the_time = 0
    
    url = 'https://www.tradegate.de/orderbuch.php?isin='+ str(ISIN)
    try:
        
        
        
        web_page = bs4.BeautifulSoup(requests.get(url, {}).text, "html5lib")
        
        the_time = pd.Timestamp.now()
        ISIN = str(url)
        ISIN = ISIN.split("=", 1)
        ISIN = str((ISIN[1]))
        e_ISIN = ISIN
        
        
        
        # Geldkurs
        
        bid = web_page.find_all(id='bid')
        atzebid = str(bid)
        bieten = atzebid.split(">", 1)
        #print(bieten)
        geldkurs = bieten[1].split("<", 1)
        #print(geldkurs)
        geldkurs = str((geldkurs[0]))
        #print(geldkurs)
        geldkurs = geldkurs.replace(",", ".")
        geldkurs = geldkurs.replace(" ", "")
        e_geldkurs = float(geldkurs)
        
        # Briefkurs
        
        ask = web_page.find_all(id='ask')
        atzeask = str(ask)
        fragen = atzeask.split(">", 1)
        briefkurs = fragen[1].split("<", 1)
        briefkurs = str((briefkurs[0]))
        briefkurs = briefkurs.replace(" ", "")
        briefkurs = briefkurs.replace(",", ".")
        briefkurs = briefkurs.replace(" ", "")
        e_briefkurs = float(briefkurs)
        
        
        
        
        # Veranderung zum Vortag
        
        delta = web_page.find_all(id='delta')
        atzedelta = str(delta)
        unterschied = atzedelta.split(">", 1)
        andvortag = unterschied[1].split("%", 1)
        andvortag = str((andvortag[0]))
        andvortag = andvortag.replace(",", ".")
        e_andvortag = (float(andvortag) / 100)
        
        # Tageshoch
        
        hoch = web_page.find_all(id='high')
        atzehoch = str(hoch)
        oben = atzehoch.split(">", 1)
        tageshoch = oben[1].split("<", 1)
        tageshoch = str((tageshoch[0]))
        tageshoch = tageshoch.replace(" ", "")
        tageshoch = tageshoch.replace(",", ".")
        tageshoch = tageshoch.replace(" ", "")
        if tageshoch == './.':
            tageshoch = 0
        e_tageshoch = float(tageshoch)
        
        # Tagestief
        
        tief = web_page.find_all(id='low')
        atzetief = str(tief)
        unten = atzetief.split(">", 1)
        tagestief = unten[1].split("<", 1)
        tagestief = str((tagestief[0]))
        tagestief = tagestief.replace(" ", "")
        tagestief = tagestief.replace(",", ".")
        tagestief = tagestief.replace(" ", "")
        if tagestief == './.':
            tagestief = 0
        e_tagestief = float(tagestief)
        type(tagestief)

        # Umsatz

        handelsvolumen = web_page.find_all(id='stueck')
        volumen = str(handelsvolumen)
        menge = volumen.split(">", 1)
        umsatz = menge[1].split("<", 1)
        umsatz = str((umsatz[0]))
        umsatz = umsatz.replace(u'\xa0', u'')
        e_umsatz = float(umsatz)
        type(e_umsatz)

        # Firmenname

        soup = web_page
            
        d = soup.find_all('h2')
        firma = str(d[4])
        firmenname = firma.split(">", 1)
        firmenname = firmenname[1].split("</h2>", 1)
        firmenname = str(firmenname)
        firmenname = firmenname.replace(",", "")
        firmenname = firmenname.replace("'", "")
        firmenname = firmenname.replace("[", "")
        firmenname = firmenname.replace("]", "")
        
    except Exception as e:
        logging.error(traceback.format_exc())
        print('Ebene eins')
        try:
            print('Ebene zwei')
        except Exception as e:
            logging.error(traceback.format_exc())
            try:
                print('Ebene drei')
            except Exception as e:
                logging.error(traceback.format_exc())
                try:
                    print('Ebene vier')
                except Exception as e:
                    logging.error(traceback.format_exc())

    return e_ISIN, firmenname, e_geldkurs, e_briefkurs, e_andvortag, e_tageshoch, e_tagestief, e_umsatz, the_time
    #print(ISIN, Brief_volumen,  Geld_volumen, Briefkurs,Geldkurs , geld_umsatz, spreadie, Zeit )

        #e_ISIN, firmenname, e_geldkurs, e_briefkurs, e_andvortag, e_tageshoch, e_tagestief, e_umsatz, the_time = schnell_kurs('NL0000235190')

        #print(e_ISIN, firmenname, e_geldkurs, e_briefkurs, e_andvortag, e_tageshoch, e_tagestief, e_umsatz, the_time)import pandas as pd





def links():
    #for li in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    #          'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']:

    for link in ['https://www.tradegate.de/indizes.php?index=DE000A1EXRV0', 'https://www.tradegate.de/indizes.php?index=DE000A1EXRW8', 'https://www.tradegate.de/indizes.php?index=DE000A1EXRY4', 'https://www.tradegate.de/indizes.php?index=DE000A1EXRX6', 'https://www.tradegate.de/indizes.php?index=US0000000002']:

    #link = ('https://www.tradegate.de/indizes.php?buchstabe=' + str(li))
        link = (link)
        print(link)
        req = Request(str(link))
        html_page = urlopen(req)

        #soup = BeautifulSoup(html_page, "lxml")
        soup = BeautifulSoup(html_page, "html5lib")

        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))

        print(links)
        links = pd.DataFrame(links)
        print(links)
        linke = links[links[0].str.contains("orderbuch") & links[0].str.contains("DE|US|")].copy()
        # linke = links[links[0].str.contains("orderbuch")].copy()
        print(linke)
        # linke['link'] = 'https://www.tradegate.de/' + linke[0]
        linke['e_ISIN'] = linke[0].str[-12:]
        linke = linke.drop_duplicates(subset=['e_ISIN'])
        print(linke)
        print(len(linke))
        # linke['link'].to_csv('us_aktien.txt', header=False, index=False)

        with open('ISIN_aktien.csv', 'a') as f:
            linke.to_csv(f, header=f.tell() == 0)







def kurslese(pathin, pathout):
    aktien = pd.read_csv(pathin, delimiter = ',')
    keule = aktien.drop_duplicates(subset=['e_ISIN'])
    

    print(len(keule))


    kurse = []
    #batze = pd.read_csv('rahmen.csv')
    liste = list(keule['e_ISIN'])
    print(len(liste))
    for ISIN in liste :


        try:
            #ISIN, Brief_volumen,  Geld_volumen, Briefkurs,Geldkurs , geld_umsatz, spreadie, Zeit = quoten(ISIN)
            #print(ISIN, Brief_volumen,  Geld_volumen, Briefkurs,Geldkurs , geld_umsatz, spreadie, Zeit )
            e_ISIN, firmenname, e_geldkurs, e_briefkurs, e_andvortag, e_tageshoch, e_tagestief, e_umsatz, the_time = schnell_kurs(ISIN)
            #print(e_ISIN, firmenname, e_geldkurs, e_briefkurs, e_andvortag, e_tageshoch, e_tagestief, e_umsatz, the_time)
            #atze = quoten(ISIN)
            #kurse.append(atze)
            atze = schnell_kurs(ISIN)
            kurse.append(atze)

        except Exception as e:
            print('___________', ISIN)
            logging.error(traceback.format_exc())
            print('Ebene eins')
            try:
                print('Ebene zwei')
            except Exception as e:
                logging.error(traceback.format_exc())
                try:
                    print('Ebene drei')
                except Exception as e:
                    logging.error(traceback.format_exc())
                    try:
                        print('Ebene vier')
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        try:
                            print('Ebene fuenf')
                        except Exception as e:
                            logging.error(traceback.format_exc())

    kurse = pd.DataFrame(kurse, columns = ['e_ISIN', 'firmenname', 'e_geldkurs', 'e_briefkurs', 'e_andvortag', 'e_tageshoch', 'e_tagestief', 'e_umsatz', 'the_time'])
    kurse = kurse.sort_values(by = 'e_andvortag', ascending = False).copy()
    kurse.head(400).to_csv(pathout)
    return kurse.head(400)




#Hauptprogramm


links()
slimestr = time.strftime("%H")
print(slimestr)


while int(slimestr) >= 8  and int(slimestr) < 22:
        
        slimestr = time.strftime("%H")
    
        keule = kurslese('ISIN_aktien.csv', 'kursdaten_lemon_tradeble_400.csv')

        #print(keule)
        with open('kursdaten_lemon_'+ timestr +'.csv', 'a') as f:
            keule.to_csv(f, header=f.tell() == 0)

            print(15*'#########')

    #atze = pd.read_csv('kursdaten_lemon.csv')
    #print(atze.columns)

    #atze.drop(['Unnamed: 0'], axis=1, inplace = True)
    #atze.tail(8000).to_csv('atze.csv')
    #print(atze.columns)





