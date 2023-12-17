import logging
import subprocess

from kubernetes.client import ApiClient
from kubernetes.utils import create_from_yaml

from .client import KubernetesApiClient

_logger = logging.getLogger(__name__)


class Deployer:
    _api_client: ApiClient

    def __init__(self, api_client: KubernetesApiClient) -> None:
        self._api_client = api_client.api_client

    def create_from_yaml(self, yaml_file_path: str, namespace: str = "default") -> list:
        _logger.info(f"Creating from yaml file {yaml_file_path}")
        return create_from_yaml(self._api_client, yaml_file_path, namespace=namespace)

    def delete_from_yaml(self, yaml_file_path: str, namespace: str = "default") -> bool:
        """
        Delete all resources defined in a yaml file.
        TODO: Change this to not use kubectl.
        """
        _logger.info(f"Deleting from yaml file {yaml_file_path}")
        kubectl = subprocess.run(
            ["kubectl", "delete", "-f", yaml_file_path, "-n", namespace],
            capture_output=True,
        )
        if kubectl.returncode != 0:
            _logger.error(
                f"Failed to delete from yaml file {yaml_file_path}: {kubectl.stderr}"
            )
            return False

        return True
