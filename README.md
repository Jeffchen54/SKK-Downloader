# SKK-Downloader
**Not meant for external use but free for any to download and play with**

Description:
Project used to play around with python and download from Sankaku while bypassing numerous methods employed by Sankaku. Method is slower than other mass downloaders and only compatible with https://chan.sankakucomplex.com/

Requirements:
- Selinium-python for Firefox: https://selenium-python.readthedocs.io/installation.html
- urllib3: https://pypi.org/project/urllib3/
- Python (ran on 3.10): https://www.microsoft.com/en-us/p/python-310/9pjpw5ldxlz5?activetab=pivot:overviewtab
- Firefox: https://www.mozilla.org/en-US/firefox/new/
- Tampermonkey addon for Firefox: https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/
- Handyimage script enabled in Tampermonkey: https://sleazyfork.org/en/scripts/109-handy-image/code
- Windows 10 (may work on other versions but tested only on Windows 10


Changelog:
General update 4/17/2022
- Removed all unused files from repo

ImageOpener(0.4) 4/17/2022
- Added .mp4 download functionality
- Added skip which skips number of urls equal to number of files in download directory (will be replaced)
- Added strategy to counter endless page errors by closing and reopening selenium browser
- Now downloads up to 2000 files with no issues


ImageOpener(0.3) 4/16/2022:
- Added save functionality exploiting XPATH of image tabs
- Changed tab system to a maximum of a single tab at a time
- Basic functionality now possible (non mp4 and non flash)

ImageOpener(0.2) 4/15/2022:
- Converted project to use Selinium for huge performance boost
- Added initiator for selinium using custom Firefox profile
- Automatic scrolling for image link harvesting
- Improved tab opening (Extract links directly instead of manual clicking)
- Added multiple flags, including demo and debug modes
- Slowdown/error screen detection and resolution detection
As of now, ImageOpener is not functional

Features to add ImageOpener(TBA):
- Improved manual termination
- Pause with save state 
- Bypass for 2000 file limit
- .swf download functionality
- Optional logging to file 

Features to add in general:
- Guide to download and setup downloader
