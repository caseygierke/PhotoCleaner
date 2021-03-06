# PhotoCleaner.py

# With Notepad++, use F5 then copy this into box
# C:\Python27\python.exe -i "$(FULL_CURRENT_PATH)"

# Written by Casey Gierke 
# of AlbuGierke Environmental Solutions
# Updated 2018-05-08
# Updated 2018-08-20

# ***Need to update program by putting the whole process
# into a loop that moves through all known file types.  
# Once the loop structure is in place, then have to have 
# an order of operations.  For now this looks like:
	# Determine if the file has exif info
		# Rename if it does
	# If not, examine the name and test if it already
	# has timestamp info
		# Rename by reformatting if it does
	# If neither, rename based on the modified info 
	# for the file. 
# In this way, every file should recieve a timestamp 
# name even if it is not correct.  Older photos will 
# just have to be kept in their folders to identify
# when they are from. ***

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
import datetime

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
# base = 'iPhone Files'
base = 'Test'

src_dir = dir_path+os.sep+base+os.sep

# Get path to iPhone photo files
Files = glob.glob(src_dir+'*.jpg*')
# Files = glob.glob(src_dir+'*.mts*')

if Files == []:
	# Get path from user
	Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
	filename = askdirectory(initialdir = "/",title = "I can't find your iPhone photos. \nPlease show me where you keep them?") # show an "Open" dialog box and return the path to the selected file
	src_dir = str(filename)
	src_dir = src_dir.replace('/','\\')
	base = src_dir[find_last(src_dir,'\\')+1:]

# Check that destination directories exist and create if not
# if not os.path.exists(dir_path+os.sep+base+"- Copy"+os.sep):
	# os.makedirs(dir_path+os.sep+base+"- Copy"+os.sep)
# copy_dir = dir_path+os.sep+base+"- Copy"+os.sep
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

# Define file types to be processed
fileTypes = [
				'.jpg',
				'.png',
				'.mov',
				'.avi', 
				'.mp4',
				'.t3g',
				'.gif',
				'.mts',
				]
				
# Get list of files
# Files = []
lastName = None

