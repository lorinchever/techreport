#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
import os.path

import nltk
import pandas


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

    # Load the dictionary of technologies
    try:
        technologies = pandas.read_csv(
            u'dictionary/dictionary.csv', usecols=[u'technology', u'keyword'],
            dtype=object, encoding='utf_8', error_bad_lines=False)
    except Exception, e:
        logging.error(u"{} {}".format(type(e), e))
        return
    technologies = technologies.dropna().drop_duplicates(subset=u'keyword')

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
        u'keyword', axis=1).drop_duplicates(
        subset=[u'technology', u'job_id']).sort_values(
        [u'technology', u'job_id'])
    try:
        technologies_to_jobs.to_csv(
            u'data/matching/matching_{}.csv'.format(iso_run_date),
            columns=[u'technology', u'job_id', u'title', u'company',
                     u'location'],
            index=False, encoding='utf_8')
    except Exception, e:
        logging.error(u"{} {}".format(type(e), e))
        return
    logging.info(u"Saved matching of technologies to jobs")


if __name__ == '__main__':
    main()
