"""
Offline support module for PWA (Progressive Web Application) functionality.

Provides service worker installation and browser capability detection
for offline operation with IndexedDB.
"""


def install_service_worker():
    """Register the service worker for offline support and PWA capabilities.

    Attempts to register 'sw.js' as a service worker. Logs the worker state
    and listens for state changes. Falls back gracefully if service workers
    are not supported by the browser.
    """
    if hasattr(navigator, "serviceWorker"):

        def reg(registration):
            """Callback invoked after successful service worker registration.

            Determines the active service worker instance (installing, waiting,
            or active) and sets up a state change listener for debugging.
            """
            if registration.installing:
                serviceWorker = registration.installing
            elif registration.waiting:
                serviceWorker = registration.waiting
            elif registration.active:
                serviceWorker = registration.active

            if serviceWorker:
                console.log(serviceWorker.state)

                def onstatechange(self, e):
                    """Log state transitions of the service worker."""
                    console.log(e.target.state)

                serviceWorker.addEventListener("statechange", onstatechange)

        def err(error):
            """Log service worker registration errors."""
            console.log(error)

        navigator.serviceWorker.register(BASE_PATH + "sw.js").then(reg).catch(err)
    else:
        console.log("The current browser doesn't support service workers")


def service_worker_and_indexedDB_test():
    """Check whether the browser supports both service workers and IndexedDB.

    Also verifies the connection is over HTTPS or localhost (required for
    service worker registration by the Secure Contexts spec).

    Returns:
        bool: True if offline support is available, False otherwise.
    """
    if (
        hasattr(navigator, "serviceWorker")
        and hasattr(window, "indexedDB")
        and (
            location.hostname == "localhost"
            or location.hostname == "127.0.0.1"
            or location.hostname == "127.0.0.2"
            or location.protocol == "https:"
        )
    ):
        return True
    else:
        return False