for type in fileTypes:
	
	for typeFile in glob.iglob(os.path.join(src_dir+os.sep, '*'+type)):
		
		# Check if file has exif info
		# ---------------------
		try:
			# Open image file
			img = Image.open(typeFile)
			
			# Get date information by getting minimum creation time
			exif_data = img._getexif()
			mtime = "?"

			# Get creation info based on different proprietary formats
			if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
				mtime = exif_data[306]
			if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
				mtime = exif_data[36867]
			if 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
				mtime = exif_data[36868]
			
			# result = mtime
			
			# Get old name from file
			oldName = typeFile[find_last(typeFile,os.sep)+1:-4]
			
			# Assign new name
			newName = mtime[:mtime.find(' ')].replace(":", "-") + mtime[mtime.find(' '):].replace(":", "")
			
			# Add "_" for each repeat of exact time
			if newName == lastName:
				newName = newName+'_'
				
			# Copy files to new directory with new name
			if os.path.exists(dst_dir+newName+type) == False:
				print('Renaming '+newName+type+' based on exif_info')
				shutil.copy2(typeFile, dst_dir+newName+type)

			# Check if it is a live photo and copy files to new directory with new name
			if os.path.exists(copy_dir+oldName+'.mov') == True:
				if os.path.exists(dst_dir+newName+'.mov') == False:
					print('Renaming '+newName+'.mov'+' based on exif_info of .img file')
					shutil.copy(typeFile[:-3]+'MOV', dst_dir+newName+'- Live.mov')
			
			# Save last name for checking for duplicates
			lastName = newName
			
			print(typeFile[-3:]+' Worked!')
			continue
			
		except:
			pass
			print(typeFile[-3:]+' Does NOT have exif_info :(')
			
		# Check if the name has timestamp info, this should catch .avi files
		# ---------------------
		
		# for avifile in glob.iglob(os.path.join(src_dir+os.sep, "*.avi")):
		# Check to see if it has creation information
		if os.path.getmtime(typeFile):
			timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(typeFile)).isoformat()
			# Develop new name
			newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+type
			# Check directory if it already exists
			if os.path.exists(dst_dir+newName) == False:
				print('Renaming '+newName+' based on fromtimestamp')
				shutil.copy2(typeFile, dst_dir+newName)
				continue
				
		# Check if movie file has related image file (live photo)
		# ---------------------
		
		# Rename based on "Modified" date
		# ---------------------
		if os.path.getmtime(typeFile):
			timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(typeFile)).isoformat()
			# Develop new name
			newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+type
			# Check directory if it already exists
			if os.path.exists(dst_dir+newName) == False:
				print('Renaming '+newName+' based on modified date')
				shutil.copy2(typeFile, dst_dir+newName)
				continue
		
		# # Do not rename, simply place in "No Timestamp" folder
		# # ---------------------
		
		# First, create the directory
		if not os.path.exists(dir_path+os.sep+base+"- No Timestamp"+os.sep):
			os.makedirs(dir_path+os.sep+base+"- No Timestamp"+os.sep)
		not_dir = dir_path+os.sep+base+"- No Timestamp"+os.sep

		# Then check if it already exists and copy if not
		if os.path.exists(not_dir+os.path.basename(os.path.normpath(typeFile))) == False:
			print('Copying '+typeFile[find_last(typeFile,os.sep)+1:])
			shutil.copy(typeFile, not_dir)
	
		# if os.path.exists(typeFile[:-4]+type) == True:
			# print('Copying '+typeFile[find_last(typeFile,os.sep)+1:]+' to Copy folder')
			# shutil.copy(typeFile, copy_dir)
			
		# # Copy to destination if it is not a live photo
		# else:
			# print('Copying '+typeFile[find_last(typeFile,os.sep)+1:])
			# shutil.copy(typeFile, not_dir)

			
# # ----------------------

	# # for mtsfile in glob.iglob(os.path.join(src_dir+os.sep, "*.mts")):
		# # # Check to see if it has creation information
		# # if os.path.getmtime(mtsfile):
			# # timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(mtsfile)).isoformat()
			# # # Develop new name
			# # newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+'.mts'
			# # # Check directory if it already exists
			# # if os.path.exists(dst_dir+newName) == False:
				# # print('Renaming '+newName)
				# # shutil.copy2(mtsfile, dst_dir+newName)
		# # else:
			# # if os.path.exists(not_dir+os.path.basename(os.path.normpath(mtsfile))) == False:
				# # print('Copying '+mtsfile[find_last(mtsfile,os.sep)+1:])
				# # shutil.copy(mtsfile, not_dir)

# # for avifile in glob.iglob(os.path.join(src_dir+os.sep, "*.avi")):
	# # # Check to see if it has creation information
	# # if os.path.getmtime(avifile):
		# # timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(avifile)).isoformat()
		# # # Develop new name
		# # newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+'.avi'
		# # # Check directory if it already exists
		# # if os.path.exists(dst_dir+newName) == False:
			# # print('Renaming '+newName)
			# # shutil.copy2(avifile, dst_dir+newName)
	# # else:
		# # if os.path.exists(not_dir+os.path.basename(os.path.normpath(avifile))) == False:
			# # print('Copying '+avifile[find_last(avifile,os.sep)+1:])
			# # shutil.copy(avifile, not_dir)

# # # ---------------------
		
# # for jpgfile in glob.iglob(os.path.join(src_dir+os.sep, "*.jpg")):
# # # for jpgfile in glob.iglob(os.path.join(src_dir, "*/*.jpg")):
    # # if os.path.exists(copy_dir+os.path.basename(os.path.normpath(jpgfile))) == False:
		# # print('Copying '+jpgfile[find_last(jpgfile,os.sep)+1:])
		# # shutil.copy(jpgfile, copy_dir)

