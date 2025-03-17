import requests
import pandas as pd
from typing import Any
from streamlit import cache_data
import os
import time

def file_age_in_days(file_path):
    """
    Calculate the age of a file in days.

    Parameters
    ----------
    file_path : str
        The path to the file to check.

    Returns
    -------
    age_in_days : int
        The age of the file in days, rounded down to the nearest whole number.
    """
    creation_time = os.path.getctime(file_path)
    current_time = time.time()
    age_in_days = (current_time - creation_time) / (24 * 3600)
    
    return int(age_in_days)

@cache_data
def get_indicators(indicator:str|None = None, get:str|None = None) -> Any:
    """
    Retrieves the list of available indicators from the IMF Data Mapper API.

    Parameters
    ----------
    indicator : str, optional
        The name of the indicator to retrieve the ID or unit for. If None, returns the entire list of indicators.
    get : str, optional
        If 'id', returns the ID of the specified indicator. If 'unit', returns the unit of the specified indicator.

    Returns
    -------
    data : pandas.DataFrame
        A DataFrame containing the list of indicators, their IDs, names, descriptions, units, and sources.
    id : str
        The ID of the specified indicator.
    unit : str
        The unit of the specified indicator.

    Raises
    ------
    Exception
        If the request to the API fails.
    """
    if os.path.isfile('data/indicators.csv') and file_age_in_days('data/indicators.csv') < 5:
        data = pd.read_csv('data/indicators.csv')
        if isinstance(indicator,str):
            if get == 'id':
                id = data[data['indicator_name'] == indicator]['indicator_id'].values[0]
                return id
            if get == 'unit':
                unit = data[data['indicator_id'] == indicator]['indicator_unit'].values[0]
                # print(unit)
                return unit
        return data
    else:
        url = r"https://www.imf.org/external/datamapper/api/v1/indicators"
        res = requests.get(url)
        if res.status_code == 200:
            json_res = dict(res.json())
            indicators_data = json_res['indicators']
            indicators = indicators_data.keys()
            data = {
                'indicator_id': [], 
                'indicator_name': [], 
                'indicator_description': [],  
                'indicator_unit': [], 
                'indicator_source': []
            }
            for indicator in indicators:
                if indicator == '':
                    continue
                data['indicator_id'].append(indicator)
                data['indicator_name'].append(str(indicators_data[indicator]['label']).replace('\n', ''))
                data['indicator_description'].append(str(indicators_data[indicator]['description']).replace('\n', ''))
                data['indicator_unit'].append(str(indicators_data[indicator]['unit']).replace('\n', ''))
                data['indicator_source'].append(str(indicators_data[indicator]['source']).replace('\n', ''))
            
            output = pd.DataFrame(data).dropna()
            output.to_csv('data/indicators.csv', index=False)

            if isinstance(indicator,str):
                if get == 'id':
                    id = output[output['indicator_name'] == indicator]['indicator_id'].values[0]
                    return id
                if get == 'unit':
                    unit = output[output['indicator_name'] == indicator]['indicator_unit'].values[0]
                    return unit

            return output
        else:
            raise Exception(f"Failed to get indicators list. Status code: {res.status_code}")

@cache_data
def get_countries(country:str|None = None, get:str|None = None) -> Any:
    """
    Retrieves the list of available countries from the IMF Data Mapper API.

    Parameters
    ----------
    country : str, optional
        The name of the country to retrieve the ID for. If None, returns the entire list of countries.
    get : str, optional
        If 'id', returns the ID of the specified country.

    Returns
    -------
    data : pandas.DataFrame
        A DataFrame containing the list of countries and their IDs.
    id : str
        The ID of the specified country.

    Raises
    ------
    Exception
        If the request to the API fails.
    """
    if os.path.isfile('data/countries.csv') and file_age_in_days('data/countries.csv') < 5:
        data = pd.read_csv('data/countries.csv')
        if isinstance(country,str):
            if get == 'id':
                id = data[data['country_name'] == country]['country_id'].values[0]
                return id
        return data
    else:
        url = r"https://www.imf.org/external/datamapper/api/v1/countries"
        res = requests.get(url)
        if res.status_code == 200:
            json_res = dict(res.json())
            countries_data = json_res['countries']
            countries = countries_data.keys()
            data = {
                'country_id': [], 
                'country_name': []
            }
            for country in countries:
                if country == '' or countries_data[country]['label'] == None:
                    continue
                data['country_id'].append(country)

                data['country_name'].append(str(countries_data[country]['label']).replace('\n', ''))
            
            output = pd.DataFrame(data).dropna()
            output.to_csv('data/countries.csv', index=False)
            # pd.DataFrame(data).to_csv('countries.csv', index=False)
            if isinstance(country,str):
                if get == 'id':
                    id = output[output['country_name'] == country]['country_id'].values[0]
                    return id
            return output
        else:
            raise Exception(f"Failed to get countries list. \nStatus code: {res.status_code}")

