# My symfonycasts.com scrapper

My first <del>serious</del> scrapping learning project. It's a harmless python script that scrape 
the video link location on [Symfonycasts](https://symfonycasts.com/) for the given course.

Here is the usage:
```
usage: scraper.py [-h] [--start START] [--end END] [--free] course

positional arguments:
  course         course's name

optional arguments:
  -h, --help     show this help message and exit
  --start START  download from
  --end END      download to
  --free         free course, no need to authenticate

```  
COURSE is not optional, you must provide it. For example:

```
$ symfonycasts_scraper.py symfony
```

Note that END should be equal or less than the actual number of videos, 
if a greater value is specified that value will be ignored and links will be gotten 
up to the actual max number of videos.

Note also that if you want free videos you don't need to authenticate, so no need to provide credentials,
just for a free course run:

```
$ symfonycasts_scraper.py --course symfony4 --free
```

In order to provide credentials you must set the following environment variables:

Linux like:
* export SCS_USER=testuser@gmail.com
* export SCS_PASS=T3s7U$erPass123*

Windows:
* set SCS_USER=testuser@gmail.com
* set SCS_PASS=T3s7U$erPass123*

but with your own credentials ;)

It will return the video links from the 
[Stellar Development with Symfony 4](https://symfonycasts.com/screencast/symfony)
in a file named out.txt

Probably it has some bugs. Feel free to help.

## Examples

* Get full course (this one was paid, at the time I wrote this)
```
$ symfonycasts_scraper.py symfony
```

* Get full course (this one was free, at the time I wrote this)

```
$ symfonycasts_scraper.py --free symfony4
```

* Get chapters from 5 to 10

```
$ symfonycasts_scraper.py --free --start 5 --end 10 symfony4
```

## TODO list 

A lot of stuff and improvements can be done. Any issue or improvement please report 
it and I will be glad to solve it.


## FAQ
Q: What is the 'course' parameter?

A: This is the typical url for a symfonycasts video: https://symfonycasts.com/screencast/symfony4/setup.
The course is the text after /screencasts/, i.e. symfony4

Q: This software can be used to get paid videos' direct link without a paid subscription?

A: No.

Q: Will this software work forever?

A: Sure not. Website DOM is changed every now and then for many reasons, 
that makes a web scraping solution temporary.

Q: How can I test if it still working?

A: Hmm... Perhaps by specifying a free course like [symfony4](https://symfonycasts.com/screencast/symfony4) 
(it was free by the time I was writting this).

Q: Do I need credentials to get links from a free course?

A: No, you don't, but remember to add the free argument

Q: Did you just invented these FAQ?

A: Yes....

Q: ...?

A: ...


## Disclaimer
Whatever happens it's on you.

