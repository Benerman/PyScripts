#!/bin/pyhton
"""
Parse CSV for Audits while checking status and writing it to Output CSV

auditSearchOrCompareTest.py <CSV to Parse> ['delete' or 'keep'] <Output CSV> <Additional CSV to compare>
auditSearchOrCompareTest.py "C:\Users\Bogey03\Downloads\TPOG Kanban Audits In Studio At Hobb (JIRA).csv" delete output_audits_csv_HOBB.csv

"""


import csv
import sys
import re
import string
import os
import time


def isAuditCheck(text):
	searchTerms = re.compile(r'[a-zA-Z0-9]{3,6}\d{3},\s')
	try:
		results = re.finditer(searchTerms, text)
	except TypeError:
		listOfAudits = ['NA']
		return False
	listOfAudits = []
	try:
		for result in results:
			audit = result.group(0)
			# print(audit)
			listOfAudits.append(audit[0:6])
			return audit[0:6]
	except AttributeError:
		print(results)
		print(results)


def csv_parser(inputName,writer):
	# def returnAuditSet(uniqueAuditSet):
	# 	return uniqueAuditSet

	# def returnProductsInAudit(productsInAudit):
	# 	return productsInAudit

	# Create tmp folder
	# write output CSVs to there
	# Compare the old CSV with the New Results
	# Notate the diferences between new and old files
	uniqueAuditSet = set()
	dupeAudit = set()
	uniqueJIRAS = set()
	printingList = set()
	productsInAudit = []
	dupeCount = 0
	auditCount = 0
	rowCount = 0
	status = ['New Content Entry', 'At Stage', 'Processing', "Needs (re)Processing"]
	with open(inputName, mode="r") as csv_file:
		csv_reader = csv.DictReader(csv_file, delimiter=',')
		for row in csv_reader:
			jira = row['Issue key']
			summary = row['Summary']
			status = row['Status']
			rowCount += 1
			# print(summary)
			# print(row[2])
			uniqueAudit = isAuditCheck(summary)
			# print(uniqueAudit)
			if uniqueAudit:
				productsInAudit.append((uniqueAudit, jira))
				if uniqueAudit not in dupeAudit:
					print('Audit Found #: {}'.format(str(uniqueAudit)))
					uniqueAuditSet.add(str(uniqueAudit))
					dupeAudit.add(str(uniqueAudit))
					uniqueJIRAS.add(jira)
					auditCount += 1
				else:
					print('Audit Found #: {} But is a duplicate'.format(uniqueAudit))
					dupeAudit.add(uniqueAudit)
					dupeCount += 1
			#print('Row Parsed, Next Row Starting')
		for audit,jira in productsInAudit:
			tallyAudits = {}
			for a,j in productsInAudit:
				auditNumCount = 0
				# print('{} + {}'.format(a,j))
				for A,J in productsInAudit:
					if a == A:
						# print('{} + {}'.format(A,J))
						auditNumCount += 1
						tallyAudits.update({A:auditNumCount})
					# print(tallyAudits)
			if audit not in printingList:
				writer.writerow([jira,audit,tallyAudits[audit],'=HYPERLINK("https://lowesinnovation.atlassian.net/browse/{}")'.format(jira),'=HYPERLINK("https://lowesinnovation.atlassian.net/secure/RapidBoard.jspa?rapidView=18&search={}")'.format(audit)])
				printingList.add(audit)
			else:
				print('Skipping Row {}, {}'.format(audit,jira))
		print("Totals for {}".format(inputName))
		print("{} Audits: {}".format(inputName.split('\\')[-1],auditCount))
		print("{} Totals: {}".format(inputName.split('\\')[-1],auditCount,dupeCount))
	return {'uniqueAudit':uniqueAuditSet, 'dupeAudit':dupeAudit, 'JIRA':uniqueJIRAS, 'auditCount':auditCount, 'dupeCount':dupeCount, 'rows':rowCount, 'products':productsInAudit}
	

# Unused
def csv_parser_set_processor(csv1, csv2):
	#for unique_audit in dupeAudit:
	if csv2 != None:
		uniqueAuditsDiff = csv1['uniqueAudit'] ^ csv2['uniqueAudit']
		uniqueJIRASDiff = csv1['JIRA'] ^ csv2['JIRA']

	
#Doesn't return anything yet
def compare_csv_parsers(csv1, csv2):
	try:
		if csv2 != None:
			auditTotals = csv1['auditCount'] + csv2['auditCount']
			dupeTotals = csv1['dupeCount'] + csv2['dupeCount']
			rowCounts = (csv1['rows']-1) + (csv2['rows']-1)
		else:
			auditTotals = csv1['auditCount']
			dupeTotals = csv1['dupeCount']
			rowCounts = (csv1['rows']-1)
			
	except:
		print('No File to compare')


def main():
	try:
		if len(sys.argv) < 2:
		    print 'Please provide a File to to search through.'
		    sys.exit(-1)

		input_csv_file = sys.argv[1]
		## Make Output file generic, rather than arg
		python_output_csv_file = sys.argv[3]
		try:
			additional_input_csv = sys.argv[4]
		except IndexError:
			additional_input_csv = None


		with open(python_output_csv_file, 'wb') as output_audits_csv:
			writer = csv.writer(output_audits_csv, quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['JIRA','Audit #',"JIRA's In Audit", 'Link to one JIRA in Audit','Audit Search in Kanban Board'])
			uniqueCSV1 = csv_parser(input_csv_file, writer)
			

			if additional_input_csv != None:
				uniqueCSV2 = csv_parser(additional_input_csv, writer)
			else:
				uniqueCSV2 = None


			csv_parser_set_processor(uniqueCSV1, uniqueCSV2)
			compare_csv_parsers(uniqueCSV1, uniqueCSV2)


		print("Audit's written to CSV: {}".format(auditTotals))
		print("Duplicate Audits found: {}".format(dupeTotals))
		print("Total Count: \t\t{}".format(auditTotals + dupeTotals))
		print("Total Products Parsed: \t{}".format(rowCounts))
	except Exception as e:
		print(e)
	finally:
		try:
			if sys.argv[2] == 'delete':
				os.remove(input_csv_file)
				try:
					os.remove(additional_input_csv)
				except:
					print('No additional CSV file')
				print("Input Files Removed!")
		except IndexError:
			print("Keeping Original Files")
	print('Done')



if __name__ == '__main__':
	main()
