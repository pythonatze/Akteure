
#finally

import time
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
import smtplib
import ssl
from email.message import EmailMessage
timestr = time.strftime("%Y%m%d")
print (timestr)

def aktuelle_daten(minuten):
    
    aktuell = pd.Timestamp.now()  
    vor_minuten = aktuell  - timedelta(minutes=minuten)
    print(vor_minuten, 'letzte ' + str(minuten) + ' minuten')
    keule = pd.read_csv('kursdaten_lemon_'+ timestr +'.csv')
    keule = keule.set_index('the_time')
    keule = keule.loc[keule.index > str(vor_minuten)]

    return keule

def tages_daten(ISIN):
    
    aktuell = pd.Timestamp.now()
    
  
    tages = pd.read_csv('kursdaten_lemon_'+ timestr +'.csv')
    tages = tages.set_index('the_time')
    tages = tages.loc[tages['e_ISIN'] == ISIN]
    
    return tages

def corle(ISIN_liste):
    corle = pd.DataFrame()
    
    
    for ease in ISIN_liste:
        
        aktuell = pd.Timestamp.now()
        #print(ease)
        
        tages = pd.read_csv('kursdaten_lemon_'+ timestr +'.csv')
        tages = tages.reset_index()
        tages['the_time'] = pd.to_datetime(tages['the_time'])
        
        tages = tages.set_index('the_time')
        tages = tages.loc[tages['e_ISIN'] == ease]
        tages = tages.resample('5Min').mean().dropna()
        corle[ease] = tages.e_geldkurs
    return corle.corr(method ='pearson').mean().mean()


def kauf_note (df, corrwert):


    email_sender = 'mavaball@gmail.com'
    email_password = ''
    email_receiver = 'mavaball@posteo.de'


    subject = 'Kaufsignale'
 
    body = str(df) + '    ' + '      Korrelation: '    +  str(round(corrwert,2))
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
def looper (rück):
    keule = aktuelle_daten(rück)

    signale = []
    
                        
    for ease in keule['e_ISIN'].unique() :

        rahmen = keule.loc[keule['e_ISIN'] == ease].tail(6)
        #print(rahmen)

        proze = rahmen.e_geldkurs.pct_change(3)*100
        #print(proze)
        letzte = rahmen.e_geldkurs.pct_change()*100
        #print(letzte)
        umse = rahmen.e_umsatz.pct_change()*100
        
        print(umse)

        echt = rahmen.e_briefkurs[-1]
        wert = proze[-1]
        letzter = letzte[-1]
        umser = umse[-1]

        vortag = rahmen.e_andvortag[-1] * 100
        spread = (rahmen.e_briefkurs[-1] - rahmen.e_geldkurs[-1])/rahmen.e_briefkurs[-1]*100
        #print('Vortag' , round(vortag,2))
        firmenname = rahmen.firmenname[-1]
        #day = tages_daten(ease)
        

        if proze[-1] > 0.4 and letzte[-1] > 0.1 and umse[-1] > 0:
            print (ease, wert, letzter, vortag, umser)
            sig = [pd.Timestamp.now(),firmenname[:8], ease, round(wert,2), round(letzter,2), round(vortag,2), round(spread,2) , round(echt,2), round(echt*1.004,2)]
            signale.append(sig)


    signale = pd.DataFrame(signale, columns = ['Zeit', 'Firma', 'ISIN', 'Steigprozent', 'Letzter', 'Vortag', 'Spread', 'Kurs', 'Verkaufen'])
    signale = signale.sort_values(by=['Steigprozent'], ascending=False)
    correlation = corle(signale['ISIN'].unique())
    print('Korrelation aller Werte:', correlation)
    with open('kaufsignale.csv', 'a') as f:
        signale.to_csv(f, header=f.tell() == 0)
    print(pd.Timestamp.now(), len(signale)*'&&&&&&&&&&&&&' )

    #if not signale.empty:
    #   kauf_note(signale, correlation)





zurück = 20

slimestr = time.strftime("%H")

    

while int(slimestr) < 22:
    
    slimestr = time.strftime("%H")
    looper(zurück)
    zeit = int(60 * zurück / 4)
    for sek in range(1,zeit):
        time.sleep(1)
        print('Aktualisierung in', zeit-sek, 'Sekunden')




