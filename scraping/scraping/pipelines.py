#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy.exporters


class CsvExportPipeline(object):
    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        f = open(spider.csv_export_fullpath, 'wb')
        self.files[spider] = f
        self.exporter = scrapy.exporters.CsvItemExporter(
            f, fields_to_export=list(spider.item_cls.fields))
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        f = self.files.pop(spider)
        f.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