@cache_data
def get_groups(group:str|None = None, get:str|None = None)-> Any:
    """
    Retrieves the list of available groups from the IMF Data Mapper API.

    Parameters
    ----------
    group : str, optional
        The name of the group to retrieve the ID for. If None, returns the entire list of groups.
    get : str, optional
        If 'id', returns the ID of the specified group.

    Returns
    -------
    data : pandas.DataFrame
        A DataFrame containing the list of groups and their IDs.
    id : str
        The ID of the specified group.

    Raises
    ------
    Exception
        If the request to the API fails.
    """

    if os.path.isfile('data/groups.csv') and file_age_in_days('data/groups.csv') < 5:
        data = pd.read_csv('data/groups.csv')
        if isinstance(group,str):
            if get == 'id':
                id = data[data['group_name'] == group]['group_id'].values[0]
                return id
        return data
    else:
        url = r"https://www.imf.org/external/datamapper/api/v1/groups"
        res = requests.get(url)
        if res.status_code == 200:
            json_res = dict(res.json())
            groups_data = json_res['groups']
            groups = groups_data.keys()
            data = {
                'group_id': [], 
                'group_name': []
            }
            for group in groups:
                if group == '' or groups_data[group]['label'] == None:
                    continue
                data['group_id'].append(group)
                data['group_name'].append(str(groups_data[group]['label']).replace('\n', ''))
            
            output = pd.DataFrame(data).dropna()
            output.to_csv('data/groups.csv', index=False)
            # pd.DataFrame(data).to_csv('groups.csv', index=False)
            if isinstance(group,str):
                if get == 'id':
                    id = output[output['group_name'] == group]['group_id'].values[0]
                    return id
            return output
        else:
            raise Exception(f"Failed to get groups. \nStatus code: {res.status_code}")

@cache_data
def get_regions(region:str|None = None, get:str|None = None)-> Any:
    """
    Retrieves the list of available regions from the IMF Data Mapper API.

    Parameters
    ----------
    region : str, optional
        The name of the region to retrieve the ID for. If None, returns the entire list of regions.
    get : str, optional
        If 'id', returns the ID of the specified region.

    Returns
    -------
    data : pandas.DataFrame
        A DataFrame containing the list of regions and their IDs.
    id : str
        The ID of the specified region.

    Raises
    ------
    Exception
        If the request to the API fails.
    """

    if os.path.isfile('data/regions.csv') and file_age_in_days('data/regions.csv') < 5:
        data = pd.read_csv('data/regions.csv')  
        if isinstance(region,str):
            if get == 'id':
                id = data[data['region_name'] == region]['region_id'].values[0]
                return id
        return data
    else:
        url = r"https://www.imf.org/external/datamapper/api/v1/regions"
        res = requests.get(url)
        if res.status_code == 200:
            json_res = dict(res.json())
            regions_data = json_res['regions']
            regions = regions_data.keys()
            data = {
                'region_id': [], 
                'region_name': []
            }
            for region in regions:
                if region == '' or regions_data[region]['label'] == None:
                    continue
                data['region_id'].append(region)
                data['region_name'].append(str(regions_data[region]['label']).replace('\n', ''))
            
            output = pd.DataFrame(data).dropna()
            output.to_csv('data/regions.csv', index=False)
            # pd.DataFrame(data).to_csv('regions.csv', index=False)
            if isinstance(region,str):
                if get == 'id':
                    id = output[output['region_name'] == region]['region_id'].values[0]
                    return id
            return output
        else:
            raise Exception(f"Failed to get regions. \nStatus code: {res.status_code}")

