# Timeout config and its two callers

`config/service.yaml`

```yaml
profile_service:
  url: https://profiles.internal/api
  timeout: 30
```

`web/src/profileClient.js`

```js
import config from "../../config/service.json"; // generated from service.yaml at build time

export function loadProfile(onDone) {
  const timer = setTimeout(() => onDone(new Error("profile timed out")), config.profile_service.timeout);
  return fetch(config.profile_service.url).then((res) => {
    clearTimeout(timer);
    return res.json();
  });
}
```

`worker/profile_sync.py`

```python
import requests

from worker.settings import CONFIG


def sync_profile(user_id):
    svc = CONFIG["profile_service"]
    return requests.get(f"{svc['url']}/{user_id}", timeout=svc["timeout"]).json()
```
