#!/usr/bin/python2
from __future__ import print_function
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from functools import wraps
from pyvirtualdisplay import Display
import csv
import os
import sys
import re
import argparse
import pickle
import pyautogui
import time
import getpass


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


def save_cookies(browser):
    try:
        pickle.dump(browser.get_cookies(), open("cookies.pkl","wb"))
        print('Cookies Saved: {}'.format(os.getcwd()))
        return True
    except:
        print('Cookies Not Saved')
        return False


def retrieve_cookies(browser):
    cookie_count = 0
    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            browser.add_cookie(cookie)
            cookie_count += 1
        print('{} Cookies retrieved'.format(cookie_count))
        return True
    except:
        return False    


def good_url(url_link):
    if 'http' not in url_link:
        return False
    else:
        return True


def export_csv(browser):
    pwd = os.getcwd()
    if os.path.exists(pwd + '/Downloads/No Attachments _ 1 month (JIRA).csv'):
        print('File Exists, will download updated file')
        os.remove(pwd + '/Downloads/No Attachments _ 1 month (JIRA).csv')
    else:
        print('file doesnt exist')
    time.sleep(4)
    browser.get('https://lowesinnovation.atlassian.net/issues/?filter=14285&atlOrigin=eyJpIjoiNzY3MTQ1ZmEwYmYzNDVmOGIyNDkzNTM2NTA3YWRiYjUiLCJwIjoiaiJ9')
    export = click_button(browser, 'Export', selector_type='span', click=True)
    export_all_csv = browser.find_element_by_id('allCsvFields')
    export_all_csv.click()
    time.sleep(2)
    pyautogui.hotkey('down')
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(2)
    if not os.path.exists(pwd + '/Downloads/No Attachments _ 1 month (JIRA).csv'):
        pyautogui.hotkey('alt', 'tab')
        time.sleep(1)
        pyautogui.hotkey('down')
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(2)
    if not os.path.exists(pwd + '/Downloads/No Attachments _ 1 month (JIRA).csv'):
        print('File not downloaded, exiting script')
        sys.exit()
    return pwd + '/Downloads/No Attachments _ 1 month (JIRA).csv'


def log_in_to_jira(browser, username, password, logged_in):
    login_form = browser.find_element_by_id('username')
    send_login = login_form.send_keys(username)
    send_enter = login_form.send_keys(Keys.ENTER)
    while True:
        print('Logging in')
        try:
            login_auth = browser.find_element_by_id('password')
            break
        except:
            login_auth = browser.find_element_by_xpath('//id[contains(text(), "password")]')
            break
        finally:
            time.sleep(1)
    send_auth = login_auth.send_keys(password)
    send_keys = login_auth.send_keys(Keys.ENTER)
    time.sleep(12)
    assert "Log in" not in browser.title
    logged_in = True
    return True


def jira_login(browser, username, password):
    login_form = browser.find_element_by_id('username')
    send_login = login_form.send_keys(username)
    send_enter = login_form.send_keys(Keys.ENTER)
    while True:
        try:
            login_auth = browser.find_element_by_id('password')
            break
        except:
            login_auth = browser.find_element_by_xpath('//id[contains(text(), "password")]')
            break
        finally:
            time.sleep(1)
    send_auth = login_auth.send_keys(password)
    send_keys = login_auth.send_keys(Keys.ENTER)
    time.sleep(4)
    if send_auth:
        return True
    else:
        sys.exit('Unable to login to JIRA. Exiting script')


def image_url_getter(webpage):
    '''
    returns Image URL on page of passed URL
    '''
    if 'http' not in webpage:
        return False 
    website_url = urllib2.urlopen(webpage)
    soup = BeautifulSoup(website_url, 'lxml')
    img_container = soup.find('img', class_='met-product-image')['src']
    return img_container


def image_downloader(image_url):
    filename = image_url.split('/')
    filenamecount = 0
    try:
        os.chdir('/tmp/')
        #print('Changed to /tmp/ folder')
    except:
        os.makedirs(os.getcwd() + '/tmp/')
        os.chdir(os.getcwd() + '/tmp/')
        #print('Creating and Navigating /tmp/ folder')
    try:
        with open(filename[-1], 'wb') as imagefile:
            imagefile.write(urllib2.urlopen(image_url).read())
            filenamecount += 1
            print('Downloaded file {} to {}'.format(filename[-1], os.getcwd()))
            return True
    except:
        filename = filename[-1] + str(filenamecount)
        with open(filename[-1], 'wb') as imagefile:
            imagefile.write(urllib2.urlopen(image_url).read())
            filenamecount += 1
            print('--Downloaded file {} to {}'.format(filename[-1], os.getcwd()))
            return True


def click_button(browser, button_name, selector_type='span', click=True):
    while True:
        print('Attempting to find DOM {}'.format(button_name))
        try:
            #print('click_button func attempt 1')
            button = browser.find_element_by_xpath('//' + selector_type + '[@aria-label="' + button_name +'"]')
        except:
            #print('click_button func attempt 2')
            button = browser.find_element_by_xpath('//' + selector_type + '[contains(text(), "' + button_name +'")]')
        if button:
            if click:
                button.click()
                print('Click ' + button_name + ' = Success')
                return True
            else:
                print(button_name + ' was found, but not clicked')
                return button


def send_img_link(browser, image_link):
    pyautogui.typewrite(os.getcwd() + '/' + image_link.split('/')[-1])
    #print('Sent ' + os.getcwd() + '/' + image_link.split('/')[-1] + ' to file browser')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('enter')
    #print('Sent Enter command x2')
    time.sleep(10)
    return True   


