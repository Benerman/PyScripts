## Intake Form Preparer

try:
	import urllib.request as urllib2
except ImportError:
	import urllib2
import csv
import sys
from datetime import datetime
import os

## Search for URL using Item Number
def search_for_url(item_number):
	search_url = 'https://www.lowes.com/search?searchTerm=' + str(item_number) # 1336779
	try:
		product_url = urllib2.urlopen(search_url).url
	except Exception as e:
		print(e)
	return product_url


csv_input_file = sys.argv[1]

output_csv = 'nolpid.csv'

##Open Writer
with open(output_csv, mode='wb') as csv_output:
	writer = csv.writer(csv_output, quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Item Number', 'LPID'])
	##Open File
	with open(csv_input_file, mode="r") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				# print(row)
				## Label Columns that need processing
				jira = row[1]
				item_number = row[2]
				if '' == item_number or len(item_number) < 3:
					continue
				if item_number == 'Item Number':
					continue
				## Don't Exist in Gap Analysis
				# order = row['Order']
				# audit = row['Audit']
				# outbound = row['Outbound']
				try:
					if item_number == '':
						url = 'NA'
						lpid = 'NA, No LPID,'
					elif 'https://www.lowes.com/search?searchTerm=' in url:
						url = 'NA, Duplicate Results with Item Number'
						lpid = 'NA'
					else:
						url = search_for_url(item_number)
						##Split URL to get LPID
						lpid = url.split('/')[-1]
				except:
					url = 'NA'
					lpid = 'NA, No LPID,'
				print('URL = ' + url)
				writer.writerow([
								jira,
								## Start off with Item #
								item_number,
								## Concatenate LPID
								'LPID: ' + lpid,
								url
								])
				print('Row wrote')
print('Done')
