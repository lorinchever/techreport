#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os.path
import re

import pandas


def is_sublist(sl, l):
    sl_length = len(sl)
    for i in xrange(len(l)):
        if l[i:i + sl_length] == sl:
            return True
    return False


def main():
    # Today's date in ISO format
    run_date = datetime.date.today()
    iso_run_date = unicode(run_date.isoformat())

    # Set up logging
    logging.basicConfig(
        filename=os.path.abspath(os.path.join(
            u'logs', u'techreport_{}.log'.format(iso_run_date))),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        level=logging.DEBUG)

    # Load the scraped jobs up to 30 days in the past
    jobs_daily_chunks = []
    for n in xrange(31):
        try:
            jobs_daily_chunk = pandas.read_csv(
                u'data/scraping/scraping_{}.csv'.format(
                    unicode((run_date - datetime.timedelta(
                        days=n)).isoformat())),
                usecols=[u'job_id', u'title', u'company', u'location',
                         u'description'],
                dtype=object, encoding='utf_8', error_bad_lines=False)
        except Exception, e:
            logging.warning(u"{} {}".format(type(e), e))
        else:
            jobs_daily_chunks.append(jobs_daily_chunk)
    jobs = pandas.concat(jobs_daily_chunks).dropna().drop_duplicates(
        subset=u'job_id')

    # Split the job descriptions into lower-case words
    jobs[u'description'] = jobs[u'description'].str.lower().apply(
        lambda x: [w.strip(u'.') for w in re.split(
            ur'[^a-zA-Z0-9_#+\-.]+', x, flags=re.U)])

    # Load the dictionary of technologies
    try:
        technologies = pandas.read_csv(
            u'dictionaries/technologies.csv',
            usecols=[u'Technology', u'Keywords', u'Category'], dtype=object,
            encoding='utf_8', error_bad_lines=False)
    except Exception, e:
        logging.error(u"{} {}".format(type(e), e))
        return
    technologies = technologies.dropna().drop_duplicates(subset=u'Technology')

    # Split the technology keywords into words
    technologies[u'Keywords'] = technologies[u'Keywords'].str.split(u'|')

    # Match the technologies to the jobs
    technologies_to_jobs = pandas.DataFrame(
        columns=[u'Technology', u'Job_ID', u'Title', u'Company', u'Location',
                 u'Category'])
    for jobs_row in jobs.itertuples(index=False):
        for technologies_row in technologies.itertuples(index=False):
            if any(is_sublist(keyword.split(), jobs_row.description)
                    for keyword in technologies_row.Keywords):
                technologies_to_jobs = technologies_to_jobs.append(
                    {u'Technology': technologies_row.Technology,
                        u'Job_ID': jobs_row.job_id, u'Title': jobs_row.title,
                        u'Company': jobs_row.company,
                        u'Location': jobs_row.location,
                        u'Category': technologies_row.Category},
                    ignore_index=True)
    technologies_to_jobs = technologies_to_jobs.drop_duplicates(
        subset=[u'Technology', u'Job_ID']).sort_values(
        [u'Technology', u'Job_ID'])

    # Save the matching
    try:
        technologies_to_jobs.to_csv(
            u'data/matching/matching_{}.csv'.format(iso_run_date),
            columns=[u'Technology', u'Job_ID', u'Title', u'Company',
                     u'Location', u'Category'],
            index=False, encoding='utf_8')
    except Exception, e:
        logging.error(u"{} {}".format(type(e), e))
        return
    logging.info(u"Saved matching of technologies to jobs")


if __name__ == '__main__':
    main()
