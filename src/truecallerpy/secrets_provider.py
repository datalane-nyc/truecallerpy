import json
import git
import os

from google.cloud.secretmanager import (
    AccessSecretVersionResponse,
    SecretManagerServiceClient,
)

SECRETS_VERSION = 7
GLOBAL_SECRET_NAME = "env_file"
GOOGLE_PROJECT_NAME = "datalane"


class NoSecretFoundError(Exception):
    """Throws when no secret is present in SecretManager"""


def get_datalane_sa_key_file_path() -> str:
    """Get Datalane Service account secret location"""
    # Get the current directory
    current_dir = os.getcwd()

    # Find the root of the Git repository
    repo = git.Repo(current_dir, search_parent_directories=True)
    root_path = repo.git.rev_parse("--show-toplevel")

    return os.path.join(root_path, "google-datalane-sa.json")


class TrueCallerSecretsProvider:
    def __init__(self):
        self.service_account_location = get_datalane_sa_key_file_path()

        if not self.service_account_location:
            raise AttributeError("Service account location not set")

        self.secrets_manager_client: SecretManagerServiceClient = (
            SecretManagerServiceClient.from_service_account_json(
                filename=self.service_account_location
            )
        )
        self._secrets: dict[str, str] = self._load_all_secrets()

    def get_secret(self, secret_name: str) -> str:
        """Get a secret from SecretsProvider given a secret name"""
        if secret_name in self._secrets:
            return self._secrets[secret_name]

        raise NoSecretFoundError(f"Secret {secret_name} not found in SecretManager")

    def set_secret_for_tests(self, secret_name: str, secret_value: str) -> None:
        """Set a secret in the SecretsProvider to test bad key flows"""
        self._secrets[secret_name] = secret_value

    def _load_all_secrets(self) -> dict[str, str]:
        name = f"projects/{GOOGLE_PROJECT_NAME}/secrets/{GLOBAL_SECRET_NAME}/versions/{SECRETS_VERSION}"
        response: AccessSecretVersionResponse = (
            self.secrets_manager_client.access_secret_version(request={"name": name})
        )

        if response.payload.data:
            self._secrets = json.loads(response.payload.data.decode("UTF-8"))
            print(f"Loaded secrets from SecretManager for path: {name}")
            return self._secrets
        return {}


def main():
    secrets_provider = TrueCallerSecretsProvider()
    print(secrets_provider.get_secret("APOLLO_API_KEY"))


if __name__ == "__main__":
    main()
