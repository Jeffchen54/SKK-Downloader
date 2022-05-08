"""
Simple image tab downloader for chan.sankakucomplex.com using a different approach
Developed since widely available image grabbing softwares
have been defeated by erroneous loading employed by Sankaku
to block batch downloaders.

Compatible with Firefox only with dark mode settings

@author Jeff Chen
@created 4/5/2022
@modified 5/5/2022
@version 0.7
- Added network loss retry where program will continuous attempt to proceed when network is cut off
- Setting to increase initial link load time
- Add minimize option
- Added scrolling confirmation option
- Added several other download types
- Fixed bug where timeout counter concat threw an exception
- Fixed bug where timeout counter was not being incremented
- Improved code organization
- Add timeout where if a file fails to be downloaded, it is skipped and save to a log
- Fixed several download exceptions
- TODO bypass download limit

"""
import time
from datetime import timedelta
import os
from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import urllib.request
from selenium.common.exceptions import TimeoutException
from queue import Queue
import keyboard
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import http


########################## REQUIRED VARIABLES ########################################
# Absolute path to Firefox profile
PROFILE_PATH = r'C:/Users/chenj/AppData/Roaming/Mozilla/Firefox/Profiles/8gtgo2sw.default-release'
# Absolute path to temp folder, stores profiles used by threads
TEMP_PATH = r'C:/Users/chenj\Downloads/fun/src/temp'
# folder to save content to
folder = r'C:/Users/chenj/Downloads/fun/img/'
# Absolute path to save logs
LOG_PATH = r'C:/Users/chenj/Downloads/fun/logs/'
########################## SETTING VARIABLES ########################################
# Maximum number of times a window can timeout before using failsafe measures
MAXNUMTIMEOUT = 5
# Only checked when MAXTIMEOUT is triggered, number of timeouts for a single file before quitting
GLOBALMAXTIMEOUT = 1 * MAXNUMTIMEOUT
SCROLL_PAUSE_TIME = 2       # Time between scrolls for infscroll in seconds
# Number of scrolls per cycle for infscroll (connection test done after each cycle, more cycles means more accuracy but less performance)
SCROLLSPERCYCLE = 7
PAUSEKEY = "alt"            # Key to pause program between downloads
# Amount of time to wait for a network disconnect to be resolved before trying again
NETWORK_LOSS_TIME = 30
LINK_LOAD_TIME = 10         # Amount of time to wait after a link is opened
# To minimize browser automatically or not, browser may flash upon initializing
MINIMIZE = False
SCROLL_CONFIRMATION = False  # Require user confirmation when scrolling is complete
HTTP_ERROR_TIMEOUT = 30      # Seconds to wait before for HTTP error
#######################################################################################################
imgNo: int = 1   # Used to check if a file is downloaded
start_time: float  # when the program started
failed: int = 0  # Number of failed files


class Error(Exception):
    """Base class for other exceptions"""
    pass


class UnknownFileTypeException(Error):
    """Raised when file type cannot be determined"""
    pass


class MaxDownloadTimeoutException(Error):
    """Raised when global timeouts is met"""
    pass


def selenium_reinit(driver: Firefox, url: str) -> Firefox:
    """
    Quits driver and initializes another driver using selenium_init()
    In new driver, open url in new tab and switch to that tab

    In visual studios, code is shown as unreachable, however,
    this is wrong and the code actually runs

    Param:
        driver: driver to reinitialize
        url: current url driver is on
    Pre: driver has not quit()
    Return: reinitialized driver
    """
    driver.quit()                   # Exit old driver
    driver = selenium_init()        # Create another driver
    time.sleep(5)                   # Wait before opening a tab
    # Open url in another tab
    opened = False
    while opened == False:
        try:
            driver.execute_script('window.open("{}","_blank");'.format(url))
            # Switch to the tab with content
            driver.switch_to.window(driver.window_handles[1])
            opened = True
        except WebDriverException:
            print("Connection loss detected, sleeping for 30 seconds", flush=True)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(30)
    return driver


