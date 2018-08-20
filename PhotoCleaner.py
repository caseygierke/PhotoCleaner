# PhotoCleaner.py

# With Notepad++, use F5 then copy this into box
# C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"

# Written by Casey Gierke of AlbuGierke Environmental Solutions
# Updated 2018-05-08

# -------------------------------------------------
# IMPORTS
# -------------------------------------------------

import glob
import shutil
import os
import exifread
# import re
import Image
from distutils.dir_util import copy_tree
import Tkinter 
from Tkinter import Tk
from tkFileDialog import askdirectory

# -------------------------------------------------
# DEFINE FUNCTIONS
# -------------------------------------------------

# Define last position finder
def find_last(s,t):
	last_pos = -1
	while True:
		pos = s.find(t, last_pos +1)
		if pos == -1:
			return last_pos
		last_pos = pos

# -------------------------------------------------
# INPUTS
# -------------------------------------------------

dir_path = os.path.abspath(os.path.dirname(__file__))

# Name base folder
base = 'iPhone Files'
base = 'test II'

src_dir = dir_path+os.sep+base+os.sep

# Get path to iPhone photo files
Files = glob.glob(src_dir+'*.jpg*')
if Files == []:
	# Get path from user
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askdirectory(initialdir = "/",title = "I can't find your iPhone photos. \nPlease show me where you keep them?") # show an "Open" dialog box and return the path to the selected file
	src_dir = str(filename)
	src_dir = src_dir.replace('/','\\')
	base = src_dir[find_last(src_dir,'\\')+1:]

# Check that destination directories exist and create if not
if not os.path.exists(dir_path+os.sep+base+"- Copy"+os.sep):
	os.makedirs(dir_path+os.sep+base+"- Copy"+os.sep)
copy_dir = dir_path+os.sep+base+"- Copy"+os.sep
if not os.path.exists(dir_path+os.sep+base+"- Timestamped"+os.sep):
	os.makedirs(dir_path+os.sep+base+"- Timestamped"+os.sep)
dst_dir = dir_path+os.sep+base+"- Timestamped"+os.sep
if not os.path.exists(dir_path+os.sep+base+"- No Timestamp"+os.sep):
	os.makedirs(dir_path+os.sep+base+"- No Timestamp"+os.sep)
not_dir = dir_path+os.sep+base+"- No Timestamp"+os.sep

# -------------------------------------------------
# OPERATIONS
# -------------------------------------------------

# Extract from file structure
# -------------------------------------------------

for jpgfile in glob.iglob(os.path.join(src_dir+os.sep, "*.jpg")):
# for jpgfile in glob.iglob(os.path.join(src_dir, "*/*.jpg")):
    if os.path.exists(copy_dir+os.path.basename(os.path.normpath(jpgfile))) == False:
		print('Copying '+jpgfile[find_last(jpgfile,os.sep)+1:])
		shutil.copy(jpgfile, copy_dir)

for pngfile in glob.iglob(os.path.join(src_dir+os.sep, "*.png")):
# for jpgfile in glob.iglob(os.path.join(src_dir, "*/*.jpg")):
    if os.path.exists(dst_dir+os.path.basename(os.path.normpath(pngfile))) == False:
		print('Copying '+pngfile[find_last(pngfile,os.sep)+1:])
		shutil.copy(pngfile, not_dir)

for movfile in glob.iglob(os.path.join(src_dir+os.sep, "*.mov")):
	# for movfile in glob.iglob(os.path.join(src_dir, "*/*.mov")):
	# Copy to copy folder if it is a live photo
	if os.path.exists(movfile[:-3]+'jpg') == True:
		print('Copying '+movfile[find_last(movfile,os.sep)+1:]+' to Copy folder')
		shutil.copy(movfile, copy_dir)
		
	# Copy to destination if it is not a live photo
	elif os.path.exists(dst_dir+os.path.basename(os.path.normpath(movfile))) == False:
		print('Copying '+movfile[find_last(movfile,os.sep)+1:])
		shutil.copy(movfile, not_dir)
		
