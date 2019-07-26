#usr/env/bin pyhton

import csv
import sys
import re
import string
import os

if len(sys.argv) < 2:
    print 'Please provide a File to to search through.'
    sys.exit(-1)

input_csv_file = sys.argv[1]	
python_output_csv_file = sys.argv[2]
try:
	additional_input_csv = sys.argv[3]
except IndexError:
	additional_input_csv = None

def isAuditCheck(text):
	listOfAudits = []
	searchTerms = re.compile(r'[a-zA-Z0-9]{3}\d{3},$')
	results = re.search(searchTerms, text)
	print(results)
	# if type(results) != None:
	# 	for result in results:
	# 		listOfAudits = listOfAudits + result
	# 		print(result)
	# 	return listOfAudits
	# else:
	# 	return None

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
			# print(summary)
			# print(row[2])
			uniqueAudit = isAuditCheck(summary)
			print(uniqueAudit)
			if type(uniqueAudit) != None:
				for audit in uniqueAudit:
					if audit not in dupeAudit:
						print('Audit Found #: ' + audit)
						uniqueAuditSet.add(audit)
						writer.writerow([jira,audit,"https://lowesinnovation.atlassian.net/browse/" + jira,"https://lowesinnovation.atlassian.net/secure/RapidBoard.jspa?rapidView=18&search="+audit])
						dupeAudit.add(audit)
						uniqueJIRAS.add(jira)
						auditCount += 1
					else:
						print('Audit Found #: ' + audit + ' But is a duplicate')
						dupeAudit.add(audit)
						dupeCount += 1
			else:
				continue
			#print('Row Parsed, Next Row Starting')
		print("Totals for {}".format(inputName))
		print("Audits: {}".format(auditCount))
		print("Totals: {}".format(auditCount,dupeCount))
	return {'uniqueAudit':uniqueAuditSet, 'dupeAudit':dupeAudit, 'JIRA':uniqueJIRAS, 'auditCount':auditCount, 'dupeCount':dupeCount, 'rows':rowCount}
						

with open(python_output_csv_file, 'wb') as output_audits_csv:
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
		
try:
	if additional_input_csv != None:
		auditTotals = uniqueCSV1['auditCount'] + uniqueCSV2['auditCount']
		dupeTotals = uniqueCSV1['dupeCount'] + uniqueCSV2['dupeCount']
		rowCounts = (uniqueCSV1['rows']-1) + (uniqueCSV2['rows']-1)
	else:
		auditTotals = uniqueCSV1['auditCount']
		dupeTotals = uniqueCSV1['dupeCount']
		rowCounts = (uniqueCSV1['rows']-1)
except:
	print('No File to compare')
	
print("Audit's written to CSV: {}".format(auditTotals))
print("Duplicate Audits found: {}".format(dupeTotals))
print("Total Count: \t\t{}".format(auditTotals + dupeTotals))
print("Total Products Parsed: \t{}".format(rowCounts))
try:
	if not sys.argv[4]:
		os.remove(input_csv_file)
		os.remove(additional_input_csv)
		print("Input Files Removed!")
except IndexError:
	print("Keeping Original Files")
print('Done')
