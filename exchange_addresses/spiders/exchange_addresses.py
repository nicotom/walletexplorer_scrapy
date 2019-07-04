import scrapy


class QuotesSpider(scrapy.Spider):
    name = "wallet_addresses"
    start_urls = [
        'https://www.walletexplorer.com/',
    ]
    wallet_types = {
        "exchange": 1,
        "pool": 2,
        "service": 3,
        "gambling": 4,
        "old": 5,
    }

    def parse(self, response):
        type_of_wallets = getattr(self, 'type', None)
        if type_of_wallets in self.wallet_types:
            wallet_type_name = type_of_wallets
            wallet_type = self.wallet_types[type_of_wallets]
        else:
            wallet_type_name = 'default'
            wallet_type = 1
        self.logger.info('Query for Type of wallet "%s": %d' % (wallet_type_name, wallet_type))
        number_of_wallets = len(response.xpath(f'//*[@id="main"]/table/tr/td[{wallet_type}]/ul/li').extract())

        for wallet in range(1, number_of_wallets + 1):
            n_wallets = getattr(self, 'n_wallets', None)
            if n_wallets:
                if wallet > int(n_wallets):
                    break
            wallet_name = response.xpath(
                f'//*[@id="main"]/table/tr/td[{wallet_type}]/ul/li[{wallet}]/a[{1}]/text()').extract()[0]
            self.logger.info('Querying wallet: "%s"' % (wallet_name))
            number_of_subwallets = len(response.xpath(
                f'//*[@id="main"]/table/tr/td[{wallet_type}]/ul/li[{wallet}]/a').extract())
            for sub_wallet in range(1, number_of_subwallets + 1):
                link = response.xpath(
                        f'//*[@id="main"]/table/tr/td[{wallet_type}]/ul/li[{wallet}]/a[{sub_wallet}]/@href').extract()
                absolute_url = QuotesSpider.start_urls[0] + link[0] + '/addresses'
                yield response.follow(
                    absolute_url,
                    callback=self.parse_addresses,
                    meta={
                        'url': absolute_url,
                        'wallet_name': wallet_name,
                        'wallet_type': wallet_type_name
                    }
                )

    def parse_addresses(self, response):
        addresses = response.xpath('//*[@id="main"]/table/tr[*]/td[1]/a/text()').getall()
        yield {
            'wallet_type': response.meta.get('wallet_type'),
            'wallet_name': response.meta.get('wallet_name'),
            'url': response.meta.get('url'),
            'addresses': addresses
        }
        next_page_url = response.xpath('//*[@id="main"]/div[2]/a[contains(text(),"Next")]/@href').get()
        if not next_page_url:
            return
        n_pages = getattr(self, 'n_pages', None)
        if n_pages:
            if int(next_page_url[-1]) > int(n_pages):
                return
        modified_meta = response.meta
        modified_meta['url'] = QuotesSpider.start_urls[0] + next_page_url
        yield response.follow(next_page_url, self.parse_addresses, meta=modified_meta)
