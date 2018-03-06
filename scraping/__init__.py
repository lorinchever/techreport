#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import scrapy.crawler
import scrapy.utils.project
import twisted.internet


@twisted.internet.defer.inlineCallbacks
def crawl(crawler_process, iso_run_date):
    yield crawler_process.crawl('indeed', iso_run_date)


def run(iso_run_date):
    os.environ.setdefault(
        'SCRAPY_SETTINGS_MODULE', 'scraping.scraping.settings')
    crawler_process = scrapy.crawler.CrawlerProcess(
        scrapy.utils.project.get_project_settings())
    crawl(crawler_process, iso_run_date)
    crawler_process.start()
