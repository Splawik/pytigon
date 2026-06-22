try:
    from django.utils.csp import CSP
except ImportError:
    CSP = None

if CSP is not None:
    SECURE_CSP = {
        "default-src": [CSP.SELF],
        "script-src": [
            CSP.SELF,
            CSP.NONCE,
            "blob:",
            "https://*.jsdelivr.net",
            "https://*.googleapis.com",
            "'sha256-HHh/PGb5Jp8ck+QB/v7zeWzuHf3vYssM0CBPvYgEHR4='",
        ],
        "style-src": [
            CSP.SELF,
            CSP.UNSAFE_INLINE,
            "https://*.jsdelivr.net",
            "https://googleapis.com",
            "https://*.googleapis.com",
        ],
        "font-src": [
            CSP.SELF,
            "https://gstatic.com",
            "https://*.gstatic.com",
            "data:",
        ],
        "img-src": [
            CSP.SELF,
            "data:",
            "blob:",
            "https://*.tile.osm.org",
            "https://*.bossanova.uk",
            "https://*.tile.openstreetmap.org",
        ],
        "worker-src": [
            CSP.SELF,
            "blob:",
        ],
        "connect-src": [
            CSP.SELF,
            "https://pytigon.cloud",
            "https://*.pytigon.cloud",
            "wss://pytigon.cloud",
            "wss://*.pytigon.cloud",
            "https://cdn.jsdelivr.net",
            "https://tile.openstreetmap.org",
            "https://*.tile.openstreetmap.org",
        ],
    }
else:
    SECURE_CSP = {}
