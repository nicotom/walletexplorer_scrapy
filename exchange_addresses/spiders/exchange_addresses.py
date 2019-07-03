import scrapy


class QuotesSpider(scrapy.Spider):
    name = "exchange_addresses"
    start_urls = [
        'https://www.walletexplorer.com/',
    ]

    def parse(self, response):
        number_of_exchanges = len(response.xpath('//*[@id="main"]/table/tr/td[1]/ul/li').extract())
        for exchange in range(1, number_of_exchanges + 1):
            n_exchanges = getattr(self, 'n_exchanges', None)
            if n_exchanges is not None:
                if exchange > int(n_exchanges):
                    break
            number_of_subexchanges = len(response.xpath(
                f'//*[@id="main"]/table/tr/td[1]/ul/li[{exchange}]/a').extract())
            for sub_exchange in range(1, number_of_subexchanges + 1):

                link = response.xpath(
                        f'//*[@id="main"]/table/tr/td[1]/ul/li[{exchange}]/a[{sub_exchange}]/@href').extract()
                absolute_url = QuotesSpider.start_urls[0] + link[0] + '/addresses'
                exchange_name = response.xpath(
                    f'//*[@id="main"]/table/tr/td[1]/ul/li[{exchange}]/a[{1}]/text()').extract()[0]
                yield response.follow(
                    absolute_url,
                    callback=self.parse_addresses,
                    meta={
                        'url': absolute_url,
                        'exchange_name': exchange_name
                    }
                )

    def parse_addresses(self, response):
        addresses = response.xpath('//*[@id="main"]/table/tr[*]/td[1]/a/text()').getall()
        yield {
            'exchange_name': response.meta.get('exchange_name'),
            'url': response.meta.get('url'),
            'addresses': addresses
        }
        next_page_url = response.xpath('//*[@id="main"]/div[2]/a[contains(text(),"Next")]/@href').get()
        n_pages = getattr(self, 'n_pages', None)
        if int(next_page_url[-1]) > int(n_pages):
            return
        modified_meta = response.meta
        modified_meta['url'] = QuotesSpider.start_urls[0] + next_page_url
        yield response.follow(next_page_url, self.parse_addresses, meta=modified_meta)
