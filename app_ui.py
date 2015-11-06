import currency
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from functools import partial

import trip
import datetime



class AppUI(App):

    current_state = StringProperty()
    state_codes = ListProperty()
    valid_state = False
    current_date = ""
    locations = []
    conversion_factor = 1
    reverse_conversion_factor = 1
    from_country_tuple = []
    home_cuntry_tuple = []
    current_date_country = ""
    is_currency_updated_flag = False

    details = trip.Details(locations)

    def build(self):
        """ build Kivy app from the kv file """
        self.title = "Foreign Exchange Calculator"
        self.root = Builder.load_file('gui')
        self.validate_config()
        # self.state_codes = sorted(STATES.keys())
        # self.current_state = self.state_codes[0]
        self.root.ids.home_country_currency_amount.bind(on_text_validate=partial(self.enter_pressed,"A"))
        self.root.ids.from_country_currency_amount.bind(on_text_validate=partial(self.enter_pressed,"B"))

        self.root.ids.home_country_currency_amount.bind(focus=partial(self.on_focus, "A"))
        self.root.ids.from_country_currency_amount.bind(focus=partial(self.on_focus, "B"))


        return self.root

    def change_state(self, state_code):

        if self.is_currency_updated_flag == False:
            print("Flag not updated")
            return
        new_country_tuple = currency.get_details(state_code)

        print(new_country_tuple)
        print(self.from_country_tuple)

        if (self.from_country_tuple and new_country_tuple[1] == self.from_country_tuple[1]):
             self.conversion_factor = 1
             self.reverse_conversion_factor = 1
             return
        if (new_country_tuple[1] == self.home_country_tuple[1]):
            self.home_country_tuple = new_country_tuple
            self.from_country_tuple = new_country_tuple
            self.conversion_factor = 1
            self.reverse_conversion_factor = 1
        else:
            self.from_country_tuple = new_country_tuple
            self.get_currency_conversion()
            current_time = datetime.datetime.now().strftime ("%H:%M:%S")
            self.root.ids.trip_detail_info.text = "Updated at \n" + current_time
            print(self.from_country_tuple)

    def validate_config(self):
        locations = self.locations
        details = self.details


        text_file = open("config.txt", "r")
        # getting the trip details
        lines = text_file.readlines()
        print(lines[0])
        country = lines[0].replace('\n','')
        tuple = currency.get_details(country)
        if len(tuple) == 0:
            self.root.ids.trip_detail_info.text = "Invalid country name \n " + country
            return

        try:

            for each_line in lines[1:len(lines)]:

                each_line_tuple_split = each_line.split(",")
                each_line_tuple_split_country = each_line_tuple_split[0].replace("\n","")
                result_tuple = currency.get_details(each_line_tuple_split_country)

                if len(result_tuple) != 0:
                    print ""
                    self.state_codes.append(each_line_tuple_split_country)
                    self.valid_state = False
                    details.add(each_line_tuple_split_country, each_line_tuple_split[1].replace("\n", ""), each_line_tuple_split[2].replace("\n",""))

                else:
                    self.root.ids.trip_detail_info.text = "Invalid country name \n " + each_line_tuple_split_country
                    self.valid_state = False
                    return

                print(each_line_tuple_split_country)

        except trip.Error as details_error:
            print("Error :"+ details_error.msg)
            self.root.ids.trip_detail_info.text = "Invalid trip details \n " + details_error.msg
            self.valid_state = False
            return


        self.root.ids.home_country.text = tuple[0]
        self.root.ids.trip_detail_info.text = "trip details accepted"

        self.current_date = datetime.datetime.now().strftime ("%Y/%m/%d")
        self.root.ids.current_date.text = "Today's Date is \n"+self.current_date
        self.current_date_country = details.current_country(self.current_date)
        self.root.ids.current_trip_location.text = "Current Trip Location \n" + self.current_date_country

        self.valid_state = True

    def button_pressed(self, button):
        self.is_currency_updated_flag = True
        if self.valid_state:
            print('app: ' + str(self))  # this is the app object
            print(self.details.current_country(self.current_date))
            self.root.ids.home_country_currency_amount.disabled = False
            self.root.ids.from_country_currency_amount.disabled = False
            self.root.ids.update_currency.disabled = True
            self.root.ids.from_country_currency_amount.focus = True
            self.home_country_tuple = currency.get_details(self.root.ids.home_country.text)
            #self.from_country_tuple = currency.get_details(self.current_date_country)
            self.root.ids.state_selection.text = self.details.current_country(self.current_date)


    def get_currency_conversion(self):
        self.conversion_factor = float(currency.convert(1, self.home_country_tuple[1], self.from_country_tuple[1]))
        self.reverse_conversion_factor = float(currency.convert(1, self.from_country_tuple[1], self.home_country_tuple[1]))
        print(self.conversion_factor)


    def enter_pressed(self, gid, value):
        print('User pressed enter in', gid, value.text)
        if (gid == "A"):
            try:
                if len(value.text) > 0 :
                    val = float(value.text)
                    self.root.ids.from_country_currency_amount.text = str(self.conversion_factor * val)
                    self.root.ids.trip_detail_info.text = self.home_country_tuple[1] + "(" + self.home_country_tuple[2].replace("\r","") + ") to " + self.from_country_tuple[1] + " (" + self.from_country_tuple[2].replace("\r","") + ")"


            except ValueError:
                    self.root.ids.trip_detail_info.text = "Invalid Amount"
                    self.focus = True

        elif (gid == "B"):
            try:
                if len(value.text) > 0 :
                    val = float(value.text)
                    print(self.reverse_conversion_factor * val)
                    self.root.ids.home_country_currency_amount.text = str(self.reverse_conversion_factor * val)
                    self.root.ids.trip_detail_info.text = self.from_country_tuple[1] + "(" + self.from_country_tuple[2].replace("\r", "") + ") to " + self.home_country_tuple[1] + " (" + self.home_country_tuple[2].replace("\r", "") + ")"


            except ValueError:
                    self.focus = True
                    self.root.ids.trip_detail_info.text = "Invalid Amount"



    def on_focus(self, gid, value, is_focus):
        print('User Focuss enter in', is_focus, id, value)
        if ((gid == "A") and (is_focus)):
            print("A IS FOCUS")
            self.root.ids.trip_detail_info.text = ""

        if ((gid == "B") and (is_focus)):
            print("B IS FOCUS")
            self.root.ids.trip_detail_info.text = ""


    def insert_text(self, substring, from_undo=False):
        from_undo = True


AppUI().run()
