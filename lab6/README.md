### Set-up Database with SQLite3
```
sqlite3 sse.db
sqlite3> create table sse_csp_keywords(
    csp_keywords_id integer primary key autoincrement,
    csp_keywords_address text,
    csp_keyvalue text
);
sqlite3> create table sse_keywords(
    sse_keywords_id integer primary key autoincrement,
    sse_keyword text,
    sse_keyword_numfiles integer,
    sse_keyword_numsearch integer
);
```

### Run SSE scheme
```
python SSE.py -i[-s]
```

* -i: initialize the dictionary
* -s: start to search the keyword

### Delete records in tables
```
sqlite3> delete from <table_name>
```
### Delete tables
```
sqlite3> drop table <table_name>
```
