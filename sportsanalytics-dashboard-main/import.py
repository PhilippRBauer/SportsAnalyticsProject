import math
import os
import sqlite3
import statistics

import sweat
import fitparse
from dotenv import dotenv_values


def check_database(database_file):
    if database_file is None:
        print("create .env file")
        exit()
    if os.path.exists(database_file):
        # Delete the file
        os.remove(database_file)
        print("File deleted successfully.")
    else:
        print("File does not exist.")

    # Check if the database file exists
    if not os.path.isfile(database_file):
        open(database_file, 'a').close()
        print("File created successfully.")


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            sport TEXT NOT NULL DEFAULT '',
            date TIMESTAMP NOT NULL,
            start_position_lat REAL DEFAULT 0,
            start_position_long REAL DEFAULT 0,
            center_latitude REAL DEFAULT 0,
            center_longitude REAL DEFAULT 0,
            zoom_level INTEGER DEFAULT 0,
            avg_heart_rate REAL DEFAULT 0,
            avg_cadence REAL DEFAULT 0,
            avg_power REAL DEFAULT 0,
            max_heart_rate REAL DEFAULT 0,
            max_cadence REAL DEFAULT 0,
            max_power INTEGER DEFAULT 0,
            total_ascent INT DEFAULT 0,
            total_descent INT DEFAULT 0,
            total_calories INT DEFAULT 0,
            total_distance REAL DEFAULT 0,
            total_elapsed_time REAL DEFAULT 0,
            total_timer_time REAL DEFAULT 0,
            total_training_effect REAL DEFAULT 0,
            total_work REAL DEFAULT 0,
            intensity_factor REAL DEFAULT 0,
            training_stress_score REAL DEFAULT 0
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_data (
            id INTEGER PRIMARY KEY,
            activity_id INTEGER NOT NULL,
            sport TEXT NOT NULL DEFAULT '',
            date TIMESTAMP NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            heartrate INTEGER DEFAULT 0,
            distance REAL DEFAULT 0,
            lap INTEGER DEFAULT 0,
            latitude REAL DEFAULT 0,
            longitude REAL DEFAULT 0,
            accumulated_power REAL DEFAULT 0,
            power REAL DEFAULT 0,
            enhanced_altitude REAL DEFAULT 0,
            enhanced_speed REAL DEFAULT 0,
            vertical_oscillation REAL DEFAULT 0,
            vertical_ratio REAL DEFAULT 0,
            step_length REAL DEFAULT 0,
            cadence INTEGER DEFAULT 0,
            FOREIGN KEY (activity_id) REFERENCES activities (id)
        )
    ''')


def calculate_center_zoom(sweat_data):
    if all(col in sweat_data.columns for col in ['latitude', 'longitude']):
        coordinates = sweat_data[['latitude', 'longitude']].values.tolist()
        # Extract latitude and longitude values separately
        latitudes = [coord[0] for coord in coordinates]
        longitudes = [coord[1] for coord in coordinates]

        # Calculate the average latitude and longitude
        center_latitude = statistics.mean(latitudes)
        center_longitude = statistics.mean(longitudes)

        # Calculate the maximum difference between latitudes and longitudes
        max_latitude_diff = max(latitudes) - min(latitudes)
        max_longitude_diff = max(longitudes) - min(longitudes)

        # Choose the larger difference as the basis for zoom level calculation
        max_diff = max(max_latitude_diff, max_longitude_diff)

        # Define the map width and height in pixels
        map_width = 640

        # Define the maximum zoom level
        max_zoom = 18

        # Calculate the zoom level based on the maximum difference and map size
        zoom_level = int(math.log2((360 * map_width) / (max_diff * 256)))

        # Clamp the zoom level within the range of 0 to max_zoom
        zoom_level = max(0, min(zoom_level, max_zoom))

        return center_latitude, center_longitude, zoom_level
    else:
        return 0, 0, 0


def write_activity_to_db(config, cursor, sweat_data, fitparse_data, activity):
    sport = activity['sport']
    # fix date
    activity['date'] = activity['date'].replace('+00:00', '')
    cursor.execute('''
        INSERT INTO activities (
            id,
            sport,
            date,
            start_position_lat,
            start_position_long,
            center_latitude,
            center_longitude,
            zoom_level,
            avg_heart_rate,
            avg_cadence,
            avg_power,
            max_heart_rate,
            max_cadence,
            max_power,
            total_ascent,
            total_descent,
            total_calories,
            total_distance,
            total_elapsed_time,
            total_timer_time,
            total_training_effect,
            total_work,
            intensity_factor,
            training_stress_score
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        activity['id'],
        activity['sport'],
        activity['date'],
        fitparse_data['start_position_lat'] if 'start_position_lat' in fitparse_data else 0,
        fitparse_data['start_position_long'] if 'start_position_long' in fitparse_data else 0,
        activity['center_latitude'] if 'center_latitude' in activity else 0,
        activity['center_longitude'] if 'center_longitude' in activity else 0,
        activity['zoom_level'] if 'zoom_level' in activity else 0,
        fitparse_data['avg_heart_rate'] if 'avg_heart_rate' in fitparse_data else 0,
        fitparse_data['avg_cadence'] if 'avg_cadence' in fitparse_data else 0,
        fitparse_data['avg_power'] if 'avg_power' in fitparse_data else 0,
        fitparse_data['max_heart_rate'] if 'max_heart_rate' in fitparse_data else 0,
        fitparse_data['max_cadence'] if 'max_cadence' in fitparse_data else 0,
        fitparse_data['max_power'] if 'max_power' in fitparse_data else 0,
        fitparse_data['total_ascent'] if 'total_ascent' in fitparse_data else 0,
        fitparse_data['total_descent'] if 'total_descent' in fitparse_data else 0,
        fitparse_data['total_calories'] if 'total_calories' in fitparse_data else 0,
        fitparse_data['total_distance'] if 'total_distance' in fitparse_data else 0,
        fitparse_data['total_elapsed_time'] if 'total_elapsed_time' in fitparse_data else 0,
        fitparse_data['total_timer_time'] if 'total_timer_time' in fitparse_data else 0,
        fitparse_data['total_training_effect'] if 'total_training_effect' in fitparse_data else 0,
        fitparse_data['total_work'] if 'total_work' in fitparse_data else 0,
        fitparse_data['intensity_factor'] if 'intensity_factor' in fitparse_data else 0,
        fitparse_data['training_stress_score'] if 'training_stress_score' in fitparse_data else 0
    ))
    print('Activity {} with {} at {} added to database'.format(activity['id'], activity['sport'], activity['date']))


