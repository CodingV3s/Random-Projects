import requests
import sys
import pandas as pd
import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt

BASE_DATA_URL = "http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData"


def yieldcurve_data(address):
    resp = requests.get(address)

    with open ("UStreasuryyieldcurve.xml", "wb") as f:
        f.write(resp.content)

    filename = open("UStreasuryyieldcurve.xml", "rb")

    tree = ET.parse(filename)
    filename.close()
    columns = ['1 month','2 month','3 month', '6 month','1 year','2 year','3 year','5 year','7 year', '10 year','20 year', '30 year']

    data = pd.DataFrame(columns= columns)
    data = data.fillna(0)

    root = tree.getroot()
    # finding the tag the should be iterated is essential,for a in use root.iter(): print (a.tag, a.attrib) this gives you the right tag
    # here properties is nested inside entry -> content subchilds of the element, but you dont need to specify that just need the right tag
    for element in root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
        nested_data= []
        for child in element:
            nested_data.append((child.text))
        data.loc[nested_data[1][0:10]]= nested_data[2:14]

    # this had to be done as US government added a new 2 month bond as I was trying to code this thing
    data = data.drop(['2 month'], axis = 1)
    new_column = ['1 month','3 month', '6 month','1 year','2 year','3 year','5 year','7 year', '10 year','20 year', '30 year']

    # apply to numeric method to change all the strings to a number so that it can be plotted
    data[new_column] = data[new_column].apply(pd.to_numeric, errors=0, axis=1)
    #print (data)

    # changing string index to date time
    data.index = pd.to_datetime(data.index)
    return data, new_column

def yieldcurve_plot(website):
    website_data, new_column = yieldcurve_data(website)
    """ Whats being done here is that all the daily data is grouped by month,average and put into a new dataframe
     this allow for the graph to be more easily viewed"""
    yearly_monthly = website_data.groupby(pd.Grouper(freq=year_or_month)).mean()
    print (yearly_monthly)
    yearly_monthly = yearly_monthly.T # required cause plot is performed column wise and not row wise

# this is done to access the properties of the particular plot
    ax = yearly_monthly.plot(title = "US Treasury bond rate yield curve", grid = 1)

# sets number of points on the x-axis equal to the number of points in a column
    ax.set_xticks(range(len(new_column)))

# sets each of the above tick with a label
    ax.set_xticklabels(new_column, rotation='vertical')
    plt.show()


def get_day_partially_inverted(website_data):
    for day in range(0, len(website_data)):
        # should print the first time the yield curve is partially inverted
        # A curve partially inverts when 30 year bond rate interest isnt the highest among the available bonds
        if website_data.iloc[day].idxmax()!='30 year' and website_data.iloc[day].idxmax()!='1 month':
            return day
    return None

def get_day_fully_inverted(website_data):
    for day in range(0, len(website_data)):
        # should print the first time the yield curve is partially inverted
        # A curve partially inverts when 30 year bond rate interest isnt the highest among the available bonds
        if website_data.iloc[day].idxmax()=='1 month':
            return day
    return None


def yieldcurve_analysis(website):
    website_data, new_column = yieldcurve_data(website)
    loop_printed = 'No'
    thisloop_printed = 'No'

    print(repr(website_data))

    day_partially_inverted = get_day_partially_inverted(website_data)
    day_fully_inverted = get_day_fully_inverted(website_data)

    if day_partially_inverted is not None:
        print ('The yield curve partially inverted')
        print (website_data.iloc[day_partially_inverted])
        website_data.iloc[day_partially_inverted].plot()
        plt.show()

    if day_fully_inverted is not None:
        print (f'The yield curve inverted\n')
        print (website_data.iloc[day_fully_inverted].argmax())
        print (website_data.iloc[day_fully_inverted])
        website_data.iloc[day_fully_inverted].plot()
        plt.show()

    if day_fully_inverted is None and day_partially_inverted is None:
        print ('The curve has not inverted this year')
        # percent_change = (website_data.iloc[len(website_data)]-website_data.iloc[0])*100/website_data.iloc[0]
        # print ('The percent change in bond rates for the year')
        # print (percent_change)
        # website_data.iloc[len(website_data)].plot()
        # plt.show()


def get_year_specific_url(year):
    return BASE_DATA_URL + "?$filter=year(NEW_DATE)%20eq%20"+str(year)

if __name__ == '__main__':
    print (' Hi I am Charles, I can plot yield curves from 1990-current year \n')
    print (' Would you like a plot from 1990-current year or would you like plot for a particular year showing 12 month \n')

    year_or_month = input( "Enter 'Y' if you want it for all the years or Enter 'M' if you want it for a particular year : ")

    if year_or_month =='Y' or year_or_month =='y':
        website = BASE_DATA_URL
    elif year_or_month =='M' or year_or_month =='m':
        what_year = input("what year would you like the yield curve for ? (1990-2018) : ")
        website = get_year_specific_url(what_year)
    else:
        print ('Invalid entry')
        sys.exit()

    yieldcurve_plot(website)

    analyze = input('Are you looking to analyze the data for the year (Y/N) : ')
    if analyze == 'Y' or analyze =='y':
        yieldcurve_analysis(website)
    else:
        print ('alright good bye')
