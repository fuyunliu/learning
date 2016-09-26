import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.xpath("//a[text()='(about)']/@href").extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_author)

        # follow pagination links
        next_page = response.xpath("//a[text()='Next ']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_author(self, response):
        def extract_with_xpath(query):
            return response.xpath(query).extract_first().strip()

        yield {
            'name': extract_with_xpath("//h3[@class='author-title']/text()"),
            'birthdate': extract_with_xpath(
                "//span[@class='author-born-date']/text()"),
            'location': extract_with_xpath(
                "//span[@class='author-born-location']/text()"),
            'desc': extract_with_xpath(
                "//div[@class='author-description']/text()"),
        }
