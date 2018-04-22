# Techreport: The latest technology trends in the job market

Techreport tackles one question: Which technologies are mostly demanded by hiring companies today? The answer comes in the form of a series of charts you can interact with.

Exploration starts on [Techreport’s website](http://techreport.ninja)!

## Authors

- Lorinc Hever ([GitHub profile](https://github.com/lorinchever))
- Christophe Parent ([GitHub profile](https://github.com/Ooxie))

## Technical implementation

The project is written in **Python** primarily, and is deployed to **AWS EC2** and **AWS S3**. Sources of raw data include job listings published on job boards (Indeed.com). Web scraping is done with **Scrapy**, matching of job listings against a custom dictionary of technologies is done with **Pandas**, and production of interactive charts is done with **dc.js**.

The results are backed with a history of 30 days of collected data, and are refreshed daily.