def keypress_pause(driver: Firefox) -> None:
    """
    Pauses program execution when a key is currently being pressed, entering a key to proceed

    params:
        driver: active selenium driver
    """
    if(keyboard.is_pressed(PAUSEKEY)):
        a = input("Enter 'y' to continue or 'n' to end> ")
        while(a != 'y'):
            if(a == 'n'):
                print("Terminating program")
                driver.quit()
                exit()


def guess_ext_type(fname: str) -> str:
    """
    Given a file name, determine file type

    Params:
        fname: file name
    Return: file extension (".png", ".webm",...), None if cannot be determined
    """
    if(".gif" in fname):
        return ".gif"
    elif(".jpg" in fname):
        return ".jpg"
    elif(".png" in fname):
        return ".png"
    elif("jpeg" in fname):
        return ".jpeg"
    elif(".mp4" in fname):
        return ".mp4"
    elif(".swf" in fname):
        return ".swf"
    elif(".webp" in fname):
        return ".webp"
    elif(".webm" in fname):
        return".webm"
    elif(".mov" in fname):
        return ".mov"
    return None

def sankaku_bad_src(driver:Firefox, src:str) -> bool:
    if("https://s.sankakucomplex.com/images/channel-dark-logo.png" in src):
        print("src loaded unproperly, refreshing window", flush=True)
        driver.get(driver.current_url)
        time.sleep(15)
        return False
    return True

def selenium_save_sankaku(driver:Firefox, src:str, url:str, downloadExt:str, req:urllib.request.Request, ssize:int, resp)->None:
    CHUNK = 16 * 1024
    print("Saving: ", src, flush=True)
    c = False
    while c == False:
        with open(folder + sankaku_postid_strip(url) + downloadExt, "wb") as fd:
            #downloaded = False
            #while downloaded == False:
            #    chunk = resp.read(CHUNK)
            #    if not chunk:
            #        downloaded = True
            #    fd.write(chunk)
            fd.write(resp.read())
        fd.close()
        localSz = os.path.getsize(folder + sankaku_postid_strip(url) + downloadExt)
        if localSz == ssize:
            c == True
        else:
            print("local size: ", str(localSz), " server size: ", str(ssize), flush=True)
            driver.get(driver.current_url)
            print("Restarting download in ", HTTP_ERROR_TIMEOUT, " seconds")
            time.sleep(HTTP_ERROR_TIMEOUT)

