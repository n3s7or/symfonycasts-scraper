# My symfonycasts.com scrapper

My first <del>serious</del> scrapping learning project. It's a harmless python script that scrape the video link location of a paid subscription on [Symfonycasts](https://symfonycasts.com/) for the given course.

Here is the usage:
```
usage: scraper.py [-h] [--start START] [--end END] --course COURSE

optional arguments:
  -h, --help       show this help message and exit
  --start START    download from
  --end END        download to
  --course COURSE  Course's name
```  
COURSE is not optional, you must provide it. For example:

```
$ symfonycasts_scraper.py --course symfony4
```

In order to provide credentials you must set the following:
* export SCS_USER='testuser@gmail.com'
* export SCS_PASS='T3s7U$erPass123*'

but with your own log in credentials ;)

It will return the video links from the 
[Stellar Development with Symfony 4](https://symfonycasts.com/screencast/symfony)
in a file named out.txt

Probably it has some bugs. Feel free to help.


##TODO list 

A lot of stuff and improvements can be done. Any issue or improvement please report 
it and I will be glad to solve it.


##FAQ

Q: This software can be used to get direct link to videos without 
a paid subscription?

A: No.

Q: Will this software work forever?

A: Sure not. Website DOM is changed every now and then for many reasons, 
that makes a web scraping solution temporary.

Q: How can I test if it still working?

A: Hmm... Perhaps buy specifying a free course like [symfony4](https://symfonycasts.com/screencast/symfony4) 
(it was free by the time I was writting this).

Q: Do I need credentials to get links from a free course?

A: So far you do.

Q: ...?

A: ...


