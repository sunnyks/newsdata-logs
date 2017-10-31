#! /usr/bin/env python2.7

import psycopg2
import sys

the_mainstream_media = "dbname=news"

def find_most_popular_articles():
    "Return a table of the 3 articles which have been accessed the most in descending order"
    conn = psycopg2.connect(the_mainstream_media)
    c = conn.cursor()
    c.execute('''select title as article, count (*) as views
                 from articles join log
                 on concat('/article/', articles.slug) = log.path
                 group by articles.title
                 order by views desc limit 3;''')
    best_clickbait = c.fetchall()
    conn.close()
    return best_clickbait

def find_most_popular_authors():
    "Return a table of the authors who get the most views in descending order"
    conn = psycopg2.connect(the_mainstream_media)
    c = conn.cursor()
    c.execute('''select authors.name as author, count(*) as views
                 from authors join articles on authors.id = articles.author
                 join log on concat('/article/', articles.slug) = log.path
                 group by authors.name order by views desc;''')
    buzzfeed = c.fetchall()
    conn.close()
    return buzzfeed

def find_error_days():
    "Return a table of the days on which more than 1 percent of requests led to errors"
    conn = psycopg2.connect(the_mainstream_media)
    c = conn.cursor()
    # Make sure that you've created the views "reqs_per_day" and "err_per_day" as instructed in README.md
    c.execute('''select pct_err.* from (
                 select reqs_per_day.day,
                 round((err_per_day.errors * 100.00 / reqs_per_day.reqs), 2) as pct_errors
                 from err_per_day join reqs_per_day
                 on err_per_day.day = reqs_per_day.day) pct_err
                 where pct_errors > 1.00;''')
    disaster_days = c.fetchall()
    conn.close()
    return disaster_days

if __name__ == '__main__':
    loganalysis = open('logs-analysis.txt', 'w')
    loganalysis.write(str(find_most_popular_articles()) + '\n')
    loganalysis.write(str(find_most_popular_authors()) + '\n')
    loganalysis.write(str(find_error_days()) + '\n')
    loganalysis.close()
