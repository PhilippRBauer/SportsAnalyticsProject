import os
import sqlite3

import pandas as pd
from dotenv import dotenv_values


class DB:
    def __init__(self):
        self._dbc = None
        self._config = None

    def __enter__(self):
        if os.path.isfile(".env"):
            self._config = dotenv_values(".env")
            try:
                self._dbc = sqlite3.connect(self._config["DATABASE_FILE"])
                if "DEBUG" in self._config and self._config["DEBUG"] == "True":
                    print("Database connection established.")
            except sqlite3.Error as e:
                print(f"Failed to connect to the database: {e}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if "DEBUG" in self._config and self._config["DEBUG"] == "True":
            print("Closing database connection...")
        if self._dbc:
            self._dbc.close()

    def get_all_activities(self, sport=None, start_date=None, end_date=None, offset=0, limit=0):
        if not self._dbc:
            return pd.DataFrame()

        if start_date:
            if sport:
                start_date_result = f" AND date >= '{start_date} 00:00:00'"
            else:
                start_date_result = f" date >= '{start_date} 00:00:00'"
        else:
            start_date_result = ""
        if end_date:
            if sport:
                end_date_result = f" AND date <= '{end_date} 23:59:59'"
            else:
                end_date_result = f" AND date <= '{end_date} 23:59:59'"
        else:
            end_date_result = ""

        if offset > 0:
            offset_result = f" OFFSET {offset}"
        else:
            offset_result = ""

        if limit > 0:
            limit_result = f" LIMIT {limit} "
        else:
            limit_result = ""

        sql = "SELECT *, strftime('%Y-%m-%d', date) AS date_group " \
              "FROM activities ORDER BY date DESC{}{};".format(limit_result, offset_result)
        if start_date or end_date:
            sql = "SELECT *, strftime('%Y-%m-%d', date) AS date_group " \
                  "FROM activities WHERE date >= '{} 00:00:00' AND date <= '{} 23:59:59'" \
                  " ORDER BY date DESC{}{};".format(start_date, end_date, limit_result, offset_result)
        if sport:
            sql = "SELECT *, strftime('%Y-%m-%d', date) AS date_group " \
                  "FROM activities WHERE sport='{}'{}{} " \
                  "ORDER BY date DESC{}{};" \
                .format(sport, start_date_result, end_date_result, limit_result, offset_result)

        # Execute a query to retrieve all activities
        cursor = self._dbc.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if "DEBUG" in self._config and self._config["DEBUG"] == "True":
            print("Execute: get_all_activities()")
            print(len(result), sql)
        # Define the column names based on the structure of your activities table
        column_names = [
            "id",
            "sport",
            "date",
            "start_position_lat",
            "start_position_long",
            "center_latitude",
            "center_longitude",
            "zoom_level",
            "avg_heart_rate",
            "avg_cadence",
            "avg_power",
            "max_heart_rate",
            "max_cadence",
            "max_power",
            "total_ascent",
            "total_descent",
            "total_calories",
            "total_distance",
            "total_elapsed_time",
            "total_timer_time",
            "total_training_effect",
            "total_work",
            "intensity_factor",
            "training_stress_score",
            "date_group"
        ]

        # Convert the query result to a Pandas DataFrame
        df = pd.DataFrame(result, columns=column_names)

        return df

    def get_total_activities_count(self, sport=None):
        if not self._dbc:
            return 0

        # Execute a query to get the count of activities
        cursor = self._dbc.cursor()
        if sport:
            cursor.execute("SELECT COUNT(*) FROM activities WHERE sport=?;", (sport,))
        else:
            cursor.execute("SELECT COUNT(*) FROM activities")
        result = cursor.fetchone()

        total_count = result[0]
        return total_count

    def get_activity_by_id(self, activity_id):
        if not self._dbc:
            return None  # Return None if the connection is not established

        # Execute a query to retrieve the activity by ID
        cursor = self._dbc.cursor()
        cursor.execute("SELECT * FROM activities WHERE id=?", (activity_id,))
        result = cursor.fetchone()

        if result:
            # Define the column names based on the structure of your activities table
            column_names = [
                "id",
                "sport",
                "date",
                "start_position_lat",
                "start_position_long",
                "center_latitude",
                "center_longitude",
                "zoom_level",
                "avg_heart_rate",
                "avg_cadence",
                "avg_power",
                "max_heart_rate",
                "max_cadence",
                "max_power",
                "total_ascent",
                "total_descent",
                "total_calories",
                "total_distance",
                "total_elapsed_time",
                "total_timer_time",
                "total_training_effect",
                "total_work",
                "intensity_factor",
                "training_stress_score"
            ]

            # Create a dictionary with the activity details
            activity = dict(zip(column_names, result))
            return activity
        else:
            return None

    def get_activity_data_by_id(self, activity_id):
        if not self._dbc:
            return pd.DataFrame()

        # Execute a query to retrieve the activity data by ID
        cursor = self._dbc.cursor()
        cursor.execute("SELECT * FROM activity_data WHERE activity_id=?", (activity_id,))
        result = cursor.fetchall()

        if result:
            column_names = [
                "id",
                "activity_id",
                "sport",
                "date",
                "timestamp",
                "heartrate",
                "distance",
                "lap",
                "latitude",
                "longitude",
                "accumulated_power",
                "power",
                "enhanced_altitude",
                "enhanced_speed",
                "vertical_oscillation",
                "vertical_ratio",
                "step_length",
                "cadence"
            ]
            df = pd.DataFrame(result, columns=column_names)
            return df
        return pd.DataFrame()