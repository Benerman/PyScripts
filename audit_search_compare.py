#usr/env/bin python

import csv
import sys
import re
import string
import os
import argparse

def isAuditCheck(text):
	# searchTerms = re.compile(r'[a-zA-Z0-9]{3}\d{3},$')
	searchTerms = re.compile(r'[a-zA-Z0-9]{3}\d{3},\s')
	result = re.search(searchTerms, text)
	if result:
		# print('Audit found is ' + str(result))
		return result.group(0)[0:5]
	else:
		return None


def CSVParser(inputName):
	uniqueAuditSet = set()
	dupeAudit = set()
	uniqueJIRAS = set()
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
			uniqueAudit = isAuditCheck(summary)
			if uniqueAudit != None:
				if uniqueAudit not in dupeAudit:
					print('Audit Found #: ' + uniqueAudit)
					uniqueAuditSet.add(uniqueAudit)
					writer.writerow([jira,uniqueAudit,"https://lowesinnovation.atlassian.net/browse/" + jira,"https://lowesinnovation.atlassian.net/secure/RapidBoard.jspa?rapidView=18&search="+uniqueAudit])
					dupeAudit.add(uniqueAudit)
					uniqueJIRAS.add(jira)
					auditCount += 1
				else:
					print('Audit Found #: ' + uniqueAudit + ' But is a duplicate')
					dupeAudit.add(uniqueAudit)
					dupeCount += 1
			else:
				continue
			#print('Row Parsed, Next Row Starting')
		print("Totals for {}".format(inputName))
		print("Audits: {}".format(auditCount))
		print("Totals: {}".format(auditCount, dupeCount))
	return {'uniqueAudit':uniqueAuditSet, 'dupeAudit':dupeAudit, 'JIRA':uniqueJIRAS, 'auditCount':auditCount, 'dupeCount':dupeCount, 'rows':rowCount}
						
parser = argparse.ArgumentParser(description='Search for Audits within a given CSV File, If second CSV given, will give difference between')
parser.add_argument('input_csv_file', help='CSV file to process', type=str) # Input CSV File

parser.add_argument('-c', '--compare', nargs='?') # Opt. CSV Compare file
parser.add_argument('-k', '--keep-file', help='Will keep file from being deleted', action='store_true') # Delete file
args= parser.parse_args()
print(args)

input_csv_file = args.input_csv_file	
additional_input_csv = args.compare

with open('audit_search_compare_output.csv', 'wb') as output_audits_csv:
	writer = csv.writer(output_audits_csv, quoting=csv.QUOTE_MINIMAL)
	writer.writerow(['JIRA','Audit #','Link to one JIRA in Audit','Audit Search in Kanban Board'])
	uniqueCSV1 = CSVParser(input_csv_file)
	
	if additional_input_csv != None:
		uniqueCSV2 = CSVParser(additional_input_csv)
	
	#for unique_audit in dupeAudit:
	if additional_input_csv != None:
		uniqueAuditsDiff = uniqueCSV1['uniqueAudit'] ^ uniqueCSV2['uniqueAudit']
		uniqueJIRASDiff = uniqueCSV1['JIRA'] ^ uniqueCSV2['JIRA']
	
		listAuditsDiff = list(uniqueAuditsDiff)
		listJIRASDiff = list(uniqueJIRASDiff)
	
		zippedList = zip(listAuditsDiff, listJIRASDiff)		
		
if additional_input_csv != None:
	auditTotals, dupeTotals, rowCounts =	(uniqueCSV1['auditCount'] + uniqueCSV2['auditCount'],
											 uniqueCSV1['dupeCount'] + uniqueCSV2['dupeCount'],
										    (uniqueCSV1['rows']-1) + (uniqueCSV2['rows']-1))
else:
	auditTotals, dupeTotals, rowCounts = 	(uniqueCSV1['auditCount'],
											 uniqueCSV1['dupeCount'],
											(uniqueCSV1['rows']-1))
	
print("Audit's written to CSV: {}".format(auditTotals))
print("Duplicate Audits found: {}".format(dupeTotals))
print("Total Count: \t\t{}".format(auditTotals + dupeTotals))
print("Total Products Parsed: \t{}".format(rowCounts))
if args.keep_file:
	print("Keeping Original Files")
else:
	os.remove(input_csv_file)
	os.remove(additional_input_csv)
	print("Input Files Removed!")
print('Done')