def search_for_url(item_number):
    search_url = 'https://www.lowes.com/search?searchTerm=' + str(item_number) # 1336779
    try:
        product_url = urllib2.urlopen(search_url).url
    except Exception as e:
        print(e)
    return product_url

def is_link_check(text):
    search_terms = re.compile(r'[URL|Online Link]:\shttps://www.lowes.com/\w+/.+/\d+')  # [https:|http:]./\d+?
    try:
        results = re.search(search_terms, text)
    except TypeError:
        print('ERROR: TypeError')
        return 'NA'
    if results:
      #print(results.group(0).split(' ')[-1])
      return results.group(0).split(' ')[-1]
    else:
      #print('No Link Found')
      return 'NA None Type'


def upload_exist_check(browser, image_link):
    try:
        jpg_filename = image_link.split('/')[-1]
        #print('Checking if image has been uploaded')
        time.sleep(10)
        try:
            existing_attachment = click_button(browser, jpg_filename, 'div', click=False)
        except:
            existing_attachment = click_button(browser, jpg_filename.split('.')[0] + '[1].' + jpg_filename.split('.')[-1], 'div', click=False)
        print('File already Uploaded')
        return True
    except:
        print('File does not exist, Starting Upload')
        return False


def upload_image_to_jira(site, browser, image_link):
    #print('Running upload_image_to_jira func')
    if not good_url(site) or not good_url(image_link):
        return False
    browser.get(site)
    if  upload_exist_check(browser, image_link):
        return False
    try:
        dload = image_downloader(image_link)
        if dload:
            print('Downloaded successfully')
    except NameError as e:
        print('ERROR: {}'.format(e))
        return False
    except:
        print('ERROR: Download Unsuccessful: Continuing script')
        return False
    if click_button(browser, 'Add attachment'):
        print('click_attachment func = True')
    else:
        print('ERROR: Unable to find/select "Add attachment" on page, will attempt once more.')
        click_button(browser, 'Add attachment')
    if click_button(browser, 'Upload a file'):
        print('click_upload func = True')
    else:
        print('ERROR: Unable to find/select "Upload a file" on page, will attempt once more.')
        click_button(browser, 'Upload a file')
    print('starting Wait [10]')
    time.sleep(10)
    print('Wait Over [10] Finish Upload')
    if send_img_link(browser, image_link):
        print('Image file sent')
    click_button(browser, 'Insert a file')
    print('starting Wait [20] Sleep')
    time.sleep(20)
    print('Wait Over [20] Finish Load+Enter')
    print('upload_image_to_jira func done')
    return True


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
            if url_link == 'NA':
                url_link = search_for_url(item_number)
                if 'https://www.lowes.com/search?searchTerm=' in url_link:
                    url_link = ['NA']
            url_list.append(tuple((jira_column, url_link)))
    return url_list  # ['List', 'to', 'Loop', 'Over']


@timing
def main():
    #display = Display(visible=0, size=(800, 600))
    #display.start()
    password = getpass.getpass('Type JIRA password: ')
    password2 = getpass.getpass('Verify JIRA password: ')
    while password != password2:
        print('Passwords do not match, please try again')
        password = getpass.getpass('Type JIRA password: ')
        password2 = getpass.getpass('Verify JIRA password: ')
    parser = argparse.ArgumentParser(description='Search for Audits within a given CSV File, If second CSV given, will give difference between')
    parser.add_argument('-f', '--file', help='CSV file to process', type=str) # Input CSV File
    parser.add_argument('-u', '--user', help='Username for JIRA', type=str)
    args = parser.parse_args()
    username = args.user
    if not username:
        try:
            username = str(raw_input('Provide JIRA Username: '))
        except NameError:
            username = str(input('Provide JIRA Username: '))
    print('JIRA Username: {}'.format(username))
    webriver_path = {'laptop':'C:\\Users\\Ben ASUS\\Documents\\Python Files\\chromedriver',
                     'tablet':'C:\\Users\\admin\\Documents\\Files to test with\\chromedriver',
                     'cc_machine':'C:\\Users\\Tpog-Local\\Documents\\Python_Files\\chromedriver',
                     'rpi':'/home/pi/PyScripts/geckodriver'}
    # browser = webdriver.Chrome(executable_path=webriver_path['cc_machine'])
    browser = webdriver.Firefox(executable_path=webriver_path['rpi'])
    browser.implicitly_wait(15)
    browser.get('https://lowesinnovation.atlassian.net/browse/CD-4330')
    pwd = os.getcwd()
    try:
        input_csv_file = args.file
    except AttributeError:
        input_csv_file = None
    logged_in = False
    if not logged_in:
        logged_in = log_in_to_jira(browser, username, password, logged_in)
    row_count = 0
    if input_csv_file == None:
        input_csv_file = export_csv(browser)
        print(input_csv_file)
    urls = csv_parser(input_csv_file)
    urlList = []
    for jira, url in urls:
        print('URLs remain: {}'.format(len(urls) - row_count))
        urlList += url
        url_img_link = image_url_getter(url)
        #print(url_img_link)
        #print(url)
        if url_img_link == False:
            row_count += 1
            continue
        jira_url = 'https://lowesinnovation.atlassian.net/browse/' + jira
        #print(jira_url)
        browser.get(jira_url)
        upload_image_to_jira(jira_url, browser, url_img_link)
        row_count += 1
    browser.close()
    print('Done')



if __name__ == '__main__':
    main()