for mp4file in glob.iglob(os.path.join(src_dir+os.sep, "*.mp4")):
# for movfile in glob.iglob(os.path.join(src_dir, "*/*.mov")):
    if os.path.exists(dst_dir+os.path.basename(os.path.normpath(mp4file))) == False:
		print('Copying '+mp4file[find_last(mp4file,os.sep)+1:])
		shutil.copy(mp4file, not_dir)

for t3gpfile in glob.iglob(os.path.join(src_dir+os.sep, "*.3gp")):
# for movfile in glob.iglob(os.path.join(src_dir, "*/*.mov")):
    if os.path.exists(dst_dir+os.path.basename(os.path.normpath(t3gpfile))) == False:
		print('Copying '+t3gpfile[find_last(t3gpfile,os.sep)+1:])
		shutil.copy(t3gpfile, not_dir)

for giffile in glob.iglob(os.path.join(src_dir+os.sep, "*.gif")):
# for movfile in glob.iglob(os.path.join(src_dir, "*/*.mov")):
    if os.path.exists(dst_dir+os.path.basename(os.path.normpath(giffile))) == False:
		print('Copying '+giffile[find_last(giffile,os.sep)+1:])
		shutil.copy(giffile, not_dir)

# Move and rename files
# -------------------------------------------------

# Get file list including iPhone, CanonPowerShot, and Nikon1 files
Files = glob.glob(copy_dir+"*.jpg")

# Open array to build dictionary
result = range(len(Files))

# Open loop to treat each jpg file
for i in range(len(Files)):
	
	# Open image file
	img = Image.open(Files[i])
	# Get date information by getting minimum creation time
	exif_data = img._getexif()
	mtime = "?"
	# Deal with images that have no data
	if exif_data is None:
		exif_data = []
		mtime = mtime
	if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
		mtime = exif_data[306]
	if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
		mtime = exif_data[36867]
	if 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
		mtime = exif_data[36868]
	
	# Add "_" for each repeat of exact time
	j = 0
	while mtime+"_"*j in result:
		j += 1
	mtime = mtime+"_"*j
	result[i] = mtime
	
	# Determine if it has relevant date information and assign name
	oldName = Files[i][find_last(Files[i],os.sep)+1:-4]
	if '?' in result[i]:
		newName = oldName
	else:
		newName = result[i][:result[i].find(' ')].replace(":", "-") + result[i][result[i].find(' '):].replace(":", "")
	# print(newName+', '+exif_data)
	
	# Copy to another folder if it does not have timestamp information
	
	if newName == oldName:
		# Copy files to new directory with same name
		if os.path.exists(not_dir+newName+'.jpg') == False:
			print('Copying '+newName+'.jpg')
			shutil.copy2(Files[i], not_dir+newName+'.jpg')
	else:
		# Copy files to new directory with new name
		if os.path.exists(dst_dir+newName+'.jpg') == False:
			print('Renaming '+newName+'.jpg')
			shutil.copy2(Files[i], dst_dir+newName+'.jpg')

	# Check if it is a live photo and copy files to new directory with new name
	if os.path.exists(copy_dir+oldName+'.mov') == True:
		if os.path.exists(dst_dir+newName+'.mov') == False:
			print('Renaming '+newName+'.mov')
			shutil.copy(Files[i][:-3]+'MOV', dst_dir+newName+'- Live.mov')

# import Tkinter as tk
# Open a message window
master = Tkinter.Tk()
whatever_you_do = "1) Select the ~- Timestamped \nand ~- No Timestamp folders, \nright click to get properties and check the file size.  \n\n2) Also right click the original folder and check its file size to be sure that they are the same.  \n\nIf they are, feel free to delete the original folder and the ~- Copy folder. If they are not, please contact me at caseygierke@gmail.com to fix the issue."
msg = Tkinter.Message(master, text = whatever_you_do)
msg.config(bg='lightblue', font=('calibri', 14, 'bold'), relief = 'groove')
msg.pack()
Tkinter.mainloop()