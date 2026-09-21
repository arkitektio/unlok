# unlok

Python client for unlok

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
