# -*- coding: utf-8 -*-
import web_utility

#Function 1 convert
def convert(amount, home_currency_code, location_currency_code):

    urlString = "https://www.google.com/finance/converter?a="+str(amount)+"&from="+home_currency_code+"&to="+location_currency_code
    print(urlString)
    result = web_utility.load_page(urlString)

    try :
        indexofMatchedData = result.index('<span class=bld>')
        newmatchedString =  result[indexofMatchedData:]
        # This will return me this text <span class=bld>0.7426 AUD</span>\n<input type= ....>
        # Next I will take the data till </span> so as to get the currency
        newmatchedString = newmatchedString[newmatchedString.index('<span class=bld>')+16:newmatchedString.index('</span>')]
        # index of span class=bld + 16. 16 is length of <span class=bld> and hence start index to get value should be after +16.
        #output 10 USD
        # we just need 10
        return newmatchedString[0:newmatchedString.index(" ")]
    except ValueError :
        return "-1"


#Function 2 getDetails
def getDetails(countryName):
    text_file = open("currency details.txt", "r")
    # fetching a list of values
    lines = text_file.readlines()
    #Source : http://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array

    checkFlag = 0
    tup = ()
    for eachLine in lines:

        eachLineTuppleSplit = eachLine.split(",")
        # For loop and eachLine is the tupple for each currency
        if countryName.upper() == eachLineTuppleSplit[0].upper():
             print("Country Name Found")
             # In the next line we make a tupple and remove whitespace in the front for tupple index(0) and remove new line for index(2) so that we get proper output
             return (eachLineTuppleSplit[0].replace('\ufeff', ''),eachLineTuppleSplit[1],eachLineTuppleSplit[2].replace('\n',''))
             #Output ('Japan', 'JPY', '¥')


    return ()








