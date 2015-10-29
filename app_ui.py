import currency
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
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

    def build(self):
        """ build Kivy app from the kv file """
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui.kv')
        self.validateConfig()
        # self.state_codes = sorted(STATES.keys())
        # self.current_state = self.state_codes[0]


        return self.root

    def change_state(self, state_code):
        """ handle change of spinner selection, output result to label widget """
        """self.root.ids.output_label.text = STATES[state_code]"""
        print "changed to", state_code

    def validateConfig(self):
        locations = []
        details = trip.Details(locations)


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

        today_date = datetime.datetime.now().strftime ("%Y/%m/%d")
        self.root.ids.date_today.text = "Today's Date is \n"+today_date
        current_date_country = details.current_country(today_date)
        self.root.ids.current_trip_location.text = "Current Trip Location \n"+current_date_country

        self.validState = True

    def button_pressed(self, button):
        if self.validState:
            print('app: ' + str(self))  # this is the app object


AppUI().run()
