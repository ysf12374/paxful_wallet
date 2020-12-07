# Paxful Test

This is a project to transfer funds between wallets using Django REST framework.

A wallet consists of the following:
  - wallet_id: a unique id for wallet
  - name: Name of the wallet holder
  - email: email of the wallet holder
  - private_key:  a 256-bit number for wallet
  - public_key: a unique id for wallet
  - private_key_wif: Base58 Wallet Import format
  - address: identifier of 26-35 alphanumeric characters, beginning with the number 1 , 3 or bc1 

```json
{
    "success": true,
    "wallet_id": "219058582399425",
    "name": "Mark Henry",
    "email": "mark@henry.com",
    "private_key": "e21fd13fad152c34ea8d05e765f1634462257fce05ac6b882f120736b6723af4",
    "public_key": "2UcifxLWA53cHLnYbQbfPrJLH8KkNuuUK9SR",
    "private_key_wif": "5KXsd5ktydxsCfknkf5Qq4dWdYhEPzu3HMcAL5Ec7hjk7PNjSV5",
    "address": "1EdRjzGk8AWAb6xMYZGBM9GCPqAu6eZqbY"
}
```
# Database Schema
![alt text](https://github.com/ysf12374/paxful_wallet/blob/main/database_model.png?raw=true)

# API Queries
#### - /api/v1/wallet/create
```http
GET /api/v1/wallet/create
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Your Name |
| `email` | `string` | **Required**. The Email. |
    Call this endpoint to create a new wallet
##### Responses

```json
{
"success":False,
"error":"Please Enter Name and Email"
}
```
```json
{
"success":False,
"error":"Please Enter New Name and Email - [Already Exists]"
}
```
```json
{
"success":True,
"wallet_id":"wallet_id",
"name":"name", "email":"email"
}
```
#### - /api/v1/wallet/generate
```http
GET /api/v1/wallet/generate
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Your Name |
| `email` | `string` | **Required**. The Email. |
    Call this endpoint to generatae the keys
##### Responses

```json
{
"success":False,
"error":"Please Enter Name and Email"
}
```
```json
{
"success":False,
"error":"Name and Email doesnt exist"
}
```
```json
{
    "success": true,
    "wallet_id": "219058582399425",
    "name": "Mark Henry",
    "email": "mark@henry.com",
    "private_key": "e21fd13fad152c34ea8d05e765f1634462257fce05ac6b882f120736b6723af4",
    "public_key": "2UcifxLWA53cHLnYbQbfPrJLH8KkNuuUK9SR",
    "private_key_wif": "5KXsd5ktydxsCfknkf5Qq4dWdYhEPzu3HMcAL5Ec7hjk7PNjSV5",
    "address": "1EdRjzGk8AWAb6xMYZGBM9GCPqAu6eZqbY"
}
```

#### - /api/v1/wallet/api
```http
GET /api/v1/wallet/api
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `private_key_wif` | `string` | **Required**. Your Wallet Private key (WIF) |
| `name` | `string` | **Required**. Your Name |
| `email` | `string` | **Required**. The Email. |
    Call this endpoint to generatae the API Key and PIN
##### Responses

```json
{
"success":False,
"error":"Please Enter Name and Email"
}
```
```json
{
"success":False,
"error":"Private Key doesnt match the wallet"
}
```
```json
{"success":True,
"API Key":"ZxIvghm4nSdeXuJp8C-A8twrAvDCYxLoeSo3IkM4uUn0I6sXBrSThi4oHkS0Bcc_AG1pTHYvoEI3iW_dfikxm4olemgVYagHvYtC2rkMT4AUDu8d66a___XpINmPRwox",
"API PIN":"cac3347f414a60f54df4a731087d2c62"
}
```

#### - /api/v1/wallet/transfer_funds/{amount}
```http
GET /api/v1/wallet/transfer_funds/{amount}
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `API_PIN` | `string` | **Required**. Your Wallet API key |
| `Public_Key` | `string` | **Required**. Your Wallet Public Key |
| `Recepient_Address` | `string` | **Required**. The Wallet address of the Recepient. |
    Call this endpoint to Transfer funds between wallets.
##### Responses

```json
{
"success":False,
"error":"Invalid PIN"
}
```
```json
{
"success":False,
"error":"Invalid Public Key"
}
```
```json
{
"success":False,
"error":"Public Key and PIN doesnt match"
}
```
```json
{
"success":False,
"error":"Please Enter Public_Key"
}
```
```json
{
"success":False,
"error":"Please Enter Recepient_Address"
}
```
```json
{
"success":False,
"error":"Please Enter API_PIN"
}
```
```json
{
"success":False,
"error":"Invalid Recepient_Address"
}
```
```json
{
"success":False,
"error":"Cannot Send to Self"
}
```
```json
{
"success":False,
"error":"Not Enough Funds"
}
```
```json
{"success":True,
'to':34249417035203,
'from':34249417012345,
'sent':19.7
}
```

#### - /api/v1/wallet/details_long
```http
GET /api/v1/wallet/details_long
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Your Name |
| `email` | `string` | **Required**. The Email. |
    Call this endpoint to get your wallet details
##### Responses

```json
{
"success":False,
"error":"Please Enter Name and Email"
}
```

```json
{"success":True,
"wallet_id": "219058582399425",
"name": "Mark Henry",
"email": "mark@henry.com",
"private_key": "e21fd13fad152c34ea8d05e765f1634462257fce05ac6b882f120736b6723af4",
"public_key": "2UcifxLWA53cHLnYbQbfPrJLH8KkNuuUK9SR",
"private_key_wif": "5KXsd5ktydxsCfknkf5Qq4dWdYhEPzu3HMcAL5Ec7hjk7PNjSV5",
"address": "1EdRjzGk8AWAb6xMYZGBM9GCPqAu6eZqbY"
"API Key":"ZxIvghm4nSdeXuJp8C-A8twrAvDCYxLoeSo3IkM4uUn0I6sXBrSThi4oHkS0Bcc_AG1pTHYvoEI3iW_dfikxm4olemgVYagHvYtC2rkMT4AUDu8d66a___XpINmPRwox",
"API PIN":"cac3347f414a60f54df4a731087d2c62,
"amount":100
}
```


#### - /api/v1/wallet/details_short
```http
GET /api/v1/wallet/details_short
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | **Required**. Your Name |
| `email` | `string` | **Required**. The Email. |
    Call this endpoint to get your wallet details
##### Responses

```json
{
"success":False,
"error":"Please Enter Name and Email"
}
```

```json
{"success":True,
"wallet_id": "219058582399425",
"name": "Mark Henry",
"email": "mark@henry.com",
"private_key": "e21fd13fad152c34ea8d05e765f1634462257fce05ac6b882f120736b6723af4",
"public_key": "2UcifxLWA53cHLnYbQbfPrJLH8KkNuuUK9SR",
"private_key_wif": "5KXsd5ktydxsCfknkf5Qq4dWdYhEPzu3HMcAL5Ec7hjk7PNjSV5",
"address": "1EdRjzGk8AWAb6xMYZGBM9GCPqAu6eZqbY"
"amount":100
}
```




## Status Codes

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |



### Installation 

Install and run with docker and docker-compose->

```sh
$ docker-compose run web python manage.py makemigrations pages
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py loaddata ./wallet/fixture/data.json
$ sudo docker-compose up
```

Run directly through terminal->

```sh
$ pip install virtualenv
$ virtualenv env
$ source ./env/bin/activate
$ pip intall -r requirements.txt
$ python manage.py makemigrations pages
$ python manage.py migrate
$ python manage.py loaddata ./wallet/fixture/data.json
$ python manage.py runserver 127.0.0.1:8000
```
