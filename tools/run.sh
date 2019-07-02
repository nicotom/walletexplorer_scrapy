#!/usr/bin/env bash

source activate walletexplorer
scrapy crawl exchange_addresses -t json -o - > addresses.json
