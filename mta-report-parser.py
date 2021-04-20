import xmltojson
import json
import requests

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.set_headless()
assert opts.headless  # Operating in headless mode
browser = Firefox(options=opts)

    #    results = browser.find_elements_by_class_name('indent')
    #    results = browser.find_elements_by_tag_name('a')
    #    results = browser.find_elements_by_id('detail-row-template')
            #print(result.tag_name)
                    #print(link.text)

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
        print("Code Comments for File = " + fileName)
        for result in results:
            codeComment = result.get_attribute('innerHTML')
            #jsonCodeComment = xmltojson.parse(codeComment)
            #print(jsonCodeComment)
            codeComments.append(codeComment)
        #break
        print(codeComments)
        return codeComments

def collect_code_comments(fileNames):
    for fileName in fileNames:
        print('========')
        extract_code_comments(fileName)
        print('========')


fileNames = get_file_list('html file input')
collect_code_comments(fileNames)

browser.quit()

