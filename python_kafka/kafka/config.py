schema_str = """
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "Cheque",
      "description": "A Confluent Kafka Python Cheque",
      "type": "object",
      "properties": {
        "chk_id": {
          "description": "Cheque's id",
          "type": "string"
        },
        "payee_bank_id": {
          "description": "The issuer bank",
          "type": "number"
        },
        "drawee_bank_id": {
          "description": "Issued bank",
          "type": "number"
        },
        "payee_id": {
          "description": "Issuer account's id",
          "type": "string"
        },
        "drawee_id": {
          "description": "Issued account's id",
          "type": "string"
        },
        "date": {
          "description": "Timestamp",
          "type": "string"
        },
        "chk_amount": {
          "description": "Cheque's amount",
          "type": "number"
        }
      },
      "required": [ "chk_id", "payee_bank_id", "drawee_bank_id", "payee_id", "date", "chk_amount" ]
    }
    """


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))