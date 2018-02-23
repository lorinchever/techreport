#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os.path

import jobs_scraper.run_scraper


def main():
    # Today's date in YYYY-mm-dd format
    run_date = unicode(datetime.date.today().strftime('%Y-%m-%d'))

    # Set up logging
    logging.basicConfig(
        filename=os.path.abspath(os.path.join(
            u'logs', u'{}{}{}'.format(u'jobs_', run_date, u'.log'))),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        level=logging.DEBUG)

    # Run the scraper
    jobs_scraper.run_scraper.run(run_date)


if __name__ == '__main__':
    main()
