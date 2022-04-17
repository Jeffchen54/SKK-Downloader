"""
Simple image tab downloader for chan.sankakucomplex.com using a different approach
Developed since widely available image grabbing softwares
have been defeated by erroneous loading employed by Sankaku
to block batch downloaders.

Compatible with Firefox only with dark mode settings

@author Jeff Chen
@created 4/5/2022
@modified 4/17/2022
@version 0.4


Future:
- append url to download names
- Logging
- Removing and cleaning up code
- .swf files

"""
import time
from tokenize import String
import pyautogui as pg
import os
import mouse
import numpy as np
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
from selenium.common.exceptions import TimeoutException
from queue import Queue


# Misc variables
BORDER_COLOR = [27, 27, 27]       # Color of image border
ERROR_COLOR = [255, 255, 255]     # Border color of Sankaku error page
WAIT_COLOR = [250, 250, 250]      # Border color of Sankaku please wait page
# Pixel difference from center of one image to next image
IMAGE_DIFFERENCE = 420
NEXT_ROW = 3.5                  # Scrolls to move to next row of images
NEXT_GRID = 5.3                 # Scrolls needed to move to next grid of images
SCROLL_BUFFER = 0.5             # Seconds to wait for scrolling
CURSOR_MOVE_BUFFER = 0.1        # Seconds to wait for cursor movement
# Pixel steps to find center point, incresing value increases speed, decreasing value too much or big results in bugs
CENTER_TOLERANCE = 35
WINSIZE = [3840, 2160]           # Size of Firefox Window
# Path of Firefox custom profile
PROFILE_PATH = r'C:/Users/chenj/AppData/Roaming/Mozilla/Firefox/Profiles/8gtgo2sw.default-release'
# Last recorded Firefox resolution (used to optimize out duplicate calculations)
lastScreenSize = None
# Debugger switch, true for additional output, false for normal output
debug = False
demo = False                    # True for demo mode, false for not
clicks = 0                      # DEPRECATED
# Resolution of Windows resolution (screen resolution)
windowsRes = None
# Ratio of Selinium firefox browser to Windows resolution
ffToWinRatio = None
# Download directory (Absolute path)
folder = r'C:/Users/chenj/Downloads/fun/img/photos/'
imgNo = 1
failed = 0
topBorder = None
maxTabs = 5                     # Maximum number of opened tabs
driver = None


def selenium_reinit(driver:Firefox, url:str)->Firefox:
    driver.quit()                   # Exit old driver
    driver = selenium_init()        # Create another driver
    driver.execute_script('window.open("{}","_blank");'.format(url))    # Open url in another tab
    driver.switch_to.window(driver.window_handles[1])   # Switch to the tab with content
    return driver

def selenium_save_image(driver: Firefox, url:str) -> Firefox:
    """
    Saves the first image on the page.
    Supports gif and png

    Post: image or gif on selinium page downloaded inside folder
    """
    global imgNo
    downloaded = False
    oldImgNo = imgNo
    timeout = 0
    # If image exists
    while(imgNo == oldImgNo):
        time.sleep(1)
        if(timeout == 5):
            driver = selenium_reinit(driver, url)
            timeout = 0
        #mp4
        try:
            try:
                #l = deo = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[3]/video') 
                l = driver.find_element(By.XPATH, '//video') 
                src = l.get_attribute('src')   
                if("https://chan.sankakucomplex.com/post/show/" in src):
                    file1 = open("C:/Users/chenj/Downloads/fun/img/log.txt", "a")  # append mode
                    file1.write(src + "\n")
                    file1.close()
                    failed+=1
                    print("Failed download, writing to log")
                else:
                    req = urllib.request.Request(src,
                        headers = {
                        'User-agent':
                        'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0'})
                    resp = urllib.request.urlopen(req)
                    with open(folder + str(imgNo) + ".mp4","wb") as fd:
                        print("Saving: ", src, flush=True)
                        fd.write(resp.read())
                        imgNo += 1
            except:
                try:
                    # Get path of image
                    l = driver.find_element(by=By.XPATH, value='//img[1]')
                    src = l.get_attribute('src')    

                    if("https://s.sankakucomplex.com/images/channel-dark-logo.png" in src):
                        print("Failed download, restarting", flush=True)
                        driver.refresh()
                        time.sleep(5)
                    else:
                        # Disguised requests to trick Sankaku
                        req = urllib.request.Request(src,
                            headers = {
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
                        with open(folder + str(imgNo) + type,"wb") as fd:
                            print("Saving: ", src, flush=True)
                            fd.write(resp.read())
                            imgNo += 1
                            
                # If image does not exists
                except:
                    selenium_resolve_slowdown(driver, url)
                    timeout += 1
        except TimeoutException as ex:
            isrunning = 0
            print("Exception has been thrown. " + str(ex))
            selenium_resolve_slowdown(driver, url)
            timeout += 1
    return driver
    

def selenium_resolve_slowdown(driver: Firefox, url:str) -> None:
    """
    Refreshes a page 
    """
    try:
        print("No content detected, closing and reopening window: ", url, flush=True)
        driver.get(url)     # Reopen page
        time.sleep(15)
    except TimeoutException as ex:
        isrunning = 0
        print("Exception has been thrown. " + str(ex))
        selenium_resolve_slowdown(driver, url)


def selenium_infscroll(driver:Firefox)->None:
    """
    Scrolls to the end of the selenium window
    DEBUG: prints old scroll height vs new scroll height
    """
    print("Scrolling...", flush=True)
    SCROLL_PAUSE_TIME = 2
    html = driver.find_element_by_tag_name('html')

    # Get scroll height
    last_height = driver.execute_script("return window.pageYOffset + window.innerHeight")


    while True:
        # Scroll down to bottom
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
        new_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
        if(debug == True):
            print("OLD: ", last_height, "\tNEW: ", new_height, flush=True)
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(SCROLL_PAUSE_TIME)
    print("Scrolling completed", flush=True)

def selenium_init()->Firefox:
    """
    Initializes and opens a selinium Firefox window with custom profile path PROFILE_PATH
    """
    print("Initializing Selenium, please wait...", flush=True)
    opt=Options()
    opt.add_argument("-profile")
    opt.add_argument(PROFILE_PATH)
    driver = webdriver.Firefox(options=opt)
    driver.set_script_timeout(15)
    driver.set_page_load_timeout(15)
    return driver

def exists(dir, substr:str)->bool:
    for entry in dir:
        if(entry.is_file() and substr in entry.name):
            return True
    return False

def selenium_visit(driver:Firefox)->Firefox:
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
            print("You did not enter a valid link, links contain https://chan.sankakucomplex.com")
        else:
            driver.get(url)
            selenium_infscroll(driver)
            time.sleep(1)
            if demo == False:
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
                print(linkQ.qsize(), " items to be processed", flush=True)
                # Process each url and save their image if is valid
                while(linkQ.empty() == False):
                    url = str(linkQ.get())
                    print("Opening: ", url, flush=True)
                    driver.execute_script('window.open("{}","_blank");'.format(url))
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
    print(failed, " failed, urls saved in log.txt")
    print("Exiting Selenium...")
    driver.quit()

if __name__=="__main__":
    main()
