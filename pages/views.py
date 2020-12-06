from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db import connections
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http.response import JsonResponse

import base64
import io
import sys
import json 
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json
from pandas import read_sql,DataFrame,to_numeric
from django.utils.encoding import smart_str
import os,sys
import secrets
import wave
import sqlite3
from sqlite3 import Error
from time import sleep,time
from datetime import datetime,timedelta
import logging

import hashlib
import base58
import ecdsa
import uuid

from ecdsa.keys import SigningKey
from utilitybelt import dev_random_entropy
from binascii import hexlify, unhexlify

from pages.models import *
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
from cryptography.fernet import Fernet

import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

logger = logging.getLogger(__name__)

def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))


def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))


def random_secret_exponent(curve_order):
    while True:
        random_hex = hexlify(dev_random_entropy(32))
        random_int = int(random_hex, 16)
        if random_int >= 1 and random_int < curve_order:
            return random_int


def generate_private_key():
    curve = ecdsa.curves.SECP256k1
    se = random_secret_exponent(curve.order)
    from_secret_exponent = ecdsa.keys.SigningKey.from_secret_exponent
    return hexlify(from_secret_exponent(se, curve, hashlib.sha256).to_string())

def generate_public_key(private_key_hex):
    hash160 = ripe_hash(private_key_hex)
    public_key_and_version_hex = b"04" + hash160 
    checksum = double_hash(public_key_and_version_hex)[:4]
    return base58.b58encode(public_key_and_version_hex + checksum)

def ripe_hash(key):
    ret = hashlib.new('ripemd160')
    ret.update(hashlib.sha256(key).digest())
    return ret.digest()

def double_hash(key):
    return hashlib.sha256(hashlib.sha256(key).digest()).digest()
def sha256(arg) :
  ''' Return a sha256 hash of a hex string '''
  byte_array = bytearray.fromhex(arg)
  m = hashlib.sha256()
  m.update(byte_array)
  return m.hexdigest()

def b58encode(hex_string) :
  ''' Return a base58 encoded string from hex string '''
  num = int(hex_string, 16)
  encode = ""
  base_count = len(alphabet)
  while (num > 0) :
    num, res = divmod(num,base_count)
    encode = alphabet[res] + encode
  return encode

def b58decode(v):
  ''' Decode a Base58 encoded string as an integer and return a hex string '''
  if not isinstance(v, str):
    v = v.decode('ascii')
  decimal = 0
  for char in v:
    decimal = decimal * 58 + alphabet.index(char)
  return hex(decimal)[2:]
def generate_private_key_wif(private_key_hex):
    private_key_and_version = b"80" + private_key_hex
    private_key_and_version = codecs.decode(private_key_and_version, 'hex')
    checksum = double_hash(private_key_and_version)[:4]
    hashed = private_key_and_version + checksum
    return base58.b58encode(hashed)
def privToWif(priv) :
  ''' Produce a WIF from a private key in the form of an hex string '''
  _priv = priv.lower() 
  priv_add_x80 = "80" + _priv
  first_sha256 = sha256(priv_add_x80)
  seconf_sha256 = sha256(first_sha256)
  first_4_bytes = seconf_sha256[0:8]
  resulting_hex = priv_add_x80 + first_4_bytes
  result_wif = b58encode(resulting_hex)
  return result_wif

def wifToPriv(wif) :
  ''' Produce the private ECDSA key in the form of a hex string from a WIF string ''' 
  if verbose : print("WIF: " + wif)
  byte_str = b58decode(wif)
  byte_str_drop_last_4bytes = byte_str[0:-8]
  byte_str_drop_first_byte = byte_str_drop_last_4bytes[2:]
  return byte_str_drop_first_byte

def hash160(hex_str):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(hex_str)
    rip.update( sha.digest() )
    return rip.hexdigest()  

def address_(public_key_hex):
    key_hash = '00' + hash160(public_key_hex)    
    sha = hashlib.sha256()
    sha.update( bytearray.fromhex(key_hash) )
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]
    return (base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) )).decode('utf-8')


