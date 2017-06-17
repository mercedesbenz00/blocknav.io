{% filter markdown %}
## `createwallet` module

#### `create_wallet`
Create a new Blockchain.info wallet. It can be created containing a pre-generated private key or will otherwise generate a new private key. Returns a `CreateWalletResponse` instance.

Params:
```
password : str - password for the new wallet. At least 10 characters.
api_code : str - API code with the create wallets permission
service_url: str - URL to an instance of service-my-wallet-v3 (with trailing slash)
priv : str - private key to add to the wallet (optional)
label : str - label for the first address in the wallet (optional)
email : str - email to associate with the new wallet (optional)
```

Usage:
```python
from blockchain import createwallet

wallet = createwallet.create_wallet('1234password', '58ck39ajuiw', 'http://localhost:3000/', label = 'Test wallet')
```


### Response object field definitions

#### `CreateWalletResponse`

```
identifier : str
address : str
label : str
```

{% endfilter %}