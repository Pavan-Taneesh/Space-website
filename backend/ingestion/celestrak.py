import requests
import psycopg2
from datetime import datetime

# --- DB connection ---
conn = psycopg2.connect(
    host="localhost",
    dbname="project_db",
    user="postgres",
    password="pavan@2805"
)
cur = conn.cursor()

# --- CelesTrak fetch ---
url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json"
response = requests.get(url)
data = response.json()

# CelesTrak source_id is 1 (from our seed data)
SOURCE_ID = 1
# category_id for "Space Stations" is 1 (from our seed data)
CATEGORY_ID = 1

inserted = 0
for sat in data:
    norad_id = sat["NORAD_CAT_ID"]
    name = sat["OBJECT_NAME"]
    cospar_id = sat["OBJECT_ID"]
    epoch = sat["EPOCH"]

    # Insert into objects, skip if norad_id already exists
    cur.execute("""
        INSERT INTO objects (name, norad_id, cospar_id, category_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (norad_id) DO NOTHING
        RETURNING object_id;
    """, (name, norad_id, cospar_id, CATEGORY_ID))

    row = cur.fetchone()
    if row:
        object_id = row[0]
    else:
        # already exists, fetch its id
        cur.execute("SELECT object_id FROM objects WHERE norad_id = %s", (norad_id,))
        object_id = cur.fetchone()[0]

    # Insert orbital elements (always new row, keeps history)
    cur.execute("""
        INSERT INTO orbital_elements (
            object_id, source_id, epoch, mean_motion, eccentricity,
            inclination, ra_of_asc_node, arg_of_pericenter, mean_anomaly,
            bstar, mean_motion_dot, mean_motion_ddot,
            element_set_no, rev_at_epoch
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        object_id, SOURCE_ID, epoch, sat["MEAN_MOTION"], sat["ECCENTRICITY"],
        sat["INCLINATION"], sat["RA_OF_ASC_NODE"], sat["ARG_OF_PERICENTER"],
        sat["MEAN_ANOMALY"], sat["BSTAR"], sat["MEAN_MOTION_DOT"],
        sat["MEAN_MOTION_DDOT"], sat["ELEMENT_SET_NO"], sat["REV_AT_EPOCH"]
    ))

    inserted += 1

conn.commit()
print(f"Inserted/updated {inserted} objects with orbital data.")

cur.close()
conn.close()