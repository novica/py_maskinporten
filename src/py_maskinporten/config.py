from cryptography.hazmat.primitives.serialization import load_pem_private_key
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional


class MaskinportenSecrets(BaseModel):
    PRIVATE_KEY: str = Field(..., description="PEM string or file contents")
    MASKINPORTEN_CLIENT_ID: str = Field(
        ..., description="Client ID used for Maskinporten"
    )
    KID: str = Field(..., description="Key ID used in JWT header")
    SCOPE: str = Field(..., description="Space-delimited scopes")

    @field_validator("PRIVATE_KEY")
    def validate_private_key(cls, v: str) -> str:
        # Skip strict validation unless explicitly enabled
        if os.getenv("STRICT_KEY_VALIDATION", "").lower() not in {"1", "true", "yes"}:
            return v

        # If strict validation enabled then parse PEM
        try:
            load_pem_private_key(v.encode(), password=None)
        except Exception as exc:
            raise ValueError(f"Invalid PRIVATE_KEY PEM: {exc}") from exc

        return v


def load_config(
    deployment: str = "local", secret_scope: Optional[str] = None
) -> MaskinportenSecrets:
    if deployment == "local":
        load_dotenv()
        raw = _load_local_env()

    elif deployment == "azure-databricks":
        if not secret_scope:
            raise ValueError("secret_scope is required for Azure Databricks")
        raw = _load_azure_secrets(secret_scope)

    else:
        raise ValueError(f"Unknown deployment type: {deployment}")

    return MaskinportenSecrets(**raw)


def _load_local_env() -> Dict[str, str]:
    """Load secret config from environment variables."""
    config: Dict[str, str] = {}

    for key in MaskinportenSecrets.model_fields.keys():
        value = os.getenv(key)
        if value is None:
            raise RuntimeError(f"Missing required environment variable: {key}")
        config[key] = value

    return config


def _load_azure_secrets(secret_scope: str) -> Dict[str, str]:
    """Load secret config from Azure Key Vault."""
    config: Dict[str, str] = {}

    for key in MaskinportenSecrets.model_fields.keys():
        value = dbutils.secrets.get(scope=secret_scope, key=key)  # noqa: F821 # type: ignore
        if value is None:
            raise RuntimeError(f"Missing required secret in Key Vault: {key}")
        config[key] = value

    return config
