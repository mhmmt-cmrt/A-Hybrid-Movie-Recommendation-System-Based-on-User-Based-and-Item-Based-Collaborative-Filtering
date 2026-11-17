#*********************************************************
#Verinin düzenlenmesi ve model için hazırlanması
#*********************************************************

import pandas as pd
import numpy as np
from holoviews.operation import collapse

pd.pandas.set_option('display.max_columns', None)
pd.pandas.set_option('display.width', 500)

filmler = pd.read_csv("C:/Users/Muhammet/PycharmProjects/HybridModel/datasetSmall/movies.csv")
filmler.head()
filmler.shape

puanlar = pd.read_csv("C:/Users/Muhammet/PycharmProjects/HybridModel/datasetSmall/ratings.csv")
puanlar.head()
puanlar.shape
puanlar["userId"].nunique()

#************************#
#veri seti bilgilerini yazar
######################################
egitim = puanlar[['userId', 'movieId', 'rating']]
print('>> {} tane kullanicidan {} satir verisi vardir'.format(len(egitim.userId.unique()),len(puanlar)))
print('>> toplam yapilan puanlama sayisi: ',egitim.shape[0],' dir')
print('>> sahip oldugumuz benzersiz kullanici sayisi:', len(egitim.userId.unique()))
print('>> sahip oldugumuz benzersiz film sayisi:', len(egitim.movieId.unique()))
print('>> maksimum oy degeri: %d'%egitim.rating.max())
print('>> minumum oy degeri: %d' %egitim.rating.min())
######################################

birlesikTablo = filmler.merge(puanlar, how="left", on="movieId")
birlesikTablo.head()
birlesikTablo.shape

# Herbir film için toplam kaç kişinin oy kullanıldığını hesaplıyoruz.
# kalabalığın bilgeliği kavramı üzerine en çok değerlenen filmleri alırız.
# çünkü ne kadar çok yorum varsa değer o kadar genelleştirilebilir.

degerlendirme_sayisi = pd.DataFrame(birlesikTablo["title"].value_counts())
degerlendirme_sayisi.shape

yetersiz_degerlenmis = degerlendirme_sayisi[degerlendirme_sayisi["title"] <= 5]
yetersiz_degerlenmis.shape
yeterli_degerlenmis = birlesikTablo[~birlesikTablo["title"].isin(yetersiz_degerlenmis)]
yeterli_degerlenmis.shape

#biased için(bilgi amaçlı kısım)
#####################################################################
oylama_sayilari = pd.DataFrame(birlesikTablo.groupby('title')['rating'].mean())
oylama_sayilari['toplam oylama'] = pd.DataFrame(birlesikTablo.groupby('title')['rating'].count())
oylama_sayilari.rename(columns={'rating': 'oy ortalamasi'}, inplace=True)

oylama_sayilari.sort_values('toplam oylama', ascending=False).head(50)

#100 den fazla oylanan filmleri inceleyelim
oylama_sayilari_top = oylama_sayilari[oylama_sayilari['toplam oylama'] >= 100]
oylama_sayilari_top = oylama_sayilari_top.sort_values('toplam oylama', ascending=False)
pd.DataFrame(oylama_sayilari_top).count()

#100 den az oylanan filmleri inceleyelim
oylama_sayilari_down = oylama_sayilari[oylama_sayilari['toplam oylama'] < 50]
oylama_sayilari_down = oylama_sayilari_down.sort_values('toplam oylama', ascending=False)
pd.DataFrame(oylama_sayilari_down).count()
#######################################################################33
