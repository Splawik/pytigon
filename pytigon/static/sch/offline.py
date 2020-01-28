__pragma__('alias', 'js_in', 'in')


def install_service_worker():
    if hasattr(navigator, 'serviceWorker'):

        def reg(registration):
            if registration.installing:
                serviceWorker = registration.installing;
            elif registration.waiting:
                serviceWorker = registration.waiting;
            elif registration.active:
                serviceWorker = registration.active;
            if serviceWorker:
                console.log(serviceWorker.state)

                def onstatechange(e):
                    console.log(e.target.state)

                serviceWorker.addEventListener('statechange', onstatechange)

        def err(error):
            console.log(error)

        navigator.serviceWorker.register(BASE_PATH + 'sw.js').then(reg).catch(err)
    else:
        console.log("The current browser doesn't support service workers")


def service_worker_and_indexedDB_test():
    if hasattr(navigator, 'serviceWorker') and hasattr(window, "indexedDB") and \
        (location.hostname == "localhost" or location.hostname == "127.0.0.1" or location.hostname == "127.0.0.2" or location.protocol == 'https:'):
        return True
    else:
        return False
