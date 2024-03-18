import os
from urllib.parse import quote_plus
from dotenv import load_dotenv


load_dotenv()

# Use environment variables for the proxy username and password
proxy_username = os.environ["PROXY_USERNAME"]
proxy_password = os.environ["PROXY_PASSWORD"]

auth_proxy_url = f"http://{quote_plus(proxy_username)}:{quote_plus(proxy_password)}@185.193.157.60:12321"

PROXY = {"http://": auth_proxy_url, "https://": auth_proxy_url}
