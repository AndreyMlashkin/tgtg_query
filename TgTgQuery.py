from tgtg import TgtgClient
from datetime import datetime
from tzlocal import get_localzone

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


class GoodItem:

    def __init__(self, item):
        self.good = False

        #self.item_id
        #self.rating
        #self.store_name
        #self.purchase_end
        #self.time_left
        #self.items_available

        now = datetime.utcnow()

        item_object = item["item"]
        if "average_overall_rating" in item_object.keys():
            rating = item_object["average_overall_rating"]["average_overall_rating"]
            if rating > 4:
                store_object = item['store']

                if not item['in_sales_window']:
                    return

                if item['items_available'] == 0:
                    return

                time_stamp = item['purchase_end']
                time_stamp_without_region = datetime.fromisoformat(time_stamp.replace('Z', ''))
                time_left_seconds = (time_stamp_without_region - now).total_seconds()

                time_left_minutes = time_left_seconds / 60
                time_left_hours = time_left_minutes / 60
                time_left_minutes = time_left_minutes % 60

                time_left_str = "{}h:{}m".format(int(time_left_hours), int(time_left_minutes))

                self.item_id = item_object['item_id']
                self.rating = rating  #round(rating, 2),
                self.store_name = store_object['store_name'],
                self.purchase_end = item['purchase_end'],
                self.time_left = time_left_str,
                self.items_available = item['items_available'],

                self.good = True

    def is_good(self):
        return self.good


    def to_string(self):
        return "rating: {}\tstore_name: {}\tpurchase_end: {}\ttime_left: {}\titems_available: {}\n\n\n".format(self.rating, self.store_name, self.purchase_end, self.time_left, self.items_available)

class TgTgQuery:

    def __init__(self):
        self.tz = get_localzone()
        self.email="beyoh24361@moenode.com"
        self.name="TestUser"
        self.credentials = {'access_token': 'e30.eyJzdWIiOiI4ODI5OTM0NiIsImV4cCI6MTY2MzQxMjE4MSwidCI6IkhGLUo4SHFCUnR5LWNqU3lNWnhzV1E6MDoxIn0.ETkJC5NVfJvdFH1yt5gnlcjxQgjEWqyi7MktRWGXi6Y',
        'refresh_token': 'e30.eyJzdWIiOiI4ODI5OTM0NiIsImV4cCI6MTY5NDc3NTM4MSwidCI6IkFiZW9MYVI0UXc2R19ib21ScDI4eFE6MDowIn0.4xXD-QoCGzQf1fhStnkIDj1drGMOI2Mti9eTPSndOJo',
        'user_id': '88299346'
        }

    def _get_good_items_list(self):
        client = TgtgClient(email=self.email, access_token=self.credentials["access_token"], refresh_token=self.credentials["refresh_token"], user_id=self.credentials["user_id"])
        #client.signup_by_email(email=email)

        if not self.credentials:
            try:
                self.credentials = client.get_credentials()
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

        good_items = []
        for item in items:
            try:
                good_item = GoodItem(item)
                if good_item.is_good():
                    good_items.append(good_item)

            except Exception as e:
                #pass
                print(e)
                print("this item invalid: {}".format(item))

        def rating_compare(item):
            return -item.rating

        good_items.sort(key=rating_compare)
        return good_items

    def query(self):
        good_items = self._get_good_items_list()
        now = datetime.utcnow()
        result = "UTC now is {}\n\n".format(now)
        for value in good_items:
            result += value.to_string()
        return result

#query = TgTgQuery()
#query.query()
