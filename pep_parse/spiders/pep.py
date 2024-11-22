import scrapy

from pep_parse.exceptions import PepDataNotFound
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://' + domain + '/' for domain in allowed_domains]

    def parse(self, response):
        links = list(
            set(
                response.css(
                    'section[id="index-by-category"] a.pep::attr(href)'
                ).getall())
        )
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        try:
            full_number = response.css(
                'ul.breadcrumbs li:nth-of-type(3)::text'
            ).get()
            status = response.css(
                'dt:contains("Status") + dd abbr::text'
            ).get()
            full_name = response.css('head title::text').get()
            if not full_name or not status or not full_number:
                raise PepDataNotFound(
                    'Не удалось получить номер, статус или имя PEP'
                )
            full_name = full_name.split(' | ')[0]
        except PepDataNotFound as e:
            self.logger.error(f'Ошибка парсинга: {e}')
            return None

        data = {
            'number': full_number.replace('PEP', ''),
            'name': full_name.replace(full_number, '').lstrip(' – '),
            'status': status
        }
        return PepParseItem(data)
