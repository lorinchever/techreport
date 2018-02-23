#!/usr/bin/env python
# -*- coding: utf_8 -*-

import json
import re

import scrapy
import slimit.ast
import slimit.parser
import slimit.visitors.nodevisitor

import jobs_scraper.jobs_scraper.base_spider
import jobs_scraper.jobs_scraper.items


class IndeedSpider(jobs_scraper.jobs_scraper.base_spider.BaseSpider):
    name = 'indeed'

    def __init__(self, run_date):
        super(self.__class__, self).__init__(
            ['indeed.com'], jobs_scraper.jobs_scraper.items.JobItem,
            'https://www.indeed.com', run_date)

    def start_requests(self):
        start_url = 'jobs?q=software+engineer&l=Seattle,+WA&sort=date'
        yield scrapy.Request(self.get_abs_url(start_url),
                             callback=self.parse_job_listings)

    def parse_job_listings(self, response):
        # Scrape the IDs and attributes of all the jobs
        js = self.xpef(response,
                       u'//script[@type="text/javascript"]'
                       u'[contains(.,"var jobmap")]/text()')
        if js is None:
            return
        job_ids = []
        all_job_attributes = []
        for node in slimit.visitors.nodevisitor.visit(
                slimit.parser.Parser().parse(js)):
            if (isinstance(node, slimit.ast.Assign)
                    and node.op == u'='
                    and isinstance(node.left, slimit.ast.BracketAccessor)
                    and isinstance(node.left.node, slimit.ast.Identifier)
                    and node.left.node.value == u'jobmap'
                    and isinstance(node.left.expr, slimit.ast.Number)
                    and isinstance(node.right, slimit.ast.Object)):
                job_attributes = {}
                for p in node.right.properties:
                    if (isinstance(p, slimit.ast.Assign)
                            and p.op == u':'
                            and isinstance(p.left, slimit.ast.Identifier)
                            and isinstance(p.right, slimit.ast.String)):
                        for source, target in [
                                (u'jk', 'job_id'), (u'title', 'title'),
                                (u'cmp', 'company'), (u'loc', 'location')]:
                            if p.left.value == source:
                                v = p.right.value.strip("'")
                                job_attributes[target] = v
                                if p.left.value == u'jk':
                                    job_ids.append(v)
                                break
                if job_attributes['job_id']:
                    all_job_attributes.append(job_attributes)

        # Fetch the descriptions of all the jobs
        if job_ids:
            yield scrapy.Request(
                self.get_abs_url(u'{}{}'.format(u'rpc/jobdescs?jks=',
                                                u','.join(job_ids))),
                callback=self.parse_job_descriptions,
                meta={u'all_job_attributes': all_job_attributes})

        # Go to the next page if applicable
        next_page_url = self.xpef(response,
                                  u'//div[@class="pagination"]'
                                  u'/a[contains(.,"Next")]/@href')
        if next_page_url is not None:
            yield scrapy.Request(self.get_abs_url(next_page_url),
                                 callback=self.parse_job_listings)

    def parse_job_descriptions(self, response):
        all_job_attributes = response.meta[u'all_job_attributes']

        try:
            all_job_descriptions = json.loads(response.body_as_unicode())
        except ValueError:
            return
        if not isinstance(all_job_descriptions, dict):
            return

        # Match the job descriptions with the job attributes
        for job_attributes in all_job_attributes:
            job_id = job_attributes['job_id']
            for k, v in all_job_descriptions.iteritems():
                if k == job_id and v is not None:
                    item = self.item_cls()
                    item['job_id'] = job_id
                    for attribute in ['title', 'company', 'location']:
                        item[attribute] = job_attributes[attribute]
                    item['description'] = u" ".join(
                        re.sub(ur"<.+?>", u" ", v, flags=re.UNICODE).split())
                    yield item
                    break
