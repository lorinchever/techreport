#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy


class JobItem(scrapy.Item):
    job_id = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
