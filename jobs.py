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
            u'logs', u'jobs_{}.log'.format(run_date))),
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        level=logging.DEBUG)

    # Run the scraper
    jobs_scraper.run_scraper.run(run_date)

    # Load the scraped jobs
    try:
        jobs = pandas.read_csv(
            u'data/jobs_scraper/indeed/jobs_scraper_indeed_{}.csv'.format(
                run_date),
            usecols=[u'job_id', u'title', u'company', u'location',
                     u'description'],
            dtype=object, encoding='utf_8', error_bad_lines=False)
    except Exception, e:
        print type(e), e
        return
    jobs = jobs.dropna().drop_duplicates(subset=u'job_id')

    # Load the dictionary of technologies
    try:
        technologies = pandas.read_csv(
            u'Dictionary/dictionary.csv', usecols=[u'technology', u'keyword'],
            dtype=object, encoding='utf_8', error_bad_lines=False)
    except Exception, e:
        print type(e), e
        return

    # Find the technology keywords in every job description
    keywords = set(technologies[u'keyword'])
    jobs[u'description'] = jobs[u'description'].str.lower().apply(
        nltk.word_tokenize).apply(set).apply(keywords.intersection)

    # Create an entry for every technology keyword
    keywords_to_jobs = pandas.DataFrame(
        columns=[u'keyword', u'job_id', u'title', u'company', u'location'])
    for row in jobs.itertuples(index=False):
        for keyword in row.description:
            keywords_to_jobs = keywords_to_jobs.append(
                {u'keyword': keyword, u'job_id': row.job_id,
                    u'title': row.title, u'company': row.company,
                    u'location': row.location},
                ignore_index=True)

    # Match technologies to jobs and save it
    technologies_to_jobs = pandas.merge(
        technologies, keywords_to_jobs, on=u'keyword').drop(
        u'keyword', axis=1).sort_values([u'technology', u'job_id'])
    try:
        technologies_to_jobs.to_csv(
            u'data/jobs_matching/indeed/jobs_matching_indeed_{}.csv'.format(
                run_date),
            columns=[u'technology', u'job_id', u'title', u'company',
                     u'location'],
            index=False, encoding='utf_8')
    except Exception, e:
        print type(e), e
        return


if __name__ == '__main__':
    main()
