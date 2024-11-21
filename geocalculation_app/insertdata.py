# import mysql.connector
# import csv

# def import_csv_to_db(csv_file_path):
#     try:
#         # Connect to the MySQL database
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='Root@123',
#             database='bihar'
#         )
#         cursor = conn.cursor()

#         # Create the table if it doesn't exist
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS geocalculation_app_gridpoint (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 latitude FLOAT,
#                 longitude FLOAT,
#                 value FLOAT,
#                 grid_data_id INT,
#                 FOREIGN KEY (grid_data_id) REFERENCES geocalculation_app_griddata(id)
#             )
#         ''')

#         # Read the CSV file and insert data
#         with open(csv_file_path, 'r') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 try:
#                     latitude = float(row['latitude'])
#                     longitude = float(row['longitude'])
#                     value = float(row['value'])
#                     grid_data_id = int(row['grid_data_id'])

#                     # Check if the grid_data_id exists in the parent table
#                     cursor.execute('''
#                         SELECT COUNT(*) FROM geocalculation_app_griddata WHERE id = %s
#                     ''', (grid_data_id,))
#                     count = cursor.fetchone()[0]
                    
#                     if count == 0:
#                         print(f"Foreign key constraint error: grid_data_id {grid_data_id} does not exist in geocalculation_app_griddata")
#                     else:
#                         cursor.execute('''
#                             INSERT INTO geocalculation_app_gridpoint (latitude, longitude, value, grid_data_id)
#                             VALUES (%s, %s, %s, %s)
#                         ''', (latitude, longitude, value, grid_data_id))
                    
#                 except ValueError as e:
#                     print(f"Value error for row {row}: {e}")
#                 except mysql.connector.Error as e:
#                     print(f"Database error for row {row}: {e}")
        
#         # Commit the transaction and close the connection
#         conn.commit()
#         print('Data imported successfully')

#     except mysql.connector.Error as e:
#         print(f"Database connection error: {e}")
    
#     finally:
#         cursor.close()
#         conn.close()

# if __name__ == '__main__':
#     csv_file_path = 'Haryana_modified2.csv'
#     import_csv_to_db(csv_file_path)



import mysql.connector
import csv

def import_csv_to_db(csv_file_path):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Root@123',
            database='bihar'
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS geocalculation_app_gridpoint (
                id INT AUTO_INCREMENT PRIMARY KEY,
                latitude FLOAT,
                longitude FLOAT,
                value FLOAT,
                grid_data_id INT,
                FOREIGN KEY (grid_data_id) REFERENCES geocalculation_app_griddata(id)
            )
        ''')

        # Read the CSV file and process data
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    latitude = float(row['latitude'])
                    longitude = float(row['longitude'])
                    value = float(row['value'])
                    grid_data_id = int(row['grid_data_id'])

                    # Check if the latitude and longitude already exist in the table
                    cursor.execute('''
                        SELECT value FROM geocalculation_app_gridpoint 
                        WHERE latitude = %s AND longitude = %s
                    ''', (latitude, longitude))
                    
                    existing_record = cursor.fetchone()
                    
                    if existing_record:
                        # Record exists, calculate the average value
                        existing_value = existing_record[0]
                        average_value = (existing_value + value) / 2
                        cursor.execute('''
                            UPDATE geocalculation_app_gridpoint
                            SET value = %s, grid_data_id = %s
                            WHERE latitude = %s AND longitude = %s
                        ''', (average_value, grid_data_id, latitude, longitude))
                    else:
                        # Record does not exist, insert new record
                        cursor.execute('''
                            INSERT INTO geocalculation_app_gridpoint (latitude, longitude, value, grid_data_id)
                            VALUES (%s, %s, %s, %s)
                        ''', (latitude, longitude, value, grid_data_id))
                    
                except ValueError as e:
                    print(f"Value error for row {row}: {e}")
                except mysql.connector.Error as e:
                    print(f"Database error for row {row}: {e}")
        
        # Commit the transaction and close the connection
        conn.commit()
        print('Data imported successfully')

    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    csv_file_path = 'Kerela_modified.csv'
    import_csv_to_db(csv_file_path)
