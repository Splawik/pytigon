__pragma__("alias", "js_continue", "continue")


INIT_DB_STRUCT = None


def init_db(struct):
    global INIT_DB_STRUCT
    INIT_DB_STRUCT = struct


window.init_db = init_db


def open_database(on_open):
    if not window.indexedDB:
        console.log("Your Browser does not support IndexedDB")
    else:
        request = window.indexedDB.open(window.PRJ_NAME, 1)

        def _onerror(event):
            console.log("Error opening DB", event)

        request.onerror = _onerror

        def _onupgradeneeded(event):
            global INIT_DB_STRUCT
            console.log("Upgrading")
            db = event.target.result
            objectStore = db.createObjectStore("param", {"keyPath": "key"})
            if INIT_DB_STRUCT:
                for pos in INIT_DB_STRUCT:
                    objectStore = db.createObjectStore(pos[0], pos[1])

        request.onupgradeneeded = _onupgradeneeded

        def _onsuccess(event):
            nonlocal on_open

            db = event.target.result

            on_open(db)

        request.onsuccess = _onsuccess


window.open_database = open_database


def get_table(table_name, on_open, read_only=True):
    def _on_open(db):
        nonlocal on_open
        if read_only == True:
            mode = "readonly"
        else:
            mode = "readwrite"
        tabTrans = db.transaction(table_name, mode)
        tabObjectStore = tabTrans.objectStore(table_name)
        on_open(tabTrans, tabObjectStore)

    open_database(_on_open)


window.get_table = get_table


def get_list_from_table(table, on_open_list):
    def on_open(trans, table):
        items = []

        def oncomplete(evt):
            on_open_list(items)

        trans.oncomplete = oncomplete

        cursor_request = table.openCursor()

        def onerror(error):
            console.log(error)

        cursor_request.onerror = onerror

        def onsuccess(evt):
            cursor = evt.target.result
            if cursor:
                items.push(cursor.value)
                cursor.js_continue()

        cursor_request.onsuccess = onsuccess

    get_table(table, on_open)


window.get_list_from_table = get_list_from_table


# example of init_sync struct
# [ ['tbl', time_href, sync_fun], [...]]
# sync_fun(on_success, on_error)


def on_sys_sync(fun):
    def _fun(cache_deleted):
        if cache_deleted:
            fun("OK-refresh")
        else:
            fun("OK-no cache")

    caches.delete("PYTIGON_" + window.PRJ_NAME).then(_fun)


_UA = window.navigator.userAgent
_MSIE = _UA.indexOf("MSIE ")
_MSIE2 = _UA.indexOf("Trident/")

if _MSIE > 0 or _MSIE2 > 0:
    SYNC_STRUCT = []
else:
    SYNC_STRUCT = [["sys", window.BASE_PATH + "schsys/app_time_stamp/", on_sys_sync]]


def init_sync(sync_struct):
    global SYNC_STRUCT
    for pos in sync_struct:
        SYNC_STRUCT.append(pos)


window.init_sync = init_sync


def sync_and_run(tbl, fun):
    rec = None
    for pos in SYNC_STRUCT:
        if pos[0] == tbl:
            rec = pos
            break
    if not rec:
        fun("error - no reg function")
        return

    if navigator.onLine:

        def complete(responseText):
            def _on_open_param(trans, db):
                nonlocal tbl
                param_get_request = db.js_get("time_sync_" + tbl)

                def _on_param_error(event):
                    rec[2](fun)
                    db.add({"key": "time_sync_" + tbl, "value": time})

                def _on_param_success(event):
                    nonlocal param_get_request, db, time, rec, fun, tbl
                    param = param_get_request.result
                    if param:
                        time2 = param.value
                        if time2 < time:
                            # rec[2](fun)
                            param.value = time
                            param_update_request = db.put(param)

                            def _on_update(event):
                                nonlocal rec, fun
                                rec[2](fun)

                            param_update_request.onerror = _on_update
                            param_update_request.onsuccess = _on_update
                        else:
                            fun("OK")
                    else:
                        # rec[2](fun)
                        param_add_request = db.add(
                            {"key": "time_sync_" + tbl, "value": time}
                        )

                        def _on_add_success(event):
                            nonlocal rec
                            rec[2](fun)

                        def _on_add_error(event):
                            nonlocal rec
                            rec[2](fun)

                        param_add_request.onerror = _on_add_error
                        param_add_request.onsuccess = _on_add_success

                param_get_request.onerror = _on_param_error
                param_get_request.onsuccess = _on_param_success

            try:
                x = JSON.parse(responseText)
                time = x["TIME"]
                get_table("param", _on_open_param, False)
            except:
                console.log(responseText)
                window.open().document.write(responseText)
                # win = window.open("data:text/html," + responseText, "_blank", "width=200,height=100")
                # win.focus()

        def _on_request_init(request):
            def _on_timeout(event):
                nonlocal fun
                fun("timeout")

            try:
                request.timeout = 2000
            except:
                pass
            request.ontimeout = _on_timeout

        ajax_get(rec[1], complete, _on_request_init)
    else:
        fun("offline")


window.sync_and_run = sync_and_run
