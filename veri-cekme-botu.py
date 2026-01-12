import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
url = "https://books.toscrape.com/catalogue/category/books/travel_2/index.html"
base_url = "https://books.toscrape.com/"
if not os.path.exists("resimler"):
    os.makedirs("resimler")
link = requests.get(url)
soup =  BeautifulSoup(link.content,"html.parser")
kitaplar = soup.find_all("article",class_="product_pod")
liste = []
print("işlem başlıyor...")
for kitap in kitaplar:
    isim = kitap.find("h3").find("a")["title"]
    fiyat = kitap.find("p",class_="price_color").text
    temiz_isim = isim.replace(":","-").replace("/","-").replace('"', '').replace("*","")
    resim_linki = kitap.find("img")["src"]
    clean_resim_link = base_url + resim_linki.replace("../../../../", "")
    resim_verisi = requests.get(clean_resim_link).content
    dosya_adi = f"resimler/{temiz_isim}.jpg"
    try:
        with open(dosya_adi, "wb") as f:
            f.write(resim_verisi)
        print(f"İndirildi: {temiz_isim}")
    except Exception as e:
        print(f"HATA OLUŞTU ({isim}): {e}")
    liste.append({
        "kitap adı":isim,
        "fiyat":fiyat,
        "resim linki":dosya_adi
    })
tablo = pd.DataFrame(liste)
tablo.to_excel("kitaplar.xlsx",index=False)
print("\nTamamlandı!")