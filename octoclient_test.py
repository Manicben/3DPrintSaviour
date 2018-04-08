from octoclient import OctoClient
from api_keys import URL,API_KEY

# Specify URL and API key for Octoprint
if URL is None:
    URL = 'YOUR OCTOPRINT IP ADDRESS'
if API_KEY is None:
    API_KEY = 'YOUR OCTOPRINT API KEY'

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
