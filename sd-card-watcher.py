
# watch specific drive
# when image files are on disk
# compare files on card to files on disk
# if not folder exist
# 	create folder with date
# those that arent on disk
# 	transfer iamges to location

# from __future__ import print_function
import os, time, datetime, subprocess, shutil
from pathlib import Path
import tkinter as tk
import tkinter.filedialog

def start_gui():
	root = tk.Tk()
	root.withdraw()
	source = get_file_path("Choose source drive letter to monitor")
	print(source)
	dest = get_file_path("Choose destination folder to move folder containing files to")
	print(dest)
	return (source, dest)
	# letter = 
	pass

def get_file_path(title):
	return str(Path(tkinter.filedialog.askdirectory(title=title)))


def monitor_drive(letter):
	pass
	if not os.name == 'nt':
		pass
		# do linux version 
	else:
		# print(letter, letter.replace('/', ''))
		# drive_check = letter in subprocess.check_output(["fsutil", "fsinfo", "drives"]).decode()
		# return os.system("vol {} 2>nul>nul".format(letter.replace('/', ''))) == 0
		return os.path.isdir("H:\\") and letter in subprocess.check_output(["fsutil", "fsinfo", "drives"]).decode()
		# output = subprocess.check_output(["wmic", "logicaldisk", "get", "name"])


def copy_file(src_file, dest):
	if os.path.isdir(dest):
		src = Path(src_file)
		dest = os.path.join(dest, '2nd_Ref')
		if not os.path.isdir(dest):
			os.mkdir(dest)
		existing = Path(os.path.join(dest, os.path.split(src_file)[-1]))
		if existing.exists():
			if src.stat().st_mtime == existing.stat().st_mtime:
				print(f'mtime - File exists at destination: {str(existing)}')
				return False
			elif src.stat().st_size == existing.stat().st_size:
				print(f'size - File exists at destination: {str(existing)}')
				return False
			else:
				print(f'File exists but it is not exact, Copying file {src_file}')
				shutil.copy(src_file, dest)
				return True
		else:
			print(f'Moving {src_file} to {dest}')
			shutil.copy(src_file, dest)
			return True
	else:
		print('Destination does not exist, file not copied')
		return False


def main():
	source, dest = start_gui()
	drive_mounted = monitor_drive(source)
	card_parsed = False
	all_images = []
	image_date_set = set()
	while True:
		if drive_mounted and card_parsed == False:
			print(f'loop = {drive_mounted}')
			drive_mounted = monitor_drive(source)
			print('drive is mounted')
			for root, dirs, files in os.walk(source):
				# print(root, dirs, files)
				image_list = []
				for file in files:
					# image check needed '.CR2' or '.JPG'
					# print(file)
					if '.jpg' in file.lower() or '.cr2' in file.lower():
						image_date = str(datetime.datetime.fromtimestamp(
							os.path.getctime(os.path.join(root,file)))
							).replace('-', '').split(' ')[0]
						image_date_set.add(image_date)
						image_list.append((os.path.join(root,file), image_date))
						# print(os.path.join(root,file), image_date)
				if len(image_list) > 0:
					all_images.extend(image_list)
			if len(image_date_set) > 0:
				for folder in image_date_set:
					if not os.path.isdir(os.path.join(dest, folder)):
						# print(f'would make dir {os.path.join(dest, folder)}')
						os.mkdir(os.path.join(dest, folder))
			# print(all_images)
			image_list_len = len(all_images)
			try:
				if all_images_dupe == all_images:
					print('No new file changes.')
					card_parsed = True
					continue
			except UnboundLocalError:
				print('Unprocessed changes detected, Starting Processing')
				all_images_dupe = all_images.copy()
			if image_list_len != len(all_images_dupe):
				nums = image_list_len - len(all_images_dupe)
			else:
				nums = len(all_images_dupe)
			count = 0
			for i in range(len(all_images)):
				popped_image = all_images.pop()
				file_to_transfer,image_date = popped_image
				# print(file_to_transfer, image_date)
				folder_loc = os.path.join(dest, image_date)
				# print(file_to_transfer)
				# print(folder_loc)
				if copy_file(file_to_transfer, folder_loc):
					count += 1
				print(f'Moved {count} out of {nums} photos')
				print()
			print(f'TOTAL: Moved {count} out of {nums} photos') # {len(files in date_folder)}')
			card_parsed = True
		else:
			if card_parsed:
				print('Card Processed and monitoring for changes')
				time.sleep(30)
				drive_mounted = monitor_drive(source)
			else:
				print('Drive is not mounted, sleeping')
				time.sleep(30)
				drive_mounted = monitor_drive(source)
			if not drive_mounted:
				card_parsed = False


if __name__ == '__main__':
	main()

