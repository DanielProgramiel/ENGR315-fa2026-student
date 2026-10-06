import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###
#Import the data from the NYT database and store it in a variable
us_counties_data = parse_nyt_data('../../data/covid/us-counties.csv')

#Define the FIPS codes for Harrisonburg and Rockingham County, found from VDH Roster.
harrisonburg_FIPS = '51660'
rockingham_FIPS = '51165'

#Create empty lists for each data set and location. The data sets that will be generated are the complete data set, the new cases and the 7-day average of new cases for both harrisonburg and Rockingham County.
harrisonburg_data = []
rockingham_data = []

harrisonburg_new_cases_data = []
harrisonburg_week_average_data = []

rockingham_new_cases_data = []
rockingham_week_average_data = []

for entry in us_counties_data:
    # Loop through the us_counties_data for each location and store the data in the appropriate list.
    if entry[3] == harrisonburg_FIPS:
        #Create a dedicated list for harrisonburg and rockingham data
        harrisonburg_data.append(entry)
    if entry[3] == rockingham_FIPS:
        rockingham_data.append(entry)

for i in (range(len(harrisonburg_data))):
    # Loop through the COVID data for each location and calculate the new cases for each day as the difference from the prior day
    if i == 0:
        #Auto populate the first index to avoid taking the -1 index in the following step.
        harrisonburg_new_cases_data.append(harrisonburg_data[i][4])
    else:
        #The difference in cases from the prior day to the cases in the current day is the number of new cases. It can be both positive and negative.
        harrisonburg_new_cases_data.append((harrisonburg_data[i][4]-harrisonburg_data[i-1][4]))
for i in (range(len(rockingham_data))):
    if i == 0:
        rockingham_new_cases_data.append(rockingham_data[i][4])
    else:
        rockingham_new_cases_data.append((rockingham_data[i][4]-rockingham_data[i-1][4]))

#The length of a list of the 7-day averages will be 6 less than the length of the list of new cases since it takes 7 data points to produce one average, so each index of the new data set corresponds to 7 datapoints of the old data set.
for i in range(len(harrisonburg_new_cases_data)-6):
    #Take the moving sum over a 7 day period and divide by 7 to get the average for that week, then append it to the list
    harrisonburg_week_average_data.append(sum(harrisonburg_new_cases_data[i:i+7])/7)
for i in range(len(rockingham_new_cases_data)-6):
    rockingham_week_average_data.append(sum(rockingham_new_cases_data[i:i+7])/7)


# The us_counties_data only starts after the first reported case, so the date of the postive case is the first data point.

# Question 1.1: Date of the first case in Harrisonburg, VA
print("Harrisonburg First Case Date: " + harrisonburg_data[0][0])
# Question 1.2: Date of the first case in Rockingham, VA
print("Rockingham First Case Date: " + rockingham_data[0][0])

# Question 2.1: Worst day for new cases in Harrisonburg, VA
print("Worst Day for New Cases in Harrisonburg: " + harrisonburg_data[harrisonburg_new_cases_data.index(max(harrisonburg_new_cases_data))][0])
# Question 2.2: Worst day for new cases in Rockingham, VA
print("Worst Day for New Cases in Rockingham: " + rockingham_data[rockingham_new_cases_data.index(max(rockingham_new_cases_data))][0])

# Question 3.1: 7-day maximum for new cases in Harrisonburg, VA
print("7-Day Maximum for New Cases in Harrisonburg: ",harrisonburg_data[harrisonburg_week_average_data.index(max(harrisonburg_week_average_data))][0]," to ",harrisonburg_data[harrisonburg_week_average_data.index(max(harrisonburg_week_average_data))+6][0])
# Question 3.2: 7-day maximum for new cases in Rockingham, VA   
print("7-Day Maximum for New Cases in Rockingham: ",rockingham_data[rockingham_week_average_data.index(max(rockingham_week_average_data))][0]," to ",rockingham_data[rockingham_week_average_data.index(max(rockingham_week_average_data))+6][0])