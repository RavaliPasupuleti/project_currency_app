
class Error(Exception):
    def __init__(self, arg):
        self.msg = arg



class Country:

    name = ""
    currency_code = ""
    currency_symbol = ""

    def __init__(self, name , currency_code , currency_symbol):
        self.name = name
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol


    def formatCurrency(self,amount):
        roundedAmount = amount/100
        roundededCent = round(roundedAmount)
        roundedCentAmount = roundededCent*100
        return self.currency_symbol+""+str(roundedCentAmount)

    def __str__(self):
        return  self.name+" "+self.currency_code +" "+self.currency_symbol



class Details:

    locations = []

    def __init__(self, locations):
       self.locations = locations

    def add(self,country_name,start_date, end_date):

            tripDetail = "\n"+country_name+","+start_date+","+end_date
            start_date_parts = start_date.split('/')
            end_date_parts = end_date.split('/')

            if len(start_date_parts) != 3:
                raise Error("Invalid Start Date Error"+tripDetail)
            elif len(start_date_parts[0]) != 4:
                raise Error("Invalid Start Date Error"+tripDetail)
            elif len(start_date_parts[1]) != 2:
                raise Error("Invalid Start Date Error"+tripDetail)
            elif len(start_date_parts[2]) != 2:
                raise Error("Invalid Start Date Error"+tripDetail)

            try:
                startYear = int(start_date_parts[0])
                startMonth = int(start_date_parts[1])
                startDay = int(start_date_parts[2])

            except ValueError:
                raise Error("Invalid Start Date Error"+tripDetail)

            if len(end_date_parts) != 3:
                raise Error("Invalid End Date Error"+tripDetail)
            elif len(end_date_parts[0]) != 4:
                raise Error("Invalid End Date Error"+tripDetail)
            elif len(end_date_parts[1]) != 2:
                raise Error("Invalid End Date Error"+tripDetail)
            elif len(end_date_parts[2]) != 2:
                raise Error("Invalid End Date Error"+tripDetail)

            try:
                endYear = int(end_date_parts[0])
                endMonth = int(end_date_parts[1])
                endDay = int(end_date_parts[2])

            except ValueError:
                raise Error("Invalid End Date Error"+tripDetail)

            if int(start_date_parts[0]) > int(end_date_parts[0]):
                raise Error("Start Date Greater than End Date"+tripDetail)
            elif int(start_date_parts[1]) > int(end_date_parts[1]):
                raise Error("Start Date Greater than End Date"+tripDetail)
            elif int(start_date_parts[2]) > int(end_date_parts[2]):
                raise Error("Start Date Greater than End Date"+tripDetail)

            listLocs = self.locations
            if len(listLocs) != 0:
                for eachTrip in listLocs:
                    # print(eachTrip)

                    eachTripStartDate = eachTrip[1]
                    eachTripEndDate = eachTrip[2]

                    eachTripStartDateArray = eachTripStartDate.split('/')
                    eachTripEndDateArray = eachTripEndDate.split('/')

                    eachTripStartDateTupple = (int(eachTripStartDateArray[0]),int(eachTripStartDateArray[1]),int(eachTripStartDateArray[2]))
                    eachTripEndDateTupple = (int(eachTripEndDateArray[0]),int(eachTripEndDateArray[1]),int(eachTripEndDateArray[2]))

                    scheduledTripStartDateTupple = (startYear,startMonth,startDay)
                    scheduledTripEndDateTupple = (endYear,endMonth,endDay)


                    if eachTripStartDateTupple <= scheduledTripStartDateTupple < eachTripEndDateTupple:
                        raise Error(" Date alreday present in Trip Schedule. \n Trip Details :  "+str(eachTrip))

                    if eachTripStartDateTupple < scheduledTripEndDateTupple <= eachTripEndDateTupple:
                        raise Error("Date alreday present in Trip Schedule. \n Trip Details :  "+str(eachTrip))

                    if scheduledTripStartDateTupple < eachTripStartDateTupple  and scheduledTripEndDateTupple > eachTripEndDateTupple:
                        raise Error("Date alreday present in Trip Schedule. \n Trip Details :  "+str(eachTrip))



                listLocs.append((country_name,start_date, end_date))
            else:
                listLocs.append((country_name,start_date, end_date))


            print("List of Locations : "+ str(listLocs))

    def current_country(self,date_string):

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
                startYear = int(start_date_parts[0])
                startMonth = int(start_date_parts[1])
                startDay = int(start_date_parts[2])
                date_string_tupple = (startYear,startMonth,startDay)

            except ValueError:
                raise Error("Invalid Input Date Error")

            listLocs = self.locations

            if len(listLocs) != 0:

                for eachTrip in listLocs:

                    # print(eachTrip)
                    eachTripStartDate = eachTrip[1]
                    eachTripEndDate = eachTrip[2]

                    startDateArray = eachTripStartDate.split('/')
                    endDateArray = eachTripEndDate.split('/')

                    startDateTupple = (int(startDateArray[0]),int(startDateArray[1]),int(startDateArray[2]))
                    endDateTupple = (int(endDateArray[0]),int(endDateArray[1]),int(endDateArray[2]))

                    if startDateTupple < date_string_tupple < endDateTupple:
                        print("Country on date : "+date_string+" - " + eachTrip[0])
                        return  eachTrip[0]
                        break
                        #Source : http://stackoverflow.com/questions/5464410/how-to-tell-if-a-date-is-between-two-other-dates-in-python

                raise  Error("Error : No Country Found on Date :"+date_string)
            raise  Error("Error : No Country Found on Date :"+date_string)

        except Error as customTripError:
            print(customTripError.msg)




    def isEmpty(self):
        if len(self.locations) > 0:
            return "Is Not Empty"
        else:
            return "Empty"


