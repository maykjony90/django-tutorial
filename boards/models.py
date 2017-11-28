from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import Truncator


# ABSTRACT:
# BURADA MODUL'LER VAR. HER BIRI BIR OBJENIN 'BLUE PRINT'I
# YENI BIR OBJE OLUSTURMAK ISTENDIGINDE BU CLASS'I CAGIRARAK
# OBJEYE YAPACAGIMIZ ATIFLARI HER SEFERINDE BASTAN GIRMEK
# ZORUNDA KALMIYORUZ.
class Board(models.Model):
	# BU CLASS'IN IKI TANE DEGISKENI VAR
	# IKISI DE KARAKTER ALANINI TEMSIL EDIYOR.
	# 'NAME' DEGISKENININ OZELLIKLERI:
	# 1. EN FAZLA 30 KARAKTER UZUNLUGUNDA OLABILIE
	# 2. AYNI ISIMLI YALNIZCA BIR OBJE BULUNABILIR
	# 'DESCRIPTION' DEGISKENININ OZELLIKLERI:
	# 1. EN FAZLA 100 KARAKTER UZUNLUGUNDA OLABILIR
	name = models.CharField(max_length=30, unique=True)
	description = models.CharField(max_length=100)

	# BOARD'LAR CAGIRILDIGINDA BOARD'LARIN 'NAME' ATIFLARINI
	# DEGERLERIYLE BIRLIKTE CAGIRMAK ICIN.
	def __str__(self):
		return self.name


	def get_posts_count(self):
		return Post.objects.filter(topic__board=self).count()


	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()



class Topic(models.Model):
	subject = models.CharField(max_length=255)
	# UZERINDE ISLEM YAPILDIGI ZAMANI OTOMATIK OLARAK KAYDET
	last_updated = models.DateTimeField(auto_now_add=True)
	# 'STARTER' DEGISKENI YALNIZCA 'USER' KISISI ILE BAGLANTILI OLABILIR
	# USER KISISI BUTUN TOPICS'LERI GOREBILIR DATABASE'DEN CAGIRABILIR
	board = models.ForeignKey(Board, related_name='topics')
	starter = models.ForeignKey(User, related_name='topics')
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.subject


class Post(models.Model):
	# METIN ALANI OLUSTUR VE UZUNLUGU 4000 OLSUN
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic, related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	# 'UPDATED_AT' BASTA DEGER ALMIYOR.
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User, related_name='posts')
	# 'UPDATED_BY' DEGISKENININ USER'I RELATED_NAME OZELLIGINI BULUNDURMASA DA OLUR
	updated_by = models.ForeignKey(User, null=True, related_name='+')

	def __str__(self):
		truncated_message = Truncator(self.message)
		return truncated_message.chars(30)