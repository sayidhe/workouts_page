import sqlite3


def convert_to_unicode(location):
    """
    Convert a given location string to its Unicode representation.
    """
    return location.encode("unicode_escape").decode("utf-8")


# Location values
# 苏州旺山
location_1 = "越溪街道, 吴中区, 苏州市, 江苏省, 320500, 中国"
unicode_location_1 = convert_to_unicode(location_1)

# 苏州东山
location_2 = "东山镇, 吴中区, 苏州市, 江苏省, 320500, 中国"
unicode_location_2 = convert_to_unicode(location_2)

# Connect to the database
db_path = "./data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Updating the first 'location_country' value
cursor.execute(
    "UPDATE activities SET location_country = ? WHERE rowid = 1;", [unicode_location_1]
)

# Updating the second 'location_country' value
cursor.execute(
    "UPDATE activities SET location_country = ? WHERE rowid = 2;", [unicode_location_2]
)

# Commit the changes and close the connection
conn.commit()
conn.close()

# Print success message
print(
    "\
Finished update:\n\
location_country_1: "
    + location_1
    + "\n\
unicode_location_country_1: "
    + unicode_location_1
    + "\n\
location_country_2: "
    + location_2
    + "\n\
unicode_location_country_2: "
    + unicode_location_2
    + "\n"
)
