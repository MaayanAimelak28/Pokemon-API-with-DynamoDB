import requests
import json
import random
from dynamodb_handler import create_dynamodb_table, insert_pokemon_data, scan_pokemon_table

# get a list of all Pokémon from the PokeAPI website
def all_the_data():
    url = 'https://pokeapi.co/api/v2/pokemon/?offset=4&limit=4'
    pokemon_json_file = requests.get(url).json()  # Get all the data
    pokemon_names_and_urls = pokemon_json_file["results"]  # Extract names and URLs
    return pokemon_names_and_urls

# return a list of Pokémon names from the provided names and URLs
def name_list(pokemon_names_and_urls):
    return [pok['name'] for pok in pokemon_names_and_urls]  # List comprehension for cleaner code

# create a JSON file containing details of a specific Pokémon and return its data
def make_file(pokemon_names_and_urls, default_pokemon_index=0):
    new_url = pokemon_names_and_urls[default_pokemon_index]['url']
    data_schema = requests.get(new_url).json()
    data = {
        'name': data_schema['name'],
        'id': data_schema['id'],
        'height': data_schema['height'],
        'weight': data_schema['weight'],
        'base_experience': data_schema['base_experience']
    }
    return data

# return the index of a new Pokémon in the list of names and URLs
def download_details(pokemon_name, pokemon_names_and_urls):
    for index, pokemon in enumerate(pokemon_names_and_urls):
        if pokemon['name'] == pokemon_name:
            return index

# Main function: prompt the user to draw a Pokémon
def collect_pokemons():
    data_names_urls = all_the_data()  # Retrieve all the data
    pokemon_name_list = name_list(data_names_urls)  # Create the Pokémon name list

    # initialize the JSON file and add the first Pokémon to the list and add it to DynamoDB database
    insert_pokemon_data(make_file(data_names_urls))

    valid_flag = False
    print('\nWelcome to my PokemonAPI Project!\n')
    while not valid_flag:
        user_input = input('Do you like to draw a Pokémon? (Y or N) ').lower()

        if user_input == 'y':
            random_pokemon = random.choice(pokemon_name_list)  # Randomly choose a Pokémon

            # check if the random Pokémon is already in the table
            current_pokemons = scan_pokemon_table()  # Get the current list of Pokémon
            
            # check if the randomly selected Pokémon is already in the current Pokémon data
            if any(pokemon['name'] == random_pokemon for pokemon in current_pokemons):
                print('\nThis Pokémon is already in our names list: ' + str(random_pokemon))
            else:  # if random Pokémon is not in the table
                new_index_pok = download_details(random_pokemon, data_names_urls)  # Get index for the new Pokémon
                new_pokemon = insert_pokemon_data(make_file(data_names_urls, new_index_pok))  # Create JSON for the new Pokémon
                print('\nNew Pokémon added: ' + str(new_pokemon))

        else:  # user input is not 'y'
            # give a farewell greeting to the user and exit
            print('\nGoodbye!\n')
            valid_flag = True

# run the project
if __name__ == '__main__':
    create_dynamodb_table()  
    collect_pokemons()