@csrf_exempt
def create(request):
    name=request.GET.get('name', 'NoName')
    email=request.GET.get('email', 'NoEmail')
    if name=='NoName' or email=='NoEmail':
      return JsonResponse({'success':False,
        "error":"Please Enter Name and Email"})
    # try:
    b = Wallet.objects.filter(name=name,
      email=email).order_by('date_created').first()
    try:
      wallet_id=b.wallet_id
    except:
      wallet_id=False
    if wallet_id:
      return JsonResponse({'success':False,
        "error":"Please Enter New Name and Email"})
    wallet_id=str(uuid.uuid4().fields[-1])[:51]
    w = Wallet.objects.create(wallet_id=wallet_id,
          name=name, email=email)
    w.save()

    return JsonResponse({'success':True,
            "wallet_id":wallet_id,
            "name":name, "email":email})
    # except Exception as e:
    #   logger.error(f"[{datetime.now()}] [create] [{name}] [{email}] {e} ")
    #   return JsonResponse({'success':False,
    #       "error":"Internal Server Error, Please contact support"})


@csrf_exempt
def generate(request):
    name=request.GET.get('name', 'NoName')
    email=request.GET.get('email', 'NoEmail')
    if name=='NoName' or email=='NoEmail':
      return JsonResponse({'success':False,
        "error":"Please Enter Name and Email"})
    # try:
    b = Wallet.objects.filter(name=name,
      email=email).order_by('date_created').first()
    try:
      wallet_id=b.wallet_id
    except:
      wallet_id=False
    if not wallet_id:
      return JsonResponse({'success':False,
        "error":"Name and Email doesnt exist"})
    private_key_hex_ = generate_private_key()
    public_key_hex_ = generate_public_key(private_key_hex_)
    private_key_wif_hex_ = privToWif(private_key_hex_.decode())
    private_key_hex = obscure(private_key_hex_)
    public_key_hex = obscure(public_key_hex_)
    private_key_wif_hex = obscure(private_key_wif_hex_.encode())
    address_str=address_(public_key_hex_)
    address_byt=obscure(address_str.encode())
    w_add=Wallet_Address.objects.create(wallet_id=b.wallet_id,
      address=address_byt.decode(),
      date_updated=datetime.now())
    w_add.save()
    b.wallet_address.add(w_add)
    w_keys = Wallet_Keys.objects.create(wallet_id=wallet_id,
          private_key=private_key_hex.decode(),
          public_key=public_key_hex.decode(),
          private_key_wif=private_key_wif_hex.decode(),
          date_updated=datetime.now())
    w_keys.save()
    w_acc=Wallet_Account.objects.create(wallet_id=wallet_id,
          currency='USD')
    w_acc.save()
    b.wallet_account.add(w_acc)
    b.wallet_keys.add(w_keys)
    return JsonResponse({'success':True,
            "wallet_id":wallet_id,
            "name":name, "email":email,
            "private_key":private_key_hex_.decode(),
            "public_key":public_key_hex_.decode(),
            "private_key_wif":private_key_wif_hex_,
            "address":address_str})
    # except Exception as e:
    #   logger.error(f"[{datetime.now()}] [regenerate] [{name}] [{email}] {e} ")
    #   return JsonResponse({'success':False,
    #       "error":"Internal Server Error, Please contact support"})

@csrf_exempt
def api(request):
    private_key_wif_hex_=request.GET.get('private_key_wif', 'NoWif')
    name=request.GET.get('name', 'NoName')
    email=request.GET.get('email', 'NoEmail')
    if name=='NoName' or email=='NoEmail':
      return JsonResponse({'success':False,
        "error":"Please Enter Name and Email"})
    # try:
    a = Wallet.objects.filter(name=name,
      email=email).order_by('date_created').first()
    if private_key_wif_hex_!='NoWif':
      private_key_wif_hex = obscure(private_key_wif_hex_.encode())
      k = Wallet_Keys.objects.filter(
        private_key_wif=private_key_wif_hex.decode()).order_by('date_created').first()
    else:
      return JsonResponse({'success':False,
        "error":"Please Enter WIF "})
    if a.wallet_id!=k.wallet_id:
      return JsonResponse({'success':False,
        "error":"Private Key doesnt match the wallet"})
    api_key_ = secrets.token_urlsafe(96)
    api_key = obscure(api_key_.encode())
    api_pin_ = secrets.token_hex(16)
    api_pin = obscure(api_pin_.encode())
    w = Wallet_API.objects.create(wallet_id=a.wallet_id,
          date_updated=datetime.now(),
          api_key=api_key.decode(),
          api_pin=api_pin.decode())
    w.save()
    a.wallet_api.add(w)
    return JsonResponse({'success':True,
      'API Key':api_key_,
      'API PIN':api_pin_})
    # except Exception as e:
    #   logger.error(f"[{datetime.now()}] [api] [{private_key_wif_hex_}] {e} ")
    #   return JsonResponse({'success':False,
    #       "error":"Internal Server Error, Please contact support"})