# # for pngfile in glob.iglob(os.path.join(src_dir+os.sep, "*.png")):
# # # for jpgfile in glob.iglob(os.path.join(src_dir, "*/*.jpg")):
    # # if os.path.exists(dst_dir+os.path.basename(os.path.normpath(pngfile))) == False:
		# # print('Copying '+pngfile[find_last(pngfile,os.sep)+1:])
		# # shutil.copy(pngfile, not_dir)

# # for movfile in glob.iglob(os.path.join(src_dir+os.sep, "*.mov")):
	# # # for movfile in glob.iglob(os.path.join(src_dir, "*/*.mov")):
	# # # Copy to copy folder if it is a live photo
	# # if os.path.exists(movfile[:-3]+'jpg') == True:
		# # print('Copying '+movfile[find_last(movfile,os.sep)+1:]+' to Copy folder')
		# # shutil.copy(movfile, copy_dir)
		
	# # # Copy to destination if it is not a live photo
	# # elif os.path.exists(dst_dir+os.path.basename(os.path.normpath(movfile))) == False:
		# # print('Copying '+movfile[find_last(movfile,os.sep)+1:])
		# # shutil.copy(movfile, not_dir)
		
# # for mp4file in glob.iglob(os.path.join(src_dir+os.sep, "*.mp4")):
	# # # Check to see if it fits the pattern for renaming based on name
	# # if mp4file[find_last(mp4file,os.sep)+1:][:2] == '20' and mp4file[find_last(mp4file,os.sep)+1:][8] == '_':
		# # # Develop new name
		# # newName = mp4file[find_last(mp4file,os.sep)+1:][:4]+'-'+mp4file[find_last(mp4file,os.sep)+1:][4:6]+'-'+mp4file[find_last(mp4file,os.sep)+1:][6:8]+' '+mp4file[find_last(mp4file,os.sep)+1:][9:]
		# # # Check directory if it already exists
		# # if os.path.exists(dst_dir+newName) == False:
			# # print('Renaming '+newName)
			# # shutil.copy2(mp4file, dst_dir+newName)
	# # else:	
		# # if os.path.exists(not_dir+os.path.basename(os.path.normpath(mp4file))) == False:
			# # print('Copying '+mp4file[find_last(mp4file,os.sep)+1:])
			# # shutil.copy(mp4file, not_dir)

# # for t3gpfile in glob.iglob(os.path.join(src_dir+os.sep, "*.3gp")):
    # # if os.path.exists(not_dir+os.path.basename(os.path.normpath(t3gpfile))) == False:
		# # print('Copying '+t3gpfile[find_last(t3gpfile,os.sep)+1:])
		# # shutil.copy(t3gpfile, not_dir)

# # for giffile in glob.iglob(os.path.join(src_dir+os.sep, "*.gif")):
    # # if os.path.exists(not_dir+os.path.basename(os.path.normpath(giffile))) == False:
		# # print('Copying '+giffile[find_last(giffile,os.sep)+1:])
		# # shutil.copy(giffile, not_dir)

# # for mtsfile in glob.iglob(os.path.join(src_dir+os.sep, "*.mts")):
	# # # Check to see if it has creation information
	# # if os.path.getmtime(mtsfile):
		# # timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(mtsfile)).isoformat()
		# # # Develop new name
		# # newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+'.mts'
		# # # Check directory if it already exists
		# # if os.path.exists(dst_dir+newName) == False:
			# # print('Renaming '+newName)
			# # shutil.copy2(mtsfile, dst_dir+newName)
	# # else:
		# # if os.path.exists(not_dir+os.path.basename(os.path.normpath(mtsfile))) == False:
			# # print('Copying '+mtsfile[find_last(mtsfile,os.sep)+1:])
			# # shutil.copy(mtsfile, not_dir)

