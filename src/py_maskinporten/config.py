from typing import Dict, Optional
import os
from dotenv import load_dotenv


REQUIRED_ENV_VARS = [
    "PRIVATE_KEY",
    "MASKINPORTEN_CLIENT_ID",
    "KID",
    "SCOPE",
]


def load_config(
    deployment: str = "local", secret_scope: Optional[str] = None
) -> Dict[str, str]:
    """
    Load secret configuration values from environment variables (local)
    or Azure Key Vault (Databricks), depending on deployment.

    Returns a dictionary containing only secret values.
    """
    if deployment == "local":
        load_dotenv()
        return _load_local_env()

    if deployment == "azure-databricks":
        if not secret_scope:
            raise ValueError("secret_scope is required for Azure Databricks")
        return _load_azure_secrets(secret_scope)

    raise ValueError(f"Unknown deployment type: {deployment}")


def _load_local_env() -> Dict[str, str]:
    """Load secret config from environment variables."""
    config: Dict[str, str] = {}

    for key in REQUIRED_ENV_VARS:
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"Missing required environment variable: {key}")
        config[key] = value

    return config


def _load_azure_secrets(secret_scope: str) -> Dict[str, str]:
    """Load secret config from Azure Key Vault."""
    config: Dict[str, str] = {}

    for key in REQUIRED_ENV_VARS:
        value = dbutils.secrets.get(scope=secret_scope, key=key)  # noqa: F821 # type: ignore
        if value is None:
            raise RuntimeError(f"Missing required secret in Key Vault: {key}")
        config[key] = value

    return config
