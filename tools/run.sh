#!/usr/bin/env bash

source activate walletexplorer
cd exchange_addresses
scrapy crawl exchange_addresses -t json -o - > addresses.json
