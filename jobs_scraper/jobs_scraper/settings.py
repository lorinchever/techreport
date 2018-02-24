#!/usr/bin/env python
# -*- coding: utf-8 -*-

BOT_NAME = 'jobs_scraper'

SPIDER_MODULES = ['jobs_scraper.jobs_scraper.spiders']
NEWSPIDER_MODULE = 'jobs_scraper.jobs_scraper.spiders'

ITEM_PIPELINES = {
    'jobs_scraper.jobs_scraper.pipelines.CsvExportPipeline': 300,
}

DOWNLOAD_HANDLERS = {
    's3': None
}

CONCURRENT_REQUESTS = 1

DOWNLOAD_DELAY = 1.0

USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 '
              'Firefox/52.0')

LOG_ENABLED = False

DUPEFILTER_DEBUG = True
