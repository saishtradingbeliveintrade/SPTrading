import upstox_client
from upstox_client.rest import ApiException
import os

ACCESS_TOKEN = os.getenv("UPSTOX_ACCESS_TOKEN")

configuration = upstox_client.Configuration()
configuration.access_token = ACCESS_TOKEN

api_client = upstox_client.ApiClient(configuration)

quote_api = upstox_client.MarketQuoteApi(api_client)
history_api = upstox_client.HistoryApi(api_client)
