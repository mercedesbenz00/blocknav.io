{% filter markdown %}
## `wallet` module

An instance of the `Wallet` class needs to be initialized before it can be used.

Constructor params:
```
identifier : str
password : str
service_url : str - URL to an instance of service-my-wallet-v3 (with trailing slash)
second_password : str (optional)
api_code : str (optional)
```

Usage:
```python
from blockchain.wallet import Wallet

wallet = Wallet('ada4e4b6-3c9f-11e4-baad-164230d1df67', 'password123', 'http://localhost:3000/')
```

#### `send`
Send bitcoin from your wallet to a single address. Returns a `PaymentResponse` object.

Params:
```
to : str - receiving address
amount : int - amount to send (in satoshi)
from_address : str - specific address to send from (optional)
fee : int - transaction fee in satoshi. Must be greater than default (optional)
note : str - public note to include with the transaction if amount >= 0.005 BTC (optional)
```

Usage:
```python
payment = wallet.send('1NAF7GbdyRg3miHNrw2bGxrd63tfMEmJob', 1000000, from_address='1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq')

print payment.tx_hash
```

#### `send_many`
Send bitcoin from your wallet to multiple addresses. Returns a `PaymentResponse` object.

Params:
```
recipients : dictionary - dictionary with the structure of 'address':amount
from_address : str - specific address to send from (optional)
fee : int - transaction fee in satoshi. Must be greater than default (optional)
note : str - public note to include with the transaction if amount >= 0.005 BTC (optional)
```

Usage:
```python
recipients = { '1NAF7GbdyRg3miHNrw2bGxrd63tfMEmJob' : 1428300,
				'1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq' : 234522117 }
payment = wallet.send_many(recipients)

print payment.tx_hash
```

#### `get_balance`
Fetch the wallet balance. Includes unconfirmed transactions and possibly double spends. Returns the wallet balance in satoshi.

Usage:
```python
print wallet.get_balance()
```

#### `list_addresses`
List all active addresses in the wallet. Returns an array of `Address` objects.

Params:
```
confirmations : int - minimum number of confirmations transactions must have before being included in balance of addresses (optional)
```

Usage:
```python
addresses = wallet.list_addresses()
for a in addresses:
	print a.balance

```

#### `get_address`
Retrieve an address from the wallet. Returns an `Address` object.

Params:
```
confirmations : int - minimum number of confirmations transactions must have before being included in the balance (optional)
```

Usage:
```python
addr = wallet.get_address('1NAF7GbdyRg3miHNrw2bGxrd63tfMEmJob', confirmations = 2)
print addr.balance
```

#### `new_address`
Generate a new address and add it to the wallet. Returns an `Address` object.

Params:
```
label : str - label to attach to the address (optional)
```

Usage:
```python
newaddr = wallet.new_address('test_label')
```

#### `archive_address`
Archive an address. Returns a string representation of the archived address.

Params:
```
address : str - address to archive
```

Usage:
```python
wallet.archive_address('1NAF7GbdyRg3miHNrw2bGxrd63tfMEmJob')
```

#### `unarchive_address`
Unarchive an address. Returns a string representation of the unarchived address.

Params:
```
address : str - address to unarchive
```

Usage:
```python
wallet.unarchive_address('1NAF7GbdyRg3miHNrw2bGxrd63tfMEmJob')
```

### Response object field definitions

#### `PaymentResponse`

```
message : str
tx_hash : str
notice : str
```

#### `Address`

```
balance : long
address : str
label : str
total_received : long
```

{% endfilter %}