@csrf_exempt
def create_address(request):
    api_key_=request.GET.get('API_Key', 'NoKey')
    api_pin_=request.GET.get('API_PIN', 'NoPin')
    # try:
    if (api_key_!='NoKey' and api_pin_!='NoPin' and api_pin_!='NoPublicKey'):
      api_key=obscure(api_key_.encode())
      api_pin=obscure(api_pin_.encode())
      a = Wallet_API.objects.filter(api_key=api_key.decode(),
        api_pin=api_pin.decode()).order_by('date_updated').first()
    else:
      return JsonResponse({'success':False,
        "error":"Please Enter API_Key and API_PIN"})
    wallet=Wallet.objects.filter(wallet_id=a.wallet_id).order_by('date_created').first()
    b = Wallet_Keys.objects.filter(wallet_id=a.wallet_id).order_by('date_created').first()
    public_key_=b.public_key
    address_str=address_(public_key_.encode())
    address_byt=obscure(address_str.encode())
    w=Wallet_Address(wallet_id=a.wallet_id,
      address=address_byt.decode(),
      date_updated=datetime.now())
    w.save()
    wallet.wallet_address.add(w)
    return JsonResponse({'success':True,
      'address':address_str})
    # except Exception as e:
    #   logger.error(f"[{datetime.now()}] [api] [{api_key_}] [{api_pin_}] {e} ")
    #   return JsonResponse({'success':False,
    #       "error":"Internal Server Error, Please contact support"})

@csrf_exempt
def create_session(request):
    api_key=request.GET.get('API_Key', 'NoKey')
    api_pin=request.GET.get('API_PIN', 'NoPin')
    now = datetime.now()
    now_plus_10 = now + timedelta(minutes = 10)
    if (api_key_!='NoKey' and api_pin_!='NoPin' and api_pin_!='NoPublicKey'):
      api_key_binary = "{:08b}".format(int(api_key.encode('utf-8').hex(),16))
      api_pin_binary = "{:08b}".format(int(api_pin.encode('utf-8').hex(),16))
      a = Wallet_API.objects.filter(api_key=api_key_binary.encode(),
        api_pin=api_pin_binary.encode()).order_by('date_updated').first()
    else:
      return JsonResponse({'success':False,
        "error":"Please Enter API_Key and API_PIN"})
    session_id = secrets.token_hex(16)
    w=Wallet_Sessions(wallet_id=a.wallet_id,
      expiry=now_plus_10,
      session_id=session_id)
    w.save()
    return JsonResponse({'success':True,
      'session_id':session_id})


