# Python-dca-binance

Small cli python script to buy cryptocurrencies on Binance

## Installation

```shell
pip3 install .
```

## Usage

Create `config.ini` file

```ini
# Binance API
[API]
secret: XXX
key: XXX

[BUY]
# What to buy
symbol: BTCEUR
# Buy 11 EUR woth of BTC
ammount: 11
```

then run

```shell
dca-binance
```

By default, `dca-binance` is using `config.ini` in the current path.
You can specify other config file using `--config-file <path_to_config_file>`
