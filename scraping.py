#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os.path

import scraping


def main():
    # Today's date in ISO format
    iso_run_date = unicode(datetime.date.today().isoformat())

    # Set up logging
    logging.basicConfig(
        filename=os.path.abspath(os.path.join(
            u'logs', u'techreport_{}.log'.format(iso_run_date))),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        level=logging.DEBUG)

    # Run the scraper
    scraping.run(iso_run_date)


if __name__ == '__main__':
    main()
