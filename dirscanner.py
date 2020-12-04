# -*- coding: UTF-8 -*-
#!/usr/bin/python
import socket
import sys
import requests
import argparse

parametre = argparse.ArgumentParser()
parametre.add_argument('-u', help="Taramak istediğin URL'i ver!")
parametre.add_argument('-w', help="Kelime listesinin(wordlist) yolunu ver!")
parametre.parse_args()
url = sys.argv[2].replace(" ", "").split(":") # url'ı : işareti ile ayırır 
webAddr = url[1].split("/")

zamanAsimi = 10 #saniye başına bağlantı sayısı (saniye başına dizin tarama)
portNumarasi = 0
if "https" in url[0]: #https veya http protokolüne göre port numarası atanır
    portNumarasi = 443
elif "http" in url[0]:
    portNumarasi = 80

serverIP = socket.gethostbyname(webAddr[2]) #IP adresini çözümler
print("Hedef IP=", serverIP)

try:
    baglan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    baglan.settimeout(zamanAsimi)
    serverDurum = baglan.connect_ex((serverIP, portNumarasi))

    if serverDurum == 0:
        print(webAddr[2])
    else:
        print("Hedef host kapalı, tarama başlayamadı :(")
        sys.exit()
    baglan.close()

    print("Tarama başlatılıyor...")
    dosya = open(sys.argv[4], "r", encoding="ISO-8859-1")
    dosyaIcerigi = dosya.readlines()

    for kelime in dosyaIcerigi:
        if portNumarasi == 443:
            dizin = "https://" + webAddr[2] +"/"+ kelime
        elif portNumarasi == 80:
            dizin = "http://" + webAddr[2] +"/"+ kelime
        istek = requests.get(dizin)
        responseCode = str(istek.status_code)
        if responseCode == "200":
            print(responseCode+ "= ", dizin )

except Exception as Hata:
    print("Hata", Hata)
