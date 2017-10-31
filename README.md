#Logs Analysis

This is a python program that uses psycopg2 to connect to a PostgreSQL database with tables: articles, authors, and logs in order to answer 3 questions.

1. What are the 3 most requested articles?
2. Who are the most requested authors?
3. On which days did more than 1% of requests lead to errors?

To run this program, you will need:
* Python 2.7
* psycopg2
* PostgreSQL 9.5
* the file 'newsdata.sql'

Instructions to run program:
1. load data of 'newsdata.sql' into database named 'news' with command: `psql -d news -f newsdata.sql`
2. connect to database with command: `psql news`
3. create view consisting of total http requests per day with command:
`create view reqs_per_day as select date(time) as day, count(status) as reqs from log group by day;`
4. create view consisting of total http errors per day with command:
`create view err_per_day as select date(time) as day, count(status) as errors from log where status != '200 OK' group by day order by errors;`
5. run python file 'logs-analysis.py' with command: `python logs-analysis.py`
6. program will create and populate a file 'logs-analysis.txt' with answers to each of the 3 questions on each respective line of the file.
