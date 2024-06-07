from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime
import mysql.connector

# Initialize router
router = APIRouter()

# Polygon.io API key
POLYGON_IO_API_KEY = 'ChbFJ6_V5_U2RErrENxyMHoQ9e54FG5p'

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Replace with your MySQL password
    'database': 'polygon',  # Replace with your database name
}

# Function to fetch data from Polygon.io API
def fetch_polygon_data(symbol: str, interval: str):
    base_url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1'
    if interval == '1h':
        url = f'{base_url}/hour/2023-01-09/2023-01-10?apiKey={POLYGON_IO_API_KEY}'
    elif interval == '4h':
        url = f'{base_url}/hour/2023-01-09/2023-01-10?apiKey={POLYGON_IO_API_KEY}'
    elif interval == '1d':
        url = f'{base_url}/day/2023-01-09/2023-01-10?apiKey={POLYGON_IO_API_KEY}'
    else:
        raise ValueError("Invalid interval specified")

    response = requests.get(url)
    try:
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json().get('results', [])
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        print(f'Response status code: {response.status_code}')
        print(f'Response content: {response.content}')
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error occurred: {http_err}")
    except KeyError as key_err:
        print(f'Key error occurred: {key_err}')
        print(f'Response content: {response.content}')
        raise HTTPException(status_code=500, detail="Error parsing response JSON.")
    except Exception as err:
        print(f'Other error occurred: {err}')
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(err)}")

# Function to insert data into MySQL database
def insert_data_into_db(symbol: str, interval: str, data: list):
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(**db_config)
        mycursor = mydb.cursor()

        # Prepare SQL statement
        sql = "INSERT INTO stock_intervals (symbol, `interval`, open, high, low, close, volume, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Insert each record into the database
        for record in data:
            val = (symbol, interval, record['o'], record['h'], record['l'], record['c'], record['v'], datetime.fromtimestamp(record['t'] / 1000))
            mycursor.execute(sql, val)
        
        # Commit changes
        mydb.commit()

        # Close cursor and connection
        mycursor.close()
        mydb.close()

        print(f"Inserted {len(data)} records into stock_intervals table for {symbol} {interval}")

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error inserting data into database: {err}")

# Define API endpoint to fetch and insert data for multiple symbols and intervals
@router.get("/fetch-and-insert-multiple-data")
def fetch_and_insert_multiple_data():
    symbols = ['AAPL', 'MSFT', 'GOOGL']
    intervals = ['1h', '4h', '1d']  # '1h' for 1-hour, '4h' for 4-hour, '1d' for 1-day

    try:
        for symbol in symbols:
            for interval in intervals:
                data = fetch_polygon_data(symbol, interval)
                if data:
                    insert_data_into_db(symbol, interval, data)
                else:
                    print(f"No data found for {symbol} {interval}")

        return {"detail": "Data fetch and insert completed."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")




# from fastapi import APIRouter, HTTPException
# import requests
# from datetime import datetime
# import mysql.connector

# # Initialize router
# router = APIRouter()

# # Polygon.io API key
# POLYGON_IO_API_KEY = 'ChbFJ6_V5_U2RErrENxyMHoQ9e54FG5p'

# # MySQL database configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',  # Replace with your MySQL password
#     'database': 'polygon',  # Replace with your database name
# }

# # Function to fetch data from Polygon.io API
# def fetch_polygon_data(symbol: str, interval: str):
#     url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{interval}/2023-01-09/2023-01-10?apiKey={POLYGON_IO_API_KEY}'
#     response = requests.get(url)
#     try:
#         response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
#         data = response.json().get('results', [])
#         return data
#     except requests.exceptions.HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')
#         print(f'Response status code: {response.status_code}')
#         print(f'Response content: {response.content}')
#         raise HTTPException(status_code=response.status_code, detail=f"HTTP error occurred: {http_err}")
#     except KeyError as key_err:
#         print(f'Key error occurred: {key_err}')
#         print(f'Response content: {response.content}')
#         raise HTTPException(status_code=500, detail="Error parsing response JSON.")
#     except Exception as err:
#         print(f'Other error occurred: {err}')
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(err)}")

