# This file holds some constants and environment variable configurations

import os

default_config = {
    "PROD_MASKINPORTEN_ISSUER": "https://maskinporten.no/token",
    "TEST_MASKINPORTEN_ISSUER": "https://test.maskinporten.no/token",
    "PRIVATE_KEY": None,
    "MASKINPORTEN_CLIENT_ID": None,
    "KID": None,
    "SCOPE": None,
}

REQUIRED_ENV_VARS = [
    "PRIVATE_KEY",
    "MASKINPORTEN_CLIENT_ID",
    "KID",
    "SCOPE",
]


def load_config() -> dict:
    config = {}
    for key, default_value in default_config.items():
        if key in REQUIRED_ENV_VARS:
            value = os.getenv(key)
            if value is None:
                raise RuntimeError(f"Missing required environment variable: {key}")
            config[key] = value
        else:
            config[key] = os.getenv(key, default=default_value)
    return config
