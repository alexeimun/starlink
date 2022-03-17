import sys
import sqlite3
import json
from haversine import haversine

con = sqlite3.connect('starlink.db')
cur = con.cursor()

def import_data():
    cur.execute("drop table if exists tracks")
    cur.execute('''create table tracks (
                    id text not null,
                    latitude text ,
                    longitude text ,
                    creation_date text
                    )''')
    tracks = []
    
    file = open('starlink_historical_data.json')
    data = json.load(file)

    for record in data:
        tracks.append((record.get('id'),
                        record.get('latitude'), 
                        record.get('longitude'), 
                        record.get('spaceTrack').get('CREATION_DATE'), 
                        ))
        
    cur.executemany("insert into tracks values (?, ?, ?, ?)", tracks)
    con.commit()

def get_max_date_by_id(id):
    cur.execute("select latitude, longitude, max(creation_date) from tracks where id = ?", (id,))
    result = cur.fetchone()
    print(f"latitude: {result[0]}, longitude: {result[1]}, creation_date: {result[2]}")

    
def get_closest_satellite(lat, long):
    cur.execute('''select t1.latitude, t1.longitude, t1.id, t2.max_date
            from tracks t1
            inner join
            (
                select max(creation_date) max_date, id
                from tracks
                group by id
            ) t2
            on t1.id = t2.id
            and t1.creation_date = t2.max_date''')

    satellites = cur.fetchall()
    
    distances = []
    if len(satellites) > 0:
        for sat in satellites:
            if(sat[0] is not None and sat[1] is not None):
                distances.append(haversine((float(lat), float(long)), (float(sat[0]), float(sat[1]))))

    print(f"The closest stallite is {min(distances)} kms away")

if "import_data" in sys.argv:
    import_data()

elif "get_latest_pos_by_id" in sys.argv and len(sys.argv) == 3:
    get_max_date_by_id(sys.argv[2])

elif "get_closest_satellite" in sys.argv and len(sys.argv) == 4:
    get_closest_satellite(sys.argv[2], sys.argv[3])

            
con.close()
