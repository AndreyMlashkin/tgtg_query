from tgtg import TgtgClient
from datetime import datetime, timezone 
import pytz
from tzlocal import get_localzone

tz = get_localzone()

def make_unique(list_with_duplicates):
    unique_list = []
    for item in list_with_duplicates:
        id = item["item"]["item_id"]
        unique = True
        for sub_item in unique_list:
            if sub_item["item"]["item_id"] == id:
                unique = False
                break
        if unique:
            unique_list.append(item)
    return unique_list


email="beyoh24361@moenode.com"
name="TestUser"

credentials = {'access_token': 'e30.eyJzdWIiOiI4ODI5OTM0NiIsImV4cCI6MTY2MzQxMjE4MSwidCI6IkhGLUo4SHFCUnR5LWNqU3lNWnhzV1E6MDoxIn0.ETkJC5NVfJvdFH1yt5gnlcjxQgjEWqyi7MktRWGXi6Y',
'refresh_token': 'e30.eyJzdWIiOiI4ODI5OTM0NiIsImV4cCI6MTY5NDc3NTM4MSwidCI6IkFiZW9MYVI0UXc2R19ib21ScDI4eFE6MDowIn0.4xXD-QoCGzQf1fhStnkIDj1drGMOI2Mti9eTPSndOJo',
'user_id': '88299346'
}

client = TgtgClient(email=email, access_token=credentials["access_token"], refresh_token=credentials["refresh_token"], user_id=credentials["user_id"])
#client.signup_by_email(email=email)

if not credentials:
    try:
        credentials = client.get_credentials()
    except Exception as e:
        pass

coordinates_list = [
(47.065677, 15.444379),
(47.045050, 15.433340),
(47.066350, 15.469640),
]

items = []
for point in coordinates_list:
    items += client.get_items(
        favorites_only=False,
        latitude=point[0],
        longitude=point[1],
        radius=2,
    )

items = make_unique(items)
now = datetime.utcnow()

good_items = []
for item in items:
    try:
        item_object = item["item"]
        if "average_overall_rating" in item_object.keys():
            rating = item_object["average_overall_rating"]["average_overall_rating"]
            if rating > 4:
                store_object = item['store']
           
                if not item['in_sales_window']:
                    continue
           
                if item['items_available'] == 0:
                    continue

                time_stamp = item['purchase_end']
                time_stamp_utc = datetime.fromisoformat(time_stamp.replace('Z', '+00:00'))
                time_stamp_without_region = datetime.fromisoformat(time_stamp.replace('Z', ''))
                time_left_seconds = (time_stamp_without_region - now).total_seconds()

                time_left_minutes = time_left_seconds / 60
                time_left_hours = time_left_minutes / 60
                time_left_minutes = time_left_minutes % 60

                time_left_str = "{}h:{}m".format(int(time_left_hours), int(time_left_minutes))
                good_item={'item_id' : item_object['item_id'],
                'rating' : rating,
                'store_name' : store_object['store_name'],
                'purchase_end' : item['purchase_end'],
                'time_left' : time_left_str,
                'items_available' : item['items_available'],
                }
                
                good_items.append(good_item)

    except Exception as e:
        #pass
        print(e)
        print("this item invalid: {}".format(item))

def rating_compare(item):
    return -item['rating']

good_items.sort(key=rating_compare)

print("UTC now is {}".format(now))
for value in good_items:
    print(value)