def selenium_save_with_url(driver: Firefox, url: str, xpath: str, downloadExt: str) -> bool:
    """
    Attempts to save a file at a specified url's xpath using driver. File is saved with the extension
    specified by downloadExt. If a url returns an error image, driver current handle is refreshed
    and nothing is downloaded
    Params:
        driver: Active selenium firefox window
        url: url to download file from
        xpath: HTML xpath where file to download is located
        downloadExt: downloaded file's extension (.mp4,.swf,...). None to guess file type
    Pre: Current page is url
    Post: content on current selinium page downloaded to folder. Content downloaded uses postid as file name
            imgno incremented upon success.
    Return: True if download succeeded and false otherwise
    Raise: UnknownFileTypeException when file type cannot be determined
    """
    global imgNo
    l = driver.find_element(By.XPATH, xpath)
    src = l.get_attribute('src')

    # Check if error image is loaded
    if("https://s.sankakucomplex.com/images/channel-dark-logo.png" in src):
        print("src loaded unproperly, refreshing window", flush=True)
        driver.refresh()
        time.sleep(5)
        return False

    # Set headers and grab file at the source
    okay = False
    while not okay:
        try:
            req = urllib.request.Request(src,
                                        headers={
                                            'User-agent':
                                            'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
            resp = urllib.request.urlopen(req)
            okay = True
        except urllib.error.URLError as e:
            print("Not found error, restarting in 30 seconds")
            print(e)
            driver.get(driver.current_url)
            time.sleep(25)
            urllib.request.urlopen(req)
            time.sleep(5)

    # determine source file type if unspecified
    if(downloadExt == None):
        downloadExt = guess_ext_type(src)

        if downloadExt == None:
            raise UnknownFileTypeException(
                "Cannot determine file extension type")

    # Download file into local storage
    downloaded = False
    while not downloaded:
        with open(folder + sankaku_postid_strip(url) + downloadExt, "wb") as fd:
            print("Saving: ", src, flush=True)
            try:
                fd.write(resp.read())
                downloaded = True
            except http.client.IncompleteRead:
                print("Less bytes than expected, refreshing and resuming after 30 seconds")
                driver.get(driver.current_url)
                time.sleep(25)
                urllib.request.urlopen(req)
                time.sleep(5)
            fd.close()
    imgNo += 1
    return True

def write_to_log(logn: str, line: str) -> None:
    """
    Appends line to log file logn within LOG_PATH

    Param:
        logn: name of log file without directory
        line: line to append to log file
    """
    log_path = LOG_PATH + logn
    if not os.path.exists(log_path):
        open(log_path, 'a').close()

    with open(log_path, "a") as myfile:
        myfile.write(line + "\n")
    myfile.close()
    print("Wrote \"", line, "\" in \"", log_path, "\"\n", flush=True)


def selenium_save_image(driver: Firefox, url: str) -> Firefox:
    """
    Saves an content on the current tab using the following system:
    1) Check if a video exists on window, if not then
    2) Check if a embed exists on window, if not then
    3) Check if a image exists on window, if not then
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
    Raise MaxDownloadTimeoutException: max global timeouts reached
    """
    global failed
    global_timeout = 0
    oldImgNo = imgNo
    timeout = 0
    # If image exists
    while(imgNo == oldImgNo):
        time.sleep(1)
        if(timeout == MAXNUMTIMEOUT):
            if(global_timeout >= GLOBALMAXTIMEOUT):
                write_to_log("link - " + str(int(start_time)) + ".txt", url)
                failed += 1
                raise MaxDownloadTimeoutException(
                    url + " download reached max timeouts")
            driver = selenium_reinit(driver, url)
            timeout = 0
        try:
            # mp4
            try:
                selenium_save_with_url(driver, url, '//video', None)
            except NoSuchElementException:
                # flash
                try:
                    selenium_save_with_url(driver, url, '//embed', None)
                except NoSuchElementException:
                    # Static image + gifs
                    selenium_save_with_url(driver, url, '//img[1]', None)
        except (TimeoutException, WebDriverException):
            timeout += 1
            global_timeout += 1
            print("Timeout has occured - Timeout counter: " +
                  str(timeout) + " Global timeout: " + str(global_timeout))
            selenium_resolve_slowdown(driver, url)
    return driver


def sankaku_postid_strip(url: str) -> str:
    """
    Strips a sankaku url and returns the post id referred to by the url
    """
    tokens = url.split("/")
    return tokens[len(tokens)-1]


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
        time.sleep(5)
    except WebDriverException:
        print("Connection loss detected, sleeping for 30 seconds", flush=True)
        time.sleep(30)


def selenium_network_test(driver: Firefox) -> bool:
    """
    Checks if there is wifi, if there is no wifi, halt program execution until
    wifi is detected
    To be used between scrolling cycles in infscroll()

    Param:
        driver: active selenium driver
    Return: true if network has not been disconnected, false if network has been disconnected
    """
    opened = False
    connected = True
    while(opened == False):
        try:
            driver.execute_script(
                'window.open("","_blank");')   # Try to open website in another tab
            # Close the opened window
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://chan.sankakucomplex.com/")
            opened = True
            driver.close()
            # Return to previous window
            driver._switch_to.window(driver.window_handles[0])
        except WebDriverException:
            print("Connection loss detected, sleeping for 30 seconds", flush=True)
            # Close the opened window
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            # Return to previous window
            driver._switch_to.window(driver.window_handles[0])
            time.sleep(NETWORK_LOSS_TIME)
            connected = False
    return connected


def selenium_infscroll(driver: Firefox) -> None:
    """
    Scrolls to the end of the selenium window

    Param:
        driver: selenium window to scroll to the bottom of
    """
    print("Scrolling...", flush=True)
    html = driver.find_element_by_tag_name('html')
    # Get scroll height
    last_height = driver.execute_script(
        "return window.pageYOffset + window.innerHeight")

    while True:
        # Scroll down to bottom, multiple scrolls done just in case
        for i in range(0, SCROLLSPERCYCLE):
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(SCROLL_PAUSE_TIME)

        # Network check
        if(selenium_network_test(driver) == False):
            connected = False
            while connected == False:
                try:
                    driver.get(driver.current_url)
                    time.sleep(5)
                    connected = True
                    html = driver.find_element_by_tag_name('html')
                except WebDriverException:
                    selenium_network_test(driver)
        elif driver.execute_script("return window.pageYOffset + window.innerHeight") == 0:
             driver.get(driver.current_url)
             time.sleep(5)
        else:
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script(
                "return window.pageYOffset + window.innerHeight")
            if new_height == last_height:
                if SCROLL_CONFIRMATION:
                    if(input('Type y if scrolling is complete, n to continue scrolling: ').lower() == 'y'):
                        break
                    else:
                        print("Scrolling...", flush=True)
                else:
                    break
            last_height = new_height

    time.sleep(SCROLL_PAUSE_TIME)
    print("Scrolling completed", flush=True)


def selenium_init() -> Firefox:
    """
    Initializes and opens a selinium Firefox window with custom profile path PROFILE_PATH

    return: active selenium Firefox driver on home screen 
    """
    print("Initializing Selenium, please wait...", flush=True)
    opt = Options()
    opt.add_argument("-profile")
    opt.add_argument(PROFILE_PATH)
    driver = webdriver.Firefox(options=opt)
    driver.set_script_timeout(15)
    driver.set_page_load_timeout(15)
    if(MINIMIZE):
        driver.minimize_window()
    return driver


def exists(dir, substr: str) -> bool:
    """
    Checks if a filename that contains substr exists in dir

    Param:
        dir: directory
        str: filename to check if exists in directory
    Return: true if exists, false if not
    """
    for entry in dir:
        if(entry.is_file() and substr in entry.name):
            return True
    return False


def sankaku_url_strip(url: str) -> str:
    """
    Strips 2 kinds of urls into their base form:
    1) https://chan.sankakucomplex.com/?tags=tag%tag%tag%tag&page=1
    Contains page number and tag(s). Formatting of tags does not matter

    2) https://chan.sankakucomplex.com/?tags=tag+tag+tag+tag+-tag&commit=Search
    Contains tag mentioned page was from a search and tag(s). Formatting of tags does not matter

    Base form: https://chan.sankakucomplex.com/?tags=tag+tag+tag+tag+-tag
    Contains only tags

    Param:
        str: sankaku url in 1 of the 2 forms or in base form
    Return: url in base form
    """
    tokens = url.split("&")
    return tokens[0]


def sankaku_url_set_next(url: str, postid: str) -> str:
    """
    Inserts next=<postid>& after the first ? in url and returns it.

    Param:
        url: sankaku url in base form (look at sankaku_url_strip)
        postid: used in token inserted into url
    Return: str with next added to it
    """
    tokens = url.split("?")
    return tokens[0] + "?next=" + postid + "&" + tokens[1]


def selenium_download_all(driver: Firefox, linkQ: Queue) -> Firefox:
    """
    Downloads all links stored in linkQ

    Param:
        driver: active selenium Firefox driver
        linkQ: Queue containing VALID download links.
    Return driver
    Post: active driver may be different after execution
    """
    while(linkQ.empty() == False):
        try:
            url = str(linkQ.get())
            print("Opening: ", url, flush=True)
            driver.execute_script(
                'window.open("{}","_blank");'.format(url))
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(LINK_LOAD_TIME)

            try:
                driver = selenium_save_image(driver, url)
            except MaxDownloadTimeoutException as e:
                print(e)
                print("Moving on to next file...")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(0.5)
        except WebDriverException:
            print(
                "Connection loss detected, sleeping for 30 seconds", flush=True)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            linkQ.put(url)
            time.sleep(30)
    return driver


def sankaku_remove_duplicates(urls: List[WebElement]) -> Queue:
    """
    *** TO BE OVERHAULED ***\n
    Trims all duplicate links in urls vs what is in dir

    Param:
        urls: List[WebElement] containing sankaku links
    Return: Queue of non-dupe links only
    """
    linkQ = Queue(-1)
    dir = os.scandir(folder)        # Everything in folder
    for a in urls:
        link = a.get_attribute('href')
        if("https://chan.sankakucomplex.com/post/show/" in link):
            if not exists(dir, sankaku_postid_strip(link)):
                linkQ.put(link)
            dir.close()
            # Make new iterator and set at beginning
            dir = os.scandir(folder)
    dir.close()
    return linkQ


def selenium_grab_sankaku_links(driver: Firefox) -> List[WebElement]:
    """
    Grabs all sankaku links on current page and returns them. 

    Param:
        driver: active Firefox driver
    Return: list of urls from current page
    Pre: driver is set to page to download content from, all links should be exposed
    """
    # Gets all urls on current page
    urls = driver.find_elements(by=By.XPATH, value='.//a')
    return urls


def selenium_visit(driver: Firefox) -> Firefox:
    """
    Opens all content urls from https://chan.sankakucomplex.com in another tab
    Pre: On page on sankakucomplex
    Post: All content urls opened in another tab, original tab returned to
    BUGS: issue where js scripts ran using Tampermonkey extension fail to activate on home page of sankakucomplex
    """
    url: str = None
    cont = False
    # Loops until all a valid url is inputted ###################################
    while not cont:
        url = input("URL to download from> ")
        if "chan.sankakucomplex.com" in url:
            cont = True
        else:
            print(
                "You did not enter a valid link, links contain https://chan.sankakucomplex.com")

    # Loop until url can be accessed, done this way due to possible network issues
    visited = False
    while(visited == False):
        try:
            driver.get(url)
            visited = True
        except WebDriverException:
            print(
                "Connection loss detected, sleeping for 30 seconds", flush=True)
            time.sleep(30)
    selenium_infscroll(driver)
    time.sleep(1)

    print("Processing urls and removing duplicate files...", flush=True)
    # Grabbing urls ##########################################################
    urls = selenium_grab_sankaku_links(driver)  # get all urls
    linkQ = sankaku_remove_duplicates(urls)     # remove dupes
    print(linkQ.qsize(), " urls to be processed", flush=True)

    # While loop made here, as long as linkQ length != 0, loop
    # multithreading also done here after breaking queue up

    # Download from each url #################################################
    driver = selenium_download_all(driver, linkQ)
    return driver


def main():
    global start_time
    start_time = time.monotonic()
    print("ImagesDownloader 0.7, by Jeff Chen 4/17/2022", flush=True)
    print("Warning: Please only operate in the console you have chosen to use. If you need to look up a tab, please use only the first tab or separate browser", flush=True)
    print("Current restrictions", flush=True)
    print("1) You are free to use your cursor during execution, program does not rely on keyboard or mouse; however, do not touch Selenium browser after you've inputted a valid url\n", flush=True)
    print("2) Note that there is a 100 page limit for free users (2000 imgs), check page depth workaround here -> https://forum.sankakucomplex.com/t/important-dont-purchase-sankaku-plus-yet-heres-why-addressing-sankaku-issues-29-days-and-not-fixed/18209/61", flush=True)
    print("3) If infinite scroll is not turned on, please enable it or not all files will be downloaded", flush=True)
    print("4) Sankaku likes to give error pages on loading even during normal use, VPNs can help and you can switch to a VPN during execution", flush=True)
    driver = selenium_init()
    driver = selenium_visit(driver)
    print("Exiting Selenium...")
    driver.quit()
    end_time = time.monotonic()
    print("Failed: ", str(failed), ", Stored in \"link - " + LOG_PATH + str(int(start_time)) + ".txt\"")
    print("Ran for ", timedelta(seconds=end_time - start_time))


if __name__ == "__main__":
    main()
