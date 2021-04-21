import sys
import xmltojson
import json
import requests

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True

browser = Firefox(options=opts)

####
# This method prases the main html file to obtain list of issues html files.
# Typically this file is named as migration_issues.html
# This method uses selinium to load and parse the html
# Selinium is used because without it 'click' action cannot be triggered on the html to render the issues links
####
def get_migration_issues_file_list(issuesFileName):
    browser.get(issuesFileName)

    if browser.page_source.find('Migration Mandatory'):
        results = browser.find_elements_by_class_name('toggle') #finds DIV tags with links in it
        for result in results:
            result.click() #this will result in expansion of DIV tag rendering the issues links
        #break
        
        results = browser.find_elements_by_class_name('indent') #finds the DIV tags with issues link
        finalFileNameList = list()
        for result in results:
            innerLinks = result.find_elements_by_tag_name('a') #finds the issues links
            if type(innerLinks) == list:
                for link in innerLinks:                   
                    longFileName = link.get_attribute('href')
                    questionMark = longFileName.find('?')
                    if questionMark != -1:
                        fileName = longFileName[:questionMark] #gets the issues physical html file name
                        finalFileNameList.append(fileName)
                 #break
        #break
        return finalFileNameList
    else :
        print('Migration is not Mandatory')

####
# This method prases the issue html file and extracts
# code comments and writes them out as JSON files
# It creates the output file in the same location as main input file
####
def extract_code_comments(fileName):
    browser.get(fileName)
    results = browser.find_elements_by_class_name('inline-source-hint-group')

    codeComments = list()
    if type(results) == list and len(results) > 0:
        count = 1
        for result in results:
            codeComment = result.get_attribute('innerHTML')
            tempStr = '<codeComment>' + codeComment + '</codeComment>'
            jsonCodeComment = xmltojson.parse(tempStr)

            write_json_output_file(fileName, count, jsonCodeComment)
            count += 1

            codeComments.append(jsonCodeComment)
        #break
        
        #console_print_code(fileName, codeComments)
        
        return codeComments

####
# This method writes the json output files
####
def write_json_output_file(fileName, fileNum, jsonCodeComment):
    outputFileName = fileName[7:] + str(fileNum) + '.json'
    jsonOutputFile = open(outputFileName, 'w+')
    jsonOutputFile.write(jsonCodeComment)
    jsonOutputFile.close()
    print("Wrote the output File = " + outputFileName)
    print('----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ')

####
# This method writes the json output to the console for testing purpose
####
def console_print_code(fileName, codeComments):
    print('========')
    print("Code Comments for File = " + fileName)
    print('----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ')
    print(codeComments)
    print('========')

def collect_code_comments(fileNames):
    for fileName in fileNames: 
        extract_code_comments(fileName)

if len(sys.argv) == 2 and (str(sys.argv[1]) != None) and str(sys.argv[1]).find('file:///') != -1:
    migrationIssuesfileNames = get_migration_issues_file_list(str(sys.argv[1]))
    collect_code_comments(migrationIssuesfileNames)
else:
    print("Please provide migration issues html file path in the format of: file:///folder/migration_issues.html")

browser.quit()
