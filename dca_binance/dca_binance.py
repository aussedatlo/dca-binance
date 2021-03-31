#!/usr/bin/env python3
# coding=utf-8

import configparser
import logging
import argparse
import sys
from pathlib import Path
from binance.client import Client
from binance.exceptions import BinanceAPIException
from .logger import setup_logger, setup_logger_filename

__author__ = "Louis Aussedat"
__copyright__ = "Copyright (c) 2021 Louis Aussedat"
__license__ = "GPLv3"

log = setup_logger(__name__, logging.INFO)

def check_section(config, section):
    if not config.has_section(section):
        log.error("Missing section %s" % section)
        exit(1)

def check_option(config, section, option):
    if not config.has_option(section, option):
        log.error("Missing option %s in section %s"
            % (option, section))
        exit(1)

def check_config(config_file):
    if not Path(config_file).is_file():
        log.error("No such file %s" % config_file)
        exit(1)

    config = configparser.ConfigParser()
    config.read(config_file)

    check_section(config, 'API')
    check_section(config, 'BUY')
    check_option(config, 'API', 'secret')
    check_option(config, 'API', 'key')
    check_option(config, 'BUY', 'symbol')
    check_option(config, 'BUY', 'ammount')

    return config

def main(argv):
    parser = argparse.ArgumentParser(argv)
    parser.add_argument("--config-file",
        default="./config.ini", help="config file path")
    parser.add_argument("--log-path", help="log file path")
    parser.add_argument("-d", "--debug", help="debug mode",
        action="store_true")
    args = parser.parse_args()

    if args.log_path:
        setup_logger_filename(__name__, args.log_path)

    log.info("starting dca-binance")

    if args.debug == True:
        log.setLevel(logging.DEBUG)
        log.debug("debug mode")

    log.debug(args)

    config = check_config(args.config_file)
    log.info("using config file %s" % args.config_file)

    api_key=config['API']['key']
    api_secret=config['API']['secret']
    symbol=config["BUY"]['symbol']
    ammount=float(config['BUY']['ammount'])

    log.debug("symbol: %s" % symbol)
    log.debug("ammount: %s" % ammount)

    client = Client(api_key, api_secret)

    avg_price = client.get_avg_price(symbol=symbol)
    avg_price = float(avg_price['price'])

    quantity = ammount / avg_price
    quantity = "{:0.0{}f}".format(quantity, 5)
    avg_price = "{:0.0{}f}".format(avg_price, 2)

    log.info("quantity to buy: %s" % (quantity))
    log.info("average price: %s" % avg_price)

    try:
        order = client.order_limit_buy(
            symbol=symbol,
            quantity=quantity,
            price=avg_price)
    except BinanceAPIException as e:
        log.error("%s, result code: %d"
            % (e.message, e.status_code))
        exit(e.status_code)

    log.debug(order)

def exec_command_line(argv):
	# Exit with correct return value
	if main(argv):
		exit(0)
	else:
		exit(255)

if __name__== "__main__":
    main(sys.argv)
