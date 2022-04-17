"""
Simple image tab downloader for chan.sankakucomplex.com using a different approach
Developed since widely available image grabbing softwares
have been defeated by erroneous loading employed by Sankaku
to block batch downloaders.

Compatible with Firefox only with dark mode settings

@author Jeff Chen
@created 4/5/2022
@modified 4/17/2022
@version 0.5

changelog (0.5):
- Added flash download functionality

Future:
- append url to download names
- Logging
- .swf files

"""
import time
import os
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.request
from selenium.common.exceptions import TimeoutException
from queue import Queue


########################## MODIFY THESE 2 VARIABLES ONLY ##############################################
PROFILE_PATH = r'C:/Users/chenj/AppData/Roaming/Mozilla/Firefox/Profiles/8gtgo2sw.default-release'
folder = r'C:/Users/chenj/Downloads/fun/img/photos/sample/'
#######################################################################################################
# Starting count of images (affected by number of files in folder)
imgNo = 1


def selenium_reinit(driver: Firefox, url: str) -> Firefox:
    """
    Quits driver and initializes another driver using selenium_init()
    In new driver, open url in new tab and switch to that tab

    Param: 
        driver: driver to reinitialize
        url: current url driver is on
    Pre: driver has not quit()
    Return: reinitialized driver 
    """
    driver.quit()                   # Exit old driver
    driver = selenium_init()        # Create another driver
    # Open url in another tab
    driver.execute_script('window.open("{}","_blank");'.format(url))
    # Switch to the tab with content
    driver.switch_to.window(driver.window_handles[1])
    return driver


