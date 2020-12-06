from __future__ import unicode_literals
from django.db import models
from datetime import datetime


class Wallet_Keys(models.Model):
	wallet_id = models.CharField('Wallet ID', max_length=120)
	# wallet = models.ManyToManyField('Wallet')
	# wallet=models.ForeignKey(to=Wallet, on_delete=models.CASCADE,primary_key=True)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	date_updated = models.DateTimeField('Date Updated',default=datetime.now)
	private_key = models.CharField(max_length=120)
	public_key = models.CharField(max_length=120)
	private_key_wif = models.CharField(max_length=120)
	


class Wallet_Address(models.Model):
	wallet_id = models.CharField('Wallet ID', max_length=120)
	# wallet=models.ForeignKey(to=Wallet, on_delete=models.CASCADE,primary_key=True)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	date_updated = models.DateTimeField('Date Updated')
	address = models.CharField(max_length=120)

class Wallet_API(models.Model):
	wallet_id = models.CharField('Wallet ID', max_length=120)
	# wallet = models.ManyToManyField(Wallet)
	# wallet=models.ForeignKey(to=Wallet, on_delete=models.CASCADE,primary_key=True)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	date_updated = models.DateTimeField('Date Updated',default=datetime.now)
	api_key = models.CharField(max_length=120)
	api_pin = models.CharField(max_length=120)


class Wallet_Transactions(models.Model):
	wallet_id_from = models.CharField('Wallet ID', max_length=120)
	# wallet=models.ForeignKey(to=Wallet, on_delete=models.CASCADE,primary_key=True)
	# wallet = models.ManyToManyField(Wallet)
	wallet_id_to = models.CharField('Wallet ID', max_length=120,default=None)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	date_updated = models.DateTimeField('Date Updated',default=datetime.now)
	transaction_id = models.CharField(max_length=120)
	transaction_amount = models.FloatField()
	transaction_currency = models.CharField(max_length=20)
	commission_rate = models.FloatField(default=1.5)
	commission = models.FloatField()


# class Wallet_Sessions(models.Model):
# 	wallet_id = models.CharField('Wallet ID', max_length=120)
# 	date_created = models.DateTimeField('Date Created',default=datetime.now)
# 	expiry = models.DateTimeField('Date Updated')
# 	transaction_remaining = models.IntegerField(default=10)
# 	session_id = models.CharField(max_length=120)


class Wallet_Account(models.Model):
	wallet_id = models.CharField('Wallet ID', max_length=120)
	# wallet=models.ForeignKey(to=Wallet, on_delete=models.CASCADE,primary_key=True)
	# wallet = models.ManyToManyField(Wallet)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	date_updated = models.DateTimeField('Date Updated',default=datetime.now)
	amount = models.FloatField(default=100.0)
	currency = models.CharField(max_length=160)




class Wallet(models.Model):
	wallet_id = models.CharField('Wallet ID', max_length=120)
	name = models.CharField('Name', max_length=120)
	date_created = models.DateTimeField('Date Created',default=datetime.now)
	email = models.CharField(max_length=120)
	wallet_keys = models.ManyToManyField(Wallet_Keys)
	wallet_api = models.ManyToManyField(Wallet_API)
	wallet_account = models.ManyToManyField(Wallet_Account)
	wallet_address = models.ManyToManyField(Wallet_Address)
