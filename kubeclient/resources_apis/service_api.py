from typing import List, Optional

from kubernetes.client import CoreV1Api, V1Service, V1ServiceList, exceptions
from kubernetes.utils import create_from_yaml

from .resource_api import ResourceApi


class Service(ResourceApi[CoreV1Api]):
    """
    A class to manage the Kubernetes Service resource.
    """

    api_client_type = CoreV1Api

    def get(self, namespace: str, name: str) -> Optional[V1Service]:
        service = None
        try:
            service = self.api_client.read_namespaced_service(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to get service {name} in namespace {namespace}: {e}"
            )

        return service

    def list(self, namespace: str) -> Optional[V1ServiceList]:
        services = None
        try:
            services = self.api_client.list_namespaced_service(namespace=namespace)
        except exceptions.ApiException as e:
            self._logger.error(f"Failed to list services in namespace {namespace}: {e}")

        return services

    def create(self, namespace: str, body: V1Service) -> Optional[V1Service]:
        created_service = None
        try:
            created_service = self.api_client.create_namespaced_service(
                namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create service {body.metadata.name} in namespace {namespace}: {e}"
            )

        return created_service

    def delete(self, namespace: str, name: str) -> Optional[V1Service]:
        deleted_service = None
        try:
            deleted_service = self.api_client.delete_namespaced_service(
                name=name, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to delete service {name} in namespace {namespace}: {e}"
            )

        return deleted_service

    def patch(self, namespace: str, name: str, body: V1Service) -> Optional[V1Service]:
        patched_service = None
        try:
            patched_service = self.api_client.patch_namespaced_service(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to patch service {name} in namespace {namespace}: {e}"
            )

        return patched_service

    def update(self, namespace: str, name: str, body: V1Service) -> Optional[V1Service]:
        updated_service = None
        try:
            updated_service = self.api_client.replace_namespaced_service(
                name=name, namespace=namespace, body=body
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to update service {name} in namespace {namespace}: {e}"
            )

        return updated_service

    def create_from_yaml(
        self, yaml_path: str, namespace: str
    ) -> Optional[List[V1Service]]:
        created_service = None
        try:
            created_service = create_from_yaml(
                self.api_client, yaml_path, namespace=namespace
            )
        except exceptions.ApiException as e:
            self._logger.error(
                f"Failed to create service from yaml in namespace {namespace}: {e}"
            )

        return created_service

    def is_ready(self, namespace: str, name: str) -> bool:
        service = self.get(namespace=namespace, name=name)
        if service is None:
            return False

        return (
            service.status.load_balancer.ingress is not None
            and len(service.status.load_balancer.ingress) > 0
        )
