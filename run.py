from tgtg import TgtgClient

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

items = client.get_items(
    favorites_only=False,
    latitude=47.07,
    longitude=15.43,
    radius=10,
)

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
           
                good_item={'item_id' : item_object['item_id'],
                'rating' : rating,
                'store_name' : store_object['store_name'],
                'purchase_end' : item['purchase_end'],
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

for value in good_items:
    print(value)