# for avifile in glob.iglob(os.path.join(src_dir+os.sep, "*.avi")):
	# # Check to see if it has creation information
	# if os.path.getmtime(avifile):
		# timeStamp = datetime.datetime.fromtimestamp(os.path.getmtime(avifile)).isoformat()
		# # Develop new name
		# newName = timeStamp[:10]+' '+timeStamp[11:13]+timeStamp[14:16]+timeStamp[17:]+'.avi'
		# # Check directory if it already exists
		# if os.path.exists(dst_dir+newName) == False:
			# print('Renaming '+newName)
			# shutil.copy2(avifile, dst_dir+newName)
	# else:
		# if os.path.exists(not_dir+os.path.basename(os.path.normpath(avifile))) == False:
			# print('Copying '+avifile[find_last(avifile,os.sep)+1:])
			# shutil.copy(avifile, not_dir)

# # # Move and rename files
# # # -------------------------------------------------

# # # Get file list including iPhone, CanonPowerShot, and Nikon1 files
# # Files = glob.glob(copy_dir+"*.jpg")
# # # Files = glob.glob(copy_dir+"*.mts")

# # # Open array to build dictionary
# # result = range(len(Files))

# # # Open loop to treat each jpg file
# # for i in range(len(Files)):
	
	# # Open image file
	# img = Image.open(Files[i])
	# # Get date information by getting minimum creation time
	# exif_data = img._getexif()
	# mtime = "?"
	# # Deal with images that have no data
	# if exif_data is None:
		# exif_data = []
		# mtime = mtime
	# if 306 in exif_data and exif_data[306] < mtime: # 306 = DateTime
		# mtime = exif_data[306]
	# if 36867 in exif_data and exif_data[36867] < mtime: # 36867 = DateTimeOriginal
		# mtime = exif_data[36867]
	# if 36868 in exif_data and exif_data[36868] < mtime: # 36868 = DateTimeDigitized
		# mtime = exif_data[36868]
	
	# # Add "_" for each repeat of exact time
	# j = 0
	# while mtime+"_"*j in result:
		# j += 1
	# mtime = mtime+"_"*j
	# result[i] = mtime
	
	# # Determine if it has relevant date information and assign name
	# oldName = Files[i][find_last(Files[i],os.sep)+1:-4]
	# if '?' in result[i]:
		# newName = oldName
	# else:
		# newName = result[i][:result[i].find(' ')].replace(":", "-") + result[i][result[i].find(' '):].replace(":", "")
	# # print(newName+', '+exif_data)
	
	# # Copy to another folder if it does not have timestamp information
	
	# if newName == oldName:
		# # Copy files to new directory with same name
		# if os.path.exists(not_dir+newName+'.jpg') == False:
			# print('Copying '+newName+'.jpg')
			# shutil.copy2(Files[i], not_dir+newName+'.jpg')
	# else:
		# # Copy files to new directory with new name
		# if os.path.exists(dst_dir+newName+'.jpg') == False:
			# print('Renaming '+newName+'.jpg')
			# shutil.copy2(Files[i], dst_dir+newName+'.jpg')

	# # Check if it is a live photo and copy files to new directory with new name
	# if os.path.exists(copy_dir+oldName+'.mov') == True:
		# if os.path.exists(dst_dir+newName+'.mov') == False:
			# print('Renaming '+newName+'.mov')
			# shutil.copy(Files[i][:-3]+'MOV', dst_dir+newName+'- Live.mov')

# # # import Tkinter as tk
# # # Open a message window
# # master = Tkinter.Tk()
# # whatever_you_do = "1) Select the ~- Timestamped \nand ~- No Timestamp folders, \nright click to get properties and check the file size.  \n\n2) Also right click the original folder and check its file size to be sure that they are the same.  \n\nIf they are, feel free to delete the original folder and the ~- Copy folder. If they are not, please contact me at caseygierke@gmail.com to fix the issue."
# # msg = Tkinter.Message(master, text = whatever_you_do)
# # msg.config(bg='lightblue', font=('calibri', 14, 'bold'), relief = 'groove')
# # msg.pack()
# # Tkinter.mainloop()
