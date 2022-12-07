from tgtg import TgtgClient

client = TgtgClient(email="malashkin.andrey@gmail.com")
print("clinet created")
credentials = client.get_credentials()

print(credentials)
