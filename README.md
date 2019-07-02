# https://walletexplorer.com Scraper
This repository can be used to scrape the url: `https://walletexplorer.com` for exchange addresses

## Installation
It is installed using the command below
```bash
# Install all the needed dependencies
./tools/install.sh
```

## Crawl the spider
```bash
# Run the exchange_addresses spider
./tools/run.sh
```

## Obtain results
The results are saved into: `addresses.json` with the format below:
```json
[
{"exchange_name": "Bittrex.com", "link": "https://www.walletexplorer.com//wallet/Bittrex.com/addresses", "addresses": ["14cQRmViAzVKa277gZznByGZtnrVPQc8Lr", "1N52wHoVR79PMDishab2XmRHsbekCdGquK"]},
{"exchange_name": "Huobi.com", "link": "https://www.walletexplorer.com//wallet/Huobi.com-2/addresses", "addresses": ["1PFQM6D3CFrf7PFtZZAW9YHr55EPsfAsrG", "13oLr3JJm4qx7PrTGtorPcxZ5YXpYKnXmE"]}
]
```
