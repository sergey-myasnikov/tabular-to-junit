
class Utilities:

	# Test execution status strings
	statusFaied = "FAIL"
	statusError = "ERR"
	statusSkipped = "SKIP"
	
	reservedFields = ["", "name", "status", "classname", "message", "suitname"]

	# Sanitise string to fit XML specification
	@staticmethod
	def sanitise(string):
		return string.strip().replace("\"",'&quot;').replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
		
	# Returns JUnit xml content as string
	@staticmethod
	def getTestSuites(str):
		str1 = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
		str2 =  "<testsuites>\n"
		str3 = str
		str4 =  "</testsuites>"
		return str1 + str2 + str3 + str4;
		
	# Returns testSuit string
	@staticmethod
	def getTestSuite(name, testsNo, errorsNo, failuresNo, skippedNo, time, timestamp, propertiesStr, testsStr):
		str1 =  "\t<testsuite name=\"" + name + "\" errors=\"" + errorsNo + "\" skipped=\"" + skippedNo + "\" tests=\"" + testsNo + "\" failures=\"" + failuresNo + "\" time=\"" + time + "\" timestamp=\"" + timestamp + "\">\n"
		str2 =  "\t</testsuite>\n"
		return str1 + propertiesStr + testsStr + str2;
		
	# Return testCase string
	@staticmethod
	def getTestCase(testName, className, time, status, message, other):
		str1 = "\t\t<testcase classname=\"" + className + "\" name=\"" + testName + "\" time=\"" + time + "\">\n"
		str1 = str1 + other
		if Utilities.isSkipped(status):
			str1 = str1 + "\t\t\t<skipped />\n"
		if Utilities.isFailed(status):	
			str1 = str1 + "\t\t\t<failure message=\"" + message + "\">Test failed</failure>\n"
		if Utilities.isError(status):
			str1 = str1 + "\t\t\t<error message=\"" + message + "\">Test failed</error>\n"
		str2 = "\t\t</testcase>\n"
		return str1 + str2
		
	# Return testcase string from a dictionary object
	@staticmethod	
	def getTestCaseFromDictionary(dict, suiteProperties):
		time = "0"
		message = ""
		other = ""
		if "time" in dict:
			time = dict["time"]
		if "message" in dict:
			message = dict["message"]
		for i in dict:
			if Utilities.isNotReserved(i) and i not in suiteProperties:
				other = other + "\t\t\t<" + i + ">" + str(dict[i]) + "</" + i + ">\n"
		res = Utilities.getTestCase(dict["name"], dict["classname"], time, dict["status"], message, other)
		return res

	# Return testSuite properties as a string
	@staticmethod	
	def getSuiteProperties(dict):
		if len(dict) == 0:
			return ""
		str1 = "\t\t<properties>\n"
		str2 = "\t\t</properties>\n"
		str = ""
		for i in dict:
			str = str + "\t\t\t<" + i + ">" + dict[i] + "</" + i + ">\n"
		return str1 + str + str2
		
	# Define common properties of testcases in test suite
	# If a value of a column is the same for all testcases in a suite,
	# the value can be put into suite properties
	@staticmethod
	def getSuitePropertiesFromDictionary(dict):
		res = {}
		isFirst = True
		for test in dict:
			for i in test:
				if Utilities.isNotReserved(i):
					if isFirst: #adding all properties
						res[i] = test[i]
						isFirst = False
					else: #just checking
						if i in res:
							if not test[i] == res[i]: #property value is different within a suite
								del res[i]
		return res
		
	# Check column mask for mandatory values
	@staticmethod
	def checkColumnMask(columnsMask, separator, mandatoryValues):
		columns = columnsMask.lower().split(separator)		
		result = True
		for value in mandatoryValues:
			if not value.lower() in columns:
				print "Mandatory column " + value.upper() + " is not defined! Please define it in columns list."
				result = False
		return result
		
	# Check whether status is FAILED
	@staticmethod
	def isFailed(status):
		return Utilities.statusFaied.lower() in status.lower()
		
	# Check whether status is ERROR
	@staticmethod
	def isError(status):
		return Utilities.statusError.lower() in status.lower()
		
	# Check whether status is SKIPPED
	@staticmethod
	def isSkipped(status):
		return Utilities.statusSkipped.lower() in status.lower()
		
	# Check whether property name is reserved
	@staticmethod
	def isNotReserved(fieldName):
		return fieldName not in Utilities.reservedFields

