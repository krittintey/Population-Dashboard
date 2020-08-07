import pandas as pd
import os
import json 
from datetime import datetime
from os import scandir

# Import Population Data
def convertDate(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date

def getFileDetails():
    fileList = list()
    dir_entries = scandir('data/')
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            fileList.append([entry.name, info.st_mtime, convertDate(info.st_mtime)])
    return fileList

def importData():
    df = pd.read_csv('data/pop_data.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = df.set_index(keys='DATE')
    return df

def createDataForGraph(dataset):
    df = list()
    df_pop = list()
    df_birth = list()
    df_death = list()

    df_pop_male = dict(x=dataset.index, y=dataset['POP_MALE'], name='Male', type='line')
    df_pop_female = dict(x=dataset.index, y=dataset['POP_FEMALE'], name='Female', type='line')
    df_pop_total = dict(x=dataset.index, y=dataset['POP_MALE'] + dataset['POP_FEMALE'], name='Total', type='line')
    df_pop_house = dict(x=dataset.index, y=dataset['HOUSE'], name='House', type='line')

    df_birth_male = dict(x=dataset.index, y=dataset['BIRTH_MALE'], name='Male', type='line')
    df_birth_female = dict(x=dataset.index, y=dataset['BIRTH_FEMALE'], name='Female', type='line')
    df_birth_total = dict(x=dataset.index, y=dataset['BIRTH_MALE'] + dataset['BIRTH_FEMALE'], name='Total', type='line')

    df_death_male = dict(x=dataset.index, y=dataset['DEATH_MALE'], name='Male', type='line')
    df_death_female = dict(x=dataset.index, y=dataset['DEATH_FEMALE'], name='Female', type='line')
    df_death_total = dict(x=dataset.index, y=dataset['DEATH_MALE'] + dataset['DEATH_FEMALE'], name='Total', type='line')

    df_pop = [df_pop_male, df_pop_female, df_pop_house, df_pop_total]
    df_birth = [df_birth_male, df_birth_female, df_birth_total]
    df_death = [df_death_male, df_death_female, df_death_total]

    df = [df_pop, df_birth, df_death]
    return df

df_popData = importData()
df_year_indicators = df_popData.reset_index()
df_visualize = createDataForGraph(df_popData)
last_modified_update = False if os.environ['UPDATE_DATA'] == 'False' else True