# # Function to insert data into MySQL database
# def insert_data_into_db(symbol: str, interval: str, data: list):
#     try:
#         # Connect to MySQL database
#         mydb = mysql.connector.connect(**db_config)
#         mycursor = mydb.cursor()

#         # Prepare SQL statement
#         sql = "INSERT INTO stock_data (symbol, `interval`, open, high, low, close, volume, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
#         # Insert each record into the database
#         for record in data:
#             val = (symbol, interval, record['o'], record['h'], record['l'], record['c'], record['v'], datetime.fromtimestamp(record['t'] / 1000))
#             mycursor.execute(sql, val)
        
#         # Commit changes
#         mydb.commit()

#         # Close cursor and connection
#         mycursor.close()
#         mydb.close()

#         print(f"Inserted {len(data)} records into stock_data table for {symbol} {interval}")

#     except mysql.connector.Error as err:
#         raise HTTPException(status_code=500, detail=f"Error inserting data into database: {err}")

# # Define API endpoint to fetch and insert data for multiple symbols and intervals
# @router.get("/fetch-and-insert-multiple-data")
# def fetch_and_insert_multiple_data():
#     symbols = ['AAPL', 'MSFT', 'GOOGL']
#     intervals = ['hour', 'day']  # 'hour' represents 1h and 'day' represents 1d and 4h can be added similarly

#     try:
#         for symbol in symbols:
#             for interval in intervals:
#                 data = fetch_polygon_data(symbol, interval)
#                 if data:
#                     insert_data_into_db(symbol, interval, data)
#                 else:
#                     print(f"No data found for {symbol} {interval}")

#         return {"detail": "Data fetch and insert completed."}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")






# from fastapi import APIRouter, HTTPException
# import requests
# from datetime import datetime
# import mysql.connector

# # Initialize router
# router = APIRouter()

# # Polygon.io API key
# POLYGON_IO_API_KEY = 'ChbFJ6_V5_U2RErrENxyMHoQ9e54FG5p'

# # MySQL database configuration
# db_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',  # Replace with your MySQL password
#     'database': 'polygon',  # Replace with your database name
# }

# # Function to fetch 1-hour interval data from Polygon.io API
# def fetch_1h_polygon_data(symbol):
#     interval = '1h'
#     url = f'https://api.polygon.io/v2/aggs/ticker/{symbol}/range/{interval}/?apiKey={POLYGON_IO_API_KEY}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()['results']
#     else:
#         raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch 1-hour data for {symbol}. Status code: {response.status_code}")

# # Function to insert data into MySQL database
# def insert_data_into_db(symbol, interval, data):
#     try:
#         # Connect to MySQL database
#         mydb = mysql.connector.connect(**db_config)
#         mycursor = mydb.cursor()

#         # Prepare SQL statement
#         sql = "INSERT INTO stock_data (symbol, `interval`, open, high, low, close, volume, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        
#         # Insert each record into the database
#         for record in data:
#             val = (symbol, interval, record['o'], record['h'], record['l'], record['c'], record['v'], datetime.fromtimestamp(record['t'] / 1000))
#             mycursor.execute(sql, val)
        
#         # Commit changes
#         mydb.commit()

#         # Close cursor and connection
#         mycursor.close()
#         mydb.close()

#         return f"Inserted {len(data)} records into stock_data table for {symbol} {interval}"

#     except mysql.connector.Error as err:
#         raise HTTPException(status_code=500, detail=f"Error inserting data into database: {err}")

# # Define API endpoint to fetch and insert 1-hour interval data for a specific symbol
# @router.get("/fetch-and-insert-1h-data/{symbol}")
# def fetch_and_insert_1h_data(symbol: str):
#     try:
#         data = fetch_1h_polygon_data(symbol)
#         if data:
#             return insert_data_into_db(symbol, '1h', data)
#         else:
#             raise HTTPException(status_code=404, detail=f"No data found for {symbol} 1h")
    
#     except HTTPException as e:
#         raise e

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
# ticker = 'AAPL'  # You can change this to any ticker you want to fetch data for
# data = fetch_polygon_data(ticker)
# insert_data_to_db(data)
