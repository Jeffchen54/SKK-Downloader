# Tab-Bundle-Software
Project used to play around with python and file control system.
- Not meant for external use but free for any to download and play with


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
- Adjustable confidence/misc settings outside of .py file 



