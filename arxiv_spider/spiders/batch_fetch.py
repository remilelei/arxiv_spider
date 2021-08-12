from urllib.parse import urlencode
import scrapy
import datetime
import xml.dom.minidom

class BatchFetchSpider(scrapy.Spider):
    name = 'batch_fetch'
    allowed_domains = ['export.arxiv.org']
    arxiv_url = 'http://export.arxiv.org/oai2'
    start_urls = [arxiv_url]
    resumptionToken = None
    record_count = 0

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def start_requests(self):
        today = datetime.date.today()
        # date_today = f'{today.year}-{today.month}-{today.day}'
        date_today = today.isoformat()
        body = {
            'verb': 'ListRecords',
            'metadataPrefix': 'arXivRaw',
            'from': date_today,
            'until': date_today
        }
        yield scrapy.Request(
            url=self.arxiv_url, method='POST', body=urlencode(body), headers=self.headers, callback=self.parse
            )

    def parse(self, response):
        root: xml.dom.minidom.Element = xml.dom.minidom.parseString(response.body)
        records: list[xml.dom.minidom.Element] = root.getElementsByTagName('record')
        for record in records:
            title = record.getElementsByTagName('title')
            if len(title) <= 0:
                continue
            title: xml.dom.minidom.Element = title[0]
            str_title =  self.getText(title.childNodes)
            self.logger.info(f'get title: { str_title }')
            self.record_count = self.record_count + 1
        list_elem_resumptionToken:list[xml.dom.minidom.Element] = root.getElementsByTagName('resumptionToken')
        if (len(list_elem_resumptionToken) > 0):
            elem_resumptionToken: xml.dom.minidom.Element = list_elem_resumptionToken[0]
            self.resumptionToken = self.getText(elem_resumptionToken.childNodes)
            if self.resumptionToken:
                body = {
                    'verb': 'ListRecords',
                    'resumptionToken': self.resumptionToken
                }
                yield scrapy.Request(
                    url=self.arxiv_url, method='POST', body=urlencode(body), headers=self.headers, callback=self.parse
                    )
        self.logger.info(f'fetch finish, record_count={self.record_count} self.resumptionToken={self.resumptionToken}')

    def getText(self, nodelist) -> str:
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
