import pandas as pd
import requests
import sys
from difflib import get_close_matches

# Get list of states and ids from IBGE API and return json
def get_brazilian_states():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response = requests.get(url)
    
    if response.status_code == 200:
        states = response.json()
        return states
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")

# Get list of cities in the state, using the state id from the IBGE API
def get_cities_by_state(state_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{state_id}/municipios"
    response = requests.get(url)
    
    if response.status_code == 200:
        cities = response.json()
        return [city['nome'] for city in cities]
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")    

# Create a dict of state:IBGE id for future requests
def create_state_dict(states):
    state_dict = {state['sigla']: state['id'] for state in states}
    return state_dict

# Creates a nrew column in the DF with the closest match to the city name
def fix_cities_names(df, state_dict):
    for sigla in df['ESTADO'].unique():
        state_id = state_dict.get(sigla)
        if state_id:
            city_names_api = get_cities_by_state(state_id)

            # remove special symbols and title case it before matchings
            for index, row in df[df['ESTADO'] == sigla].iterrows():
                city_name = row['CIDADE']
                city_name = city_name.replace('?', '').title()
                city_name = city_name.replace('¿', '')
                
                closest_match = get_close_matches(city_name, city_names_api)
                if closest_match:
                    df.at[index, 'CIDADE_FIX'] = closest_match[0]
    
    return df

if __name__ == "__main__":
    states = get_brazilian_states()
    state_dict = create_state_dict(states)

    file_name = sys.argv[1]

    # use parameter to open file
    df = pd.read_excel(file_name)

    # remove null values from states and cities before calling function 
    df = df[df['ESTADO'].notnull()]
    df = df[df['CIDADE'].notnull()]

    try:
        df = fix_cities_names(df, state_dict)
        print("Fix successfull!")
    except Exception as error:
        print("Error fixing names: " + str(error))

    try:
        df.to_excel(file_name, index=False)
        print("File saved!")
    except Exception as error:
        print("Error saving file: " + str(error))