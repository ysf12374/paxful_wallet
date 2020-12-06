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
