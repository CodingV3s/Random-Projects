import requests
import pandas as pd
import xml.etree.cElementTree as ET
import matplotlib.pyplot as plt

what_year = input("what year would you like the yield curve for ? (1990-2018) :")

website = "http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20"+str(what_year)

resp = requests.get(website)

with open ("UStreasuryyieldcurve.xml", "wb") as f:
  f.write(resp.content)

filename = open("UStreasuryyieldcurve.xml", "rb")

tree = ET.parse(filename)
columns = ['1 month','2 month','3 month', '6 month','1 year','2 year','3 year','5 year','7 year', '10 year','20 year', '30 year']

data = pd.DataFrame(columns= columns)
data = data.fillna(0)

root = tree.getroot()
# finding the tag the should be iterated is essential,for a in use root.iter(): print (a.tag, a.attrib) this gives you the right tag
# here properties is nested inside entry -> content subchilds of the element, but you dont need to specify that just need the right tag
for a in root.iter('{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}properties'):
    c= []
    for b in a:
        c.append((b.text))
    data.loc[c[1][0:10]]= c[2:14]

# this had to be done as US government added a new 2 month bond as I was trying to code this thing
data = data.drop(['2 month'], axis = 1)
new_column = ['1 month','3 month', '6 month','1 year','2 year','3 year','5 year','7 year', '10 year','20 year', '30 year']

# apply to numeric method to change all the strings to a number so that it can be plotted
data[new_column] = data[new_column].apply(pd.to_numeric, errors=0, axis=1)
#print (data)

# changing string index to date time
data.index = pd.to_datetime(data.index)

""" Whats being done here is that all the daily data is grouped by month,average and put into a new dataframe
 this allow for the graph to be more easily viewed"""
monthly = data.groupby(pd.Grouper(freq='M')).mean()

monthly = monthly.T # required cause plot is performed column wise and not row wise

# this is done to access the properties of the particular plot
ax = monthly.plot(title = "US Treasury bond rate yield curve", grid = 1)

# sets number of points on the x-axis equal to the number of points in a column
ax.set_xticks(range(len(new_column)))

# sets each of the above tick with a label
ax.set_xticklabels(new_column, rotation='vertical')
plt.show()

