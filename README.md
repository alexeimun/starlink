### How to run the script

* Install the dependencies:
    ```
    pip install -r requirements.txt
    ```

* Import the data with the following command:
    ```
    python starlink.py import_data
    ```

* To get the latest known position given an id, run the following command:
    ```
    python starlink.py get_latest_pos_by_id <id>
    ```

* To get the closest position given a position (lat, long), run the following command:
    ```
    python starlink.py get_closest_satellite <lat> <long>
    ```


### Development tools
+ Python 3
+ Sqlite3
