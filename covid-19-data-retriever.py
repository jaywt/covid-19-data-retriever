# last run on Tue Oct  6 10:53:54 EDT 2020
# last run on Wed Sep 23 16:52:20 EDT 2020
# last run on Tue Sep 22 13:39:57 EDT 2020
# last run on Mon Sep 21 15:37:56 EDT 2020
# last run on Sun Sep 20 17:30:40 EDT 2020
# last run on Mon Sep 14 16:07:26 EDT 2020
# last run on Mon Sep 14 01:33:03 EDT 2020
# last run on Tue Sep  8 11:36:02 EDT 2020
# last run on Wed Sep  2 12:07:24 EDT 2020
# last run on Thu Aug 27 16:59:22 EDT 2020
# last run on Sun Aug 23 13:41:00 EDT 2020
# last run on Sat Aug 22 11:59:27 EDT 2020
# last run on Wed Aug 19 14:05:57 EDT 2020
# last run on Mon Aug 17 14:15:16 EDT 2020
# last run on Fri Aug 14 17:02:46 EDT 2020
# last run on Wed Aug 12 14:55:41 EDT 2020
# last run on Sat Aug  8 10:56:24 EDT 2020
# last run on Sat Aug  1 15:36:06 EDT 2020
# last run on Mon Jul 27 00:42:27 EDT 2020
# last run on 07/17/2020 14:28:00
# last run on 07/06/2020 03:16:00
# last run on 06/25/2020 09:19:00
# last run on 06/10/2020 02:03:00
# last run on 05/31/2020 16:12:00
# last run on 05/27/2020 00:05:00
# last run on 05/20/2020 13:37:00
# last run on 05/08/2020 11:25:00
# last run on 04/27/2020 16:49:00
# last run on 04/22/2020 23:13:00
# last run on 04/21/2020 23:05:00
# last run on 04/18/2020 15:42:00
# last run on 04/18/2020 00:17:00
# last run on 04/16/2020 15:04:00
# last run on 04/15/2020 13:56:00
# last run on 04/13/2020 13:28:00
# last run on 04/11/2020 22:06:00
# last run on 04/10/2020 14:34:00
# last run on 04/09/2020 14:14:00
# last run on 04/08/2020 13:20:00
# last run on 04/07/2020 11:00:00
# last run on 04/06/2020 10:00:00
# last run on 04/04/2020 21:00:00

#!/usr/bin/env python

# In[2]:


import pandas as pd
import geopandas as gpd


# In[3]:


# retrieve data of confirmed cases
url1 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
US_confirmed = pd.read_csv(url1, dtype={'UID': str})


# In[4]:


# retrieve data of deaths
url2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
US_death = pd.read_csv(url2, dtype={'UID': str})


# In[5]:


# extract data from PA, MI,and NY
#PA_confirmed = US_confirmed[US_confirmed.UID.str.contains('84042')]
#MI_confirmed = US_confirmed[US_confirmed.UID.str.contains('84026')]
#NY_confirmed = US_confirmed[US_confirmed.UID.str.contains('84036')]
PA_MI_NY_confirmed = US_confirmed[US_confirmed['UID'].str.contains('84042|84026|84036', na=False)]
PA_MI_NY_death = US_death[US_death['UID'].str.contains('84042|84026|84036', na=False)]


# In[6]:


# remove additional columns
#PA_confirmed = PA_confirmed.iloc[:,[5]+list(range(11, len(PA_confirmed.columns), 1))]
#MI_confirmed = MI_confirmed.iloc[:,[5]+list(range(11, len(MI_confirmed.columns), 1))]
#NY_confirmed = NY_confirmed.iloc[:,[5]+list(range(11, len(NY_confirmed.columns), 1))]
PA_MI_NY_confirmed = PA_MI_NY_confirmed.iloc[:,[5,6,-1]]
PA_MI_NY_death = PA_MI_NY_death.iloc[:,[5,6,-1]]


# In[7]:


date = PA_MI_NY_confirmed.columns[2]


# In[8]:


# rename column names
PA_MI_NY_confirmed.rename(columns={'Admin2': 'County', 'Province_State': 'State',
                                   PA_MI_NY_confirmed.columns[2]: 'confirmed_cases'}, inplace=True)
PA_MI_NY_death.rename(columns={'Admin2': 'County', 'Province_State': 'State',
                               PA_MI_NY_death.columns[2]: 'deaths'}, inplace=True)


# In[9]:


PA_MI_NY_confirmed['Date'] = date
PA_MI_NY_death['Date'] = date


# In[10]:


# convert time column to time type
PA_MI_NY_confirmed['Date'] = pd.to_datetime(PA_MI_NY_confirmed['Date'])
PA_MI_NY_death['Date'] = pd.to_datetime(PA_MI_NY_death['Date'])


# In[11]:


PA_MI_NY_confirmed['State'].replace({"Pennsylvania": "PA", "Michigan": "MI", "New York": "NY"}, inplace=True)
PA_MI_NY_death['State'].replace({"Pennsylvania": "PA", "Michigan": "MI", "New York": "NY"}, inplace=True)


# In[12]:


# import county boundary geojson file
PA_county = gpd.read_file('../jaywt.github.io/covid19/county_boundary/PA_County.geojson')
MI_county = gpd.read_file('../jaywt.github.io/covid19/county_boundary/MI_County.geojson')
NY_county = gpd.read_file('../jaywt.github.io/covid19/county_boundary/NY_County.geojson')


# In[13]:


PA_MI_NY_boundary = pd.concat([PA_county, MI_county, NY_county], ignore_index=True)


# In[14]:


# remove additional columns in geojson
PA_MI_NY_boundary = PA_MI_NY_boundary.iloc[:,[2,6,19]]


# In[15]:


PA_MI_NY_boundary.rename(columns={'name': 'County', 'stusab': 'State', 'geometry': 'geometry'}, inplace=True)


# In[16]:


# merge number of cases file into geojson
PA_MI_NY_data = PA_MI_NY_boundary.merge(PA_MI_NY_confirmed, on=['County','State'])
PA_MI_NY_death_data = PA_MI_NY_boundary.merge(PA_MI_NY_death, on=['County','State'])


# In[17]:


PA_MI_NY_data.to_file("../jaywt.github.io/covid19/PA_MI_NY_latest_confirmed.geojson", driver='GeoJSON')


# In[18]:


PA_MI_NY_death_data.to_file("../jaywt.github.io/covid19/PA_MI_NY_latest_death.geojson", driver='GeoJSON')


# In[19]:


#########################
# codes bin
#########################
# convert from wide to long format
# PA_confirmed_long = pd.melt(PA_confirmed, id_vars=['Admin2'])

# PA_confirmed_long['time'] = PA_confirmed_long['time'].dt.strftime('%Y-%m-%d'+'T00:00:00')

# PA_county.to_file("PA_county_cases.geojson", driver='GeoJSON')

# PA_test = PA_county[PA_county['time'].isin(['2020-04-01T00:00:00', '2020-04-02T00:00:00'])]
# PA_test.to_file("PA_county_twodayscases.geojson", driver='GeoJSON')
