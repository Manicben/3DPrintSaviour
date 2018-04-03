from octoclient import OctoClient

URL = 'http://146.169.145.97/'
API_KEY = '91B5F50805DE468799850E3BCF804CE6'

try:
    client = OctoClient(url=URL, apikey=API_KEY)
    print(client.version)
    print(client.job_info())
    print(client.connection_info())
    printing = client.printer()['state']['flags']['printing']
    if printing:
        print("Currently printing")
    else:
        print("Not currently printing")
except Exception as e:
    print(e)
