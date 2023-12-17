import logging
from abc import ABCMeta, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from ..client import KubernetesApiClient
from ._condition import Condition

T = TypeVar("T")
logging.basicConfig(level=logging.INFO)


class ResourceApi(Generic[T], metaclass=ABCMeta):
    api_client_type: Type[T] = None
    api_client: T
    _logger = logging.getLogger(__name__)

    def __init__(self, kubeclient: KubernetesApiClient):
        if not getattr(self, "api_client_type", None):
            raise AttributeError("api_client_type must be set")
        self.api_client = self.api_client_type(kubeclient.api_client)

    @abstractmethod
    def get(self, namespace: str, name: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def list(self, namespace: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create(self, namespace: str, body: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def create_from_yaml(
        self, namespace: str, yaml_file_path: str, **kwargs
    ) -> Optional[List[dict]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, namespace: str, name: str, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def patch(self, namespace: str, name: str, body: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, namespace: str, name: str, body: dict, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def is_ready(self, namespace: str, name: str, **kwargs):
        raise NotImplementedError

    def wait_for_ready(
        self,
        namespace: str,
        name: str,
        timeout: Optional[int],
        interval: Optional[float],
    ) -> bool:
        return self.wait_for_condition(
            Condition(
                name=f"{self.__class__.__name__} {name} in namespace {namespace} to be ready",
                fn=lambda: self.is_ready(namespace, name),
                timeout=timeout,
                interval=interval,
            )
        )

    def wait_for_condition(self, condition: Condition) -> bool:
        self._logger.info(f"Waiting for {condition._name}")
        return condition.wait()