def selenium_save_image(driver: Firefox, url: str) -> Firefox:
    """
    Saves an content on the current tab using the following system:
    1) Check if a video (.mp4) exists on window, if not then
    2) Check if a embed (.swf) exists on window, if not then
    3) Check if a image (.png,.jpg,.jpeg,.gif) exists on window, if not then
    4) Refresh window and start over

    If a piece of content exists, it will be saved to folder and driver used to download
    the content will be returned.

    If a piece of content does not exists (1,2,3), then refresh window and increment timeout

    Once timeout reaches MAXNUMTIMEOUT, driver will be quit() and a new driver will be reinitialized
    to the starting. timeout counter will be reset.

    Param:
        driver: Selenium Firefox window to save content from
        url: URL linked to tab to save content from
    Return: driver which may or may not be the same driver in args

    Pre: folder must exists. Content to download on current tab of driver.
    Post: content on current selinium page downloaded to folder
    """
    global imgNo
    oldImgNo = imgNo
    timeout = 0
    # If image exists
    while(imgNo == oldImgNo):
        time.sleep(1)
        if(timeout == 5):
            driver = selenium_reinit(driver, url)
            timeout = 0
        try:
            # mp4
            try:
                l = driver.find_element(By.XPATH, '//video')
                src = l.get_attribute('src')
                req = urllib.request.Request(src,
                                             headers={
                                                 'User-agent':
                                                 'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
                resp = urllib.request.urlopen(req)
                with open(folder + str(imgNo) + ".mp4", "wb") as fd:
                    print("Saving: ", src, flush=True)
                    fd.write(resp.read())
                    imgNo += 1
            except:
                # flash
                try:
                    l = driver.find_element(By.XPATH, '//embed')
                    src = l.get_attribute('src')
                    req = urllib.request.Request(src,
                                                 headers={
                                                     'User-agent':
                                                     'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
                    resp = urllib.request.urlopen(req)
                    with open(folder + str(imgNo) + ".swf", "wb") as fd:
                        print("Saving: ", src, flush=True)
                        fd.write(resp.read())
                        imgNo += 1
                except:
                    # Static image + gifs
                    try:
                        # Get path of image
                        l = driver.find_element(by=By.XPATH, value='//img[1]')
                        src = l.get_attribute('src')

                        if("https://s.sankakucomplex.com/images/channel-dark-logo.png" in src):
                            print(
                                "src loaded unproperly, refreshing window", flush=True)
                            driver.refresh()
                            time.sleep(5)
                        else:
                            # Disguised requests to trick Sankaku
                            req = urllib.request.Request(src,
                                                         headers={
                                                             'User-agent':
                                                             'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
                            resp = urllib.request.urlopen(req)

                            # Determine type of file
                            type = ".png"
                            if(".gif" in src):
                                type = ".gif"
                            elif(".jpg" in src):
                                type = ".jpg"
                            elif("jpeg" in src):
                                type = ".jpeg"

                            # Download image
                            with open(folder + str(imgNo) + type, "wb") as fd:
                                print("Saving: ", src, flush=True)
                                fd.write(resp.read())
                                imgNo += 1

                    # If image does not exists
                    except:
                        selenium_resolve_slowdown(driver, url)
                        timeout += 1
        except TimeoutException:
            print("Timeout has occured - Timeout counter: " + timeout)
            selenium_resolve_slowdown(driver, url)
            timeout += 1
    return driver


def selenium_resolve_slowdown(driver: Firefox, url: str) -> None:
    """
    Resolves a situation where no content has been detected by refreshing the current page
    and waiting some time
    
    Param:
        driver: selenium browser to refresh
        url: url of page to regresh
    """
    try:
        print("No content detected, closing and reopening window: ", url, flush=True)
        driver.get(url)     # Reopen page
        time.sleep(15)
    except TimeoutException as ex:
        print("Exception has been thrown. " + str(ex))
        selenium_resolve_slowdown(driver, url)


def selenium_infscroll(driver: Firefox) -> None:
    """
    Scrolls to the end of the selenium window

    Param:
        driver: selenium window to scroll to the bottom of
    """
    print("Scrolling...", flush=True)
    SCROLL_PAUSE_TIME = 2
    html = driver.find_element_by_tag_name('html')

    # Get scroll height
    last_height = driver.execute_script(
        "return window.pageYOffset + window.innerHeight")

    while True:
        # Scroll down to bottom, multiple scrolls done just in case
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(
            "return window.pageYOffset + window.innerHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(SCROLL_PAUSE_TIME)
    print("Scrolling completed", flush=True)


def selenium_init() -> Firefox:
    """
    Initializes and opens a selinium Firefox window with custom profile path PROFILE_PATH
    """
    print("Initializing Selenium, please wait...", flush=True)
    opt = Options()
    opt.add_argument("-profile")
    opt.add_argument(PROFILE_PATH)
    driver = webdriver.Firefox(options=opt)
    driver.set_script_timeout(15)
    driver.set_page_load_timeout(15)
    return driver


def exists(dir, substr: str) -> bool:
    """
    Checks if a filename that contains substr exists in dir
    """
    for entry in dir:
        if(entry.is_file() and substr in entry.name):
            return True
    return False


def selenium_visit(driver: Firefox) -> Firefox:
    """
    Opens all content urls from https://chan.sankakucomplex.com in another tab
    Pre: On page on sankakucomplex
    Post: All content urls opened in another tab, original tab returned to
    BUGS: issue where js scripts ran using Tampermonkey extension fail to activate on home page of sankakucomplex
    """
    cont = True
    global imgNo
    while(cont == True):
        print("Type the sankaku url you want to visit:")
        url = input("URL> ")

        if("chan.sankakucomplex.com" not in url):
            print(
                "You did not enter a valid link, links contain https://chan.sankakucomplex.com")
        else:
            driver.get(url)
            selenium_infscroll(driver)
            time.sleep(1)

            # Get starting index
            numParsed = len(next(os.walk(folder))[2])
            imgNo = numParsed + 1
            print("Processing urls and removing duplicate files...", flush=True)
            # Make a deep copy of all urls.
            urls = driver.find_elements(by=By.XPATH, value='.//a')
            linkQ = Queue(-1)
            dir = os.scandir(folder)
            for a in urls:
                link = a.get_attribute('href')
                if("https://chan.sankakucomplex.com/post/show/" in link and not exists(dir, link)):
                    linkQ.put(link)
            print(linkQ.qsize(), " urls to be processed", flush=True)
            # Process each url and save their image if is valid
            while(linkQ.empty() == False):
                url = str(linkQ.get())
                print("Opening: ", url, flush=True)
                driver.execute_script(
                    'window.open("{}","_blank");'.format(url))
                time.sleep(3)
                driver.switch_to.window(driver.window_handles[1])
                driver = selenium_save_image(driver, url)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)
            cont = False
    return driver


def main():

    print("ImagesDownloader 0.3, by Jeff Chen 4/15/2022", flush=True)
    print("Warning: Please only operate in the console you have chosen to use. If you need to look up a tab, please use only the first tab or separate browser", flush=True)
    print("Current restrictions", flush=True)
    print("1) Only images or gifs work, flash game downloads or any videos will not work", flush=True)
    print("2) Requires TamperMonkey add-on and Handy Image script", flush=True)
    print("3) Cannot pause execution, can only end program by closing out of terminal or ctrl-c in some circumstances (ctrl-z may be able to pause effectively but untested)", flush=True)
    print("4) Only tested on Windows 10, other OS not tested", flush=True)
    print("5) You are free to use your cursor during execution, program does not rely on keyboard or mouse; however, do not touch Selenium browser after you've inputted a valid url\n", flush=True)
    print("6) Images are downloaded in order first to last, use 'order:id' tag to get downloads in correct order", flush=True)
    print("7) Note that there is a 100 page limit for free users (2000 imgs), check page depth workaround here -> https://forum.sankakucomplex.com/t/important-dont-purchase-sankaku-plus-yet-heres-why-addressing-sankaku-issues-29-days-and-not-fixed/18209/61", flush=True)

    driver = selenium_init()
    driver = selenium_visit(driver)
    time.sleep(0.5)
    print(imgNo - 1, " images saved to ", folder)
    print("Exiting Selenium...")
    driver.quit()


if __name__ == "__main__":
    main()
