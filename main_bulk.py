import requests
import time
from bs4 import BeautifulSoup
import os
from optparse import OptionParser
import datetime
import threading

# paramaters to be defined
website = 'http://konachan.net/post'  # 'http://lolibooru.moe/post'
download_path = '/home/chaos/opt/pip/white'
tags = ''
pages = 1
image_count = 1


class dThread(threading.Thread):
    def __init__(self, fadr):
        threading.Thread.__init__(self)
        self.fadr = fadr

    def run(self):
        name = requests.utils.unquote(self.fadr[self.fadr.rfind('/') + 1:])
        self.iname = name
        if os.path.isfile(download_path + '/' + name):
            return
        if not os.path.isdir(download_path):
            os.mkdir(download_path)
        print('Downloading ' + name[name.rfind('/') + 1:])
        content = requests.get(self.fadr)
        with open(download_path + '/' + name, 'wb') as f:
            f.write(content.content)


def dpage(page):
    main_page = requests.get(website, params={'tags': tags, 'page': page})
    soup = BeautifulSoup(main_page.text, 'html.parser')
    images = soup.find_all('a', class_='directlink')
        #soup.find_all('a', {'class': 'directlink smallimg'})
    threads = []
    for img in images:
        t = dThread('http:' + img['href'])
        t.start()
        threads.append(t)
        time.sleep(0.5)
    for t in threads:
        t.join()
        print('Fnished downloading {}'.format(t.iname))


def arguments():
    parser = OptionParser()
    parser.add_option("-t", "--tag", help="the tags of picture you want")
    parser.add_option('-p', '--page', help='pages of images you want')
    parser.add_option('-u', '--url', help='url of the target website')
    parser.add_option(
        '-d', '--directory', help='directory where pictures are to be stored')
    return parser.parse_args()


if __name__ == '__main__':
    # processing args
    (options, args) = arguments()
    # download_path += ('/' + str(datetime.date.today()))
    if options.tag:
        tags = options.tag
    if options.page:
        pages = int(options.page)
    if options.url:
        website = options.url
    if options.directory:
        download_path = options.directory

    # Downloading files
    for i in range(pages):
        dpage(i + 1)
