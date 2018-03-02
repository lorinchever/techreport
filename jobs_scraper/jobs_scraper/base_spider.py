#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import os.path
import urlparse

import scrapy.spiders


class BaseSpider(scrapy.spiders.CrawlSpider):
    __metaclass__ = abc.ABCMeta

    @property
    def name(self):
        raise NotImplementedError("Field 'name' not initialized in subclass")

    @abc.abstractmethod
    def __init__(self, domains, item_cls, root_url, run_date):
        self.allowed_domains = domains
        self.item_cls = item_cls
        self.root_url = root_url
        self.run_date = run_date
        self.csv_export_fullpath = os.path.abspath(os.path.join(
            u'data',
            os.path.basename(os.path.dirname(os.path.abspath(__file__))),
            self.name, u'jobs_scraper_{}_{}.csv'.format(self.name, run_date)))

    def get_abs_url(self, url):
        return urlparse.urljoin(self.root_url, url)

    def xpef(self, src, xp):
        return src.xpath(xp).extract_first()
