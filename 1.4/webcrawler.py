import urllib.request
import ssl
import re
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.url = "https://sport050.nl/sportaanbieders/alle-aanbieders/"
        self.soup = self.open_url(self.url)
        self.sub_urls = self.read_hrefs(self.soup)
        self.sub_urls = [s for s in self.sub_urls if '<a href="/sportaanbieders' in str(s)]
        self.sub_urls = self.sub_urls[3:]
        self.pointer = -1

    def hack_ssl(self):

        """ Ignores the certificate errors
        """

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def open_url(self, url):

        """ 
        
        Processes a URL file, treating it as a large string,
        performs cleanup on the HTML content to enhance readability. 
        Input is a URL, and the output is a soup object.

        """

        ctx = self.hack_ssl()
        html = urllib.request.urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def read_hrefs(self, soup):

        """ 
        Retrieve a collection of anchor tags from a soup object, 
        extract the href attributes, and display them. The input should be a soup object.
        """

        reflist = []
        tags = soup('a')
        for tag in tags:
            reflist.append(tag)
        return reflist

    def read_li(self, soup):
        lilist = []
        tags = soup('li')
        for tag in tags:
            lilist.append(tag)
        return lilist

    def get_phone(self, info):
        reg = r"(?:(?:00|\+)?[0-9]{4})?(?:[ .-][0-9]{3}){1,5}"
        phone = [str(s) for s in info if 'Telefoon' in str(s)]
        try:
            phone = phone[0]
        except IndexError:
            phone = [str(s) for s in info if re.findall(reg, str(s))]
            try:
                phone = phone[0]
            except IndexError:
                phone = ""
        return phone.replace('Facebook', '').replace('Telefoon:', '')

    def get_email(self, soup):
        try:
            email = [str(s) for s in soup if '@' in str(s)]
            email = str(email[0])[4:-5]
            bs = BeautifulSoup(email, features="html.parser")
            email = bs.find('a').attrs['href'].replace('mailto:', '')
        except:
            email = ""
        return email

    def remove_html_tags(self, text):

        """
        Removes html tags from a string

        """
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def fetch_sidebar(self, soup):

        """ 
        Processes an HTML file, treating it as a sizable string, and carries out formatting enhancements on the HTML content to improve its legibility.
        Input is an HTML file, and the output is structured data in the form of tables.
        """
        sidebar = soup.findAll(attrs={'class': 'sidebar'})
        return sidebar[0]

    def extract(self, url):
        text = str(url)
        text = text[26:].split('"')[0] + "/"
        return text
    def __iter__(self):
        self.pointer = 0
        while self.pointer < len(self.sub_urls):
            sub = self.extract(self.sub_urls[self.pointer])
            site = self.url[:-16] + sub
            soup = self.open_url(site)
            info = self.fetch_sidebar(soup)
            info = self.read_li(info)
            phone = self.get_phone(info)
            phone = self.remove_html_tags(phone).strip()
            email = self.get_email(info)
            email = self.remove_html_tags(email).replace("/", "")
            yield f"{site} ; {phone} ; {email}"
            self.pointer += 1

crawler = Crawler()
for data in zip(crawler, range(5)):
    print(data[0])