@csrf_exempt
def transfer_funds(request,amount):
    api_pin_=request.GET.get('API_PIN', 'NoPin')
    to_address_=request.GET.get('Recepient_Address', 'NoAddress')
    pub_key_=request.GET.get('Public_Key', 'NoPublicKey')
    try:
      api_pin=obscure(api_pin_.encode())
      to_address=obscure(to_address_.encode())
      pub_key=obscure(pub_key_.encode())
      if (api_pin_!='NoPin' and pub_key_!='NoPublicKey'):

        f = Wallet_API.objects.filter(
          api_pin=api_pin.decode()).order_by('date_updated').first()
        try:
          wallet_id1=f.wallet_id
        except:
          wallet_id1=False
        if not wallet_id1:
          return JsonResponse({'success':False,
            "error":"Invalid PIN"})
        f = Wallet_Keys.objects.filter(
          public_key=pub_key.decode()).order_by('date_updated').first()
        try:
          wallet_id2=f.wallet_id
        except:
          wallet_id2=False
        if not wallet_id2:
          return JsonResponse({'success':False,
            "error":"Invalid Public Key"})
        if wallet_id1!=wallet_id2:
          return JsonResponse({'success':False,
            "error":"Public Key and PIN doesnt match"})
      elif pub_key_!='NoPublicKey':
        return JsonResponse({'success':False,
          "error":"Please Enter Public_Key"})
      elif to_address_=='NoAddress':
        return JsonResponse({'success':False,
          "error":"Please Enter Recepient_Address"})
      else:
        return JsonResponse({'success':False,
          "error":"Please Enter API_PIN"})

      t_deet=Wallet_Address.objects.filter(address=to_address.decode()).order_by('date_updated').first()
      try:
        wallet_id3=t_deet.wallet_id
      except:
        wallet_id3=False
      if not wallet_id3:
        return JsonResponse({'success':False,
          "error":"Invalid Recepient_Address"})
      if t_deet.wallet_id==f.wallet_id:
        return JsonResponse({'success':False,
          "error":"Cannot Send to Self"})

      w=Wallet_Account.objects.filter(wallet_id=f.wallet_id).order_by('date_updated').first()
      if float(w.amount)<=0:
        return JsonResponse({'success':False,
          "error":"Not Enough Funds"})
      w.amount = float(w.amount)-float(amount)
      
      t=Wallet_Account.objects.filter(wallet_id=t_deet.wallet_id).order_by('date_updated').first()
      t.amount = float(t.amount)+(float(amount)-(0.015*float(amount)))
      
      c=Wallet.objects.filter(name="Company",
        email="company@company.com").order_by('date_created').first()
      c_=Wallet_Account.objects.filter(wallet=c).order_by('date_updated').first()
      c_.amount = float(c_.amount)+(0.015*float(amount))

      w.save(update_fields=['amount'])
      t.save(update_fields=['amount'])
      c_.save(update_fields=['amount'])

      transaction_id = secrets.token_hex(16)

      w = Wallet_Transactions.objects.create(wallet_id_from=f.wallet_id,
            wallet_id_to=t_deet.wallet_id,
            transaction_id=transaction_id, transaction_amount=float(amount),
            transaction_currency='USD',
            commission=0.015*float(amount))
      return JsonResponse({'success':True,
        'to':t_deet.wallet_id,
        'from':f.wallet_id,
        'sent':(float(amount)-(0.015*float(amount)))})
    except Exception as e:
      logger.error(f"[{datetime.now()}] [transfer_funds] [{api_key_}] [{api_pin_}] [{to_address_}] {e} ")
      return JsonResponse({'success':False,
          "error":"Internal Server Error, Please contact support"})


@csrf_exempt
def details_long(request):
    name=request.GET.get('name', 'NoName')
    email=request.GET.get('email', 'NoEmail')
    
    if name=='NoName' or email=='NoEmail':
      return JsonResponse({'success':False,
        "error":"Please Enter Name and Email"})
    try:
      w=Wallet.objects.filter(name=name,
        email=email).order_by('date_created').first()

      t=Wallet_Address.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()

      a=Wallet_Account.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()

      api=Wallet_API.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()
      return JsonResponse({'success':True,
              "wallet_id":w.wallet_id,
              "name":w.name, "email":w.email,
              "private_key":unobscure((w.private_key).encode()).decode(),
              "public_key":unobscure((w.public_key).encode()).decode(),
              "private_key_wif":unobscure((w.private_key_wif).encode()).decode(),
              "address":unobscure((t.address).encode()).decode(),
              "API Key":unobscure((api.api_key).encode()).decode(),
              "API PIN":unobscure((api.api_pin).encode()).decode(),
              "amount":a.amount
              })      
    except:
      return JsonResponse({'success':False,
        'Error':'Run /api endpoint to generate API KEY and PIN'})

@csrf_exempt
def details_short(request):
    name=request.GET.get('name', 'NoName')
    email=request.GET.get('email', 'NoEmail')
    
    if name=='NoName' or email=='NoEmail':
      return JsonResponse({'success':False,
        "error":"Please Enter Name and Email"})
    # try:
    w=Wallet.objects.filter(name=name,
      email=email).order_by('date_created').first()
    a=Wallet_Account.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()
    k=Wallet_Keys.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()
    ad=Wallet_Address.objects.filter(wallet_id=w.wallet_id).order_by('date_updated').first()
    private_key_=k.private_key
    private_key=unobscure(private_key_.encode())
    public_key_=k.public_key
    public_key=unobscure(public_key_.encode())
    private_key_wif_=k.private_key_wif
    private_key_wif=unobscure(private_key_wif_.encode())
    address_=ad.address
    address=unobscure(address_.encode())
    return JsonResponse({'success':True,
            "wallet_id":w.wallet_id,
            "name":w.name, "email":w.email,
            "private_key":private_key.decode(),
            "public_key":public_key.decode(),
            "private_key_wif":private_key_wif.decode(),
            "address":address.decode(),
            "amount":a.amount
            })    
    # except Exception as e:
    #   logger.error(f"[{datetime.now()}] [details_short] [{name}] [{email}] {e} ")
    #   return JsonResponse({'success':False,
    #       "error":"Internal Server Error, Please contact support"})















