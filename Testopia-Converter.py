"""
 Created by Luis Angamarca
 June 4, 2015
 Converts text files outputed from HP Quality Center into
 Testopia format xml file. Thus making files able to be
 imported into Testopia.
"""
import re

# function to iterate to next line variable in for loop below
def getNextLine(line, file, count):
    while (':' not in file[count+1]):
            count += 1
            line = line + file[count]
    return line

def cases(line, file, count):
    line = line + '<li>'
    while (':' not in file[count+1]):
        count += 1
        line = line + '\n' + file[count]
        if file[count+1] == '\n%%':
                line = line + '</li>'
                return line
    line = line + '</li>'
    return line

# getting input from user
path = input('Enter path to xml file: ')
product = input('Enter product: ')

# opening file and getting data
data = open(path, 'r')
textFile = data.readlines()
data.close()
textFile.append('\n%%')

# declaring variables
inID = False
inTitle = False
inTester = False
inDate = False
inCategory = False
inCase = False
inResult = False

ID = []
title = []
tester = []
date = []
category = []
caseWords = []
resultWords = []

lineCount = 0
num = -1
# converting tags
for line in textFile:
    if 'Test ID' in line:
        num += 1
        caseWords.append([])
        resultWords.append([])
        inID = True
    elif 'Test Name:' in line:
        inTitle = True
    elif 'Designer:' in line:
        inTester = True
    elif 'Creation Date:' in line:
        inDate = True
    elif 'Status:' in line:
        inCategory = True
    elif 'Description:' in line:
        inCase = True
    elif 'Expected Result:' in line:
        inResult = True


    if inID:
        line = line.replace('Planning ReportPlanning ReportTest ', '')
        line = line.replace('ID (','')
        line = line.replace('Test ID (','')
        line = re.sub('\) \- [0-9]+.[0-9]+.[0-9]+ .*', '', line)
        line = line.replace('\n','')
        ID.append(line)
        inID = False
    elif inTitle:
        line = re.sub(' *Test Name: ', '', line)
        line = getNextLine(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        line = line.replace('\n', '')
        title.append(line)
        inTitle = False
    elif inTester:
        line = line.replace('Designer: ', '')
        line = getNextLine(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        line = re.sub(' \(.+\,* .+\)', '', line)
        line = line.replace('\n', '')
        tester.append(line)
        inTester = False
    elif inDate:
        line = line.replace('Creation Date: ', '')
        line = getNextLine(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        line = line.replace('\n', '')
        date.append(line)
        inDate = False
    elif inCategory:
        line = line.replace('Status: ', '')
        line = getNextLine(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        line = line.replace('\n', '')
        category.append(line)
        inCategory = False
    elif inCase:
        line = cases(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        caseWords[num].append(line)
        inCase = False
    elif inResult:
        line = cases(line, textFile, lineCount)
        line = re.sub(' + ', '', line)
        resultWords[num].append(line)
        inResult = False

    lineCount += 1

# formarting and cleaning up output
finalCopy = '<?xml version="1.0" ?>\n<tr:testopia version="2.3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:tr="http://www.mozilla.org/projects">\n<tr:testplan id="1">\n<tr:name>Imported Tests</tr:name>\n<tr:product id="1">' + product + '</tr:product>\n<tr:author id="1">\n<tr:login></tr:login>\n<tr:name></tr:name>\n</tr:author>\n<tr:plan_type id="1">Product</tr:plan_type>\n<tr:default_product_version>unspecified</tr:default_product_version>\n<tr:creation_date>2015-05-25T14:18:24</tr:creation_date>\n<tr:last_changed>2015-05-25T14:18:24</tr:last_changed>\n<tr:archived>false</tr:archived>\n<tr:document version="1">\n<tr:author>import</tr:author>\n<tr:text><![CDATA[Importing test cases.<br>]]></tr:text>\n</tr:document>\n\n\n'

for i in range(0,num+1):
    author = '<tr:author>' + tester[i] + '</tr:author>\n'
    userDetails = '<tr:login>' + tester[i] + '@email.com</tr:login>\n<tr:name>' + tester[i] + '</tr:name>\n'
    testcaseStart = '<tr:testcase>\n<tr:summary>' + title[i]
    testcaseEnding = '</tr:summary>\n<tr:case_status>CONFIRMED</tr:case_status>\n<tr:priority>Normal</tr:priority>\n<tr:category>\n<tr:name>Imported</tr:name>\n<tr:product>' + product + '</tr:product>\n</tr:category>\n<tr:author>\n'+ userDetails + '</tr:author>\n<tr:creation_date>2015-05-27T11:53:29</tr:creation_date>\n<tr:last_changed>2015-05-27T11:53:29</tr:last_changed>\n<tr:estimated_time>00:00:00</tr:estimated_time>\n<tr:isautomated>false</tr:isautomated>\n<tr:script></tr:script>\n<tr:arguments></tr:arguments>\n<tr:sortkey>1</tr:sortkey>\n<tr:requirement></tr:requirement>\n<tr:run_count>1</tr:run_count>\n<tr:blocks></tr:blocks>\n<tr:dependson></tr:dependson>\n<tr:bugs></tr:bugs>\n<tr:linked_plans>1</tr:linked_plans>\n<tr:text version="3">\n' + author + '<tr:action><![CDATA[<ol>\n'
    finalCopy = finalCopy + testcaseStart + testcaseEnding
    for j in range(0, len(caseWords[i])):
        finalCopy = finalCopy + caseWords[i][j]
    finalCopy = finalCopy + '\n</ol>]]></tr:action>\n<tr:expected_result><![CDATA[<ol>\n'
    for j in range(0, len(resultWords[i])):
        finalCopy = finalCopy + resultWords[i][j]
    finalCopy = finalCopy + '\n</ol>]]></tr:expected_result>\n</tr:text>\n</tr:testcase>\n\n\n'

finalCopy = finalCopy.replace('&', 'and')
finalCopy = finalCopy.replace('Description:', '')
finalCopy = finalCopy.replace('Expected Result:', '')
finalCopy = re.sub('Step [0-9]+','',finalCopy)
finalCopy = finalCopy + '\n</tr:testplan>\n</tr:testopia>'

# writing output to new file
output = open('output.xml', 'w')
output.write(finalCopy)
output.close()

print('Done')
