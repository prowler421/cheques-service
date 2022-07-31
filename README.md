# Cheques Service - Kafka-based

### How to run the project:

1. Clone this seed repository.
2. Clone https://github.com/confluentinc/cp-all-in-one and execute docker-compose.yml of cp-all-in-one-community
3. Execute dev_main
---

### Endpoints

#### Cheques Service

|HTTP Method|URL|Description|
|---|---|---|
|`GET`|http://localhost:8004/accounts | Get all banks accounts |
|`GET`|http://localhost:8004/accounts/{bank_id}}/ | Get all bank accounts |
|`GET`|http://localhost:8004/{bank_id}/accounts/{account_id} | Get account details |
|`POST`|http://localhost:8004/accounts/{bank_id}/{account_id} | Create new cheque deposition |

Example:

`curl --location --request POST 'http://localhost:8004/cheque-deposit/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "payee_bank_id": 23,
    "drawee_bank_id": 13,
    "drawee_id": "5d90bd70-a5f1-4d5b-b54a-4c5ebbab7d39",
    "payee_id": "7813e6c6-d462-4cbf-be5b-fb91dd72b6f9",
    "chk_amount": 25000`

#### Data Flow

Each instance represents a different bank - each and every bank subscribes itself to 3 topics
- clearinghouse - upon new cheque deposition arrival, the payee bank pushes new message to clearinghouse, asking the drawee bank (i.e. the consumer) to pull the message and validate the cheque   
- stale - once cheque has been validated and approved, the drawee bank pushes new message of stale cheque for the payee bank to consume later
- postdated - if the cheque has turned out to be invalid, the drawee bank pushes new message of postdated cheque for the payee bank to consume later

Current implementation produces for each and every bank the required topics