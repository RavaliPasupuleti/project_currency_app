import currency
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from functools import partial

import trip
import datetime


__author__ = 'Lindsay Ward'
STATES = {'QLD': "Queensland", 'NSW': "New South Wales", 'VIC': "Victoria", 'WA': "Western Australia",
          'TAS': "Tasmania", 'NT': "Northern Territory", 'SA': "South Australia", 'ACT': "Canberra",
          'NQ': "Cowboys!", 'NZ': "New Zealand"}


class AppUI(App):

    current_state = StringProperty()
    state_codes = ListProperty()
    validState = False
    today_date = ""
    locations = []
    conversionfactor = 21.0
    revConversionFactor = 100.22
    fromCountryTupple = []
    homeCountryTupple = []
    current_date_country = ""

    details = trip.Details(locations)

    def build(self):
        """ build Kivy app from the kv file """
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        self.validateConfig()
        # self.state_codes = sorted(STATES.keys())
        # self.current_state = self.state_codes[0]
        self.root.ids.home_country_currency_amount.bind(on_text_validate=partial(self.enterPressed,"A"))
        self.root.ids.from_country_currency_amount.bind(on_text_validate=partial(self.enterPressed,"B"))

        self.root.ids.home_country_currency_amount.bind(focus=partial(self.onFocus,"A"))
        self.root.ids.from_country_currency_amount.bind(focus=partial(self.onFocus,"B"))


        return self.root

    def change_state(self, state_code):
        """ handle change of spinner selection, output result to label widget """
        """self.root.ids.output_label.text = STATES[state_code]"""
        print("State Code"+state_code)
        newCountryTupple = currency.getDetails(state_code)
        self.fromCountryTupple = newCountryTupple
        self.getCurrencyConversion()
        timeNow = datetime.datetime.now().strftime ("%H:%M:%S")
        self.root.ids.trip_detail_info.text = "Updated at \n"+timeNow
        print(self.fromCountryTupple)

    def validateConfig(self):
        locations = self.locations
        details = self.details


        text_file = open("config.txt", "r")
        # fetching a list of values
        lines = text_file.readlines()
        #Source : http://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array
        print(lines[0])
        country = lines[0].replace('\n','')
        tuple = currency.getDetails(country)
        if len(tuple) == 0:
            self.root.ids.trip_detail_info.text = "Invalid country name \n "+country
            return

        try:

            for eachLine in lines[1:len(lines)]:

                eachLineTuppleSplit = eachLine.split(",")
                eachLineTuppleSplitCountry = eachLineTuppleSplit[0].replace("\n","")
                resultTupple = currency.getDetails(eachLineTuppleSplitCountry)

                if len(resultTupple) != 0:
                    print ""
                    self.state_codes.append(eachLineTuppleSplitCountry)
                    self.validState = False
                    details.add(eachLineTuppleSplitCountry,eachLineTuppleSplit[1].replace("\n",""),eachLineTuppleSplit[2].replace("\n",""))

                else:
                    self.root.ids.trip_detail_info.text = "Invalid country name \n "+eachLineTuppleSplitCountry
                    self.validState = False
                    return

                print(eachLineTuppleSplitCountry)

        except trip.Error as detailsError:
            print("Error :"+detailsError.msg)
            self.root.ids.trip_detail_info.text = "Invalid trip details \n "+detailsError.msg
            self.validState = False
            return


        self.root.ids.home_country.text = tuple[0]
        self.root.ids.trip_detail_info.text = "trip details accepted"

        self.today_date = datetime.datetime.now().strftime ("%Y/%m/%d")
        self.root.ids.date_today.text = "Today's Date is \n"+self.today_date
        self.current_date_country = details.current_country(self.today_date)
        self.root.ids.current_trip_location.text = "Current Trip Location \n"+self.current_date_country

        self.validState = True

    def button_pressed(self, button):
        if self.validState:
            print('app: ' + str(self))  # this is the app object
            print(self.details.current_country(self.today_date))
            self.root.ids.home_country_currency_amount.disabled = False
            self.root.ids.from_country_currency_amount.disabled = False
            self.root.ids.update_currency.disabled = True
            self.root.ids.from_country_currency_amount.focus = True
            self.homeCountryTupple = currency.getDetails(self.root.ids.home_country.text)
            self.fromCountryTupple = currency.getDetails(self.current_date_country)
            self.root.ids.state_selection.text = self.details.current_country(self.today_date)
            print(self.homeCountryTupple[1])
            print(self.fromCountryTupple[1])

    def getCurrencyConversion(self):
        self.conversionfactor = float(currency.convert(1,self.homeCountryTupple[1],self.fromCountryTupple[1]))
        self.revConversionFactor = float(currency.convert(1,self.fromCountryTupple[1],self.homeCountryTupple[1]))
        print(self.conversionfactor)


    def enterPressed(self, gid,value):
        print('User pressed enter in',gid,value.text)
        if (gid == "A"):
            try:
                if len(value.text) > 0 :
                    val = float(value.text)
                    self.root.ids.from_country_currency_amount.text = str(self.conversionfactor*val)
                    self.root.ids.trip_detail_info.text = self.homeCountryTupple[1]+"("+self.homeCountryTupple[2].replace("\r","")+") to "+self.fromCountryTupple[1]+" ("+self.fromCountryTupple[2].replace("\r","")+")"


            except ValueError:
                    self.root.ids.trip_detail_info.text = "Invalid Amount"
                    self.focus = True

        elif (gid == "B"):
            try:
                if len(value.text) > 0 :
                    val = float(value.text)
                    print(self.revConversionFactor*val)
                    self.root.ids.home_country_currency_amount.text = str(self.revConversionFactor*val)
                    self.root.ids.trip_detail_info.text = self.fromCountryTupple[1]+"("+self.fromCountryTupple[2].replace("\r","")+") to "+self.homeCountryTupple[1]+" ("+self.homeCountryTupple[2].replace("\r","")+")"


            except ValueError:
                    self.focus = True
                    self.root.ids.trip_detail_info.text = "Invalid Amount"



    def onFocus(self,gid,value,isFocus):
        print('User Focuss enter in',isFocus,id,value)
        if ((gid == "A") and (isFocus)):
            print("A IS FOCUS")
            self.root.ids.trip_detail_info.text = ""

        if ((gid == "B") and (isFocus)):
            print("B IS FOCUS")
            self.root.ids.trip_detail_info.text = ""


    def insert_text(self, substring, from_undo=False):
        from_undo = True




AppUI().run()
