
import sys
import os
import glob
import argparse
from Util import Utilities

# Arguments description for application help
parser=argparse.ArgumentParser(
    description="""Script parses test results in raw text table format (e.g. CSV) to standard JUnit xml results file.""",
    epilog="""Good luck!""")

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-i", "--input", help="Input data location, either file(s) with test results or 'stdin' to parse from pipe. Multiple files supported, e.g. '*.txt'", required=True)
requiredNamed.add_argument("-c", "--columns", help="""List of column names. Defauld separator is comma (','), unless set with -s parameter. 
													Mandatory columns are: Name, Status, and Classname. Optional: Message.
													Other columns are also supported, see documentation for details.""", required=True)

parser.add_argument("-o", "--output", help="Destination JUnit xml. Default = 'junit.xml'", default="junit.xml")
parser.add_argument("-s", "--separator", help="Separator used in query. Default = ',' (comma, corresponds CSV)", default=",")
parser.add_argument("-ih", "--ignoreheader", help="Skip the first line in input file. Use it when table contains header.", action="store_true")
parser.add_argument("-v", "--verbose", help="Put extended log to console. Note: log may become rather heavy.", action="store_true")

args=parser.parse_args()

# Get argument values
inputFileLocation = args.input
isStdIn = (inputFileLocation.lower() == "stdin")
columnsMask = args.columns
outputFileLocation = args.output
separator = args.separator
ignoreHeader = args.ignoreheader
isVerbose = args.verbose
mandatoryColumns = ["name", "status", "classname"]

# Print something to console
def printToConsole( obj ):
	if isVerbose:
		print str(obj)

		
########## STEP 1. Check column mask for mandatory columns ##########
printToConsole("\nChecking the list of columns. Mandatory columns are:")
for column in mandatoryColumns:
	printToConsole("\t - " + column)
if not Utilities.checkColumnMask(columnsMask, separator, mandatoryColumns):
	quit()
print "\nList of columns is valid"


########## STEP 2. Parse files (or pipe input) into dictionary object ##########

# Process a single line
def processLines(f, dictionaries):
	dict = {}
	lineCount = 0
	for line in f:
		#Ignoring header (first line) if needed.
		if lineCount == 0:
			lineCount += 1
			if ignoreHeader:
				continue
		columns = columnsMask.lower().split(separator)
		values = line.split(separator)

		for column in columns:
			column = Utilities.sanitise(column.lower())
				
			#meaningless columns defined by 'null' or empty value
			if column == "null" or column == "":
				continue

			if len(values) <= columns.index(column):
				dict[column] = ""
			else:
				dict[column] = Utilities.sanitise(values[columns.index(column)])
			
		#'name' and 'classname' are mandatory. Ignoring lines without any of these fields.
		if not (dict["name"] == "" or dict["classname"] == "" or dict["status"] == ""):
			if dict["classname"] in dictionaries:
				dictionaries[dict["classname"]].append(dict.copy())
			else:
				dictionaries[dict["classname"]] = []
				dictionaries[dict["classname"]].append(dict.copy())

dictionaries = {}

if not isStdIn:
	files = glob.glob(inputFileLocation)
	print "\nInput files:" + str(files)
	for file in files:
		with open(file, 'r') as f:
			processLines(f, dictionaries)
else:
	print "\nInput at StdIn"
	processLines(sys.stdin, dictionaries)

	
########## STEP 3. Convert dictionary into result string ##########

aGroupsStringsList = ""			

for suite in dictionaries: # iterating test suites
	tests = ""
	testsNo = 0
	errorsNo = 0
	failuresNo = 0
	skippedNo = 0
	time = "0"
	timestamp = "0"
	suiteProperties = Utilities.getSuitePropertiesFromDictionary(dictionaries[suite])
	suitePropertiesStr = Utilities.getSuiteProperties(suiteProperties)
	
	for i in dictionaries[suite]: # iterating testcase
		testsNo += 1
		if Utilities.isFailed(i["status"]):
			failuresNo += 1
		elif Utilities.isSkipped(i["status"]):
			skippedNo += 1
		elif Utilities.isError(i["status"]):
			errorsNo += 1
			
		test = Utilities.getTestCaseFromDictionary(i, suiteProperties)
		tests += test

	suitString = Utilities.getTestSuite(suite, str(testsNo), str(errorsNo), str(failuresNo), str(skippedNo), time, timestamp, suitePropertiesStr, tests)
	aGroupsStringsList = aGroupsStringsList + suitString
	
finalXML = Utilities.getTestSuites(aGroupsStringsList)

print "\nParsing finished, result file: " + str(os.path.abspath(outputFileLocation))
printToConsole("\nResult data:\n\n" + finalXML)
	
fo = open(outputFileLocation,'w')
fo.write(finalXML) # python will convert \n to os.linesep
fo.close()

