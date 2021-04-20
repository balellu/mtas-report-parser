import xmltojson
import json
import requests

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True

browser = Firefox(options=opts)

def get_file_list(issuesFileName):
    browser.get(issuesFileName)

    if browser.page_source.find('Migration Mandatory'):
        results = browser.find_elements_by_class_name('toggle')
        for result in results:
            result.click()
        #break
        
        results = browser.find_elements_by_class_name('indent')
        finalFileNameList = list()
        for result in results:
            innerLinks = result.find_elements_by_tag_name('a')
            if type(innerLinks) == list:
                for link in innerLinks:                   
                    longFileName = link.get_attribute('href')
                    questionMark = longFileName.find('?')
                    if questionMark != -1:
                        fileName = longFileName[:questionMark]
                        finalFileNameList.append(fileName)
                 #break
        #break
        return finalFileNameList
    else :
        print('Migration is not Mandatory')

def extract_code_comments(fileName):
    browser.get(fileName)
    results = browser.find_elements_by_class_name('inline-source-hint-group')

    codeComments = list()
    if type(results) == list and len(results) > 0:
        for result in results:
            codeComment = result.get_attribute('innerHTML')
            tempStr = '<root>' + codeComment + '</root>'
            jsonCodeComment = xmltojson.parse(tempStr)
            codeComments.append(jsonCodeComment)
        #break
        print('========')
        print("Code Comments for File = " + fileName)
        print('----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ')
        print(codeComments)
        print('========')
        return codeComments

def collect_code_comments(fileNames):
    for fileName in fileNames:
        extract_code_comments(fileName)


fileNames = get_file_list('html file name')
collect_code_comments(fileNames)

browser.quit()

