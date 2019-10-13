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


today = datetime.now()
if not os.path.exists('processed_audits\\' + today.strftime('%Y%m%d')):
	os.makedirs('processed_audits\\' + today.strftime('%Y%m%d'))
	print('Folder Created Successfully')

csv_input_file = sys.argv[1]

### Try Args
## Ask for Order Var
order = str(raw_input('Order Number(i.e. MASS 20190702-01) :'))
## Ask for Audit Var
audit = str(raw_input('Audit Number: '))
## Ask for Outbound Var
outbound = str(raw_input('Outbound Status(DONATE, RTV, NA): ')).upper()

output_csv = (order.split(' ')[0] + '_' + order.split(' ')[-1]) + '_' + audit + '.csv'

##Open Writer
with open(r'processed_audits\\' + today.strftime('%Y%m%d') + '\\' + output_csv, mode='wb') as csv_output:
	writer = csv.writer(csv_output, quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['Item Number', 'Summary', 'Description'])
	##Open File
	with open(csv_input_file, mode="r") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			for row in csv_reader:
				# print(row)
				## Label Columns that need processing
				barcode = row[1]
				if barcode == '' or barcode == 'Barcode' or len(barcode) < 3:
					continue
				item_number = row[2]
				model_number = row[4]
				vendor_number = row[3] # not necesary?
				product_description = row[5]
				product_group = row[6]
				if '' == barcode == item_number == model_number == product_description or len(item_number) < 3:
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
					else:
						url = search_for_url(item_number)
						##Split URL to get LPID
						lpid = url.split('/')[-1]
						if 'https://www.lowes.com/search?searchTerm=' in url:
							url = search_for_url(model_number)
							##Split URL to get LPID
							lpid = url.split('/')[-1]
						if 'https://www.lowes.com/search?searchTerm=' in url:
							lpid = 'NA, No LPID'
				except:
					print('Exception: ' + item_number)
					url = 'NA'
					lpid = 'NA, No LPID,'
				print('URL = ' + url)
				if 'https://www.lowes.com/search?searchTerm=' in url:
					print('Item not found: ' + item_number)
					lpid = url
					url = 'NA'
				if url != 'NA':
					url_split = url.split('/')
					url_summary = url_split[-2].split('-')
					url_parsed = ''
					for item in url_summary:
						url_parsed = url_parsed + item +' '
					product_description = url_parsed
				if 'lowes' in product_description:
					product_description = 'Unable to find Product on Lowes.com'
					lpid = 'NA, No LPID'
				print('Product Description = ' + product_description)
				writer.writerow([
								## Start off with Item #
								item_number,
								## create Summary
								order + ' ' + audit + ', ' + product_description + ' - ' + product_group,
								## create description
								'Item Number: ' + item_number + ',\n'
								'Model Number: ' + model_number + ',\n'
								'Barcode: ' + barcode + ',\n\n'
								'Outbound: ' + outbound + ',\n'
								'Product Description: ' + product_description + ',\n'
								'Product Group: ' + product_group + ',\n'
								'URL: ' + url + '\n\n'
								'LPID: ' + lpid
								])
				print('Row wrote')
print('Done')
