import httpx
# import os
# import aiohttp
from phonenumbers import parse
from .proxy import PROXY, SSL_CONTEXT
# from aiohttp import ClientSession
import ssl
import sys
import traceback
import asyncio


# _PROXY_URL = "http://185.193.157.60:12321"
# proxy_username = os.environ["PROXY_USERNAME"]
# proxy_password = os.environ["PROXY_PASSWORD"]
# proxy_auth = aiohttp.BasicAuth(proxy_username, proxy_password)
# # session = ClientSession()

class CancelledError(Exception):
    """ Custom Error For Cancelled Operation"""
    pass

async def search_phonenumber(phoneNumber, countryCode, installationId):
    """
    Search for a phone number using Truecaller API.

    Args:
        phoneNumber (str): The phone number to search.
        countryCode (str): The country code of the phone number.
        installationId (str): The installation ID for authorization.

    Returns:
        dict: The search result containing information about the phone number.

    Raises:
        httpx.RequestError: If an error occurs during the API request.
    """
    phone_number = parse(str(phoneNumber), str(countryCode))
    significant_number = phone_number.national_number

    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "Authorization": f"Bearer {installationId}"
    }
    params = {
        "q": str(significant_number),
        "countryCode": phone_number.country_code,
        "type": 4,
        "locAddr": "",
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json"
    }
    cont = ssl.create_default_context()
    cont.options &= ~ssl.OP_NO_TLSv1_3
    cont.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2
    try:
        # async with session.get(url="https://search5-noneu.truecaller.com/v2/search", params=params, headers=headers, proxy=_PROXY_URL, proxy_auth=proxy_auth) as response:
        async with httpx.AsyncClient(proxies=PROXY, verify=cont) as client:
            response = await client.get(
                "https://search5-noneu.truecaller.com/v2/search", params=params, headers=headers
            )

        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "data": response.json()
        }
    except asyncio.CancelledError as e:
         # Print the exception's message

        # Print more detailed info about the exception itself
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if exc_tb:
            fname = exc_tb.tb_frame.f_code.co_filename
            line_no = exc_tb.tb_lineno

        # Print the full traceback to understand the exception's origin and propagation
        tb_str = traceback.format_exception(exc_type, exc_obj, exc_tb)
        traceback_str = "".join(tb_str)

        # Log the full traceback
        raise CancelledError(f"Operation Cancelled with stacktrace {traceback_str} and error {e}")
    except httpx.HTTPError as exc:
        error_message = "An HTTP error occurred: " + str(exc)
        return {
            "status_code": exc.response.status_code if hasattr(exc, "response") else None,
            "error": "HTTP Error",
            "message": error_message
        }



async def bulk_search(phoneNumbers, countryCode, installationId):
    """
    Perform bulk search for a list of phone numbers using Truecaller API.

    Args:
        phoneNumbers (list[str]): The list of phone numbers to search.
        countryCode (str): The country code of the phone numbers.
        installationId (str): The installation ID for authorization.

    Returns:
        dict: The bulk search result containing information about the phone numbers.

    Raises:
        httpx.RequestError: If an error occurs during the API request.
    """
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "Truecaller/11.75.5 (Android;10)",
        "Authorization": f"Bearer {installationId}"
    }
    params = {
        "q": str(phoneNumbers),
        "countryCode": countryCode,
        "type": 14,
        "placement": "SEARCHRESULTS,HISTORY,DETAILS",
        "encoding": "json"
    }
    try:
        async with httpx.AsyncClient(proxies=PROXY, verify=SSL_CONTEXT) as client:
            response = await client.get(
                "https://search5-noneu.truecaller.com/v2/bulk", params=params, headers=headers
            )
        response.raise_for_status()

        return {
            "status_code": response.status_code,
            "data": response.json()
        }
    except httpx.HTTPError as exc:
        error_message = "An HTTP error occurred: " + str(exc)
        return {
            "status_code": exc.response.status_code if hasattr(exc, "response") else None,
            "error": "HTTP Error",
            "message": error_message
        }


