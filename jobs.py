#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os.path

import nltk
import pandas

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

    # Load the scraped jobs and split their descriptions into lower-case words
    try:
        jobs = pandas.read_csv('data/jobs_scraper/indeed/jobs_scraper_indeed_{}.csv'.format(run_date), dtype=object, encoding='utf_8', error_bad_lines=False, usecols=[u'job_id', u'title', u'company', u'location', u'description'])
    except Exception, e:
        print type(e), e
        return
    jobs = jobs.dropna().drop_duplicates(subset=u'job_id')
    jobs[u'description'] = jobs[u'description'].str.lower().apply(nltk.word_tokenize)

    # Load the dictionary of keywords
    try:
        multi_keywords = pandas.read_csv('Dictionary/dictionary.csv', dtype=object, encoding='utf_8', error_bad_lines=False, squeeze=True, usecols=[u'Keyword'])
    except Exception, e:
        print type(e), e
        return
    multi_keywords = multi_keywords.dropna().drop_duplicates()

    # Find the jobs whose descriptions mention every keyword
    matching_jobs = pandas.DataFrame(columns=[u'multi_keyword', u'job_id', u'title', u'company', u'location'])
    for multi_keyword in multi_keywords:
        keywords = multi_keyword.split(u',')
        for row in jobs.itertuples(index=False):
            if any(keyword in row.description for keyword in keywords):
                matching_jobs = matching_jobs.append({u'multi_keyword': multi_keyword, u'job_id': row.job_id, u'title': row.title, u'company': row.company, u'location': row.location}, ignore_index=True)
    matching_jobs = matching_jobs.sort_values([u'multi_keyword', u'job_id'])

    # Save the matching jobs
    try:
        matching_jobs.to_csv('data/jobs_matching/indeed/jobs_matching_indeed_{}.csv'.format(run_date), encoding='utf_8', index=False)
    except Exception, e:
        print type(e), e
        return


if __name__ == '__main__':
    main()
