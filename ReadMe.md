# My symfonycast.com scrapper

My first <del>serious</del> scrapping learning project. It's a harmless python script that scrape the video link location of a paid subscription on [Symfonycasts](https://symfonycasts.com/) for the given course.

I don't know if it stills functional, I made it since more than a year ago. By now I can't test it because my subscription is over.

Here is the usage:

usage: symfonycasts_scraper.py [-h] [--start START] [--end END] --course COURSE

optional arguments:
  -h, --help       show this help message and exit
  --start START    download from
  --end END        download to
  --course COURSE  Course's name
  
COURSE is not optional, you must provide it. For example:

```
$ symfonycasts_scraper.py --course symfony
```

It will return the video links from the [Stellar Development with Symfony 4](https://symfonycasts.com/screencast/symfony).

Probably it has some bugs. Feel free to help.
