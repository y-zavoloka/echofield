"""
Security settings for Django application.

This module conditionally defines SSL/HTTPS security settings based on the USE_SSL
configuration flag. When SSL is enabled, it applies comprehensive security headers
and cookie settings to ensure secure communication.
"""

from __future__ import annotations

from echofield.settings.config import cfg

# Security settings are only created when needed; Django will use defaults for missing values
if cfg.USE_SSL:
    # Force HTTPS redirects for all requests
    SECURE_SSL_REDIRECT = True

    # Trust the X-Forwarded-Proto header from reverse proxy (e.g., nginx, load balancer)
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # HTTP Strict Transport Security (HSTS) - force HTTPS for 1 year
    SECURE_HSTS_SECONDS = 31536000  # 365 days

    # Ensure session cookies are only sent over HTTPS
    SESSION_COOKIE_SECURE = True

    # Ensure CSRF cookies are only sent over HTTPS
    CSRF_COOKIE_SECURE = True

    # Prevent the site from being embedded in frames (clickjacking protection)
    X_FRAME_OPTIONS = "DENY"

# Export only the settings that are actually defined
# This allows the module to be imported safely regardless of USE_SSL value
__all__ = [
    *(
        [
            "SECURE_SSL_REDIRECT",
            "SECURE_PROXY_SSL_HEADER",
            "SECURE_HSTS_SECONDS",
            "SESSION_COOKIE_SECURE",
            "CSRF_COOKIE_SECURE",
            "X_FRAME_OPTIONS",
        ]
        if cfg.USE_SSL
        else []
    ),
]
