#!/usr/bin/env bash

# Getting options
while getopts ":t:n:p:f:" opt;
do
    case $opt in
        t) type="$OPTARG"
        ;;
        f) file="$OPTARG"
        ;;
        n) number="$OPTARG"
        ;;
        p) pages="$OPTARG"
        ;;
        \?) echo "https://www.walletexplorer.com Scraper"
            echo ""
            echo "Valid options:"
            echo "-t : type of exchange. Options: exchange pool service gambling old"
            echo "-f : path where to store the results. Default is tmp.json"
            echo "-n : number of distinct wallets to scrape. By default scrapes all"
            echo "-p : number of pages to scrape. By default scrapes all"
            echo ""
            echo "Example:"
            echo "$0 -t exchange -f exchange_addresses.json -n 1 -p 2 "
            exit 0
        ;;
    esac
done

function list_include_item {
  list="$1"
  item="$2"
  if [[ $list =~ (^|[[:space:]])"$item"($|[[:space:]]) ]] ; then
    # yes, list include item
    result=1
  else
    result=0
  fi
}

if [[ -z  ${type} ]]
then
    type="exchange"
fi
list_include_item "exchange pool service gambling old" ${type}
if [[ "$result" -eq "0" ]]
then
    echo "Unknown type of wallet type"
    echo "Run $0 -h to see available parameters."
    exit 1
fi

echo "Querying addresses of type \"$type\"."

if [[ -z  ${file} ]]
then
    file='tmp.json'
fi

if [[ -z  ${number} ]]
then
    number=''
else
    echo "For a total of $number distinct."
fi

if [[ -z  ${pages} ]]
then
    pages=''
else
    echo "For $pages pages."
fi
echo "Saving results in \"$file\""

echo "crawl wallet_addresses -t json -o - -a type=${type} -a n_wallets=${number} -a n_pages=${pages} > ${file}"
source activate walletexplorer
scrapy crawl wallet_addresses -t json -o - \
    -a type=${type} -a n_wallets=${number} -a n_pages=${pages} > ${file}
