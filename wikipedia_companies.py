# -*- coding: utf-8 -*-
import scrapy
import re
from IPython import embed


class WikipediaCompaniesSpider(scrapy.Spider):
    name = 'wikipedia_companies'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue']
    output_file = './output.csv'

    def write_to_csv(self,data):


        with open(self.output_file,'w') as ofh:
            output_str = ''
            headers = [k for k in data[0].keys()]
            print(headers)
            first_line = ",".join(headers)
            ofh.write("%s\n" % first_line)

            
            for row in data:
                values = [re.sub(',','',row[k]) for k in headers]

                line = ",".join(values)
                output_str += "%s\n" % line
            
            embed()
            ofh.write(output_str)



    def parse(self, response):
        print(response.body_as_unicode())
        table_element = response.xpath('//div[@id="mw-content-text"]//table[contains(@class,"wikitable")]')
        rows = table_element.xpath('//tr')

        row_xpath_map = {
            'company_name': 'td[1]/a/text()',
            'revenue': 'td[3]/text()',
            'employees': 'td[5]/text()'

        }

        all_data = []

        for tr in rows:
            data_row = {}
            for data_key, xpath_xpr in row_xpath_map.items():
                data_row[data_key] = tr.xpath(xpath_xpr).extract_first() or ''
                print("%s: %s" % (data_key, data_row[data_key]))
            all_data.append(data_row)

        print(all_data)
        self.write_to_csv(all_data)


