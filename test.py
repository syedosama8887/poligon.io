import requests

# Define your API key (replace with your actual API key)
POLYGON_IO_API_KEY = 'MJs5q7JnmTgh8CsA0PDxE2yOI8JeukBX'

def fetch_polygon_data(symbol, start_date, end_date):
    url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_IO_API_KEY}'
    response = requests.get(url)

    try:
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()['results']
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response status code: {response.status_code}')
        print(f'Response content: {response.content}')
        raise  # Re-raise the exception to propagate it up
    except KeyError as key_err:
        print(f'Key error occurred: {key_err}')
        print(f'Response content: {response.content}')
        raise
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise

# Example usage:
symbol = 'AAPL'
start_date = '2023-01-09'
end_date = '2023-01-09'

try:
    data = fetch_polygon_data(symbol, start_date, end_date)
    print(data)  # Check if data is fetched successfully
except Exception as e:
    print(f'Error fetching data: {str(e)}')



# import requests

# def fetch_polygon_data(symbol, interval):
#     url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{interval}/?apiKey={POLYGON_IO_API_KEY}'
#     response = requests.get(url)

#     try:
#         response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
#         data = response.json()['results']
#         return data
#     except requests.exceptions.HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#         print(f'Response status code: {response.status_code}')
#         print(f'Response content: {response.content}')
#         raise  # Re-raise the exception to propagate it up
#     except KeyError as key_err:
#         print(f'Key error occurred: {key_err}')
#         print(f'Response content: {response.content}')
#         raise
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#         raise

# # Now, let's call this function in your router endpoint or another test script to see the detailed error messages:
# symbol = 'AAPL'
# interval = '1d'
# data = fetch_polygon_data(symbol, interval)
# print(data)  # Check if data is fetched successfully

# # Make sure to handle exceptions appropriately in your FastAPI endpoint as shown previously.



# import requests
# import mysql.connector

# # Polygon.io API key
# POLYGON_IO_API_KEY = 'ChbFJ6_V5_U2RErrENxyMHoQ9e54FG5p'

# # Function to fetch data from Polygon.io
# def fetch_polygon_data(ticker):
#     url = f'https://api.polygon.io/v1/meta/symbols/{ticker}/company?apiKey={POLYGON_IO_API_KEY}'
#     response = requests.get(url)
#     data = response.json()
#     return data

# # Function to insert data into MySQL database
# def insert_data_to_db(data):
#     # Database connection details
#     db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',  # Replace with your MySQL password
#     'database': 'polygon',
# }

#     # Create a connection to the database
#     conn = mysql.connector.connect(**db_config)
#     cursor = conn.cursor()

#     # Define the SQL query to insert data
#     sql = '''
#     INSERT INTO company_info (symbol, name, exchange, industry, sector)
#     VALUES (%s, %s, %s, %s, %s)
#     '''

#     # Extract the data you need from the API response
#     values = (
#         data['symbol'],
#         data['name'],
#         data['exchange'],
#         data['industry'],
#         data['sector']
#     )

#     # Execute the SQL query
#     cursor.execute(sql, values)

#     # Commit the transaction
#     conn.commit()

#     # Close the connection
#     cursor.close()
#     conn.close()

# # Example usage
# ticker = 'MSFT'  # You can change this to any ticker you want to fetch data for
# data = fetch_polygon_data(ticker)
# insert_data_to_db(data)
