import sys
import mechanize
import cookielib
import time
import random
from bs4 import BeautifulSoup

class AnonScrapper(object):

    """
        Main scrapper object.
        Use self.do_anonymous_scrapping after setting self.url
        (or use scrap() function)
        If safe is set to false and proxies.txt is not present it will
        do the request unproxied.

        TODO:  Reconcile proxies and safe-mode    
        TODO:  Random sleeps 
        TODO:  Random useragents
    """

    def __init__(self, safe=True, throttle=False):

        """
        Set properties

        ; safe:
        ; throttle:

        """

        self.browser = False
        self.data = False
        self.url = False
        self.safe = safe
        self.cj = False
        self.throttle = throttle

    def setup(self):

        """
        Setup scraping engine
        """

        # Browser Initiation
        self.browser = mechanize.Browser()

        # Set up cookie jar
        self.cj = cookielib.LWPCookieJar()
        self.browser.set_cookiejar(self.cj)

        # Set Browser options
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_gzip(True)
        self.browser.set_handle_redirect(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)

        # Follow refresh 0 but not hangs on refresh
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # User-Agent (this is cheating, ok?)
        self.browser.addheaders = [x for x in self.add_headers()]


    def anonymize(self):
        """
        Anonymize those browser properties that
        should be changed each time a url is invoked in order
        to minimize detection as a scrapper

        TODO: seperate out 'setup' to only include those properties that do not change,
              otherwise, place in 'anonymize' function 
        """

        pass


    def choose_random_user_agent(self):
        """
        Choose random 'user agent'


        TODO: Add user agents to randomly choose from
        """

        return 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'

    def add_headers(self):
        """
        Add various headers to the browser

        TODO:  Research what each of these headers does and decide whether to include or not

        """

        return [
            ('User-Agent', self.choose_random_user_agent()), 
            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
            ('Accept-Language', 'en-gb,en;q=0.5'),
            ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'),
            ('Keep-Alive', '115'),
            ('Connection', 'keep-alive'),
            ('Cache-Control', 'max-age=0')
            ]

    def throttle_scrape(self):

        """
        TODO:  Add a class property and functions that determine whether scraper has slept

        """
        sleep_time_each_scrape = int(60/self.throttle)+1
        print '**-Throttling-**-%s seconds-**' % (str(sleep_time_each_scrape))
        time.sleep(sleep_time_each_scrape)
       

    def scrape(self, url):

        """
        Scrape away
        """

        self.url = url
        if not self.browser:
            self.setup()
        
        if self.throttle:
            self.throttle_scrape()

        self.do_anon_scrapping()
        
        return self.data

    def do_anon_scrapping(self):

        """
        Scrapping engine
        """
        
        # proxy = self.proxy

        # if proxy or not self.safe:
        
        #     self.browser.set_proxies({"http": proxy})
        
        # elif not proxy and self.safe:
        #     raise Exception("No proxies.txt and safe mode specified")

        self.data = self.browser.open(str(self.url)).read()
         

    @property
    def proxy(self):
        """
        Get a random proxy
        """

        try:
            with open('proxies.txt', 'r') as proxy_file:
                return choice(proxy_file.readlines())
        except IOError:
            return False


if __name__ == "__main__":
    print AnonScrapper(safe=False, throttle=10).scrape("http://www.alexandriava.gov")