import time
from bs4 import BeautifulSoup
import os
from optparse import OptionParser
import datetime
import gevent
from gevent import monkey
monkey.patch_all()
import requests
from gevent.pool import Pool

# paramaters to be defined
website = 'http://konachan.com/post'
download_path = '/home/chaos/opt/pip'
tags = ''
pages = 1
image_count = 1
concurrency_limit = 20


def dpic(fadr):
    name = requests.utils.unquote(fadr[fadr.rfind('/') + 1:])
    if os.path.isfile(download_path + '/' + name):
        return
    if not os.path.isdir(download_path):
        os.makedirs(download_path)
    print('Downloading ' + name[name.rfind('/') + 1:])
    content = requests.get(fadr)
    with open(download_path + '/' + name, 'wb') as f:
        f.write(content.content)
    print('Finished downloading {}'.format(name))


def dpage(page, pool):
    main_page = requests.get(website, params={'tags': tags, 'page': page})
    soup = BeautifulSoup(main_page.text, 'html.parser')
    images = soup.find_all('a', class_='directlink')
    #soup.find_all('a', {'class': 'directlink smallimg'})
    for img in images:
        pool.spawn(dpic, img['href'])
        time.sleep(0.5)


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
    download_path += ('/' + str(datetime.date.today()))
    if options.tag:
        tags = options.tag
    if options.page:
        pages = int(options.page)
    if options.url:
        website = options.url
    if options.directory:
        download_path = options.directory

    pool = Pool(concurrency_limit)
    # Downloading files
    for i in range(pages):
        dpage(i + 1, pool)
    pool.join()
