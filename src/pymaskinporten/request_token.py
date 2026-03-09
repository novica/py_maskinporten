from datetime import datetime, timedelta, timezone
import httpx
from jwt import encode
import uuid
from pymaskinporten.config import load_config


def request_maskinporten_token(api_env: str) -> tuple:
    """
    Requests an access token from Maskinporten using API-specific credentials.

    Args:
        api_env (str): The environment of the API (e.g., "prod" or "test").

    Returns:
        tuple: A tuple containing the access token (str) and its expiration time (int).

    Raises:
        Exception: If the token request fails.

    Examples:
        request_maskinporten_token(api_env = "test")
    """

    if api_env == "test":
        issuer_url = "https://test.maskinporten.no/token"
    else:
        issuer_url = "https://maskinporten.no/token"

    cfg = load_config()

    header = {"kid": cfg.KID}
    if not header["kid"]:
        raise ValueError("JWK must include 'kid'.")

    payload = {
        "aud": issuer_url,
        "iss": cfg.MASKINPORTEN_CLIENT_ID,
        "scope": cfg.SCOPE,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=1),
        "jti": str(uuid.uuid4()),
    }

    private_key = cfg.PRIVATE_KEY
    jwt_assertion = encode(payload, private_key, algorithm="RS256", headers=header)

    response = httpx.post(
        issuer_url,
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt_assertion,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("access_token")
        expires_in = response_data.get("expires_in")
        print(
            f"Access token for {cfg.SCOPE} in {api_env} environment fetched successfully."
        )
        return access_token, expires_in
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
