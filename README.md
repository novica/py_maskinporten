# py_maskinporten

This is a python package to request a token from Maskinporten - the Norwegian 
national access control solution for businesses that exchange data.

## Example usage

This assumes that: 
1. You have created the integration on digidir.no and,
2. You have set the necessary environment variables for your API credentials.

```python
# set environment variables for your API    
import os
os.environ["KID"] = "your_kid"
os.environ["PRIVATE_KEY"] = "your_private_key"
os.environ["MASKINPORTEN_CLIENT_ID"] = "your_client_id"
os.environ["SCOPE"] = "your_scope"

# get the access token
from py_maskinporten.request_token import request_maskinporten_token
access_token, expires_in = request_maskinporten_token("my_api", "test")
print(f"Access Token: {access_token}")
print(f"Expires In: {expires_in} seconds")
```