def get_data(indicators_list:list[str], countries:list[str]|str|None = None, groups:list[str]|str|None = None, regions:list[str]|str|None = None)-> Any:
    indicators_ids = [get_indicators(x,'id') for x in indicators_list]
    indicators = '/'.join(indicators_ids)
    url = f"https://www.imf.org/external/datamapper/api/v1/{indicators}"
    if countries:
        countries_ids_list = [get_countries(x,'id') for x in countries]
        countries_ids = '/'.join(countries_ids_list)
        url += f"/{countries_ids}"
    if groups:
        groups_ids_list = [get_groups(x,'id') for x in groups]
        groups_ids = '/'.join(groups_ids_list)
        url += f"/{groups_ids}"
    if regions:
        regions_ids_list = [get_regions(x,'id') for x in regions]
        regions_ids = '/'.join(regions_ids_list)
        url += f"/{regions_ids}"

    # print(url)
    # print('----------------------------------')

    res = requests.get(url)
    if res.status_code == 200:
        json_res = res.json()
        try:
            all_data = json_res['values']            
        except KeyError:
            return 'Nothing to show :worried:'
        # print(json_res)
        # print('----------------------------------')
        compiled_data = {'Country': [], 'Year': [] , 'Indicator': [], 'Value': [], 'Unit': []}

        for indicator in all_data.keys():
            countires = all_data[indicator].keys()
            # print(indicator, countires)
            # break
            for country in countires:        
                years = all_data[indicator][country].keys()
                values = all_data[indicator][country].values()
                compiled_data['Country'].extend([country]*len(years))
                compiled_data['Year'].extend(years)
                compiled_data['Indicator'].extend([indicator]*len(years))
                compiled_data['Value'].extend(values)
                compiled_data['Unit'].extend([get_indicators(indicator,'unit')]*len(years))
        return pd.DataFrame(compiled_data)

# get_data(['Real GDP growth'], ['India','United States'])

# def get_data(indicator:list[str], country:list[str]|str|None = None)-> Any:
#     if isinstance(indicator, list):
#         indicator_id = '/'.join(indicator)
#     elif isinstance(indicator, str):
#         indicator_id = indicator
    
#     if isinstance(country, list):
#         country_id = '/'.join(country)
#     elif isinstance(country, str):
#         country_id = country

#     url = f"https://www.imf.org/external/datamapper/api/v1/{indicator_id}"
#     if country_id:
#         url += f"/{country_id}"
#     res = requests.get(url)
#     if res.status_code == 200:
#         print(res.status_code)
#         json_res = dict(res.json())
#         all_data = json_res['values']
#         compiled_data = {'Country': [], 'Year': [] , 'Indicator': [], 'Value': [], 'Unit': []}

#         for indicator in all_data.keys():
#             countires = all_data[indicator].keys()
#             for country in countires:
#                 data = all_data[indicator][country]
#                 keys = data.keys()
#                 values = data.values()
#                 compiled_data['Country'].extend([country]*len(keys))
#                 compiled_data['Indicator'].extend([indicator]*len(keys))
#                 compiled_data['Year'].extend(keys)
#                 compiled_data['Value'].extend(values)
#                 unit = get_indicators(indicator=indicator, get='unit')
#                 compiled_data['Unit'].extend([unit]*len(keys))
#         compiled_data = pd.DataFrame(compiled_data)
#         compiled_data.to_csv('data.csv', index=False)
#         # print(compiled_data.head())        
#         return compiled_data
#     else:
#         raise Exception(f"Failed to get data. \nStatus code: {res.status_code}")

# # print(get_data(['NGDP_RPCH','NGDPD'], ['IND','USA']))