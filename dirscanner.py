import socket
import sys
import requests

url = input("Url'i Girin: ")
url = url.replace(" ", "").split(":") # url'ı : işareti ile ayırır 
webAddr = url[1].split("/")

zamanAsımı = 10 #saniye başına bağlantı sayısı (saniye başına dizin tarama)
portNumarası = 0

if url[0] == "http": #http veya https protokolüne göre port numarası atanır
    portNumarası = 80
elif url[0] == "https":
    portNumarası = 443

serverIP = socket.gethostbyname(webAddr[2]) #IP adresini çözümler
print("Hedef IP=", serverIP)

try:
    baglan = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    baglan.settimeout(zamanAsımı)
    serverDurum = baglan.connect_ex((serverIP, portNumarası))

    if serverDurum == 0:
        kelimeListesi = input("Dizin taramak için kelime listesinin dosya yolunu belirtiniz= ")
        print("Tarama başlatılıyor...")
        dosya = open(kelimeListesi, "r", encoding="ISO-8859-1")
        dosyaIcerigi = dosya.readlines()
    else:
        print("Hedef host kapalı, tarama başlayamadı :(")
        sys.exit()
    baglan.close()

    for kelime in dosyaIcerigi:
        if portNumarası == 443:
            dizin = "https://" + webAddr[2] +"/"+ kelime
        elif portNumarası == 80:
            dizin = "http://" + webAddr[2] +"/"+ kelime

        istek = requests.get(dizin)
        responseCode = str(istek.status_code)
        if responseCode == "200":
            print(responseCode+ " =", dizin)

except Exception as hata:
    print("Hata:", hata)