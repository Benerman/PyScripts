from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import csv
import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import pyautogui
import time
# from time import time
from functools import wraps


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap


def save_cookies(site, browser):
    # browser = webdriver.Chrome(executable_path='C:\\Users\\Ben ASUS\\Documents\\Python Files\\chromedriver')
    pickle.dump(browser.get_cookies(), open("cookies.pkl","wb"))
    print('Cookies Saved')


def retrieve_cookies(site):
    cookie_count = 0
    # browser = webdriver.Chrome(executable_path='C:\\Users\\Ben ASUS\\Documents\\Python Files\\chromedriver')
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)
        cookie_count += 1
    print('{} Cookies retrieved'.format(cookie_count))


def image_url_getter(webpage):
    '''
    returns URL of passed URL
    '''
    if 'http' not in webpage:
        return ''
    website_url = urllib2.urlopen(webpage)
    soup = BeautifulSoup(website_url, 'lxml')
    img_container = soup.find('img', class_='met-product-image')['src']
    # print(img_container)
    return img_container


def image_downloader(image):
    filename = image.split('/')
    filenamecount = 0
    pwd = os.getcwd()
    try:
        os.chdir(pwd + '\\tmp\\')
        print('Changed to \\tmp\\ folder')
    except WindowsError:
        os.makedirs(pwd + '\\tmp\\')
        os.chdir(pwd + '\\tmp\\')
        print('Creating and Navigating \\tmp\\ folder')
    except:
        pass
    try:
        with open(filename[-1], 'wb') as imagefile:
            imagefile.write(urllib2.urlopen(image).read())
            filenamecount += 1
            print('Downloaded file {} to {}'.format(filename[-1], os.getcwd()))
    except:
        filename = filename[-1] + str(filenamecount)
        with open(filename[-1], 'wb') as imagefile:
            imagefile.write(urllib2.urlopen(image).read())
            filenamecount += 1
            print('--Downloaded file {} to {}'.format(filename[-1], os.getcwd()))


def upload_image_to_jira(site, browser, image_link):
    # browser = webdriver.Chrome(executable_path='C:\\Users\\Ben ASUS\\Documents\\Python Files\\chromedriver')
    if 'http' not in site:
        return False
    if 'http' not in image_link:
        return False
    site = browser.get(site)
    try:
        login_form = browser.find_element_by_id('username')
        send_login = login_form.send_keys(username)
        login_form.send_keys(Keys.ENTER)
        login_auth = browser.find_element_by_id('password')
        browser.implicitly_wait(2)
        send_auth = login_auth.send_keys(password)
        login_auth.send_keys(Keys.ENTER)
    except:
        print('Already Logged In ? ? ?')
        # cookies_saved = True
    global cookies_saved
    if cookies_saved == False:
        save_cookies(site, browser)
        cookies_saved = True
        print('Saved Cookies')
    browser.implicitly_wait(7)
    # pickle.dump( browser.get_cookies() , open("cookies.pkl","wb"))
    try:
        jpg_filename = image_link.split('/')[-1]
        existing_attachment = browser.find_element_by_xpath('//div[@aria-label="' + jpg_filename.split('.')[0] + '[1].' + jpg_filename.split('.')[-1] + '"]')
        print('File already Uploaded')
        return False
    except:
        print('File does not exist, Starting Upload')
    try:
        attachment = browser.find_element_by_xpath('//span[@aria-label="Add attachment"]')
        attachment.click()
    except:
        browser.implicitly_wait(5)
        attachment = browser.find_element_by_xpath('//span[@aria-label="Add attachment"]')
        attachment.click()
    try:
        upload = browser.find_element_by_xpath('//span[contains(text(), "Upload a file")]')
        upload.click()
    except:
        browser.implicitly_wait(5)
        upload = browser.find_element_by_xpath('//span[contains(text(), "Upload a file")]')
        upload.click()
    time.sleep(3)
    pyautogui.typewrite(image_link)
    browser.implicitly_wait(3)
    pyautogui.hotkey('enter')
    browser.implicitly_wait(6)
    insert_file = browser.find_element_by_xpath('//span[contains(text(), "Insert a file")]')
    insert_file.click()
    time.sleep(3)
    return True


def is_link_check(text):
    search_terms = re.compile(r'URL:\shttps://www.lowes.com/\w+/.+/\d+')  # [https:|http:]./\d+?
    try:
        results = re.search(search_terms, text)
        #print(results)
    except TypeError:
        link = ['NA']
        return link
    try:
        link = results.group(0).split(' ')[-1] # url.group(0).split(' ')[1]
    except AttributeError:
        print('Link Checker Error')
        # print(results)
        # print(text)
        link = 'NA None Type'
    return link


def search_for_url(item_number):
    search_url = 'https://www.lowes.com/search?searchTerm=' + str(item_number) # 1336779
    try:
        product_url = urllib2.urlopen(search_url).url
    except Exception as e:
        print(e)
    return product_url


def csv_parser(input_name):
    url_list = []
    row_count = 0
    with open(input_name, mode="r", encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            description_column = row['Description']
            item_number = row['Issue id']
            jira_column = row['Issue key']
            row_count += 1
            url_link = is_link_check(description_column)
            if url_link == ['NA']:
                url_link = search_for_url(item_number)
                if 'https://www.lowes.com/search?searchTerm=' in url_link:
                    url_link = ['NA']
            url_list.append(tuple((jira_column, url_link)))
    return url_list  # ['List', 'to', 'Loop', 'Over']


#@timing
def main():
    row_count = 0
    urls = csv_parser(input_csv_file)
    urlList = []
    global cookies_saved
    cookies_saved = False
    for jira, url in urls:
        print('URLs remain: {}'.format(len(urls) - row_count))
        urlList += url
        url_img_link = image_url_getter(url)
        jira_url = 'https://lowesinnovation.atlassian.net/browse/' + jira
        upload_image_to_jira(jira_url, browser, url_img_link)
        row_count += 1
    browser.close()
    print('Done')


input_csv_file = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
if __name__ == '__main__':
    webriver_path = {'laptop':'C:\\Users\\Ben ASUS\\Documents\\Python Files\\chromedriver',
                     'tablet':'C:\\Users\\admin\\Documents\\Files to test with\\chromedriver',
                     'cc_machine':'C:\\Users\\Tpog-Local\\Documents\\Python_Files\\chromedriver',
                     'rpi':'/home/pi/PyScripts/chromedriver'}
    browser = webdriver.Chrome(executable_path=webriver_path['cc_machine'])
    main(username, password)
