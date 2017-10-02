# tabular-to-junit
Application to convert test results from simple tabular form (e.g. CSV) into JUnit XML format

# Usage example
Given test results file __input.csv__ with the following content
~~~
Suite1,Test1,com.test.my,Success,
Suite1,Test2,com.test.my,Success,
Suite1,Test3,com.test.my,Failed,Some dummy error!
Suite2,Test1,com.test.my,Success,
Suite2,Test2,com.test.my,Success,
Suite3,Test1,com.test.my,Success,
Suite3,Test2,com.test.my,Skipped,
Suite3,Test3,com.test.my,Success,
Suite2,Test3,com.test.my,Error,Some dummy error!
~~~
Running script:
~~~
toJUnit.py -i result.csv -c classname,name,package,status,message
~~~
Output file is __junit.xml__
~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
	<testsuite name="Suite2" errors="1" skipped="0" tests="3" failures="0" time="0" timestamp="0">
		<properties>
			<package>com.test.my</package>
		</properties>
		<testcase classname="Suite2" name="Test1" time="0">
		</testcase>
		<testcase classname="Suite2" name="Test2" time="0">
		</testcase>
		<testcase classname="Suite2" name="Test3" time="0">
			<error message="Some dummy error!">Test failed</error>
		</testcase>
	</testsuite>
	<testsuite name="Suite3" errors="0" skipped="1" tests="3" failures="0" time="0" timestamp="0">
		<properties>
			<package>com.test.my</package>
		</properties>
		<testcase classname="Suite3" name="Test1" time="0">
		</testcase>
		<testcase classname="Suite3" name="Test2" time="0">
			<skipped />
		</testcase>
		<testcase classname="Suite3" name="Test3" time="0">
		</testcase>
	</testsuite>
	<testsuite name="Suite1" errors="0" skipped="0" tests="3" failures="1" time="0" timestamp="0">
		<properties>
			<package>com.test.my</package>
		</properties>
		<testcase classname="Suite1" name="Test1" time="0">
		</testcase>
		<testcase classname="Suite1" name="Test2" time="0">
		</testcase>
		<testcase classname="Suite1" name="Test3" time="0">
			<failure message="Some dummy error!">Test failed</failure>
		</testcase>
	</testsuite>
</testsuites>
~~~


