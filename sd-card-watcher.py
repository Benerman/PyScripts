
# watch specific drive
# when image files are on disk
# compare files on card to files on disk
# if not folder exist
# 	create folder with date
# those that arent on disk
# 	transfer iamges to location


import os, time

def moinitor_drive():
	pass
	# move_files()

def move_files():
	pass
	# monitor_drive()

def main():
	pass
# 	source = get watch drive
# 	dest = get folder to transfer files to

	# move_files()
	while True:
		if card in drive:
			# os walk
			for image in files_on_card:
				# image check needed '.CR2' or '.JPG'
				# list of files in the folder
				all_images.extend([image])
				# file information check, Get date modified or created
				image_date = str(datetime.datetime.fromtimestamp(os.path.getctime(image))).replace('-', '').split(' ')[0]
# parse image_date to be OS friendly

				image_date_set.add(image_date)
			if image_date_set > 0:
				if not path isdir(os.path.join(dest, date_folder):
					os.mkdir(image_date)
			files_to_transfer = all_images.pop()
			folder_loc = os.path.join(dest, date_folder)
		#	# Copy all files to folder_loc

			print(f'{len(files_to_transfer)} out of {len(files in date_folder)}')
		else:	
			time.sleep(5)


if __name__ == '__main__':
	main()
