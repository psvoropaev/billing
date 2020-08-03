# Billing

## Описание
Billing


### API
1. Список пользователей
curl --location --request GET '127.0.0.1:5000/v1/users' \
--header 'Content-Type: application/json' '

2. Создать пользователя и привязать кошелек в валюте
curl --location --request POST '127.0.0.1:5000/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "User 2",
    "pasport_data": "2",
    "currency_code": "USD"
}'

3. Перевести средства со счета на счет
curl --location --request POST '127.0.0.1:5000/v1/wallets/transfer' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bill_number_sender": "d72db7b7-ede3-4831-aef7-cbdff67475ac",
    "amount": 10,
    "bill_number": "d72db7b7-ede3-4831-aef7-cbdff67475ac"
}'

4. Зачислить средства
curl --location --request POST '127.0.0.1:5000/v1/wallets/topUp' \
--header 'Content-Type: application/json' \
--data-raw '{
    "amount": 10,
    "bill_number": "d72db7b7-ede3-4831-aef7-cbdff67475ac"
}'