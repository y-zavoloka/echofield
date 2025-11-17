from __future__ import annotations

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from echofield.settings.config import cfg

SENTRY_DSN = cfg.SENTRY_DSN
SENTRY_ENVIRONMENT = cfg.SENTRY_ENVIRONMENT
SENTRY_TRACES_SAMPLE_RATE = cfg.SENTRY_TRACES_SAMPLE_RATE
SENTRY_PROFILES_SAMPLE_RATE = cfg.SENTRY_PROFILES_SAMPLE_RATE

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
        environment=SENTRY_ENVIRONMENT,
        send_default_pii=True,
    )

__all__ = [
    "SENTRY_DSN",
    "SENTRY_ENVIRONMENT",
    "SENTRY_TRACES_SAMPLE_RATE",
    "SENTRY_PROFILES_SAMPLE_RATE",
]
