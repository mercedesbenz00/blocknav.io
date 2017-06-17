{% filter markdown %}
## `exchangerates` module

All functions support an optional parameter called `api_code`. It won't be listed with every function description.

#### `get_ticker`
Call the 'ticker' method and return a dictionary of `Currency` objects. Keys are currency symbols (str) and values are `Currency` objects.


Usage:
```python
from blockchain import exchangerates

ticker = exchangerates.get_ticker()
#print the 15 min price for every currency
for k in ticker:
	print k, ticker[k].p15min
```

#### `to_btc`
Call the 'tobtc' method and convert x value in the provided currency to BTC. Returns a `float`.

Params:
```
ccy : str - currency code
value : float
```

Usage:
```python
btc_amount = exchangerates.to_btc('USD', 4342.11)
```

### Response object field definitions

#### `Currency`

```
last : float
buy : float
sell : float
symbol : str
p15min : float - 15 minute delayed price
```
{% endfilter %}