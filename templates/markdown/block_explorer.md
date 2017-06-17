{% filter markdown %}
## `blockexplorer` module
All functions support an optional parameter called `api_code`. It won't be listed with every function description.

#### `get_block`
Get a single block based on a block hash. Returns a `Block` object.

Params:
```
block_id : str - block hash
```

Usage:
```python
from blockchain import blockexplorer

block = blockexplorer.get_block('000000000000000016f9a2c3e0f4c1245ff24856a79c34806969f5084f410680')
```

#### `get_tx`
Get a single transaction based on a transaction hash. Returns a `Transaction` object.

Params:
```
tx_id : str - transaction hash
```

Usage:
```python
tx = blockexplorer.get_tx('d4af240386cdacab4ca666d178afc88280b620ae308ae8d2585e9ab8fc664a94')
```

#### `get_block_height`
Get an array of blocks at the specified height. Returns an array of `Block` objects.

Params:
```
height : int - block height
```

Usage:
```python
blocks = blockexplorer.get_block_height(2570)
```

#### `get_address`
Get a single address and its transactions. Returns an `Address` object.

Params:
```
address : str - address(base58 or hash160) to look up
filter : FilterType - the filter for transactions selection (optional)
limit : int - limit number of transactions to display (optional)
offset : int - number of transactions to skip when display (optional)```

Usage:
```python
address = blockexplorer.get_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd')
```

#### `get_xpub`
Get a single xpub and its transactions. Returns an `Xpub` object.

Params:
```
xpu: str xpub to look up
filter : FilterType - the filter for transactions selection (optional)
limit : int - limit number of transactions to display (optional)
offset : int - number of transactions to skip when display (optional)```

Usage:
```python
xpub = blockexplorer.get_xpub('xpub6CmZamQcHw2TPtbGmJNEvRgfhLwitarvzFn3fBYEEkFTqztus7W7CNbf48Kxuj1bRRBmZPzQocB6qar9ay6buVkQk73ftKE1z4tt9cPHWRn')
```


#### `get_multi_address`
Get aggregate summary for multiple addresses including overall balance, per address balance
and list of relevant transactions. Returns an `MultiAddress` object.

Params:
```
addresses : tuple - addresses(base58 or xpub) to look up
filter : FilterType - the filter for transactions selection (optional)
limit : int - limit number of transactions to display (optional)
offset : int - number of transactions to skip when display (optional)```

Usage:
```python
addresses = blockexplorer.get_multi_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd', xpub6CmZamQcHw2TPtbGmJNEvRgfhLwitarvzFn3fBYEEkFTqztus7W7CNbf48Kxuj1bRRBmZPzQocB6qar9ay6buVkQk73ftKE1z4tt9cPHWRn)
```

####`get_balance`
Get balances for each address provided. Returns a dictionary of str to `Balance` objects.

Params:
```
addresses : tuple - addresses(base58 or xpub) to look up
filter : FilterType - the filter for transactions selection (optional)

Usage:
```python
addresses = blockexplorer.get_multi_address('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd', xpub6CmZamQcHw2TPtbGmJNEvRgfhLwitarvzFn3fBYEEkFTqztus7W7CNbf48Kxuj1bRRBmZPzQocB6qar9ay6buVkQk73ftKE1z4tt9cPHWRn)
```

#### `get_unspent_outputs`
Get an array of unspent outputs for an address. Returns an array of `UnspentOutput` objects.

Params:
```
addresses : tuple addresses - addresses in the base58 or xpub format
confirmations : int - minimum confirmations to include (optional)
limit : int - limit number of unspent outputs to fetch (optional)
```

Usage:
```python
outs = blockexplorer.get_unspent_outputs('1HS9RLmKvJ7D1ZYgfPExJZQZA1DMU3DEVd')
```

#### `get_latest_block`
Get the latest block on the main chain. Returns a `LatestBlock` object.

Usage:
```python
latest_block = blockexplorer.get_latest_block()
```

#### `get_unconfirmed_tx`
Get a list of currently unconfirmed transactions. Returns an array of `Transaction` objects.

Usage:
```python
txs = blockexplorer.get_unconfirmed_tx()
```

#### `get_blocks`
Get a list of blocks for a specific day or mining pool. Returns an array of `SimpleBlock` objects.

Params:
```
time : int - unix time in ms (optional)
pool_name : str - pool name (optional)
```
At least one parameter is required.

Usage:
```python
blocks = blockexplorer.get_blocks(pool_name = 'Discus Fish')
```

### Response object field definitions

#### `Block`

```
hash : str
version : int
previous_block : str
merkle_root : str
time : int
bits : int
fee : int
nonce int
n_tx : int
size : int
block_index : int
main_chain : bool
height : int
received_time : int
relayed_by : string
transactions : array of Transaction objects
```

#### `Transaction`

```
double_spend : bool
block_height : int (if -1, the tx is unconfirmed)
time : int
relayed_by : str
hash : str
tx_index : int
version : int
size : int
inputs : array of Input objects
outputs: array of Output objects
```

#### `Input`

```
n : int
value : int
address : str
tx_index : int
type : int
script : str
script_sig : str
sequence : int
```

Note: if coinbase transaction, then only `script` and `script_siq` will be populated.

#### `Output`

```
n : int
value : int
address : str
tx_index : int
script : str
spent : bool
```

#### `Address`

```
hash160 : str
address : str
n_tx : int
total_received : int
total_sent : int
final_balance : int
transactions : array of Transaction objects
```

####`SimpleAddress`

```
address : str
n_tx : int
total_received : int
total_sent : int
final_balance : int
change_index : int
account_index : int
```

####`MultiAddress`

```
n_tx : int
n_tx_filtered : int
total_received : int
total_sent : int
final_balance : int
addresses : array of SimpleAddress objects
transactions : array of Transaction objects
```

####`Xpub`

```
address : str
n_tx : int
total_received : int
total_sent : int
final_balance : int
change_index : int
account_index : int
gap_limit : int
transactions : array of Transaction objects
```

####`Balance`

```
n_tx : int
total_received : int
final_balance : int
```

#### `UnspentOutput`

```
tx_hash : str
tx_index : int
tx_output_n : int
script : str
value : int
value_hex : str
confirmations : int
```

#### `LatestBlock`

```
hash : str
time : int
block_index : int
height : int
tx_indexes : array of TX indexes (integers)
```

#### `SimpleBlock`

```
height : int
hash : str
time : int
main_chain : bool
```
{% endfilter %}