from tgtg import TgtgClient

client = TgtgClient(email="sabadir758@edinel.com")
print("clinet created")
credentials = client.get_credentials()

print(credentials)
