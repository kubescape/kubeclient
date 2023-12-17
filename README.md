# kubeclient

This is a wrapper around the k8s python client that provides a more pythonic interface to the k8s api.
The goal is to make it easier to write tests for k8s resources. It is not intended to be a full replacement for the k8s python client.
_This is a work in progress and is not ready for production use yet 🏗️._

# Usage

```python
from kubeclient import KubernetesApiClient, resources_apis, Deployer

from pathlib import Path

YAML = Path(__file__).parent / "deployments" / "pod-with-host-mount.yaml"

def test_deployer():
    client = KubernetesApiClient()
    deployer = Deployer(client)
    deployer.create_from_yaml(YAML)

    pod_api = resources_apis.Pod(client)
    if pod_api.wait_for_ready("default", "host-mount-pod", 10, 0.5):
        pod = pod_api.get("default", "host-mount-pod")
        assert pod.status.phase == "Running"

    assert deployer.delete_from_yaml(YAML)
    assert not pod_api.wait_for_ready("default", "host-mount-pod", 5, 0.5)
```

## Installation

```bash
pip install kubeclient
```

## Development

### Setup

1. Clone the repo
2. Create a virtualenv
3. Install the requirements
4. Install the pre-commit hooks with `pre-commit install`
5. Run the tests with `pytest`