def write_activity_data_to_db(config, cursor, sweat_data, activity):
    data = []
    for index, row in sweat_data.iterrows():
        data.append((
            activity['id'],
            activity['sport'],
            activity['date'],
            row['timestamp'],
            row['heartrate'],
            row['distance'] if 'distance' in row else 0,
            row['lap'] if 'lap' in row else 0,
            row['latitude'] if 'latitude' in row else 0,
            row['longitude'] if 'longitude' in row else 0,
            row['accumulated_power'] if 'accumulated_power' in row else 0,
            row['power'] if 'power' in row else 0,
            row['enhanced_altitude'] if 'enhanced_altitude' in row else 0,
            row['enhanced_speed'] if 'enhanced_speed' in row else 0,
            row['vertical_oscillation'] if 'vertical_oscillation' in row else 0,
            row['vertical_ratio'] if 'vertical_ratio' in row else 0,
            row['step_length'] if 'step_length' in row else 0,
            row['cadence'] if 'cadence' in row else 0,
        ))

    cursor.executemany('''
                INSERT INTO activity_data (
                    activity_id,
                    sport,
                    date,
                    timestamp,
                    heartrate,
                    distance,
                    lap,
                    latitude,
                    longitude,
                    accumulated_power,
                    power,
                    enhanced_altitude,
                    enhanced_speed,
                    vertical_oscillation,
                    vertical_ratio,
                    step_length,
                    cadence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', data)
    print('ActivityData {} added {} items for {} to database'.format(activity['id'], len(data),
                                                                     activity['sport']))


def import_database():
    config = dotenv_values(".env")
    folder_path = 'data'
    database_file = config.get('DATABASE_FILE')

    # Check if the database file exists
    check_database(database_file)

    # Connect to the database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Create the activities table if it doesn't exist
    create_tables(cursor)
    try:
        # Get a list of all .fit files in the folder
        fit_files = [f for f in os.listdir(folder_path) if f.endswith('.fit')]
        i = 0
        for file_name in fit_files:
            fit_path = os.path.join(folder_path, file_name)
            data_by_sweat = sweat.read_fit(fit_path)
            data_by_fitparse = fitparse.FitFile(fit_path)
            fit_data_fitparse = {}
            for record in data_by_fitparse.get_messages('session'):
                # Define the desired field names
                desired_fields = [
                    'avg_heart_rate',
                    'max_heart_rate',
                    'sport',
                    'total_ascent',
                    'total_calories',
                    'total_descent',
                    'total_distance',
                    'total_elapsed_time',
                    'total_timer_time',
                    'total_training_effect',
                    'training_stress_score',
                    'avg_cadence',
                    'avg_power',
                    'intensity_factor',
                    'max_cadence',
                    'max_power',
                    'start_position_lat',
                    'start_position_long',
                    'timestamp'
                ]

                for field in record:
                    if field.name in desired_fields:
                        fit_data_fitparse[field.name] = field.value
            # add timestamp column
            sweat_data = data_by_sweat.copy()
            sweat_data['timestamp'] = data_by_sweat.index
            sweat_data = sweat_data.reset_index(drop=True)
            sweat_data['timestamp'] = sweat_data['timestamp'].astype(str)

            # Extract the ID from the file name
            activity_id = file_name.split('_')[0]

            # Get the timestamp
            sport = None
            get_sport = sweat_data['sport'].unique()
            if get_sport.size > 0:
                sport = get_sport[0]

            date = None
            get_date = sweat_data['timestamp'][0]
            if get_date:
                date = sweat_data['timestamp'][0]

            if activity_id and sport and date:
                center_latitude, center_longitude, zoom_level = calculate_center_zoom(sweat_data)
                write_activity_to_db(config, cursor, sweat_data, fit_data_fitparse, {
                    'id': activity_id,
                    'sport': sport,
                    'date': date,
                    'center_latitude': center_latitude,
                    'center_longitude': center_longitude,
                    'zoom_level': zoom_level
                })
                write_activity_data_to_db(config, cursor, sweat_data, {
                    'id': activity_id,
                    'sport': sport,
                    'date': date
                })
                if i == 4:
                    exit()
            else:
                Exception("Error inserting data exit...")
                exit()
            conn.commit()
        conn.close()
        exit()

    except Exception as e:
        print("Error:", e)


if __name__ == '__main__':
    import_database()
