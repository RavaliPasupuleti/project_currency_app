
class Error(Exception):
    def __init__(self, arg):
        self.msg = arg


class Country:

    name = ""
    currency_code = ""
    currency_symbol = ""

    def __init__(self, name, currency_code, currency_symbol):
        self.name = name
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol


    def format_currency(self, amount):
        rounded_amount = amount/100
        rounded_cent = round(rounded_amount)
        rounded_cent_amount = rounded_cent*100
        return self.currency_symbol + "" + str(rounded_cent_amount)

    def __str__(self):
        return  self.name + " " + self.currency_code + " " + self.currency_symbol



class Details:

    locations = []

    def __init__(self, locations):
       self.locations = locations

    def add(self, country_name, start_date, end_date):

            trip_detail = "\n" + country_name + "," + start_date + "," + end_date
            start_date_parts = start_date.split('/')
            end_date_parts = end_date.split('/')

            if len(start_date_parts) != 3:
                raise Error("Invalid Start Date Error" + trip_detail)
            elif len(start_date_parts[0]) != 4:
                raise Error("Invalid Start Date Error" + trip_detail)
            elif len(start_date_parts[1]) != 2:
                raise Error("Invalid Start Date Error" + trip_detail)
            elif len(start_date_parts[2]) != 2:
                raise Error("Invalid Start Date Error" + trip_detail)

            try:
                start_year = int(start_date_parts[0])
                start_month = int(start_date_parts[1])
                start_day = int(start_date_parts[2])

            except ValueError:
                raise Error("Invalid Start Date Error" + trip_detail)

            if len(end_date_parts) != 3:
                raise Error("Invalid End Date Error" + trip_detail)
            elif len(end_date_parts[0]) != 4:
                raise Error("Invalid End Date Error" + trip_detail)
            elif len(end_date_parts[1]) != 2:
                raise Error("Invalid End Date Error"+ trip_detail)
            elif len(end_date_parts[2]) != 2:
                raise Error("Invalid End Date Error" + trip_detail)

            try:
                end_year = int(end_date_parts[0])
                end_month = int(end_date_parts[1])
                end_day = int(end_date_parts[2])

            except ValueError:
                raise Error("Invalid End Date Error" + trip_detail)

            if int(start_date_parts[0]) > int(end_date_parts[0]):
                raise Error("Start Date Greater than End Date"+ trip_detail)
            elif int(start_date_parts[1]) > int(end_date_parts[1]):
                raise Error("Start Date Greater than End Date"+ trip_detail)
            elif int(start_date_parts[2]) > int(end_date_parts[2]):
                raise Error("Start Date Greater than End Date"+ trip_detail)

            list_of_locations = self.locations
            if len(list_of_locations) != 0:
                for each_trip in list_of_locations:
                    # print(each_trip)

                    each_trip_start_date = each_trip[1]
                    each_trip_end_date = each_trip[2]

                    each_trip_start_date_array = each_trip_start_date.split('/')
                    each_trip_end_date_array = each_trip_end_date.split('/')

                    each_trip_start_date_tuple = (int(each_trip_start_date_array[0]), int(each_trip_start_date_array[1]), int(each_trip_start_date_array[2]))
                    each_trip_end_date_tuple = (int(each_trip_end_date_array[0]), int(each_trip_end_date_array[1]), int(each_trip_end_date_array[2]))

                    scheduled_trip_start_date_tuple = (start_year, start_month, start_day)
                    scheduled_trip_end_date_tuple = (end_year, end_month, end_day)


                    if each_trip_start_date_tuple <= scheduled_trip_start_date_tuple < each_trip_end_date_tuple:
                        raise Error(" Date alreday present in Trip Schedule. \n Trip Details :  " + str(each_trip))

                    if each_trip_start_date_tuple < scheduled_trip_end_date_tuple <= each_trip_end_date_tuple:
                        raise Error("Date alreday present in Trip Schedule. \n Trip Details :  " + str(each_trip))

                    if scheduled_trip_start_date_tuple < each_trip_start_date_tuple  and scheduled_trip_end_date_tuple > each_trip_end_date_tuple:
                        raise Error("Date alreday present in Trip Schedule. \n Trip Details :  " + str(each_trip))



                list_of_locations.append((country_name, start_date, end_date))
            else:
                list_of_locations.append((country_name, start_date, end_date))


            print("List of Locations : " + str(list_of_locations))

    def current_country(self, date_string):

        try:
            start_date_parts = date_string.split('/')
            if len(start_date_parts) != 3:
                raise Error("Invalid Input Date Error")
            elif len(start_date_parts[0]) != 4:
                raise Error("Invalid Input Date Error")
            elif len(start_date_parts[1]) != 2:
                raise Error("Invalid Input Date Error")
            elif len(start_date_parts[2]) != 2:
                raise Error("Invalid Input Date Error")

            try:
                start_year = int(start_date_parts[0])
                start_month = int(start_date_parts[1])
                start_day = int(start_date_parts[2])
                date_string_tuple = (start_year, start_month, start_day)

            except ValueError:
                raise Error("Invalid Input Date Error")

            list_of_locations = self.locations

            if len(list_of_locations) != 0:

                for each_trip in list_of_locations:

                    # print(each_trip)
                    each_trip_start_date = each_trip[1]
                    each_trip_end_date = each_trip[2]

                    start_date_array = each_trip_start_date.split('/')
                    end_date_array = each_trip_end_date.split('/')

                    start_date_tuple = (int(start_date_array[0]), int(start_date_array[1]), int(start_date_array[2]))
                    end_date_tuple = (int(end_date_array[0]), int(end_date_array[1]), int(end_date_array[2]))

                    if start_date_tuple < date_string_tuple < end_date_tuple:
                        print("Country on date : " + date_string + " - " + each_trip[0])
                        return  each_trip[0]
                        break

                raise  Error("Error : No Country Found on Date :" + date_string)
            raise  Error("Error : No Country Found on Date :" + date_string)

        except Error as custom_trip_error:
            print(custom_trip_error.msg)


    def is_empty(self):
        if len(self.locations) > 0:
            return "Is Not Empty"
        else:
            return "Empty"


