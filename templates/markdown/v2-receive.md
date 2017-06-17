{% filter markdown %}
## `v2.receive` module

#### `receive`
Call the 'api.blockchain.info/v2/receive' endpoint and create a forwarding address. Returns a `ReceiveResponse` object.

Params:
```
xpub : str
callback : str
api_code : str
```

Usage:
```python
from blockchain.v2 import receive

resp = receive.receive('1hNapz1CuH4DhnV1DFHH7hafwDE8FJRheA', 'http://your.url.com?invoice=1234465', 'your api key')

```


### Response object field definitions

#### `ReceiveResponse`

```
address : str
index : int
callback_url : str
```

#### `callback_log`
Call the 'api.blockchain.info/v2/receive/callback_log' endpoint and returns the list of callbacks performed for a given
callback URI.
Returns a list of `LogEntry` objects.

Params:
```
callback : str
api_code : str
```

Usage:
```python
from blockchain.v2 import receive

logs = receive.callback_log('http://your.url.com?invoice_id=1234465', 'your api key')

```

### Log entry object field definitions

#### `LogEntry`

```
callback_url : str
callback_at : str
raw_response : str
response_code : int

```

{%endfilter %}