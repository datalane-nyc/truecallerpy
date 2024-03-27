import os
from urllib.parse import quote_plus
import ssl
from dotenv import load_dotenv


load_dotenv()

SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.options &= ~ssl.OP_NO_TLSv1_3
SSL_CONTEXT.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2

# Use environment variables for the proxy username and password
proxy_username = os.environ["PROXY_USERNAME"]
proxy_password = os.environ["PROXY_PASSWORD"]

auth_proxy_url = f"http://{quote_plus(proxy_username)}:{quote_plus(proxy_password)}@185.193.157.60:12321"

PROXY = {"http://": auth_proxy_url, "https://": auth_proxy_url}
