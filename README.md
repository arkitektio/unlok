# unlok

[![PyPI version](https://badge.fury.io/py/unlok.svg)](https://pypi.org/project/unlok/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/unlok.svg)](https://pypi.python.org/pypi/unlok/)

The python client for lok, the authentication and identity server of an
[Arkitekt](https://arkitekt.live) deployment: users and groups, apps, releases and their clients,
the services a deployment composes, and the redeem tokens deployed apps enrol with.

## Installation

```bash
pip install unlok
```

With arkitekt, `pip install "arkitekt[rekuest,unlok]"` brings it in.

## Usage

Every lok operation is a method of the `Unlok` client, in a blocking and an `a`-prefixed async
flavour (`unlok.me()`, `await unlok.ame()`).

Unlike the other service clients, unlok requires nothing from the deployment: it talks to the
app's *own* lok server, the one the app authenticated against.

### In an arkitekt app

Add the service to your app and ask for `unlok: Unlok`; the client is injected by annotation.
Services travel between actions by id (`@lok/service`):

```python
from arkitekt import App, run
from unlok import Unlok, unlok_service

app = App("whoami", "0.1.0", services=[unlok_service])


@app.action
def whoami(unlok: Unlok) -> str:
    """Who Am I

    The user this app is acting for.
    """
    return unlok.me().username


if __name__ == "__main__":
    run(app)
```

### From a script

```python
from arkitekt import easy
from unlok import unlok_service

with easy("my-script", unlok_service) as unlok:
    for service in unlok.list_services():
        print(service.identifier, service.name)
```

## Testing

Unit tests need nothing but the package:

```bash
uv run pytest -k "not integration"
```

The integration tests start a real lok (plus postgres, redis and minio) with
docker compose through [dokker](https://github.com/jhnnsrs/dokker), enrol into
it the way a deployed app does — by redeeming the token provisioned in
`tests/integration/configs/lok.yaml` through the fakts redeem grant — and then
exercise the client against it, including the pinned redeem-token flow a
deployer drives:

```bash
uv run pytest -m integration
```

The stack runs the published `jhnnsrs/lok:${LOK_SERVICE_TAG:-latest}` image, so the
schema under test is whatever was last pushed to `:latest`. CI defaults to the same tag;
set the repository variable `LOK_SERVICE_TAG` (or export it locally) to test against
another published tag, such as `next`. To test against a local
server checkout instead, drop a gitignored `tests/integration/docker-compose.local.yml`
next to the compose file that builds the `lok` service from that checkout; the
fixtures pick it up automatically.
