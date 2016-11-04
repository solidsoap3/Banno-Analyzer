"""
File: HTMLAnalyzer.py
Author: Collin Eggena
Description: This program will pull in the HTML from the
Banno website and analyze the data, printing out useful information.
"""
import re
import requests

def main():
    response = requests.get("https://banno.com")
    HTMLText = response.text.split("\n")
    topThreeList = getTopThreeAlphanums(HTMLText)
    twitterHandle = getTwitterHandle(HTMLText)
    pngIndexList = getImageCount(HTMLText)
    finInstIndexList = getFinInstCount(HTMLText)
    platformFeatureIndexList = getPlatformFeatureCount(HTMLText)

    # Time to print out all the info.
    print("Analysis of Banno HTML\n"
          "----------------------------------------------\n"
          "Top three occurring alphanumeric characters:")
    for tup in topThreeList:
        print(tup[0],"occured",tup[1],"times")

    print("\nBanno twitter handle:",twitterHandle)

    print("\nNumber of .png images:",len(pngIndexList))

    print("\nNumber of occurrences of 'financial institution':",len(finInstIndexList))  

    print("\nNumber of platform features offered:",len(platformFeatureIndexList))

    input("\nPlease Press enter to quit.")


"""
Input: A string that is the text of an HTML file.
Output: A list of tuples with the top three occuring alphanumeric characters in
the file and the number of times each appeared.
Description: This function will take in an HTML file string and then return a
list with the top three most occurring alphanumeric characters in the file along
with the number of times each appeared. Note: the characters are case sensitive.
"""
def getTopThreeAlphanums(text):
    charDict = {}
    for line in text:
        for char in line:
            if not char.isalnum():
                pass
            elif char not in charDict:
                charDict[char] = 1
            else:
                charDict[char] += 1

# Loop three times to get the top three characters; pop maxValue each time
# so that we can easily get the second and then third most ocurring characters.
    topThreeList = []
    for i in range(3):
        maxValue = max(charDict, key=lambda key: charDict[key]) #python trick
        keyValueTuple = (maxValue, charDict.pop(maxValue))
        topThreeList.append(keyValueTuple)
        
    return topThreeList   


"""
Input: A string that is the text of an HTML file.
Output: A string that is the twitter handle for Banno.
Description: This function finds where the Banno twitter handle is defined in
the HTML of the Banno website and then returns it.
"""
def getTwitterHandle(text):
    for line in text:
        if "twitter:site" in line:
            twitterHandle = line[37:-2]
            break
        else:
            pass

    return twitterHandle


"""
Input: A string that is the text of an HTML file.
Output: A list containing the starting index of each match of the regular
expression.
Description: This function will use a regular expression to search the text of
an HTML file for all occurences of a png file and then append the starting index
to the index list.
"""
def getImageCount(text):
    indexList = []
    for line in text:
        for match in re.finditer(".png", line): #use regular expression
            indexList.append(match.start())

    return indexList


"""
Input: A string that is the text of an HTML file.
Output: A list containing the starting index of each match of the regular
expression.
Description: This function will use a regular expression to search the text of
an HTML file for all occurences of "financial institution" and then append
the starting index to the index list.
"""
def getFinInstCount(text):
    indexList = []
    for line in text:
        for match in re.finditer("financial institution", line): #regex
            indexList.append(match.start())

    return indexList


"""
Input: A string that is the text of an HTML file.
Output: A list containing the starting index of each match of the regular
expression.
Description: This function will use a regular expression to search the text of
an HTML file for all occurences of "platform-feature" and add the starting index
to the index list. Counting the occurences of "platform-feature" will give us
the number of platform features offered.
"""
def getPlatformFeatureCount(text):
    indexList = []
    for line in text:
        for match in re.finditer("platform-feature", line): #regex
            indexList.append(match.start())

    return indexList
    

main()

