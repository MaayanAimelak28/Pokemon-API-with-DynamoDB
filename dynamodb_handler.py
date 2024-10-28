import boto3
# This file is responsible for all interactions with DynamoDB.
# It includes functions for creating a table, adding Pokemon data to an issue,
# and scanning the table to load data.

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Specify your preferred region

# Create the DynamoDB table
def create_dynamodb_table():
    table_name = 'PokemonCollection'
    try:
        table = dynamodb.Table(table_name)
        table.load()  # Try to load the table to verify existence
        print(f"Table '{table_name}' already exists.")
    except dynamodb.meta.client.exceptions.ResourceNotFoundException:
        print(f"Table '{table_name}' not found. Creating a new table.")

        try:
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'id',  # Primary key name
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'  # 'S' means String type
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )

            # Wait until the table exists.
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            print(f"Table '{table_name}' created successfully!")
        except Exception as e:
            print(f"Failed to create table: {str(e)}")

# Insert Pokémon data into the table
def insert_pokemon_data(pokemon_data):
    table_name = 'PokemonCollection'
    table = dynamodb.Table(table_name)
    try:
        # Insert a single item into the table
        response = table.put_item(
            Item={
                'id': str(pokemon_data['id']),
                'name': pokemon_data['name'],
                'height': pokemon_data['height'],
                'weight': pokemon_data['weight'],
                'base_experience': pokemon_data['base_experience']
            }
        )
        print("Data inserted successfully!")
    except Exception as e:
        print(f"Failed to insert data: {str(e)}")

    return pokemon_data

# Scan the Pokémon table to retrieve all data
def scan_pokemon_table():
    table_name = 'PokemonCollection'
    table = dynamodb.Table(table_name)
    try:
        # Scan the table to retrieve all data
        response = table.scan()
        # Get all items
        items = response.get('Items', [])
        return items
         
    except Exception as e:
        print(f"Failed to retrieve data: {str(e)}")
        return []  # Return an empty list in case of an error
