"""
IndexedDB database layer and server synchronization module.

Provides:
- IndexedDB initialization and table management.
- Generic CRUD helpers (open, get_table, get_list_from_table).
- Time-stamp based synchronization between server and local IndexedDB.
- Support for configurable sync structures (multiple tables).
"""

# =============================================================================
# Database initialization
# =============================================================================

import contextlib
INIT_DB_STRUCT = None


def init_db(struct):
    """Initialize the database schema definition.

    Called before open_database to define which object stores to create.

    Args:
        struct: List of (store_name, options) tuples for IndexedDB object stores.
    """
    global INIT_DB_STRUCT
    INIT_DB_STRUCT = struct


window.init_db = init_db


def open_database(on_open):
    """Open (or create) the IndexedDB database for the current project.

    The database name is derived from window.PRJ_NAME. On first creation,
    creates a 'param' key-value store plus any stores defined via init_db().

    Args:
        on_open: Callback invoked with the opened database instance on success.
    """
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
            # Always create a key-value parameter store
            objectStore = db.createObjectStore("param", {"keyPath": "key"})
            # Create additional stores from schema definition
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


# =============================================================================
# Table access helpers
# =============================================================================


def get_table(table_name, on_open, read_only=True):
    """Open a specific object store within the IndexedDB database.

    Args:
        table_name: Name of the object store to open.
        on_open: Callback receiving (transaction, objectStore).
        read_only: If True, opens in readonly mode; otherwise readwrite.
    """

    def _on_open(db):
        nonlocal on_open
        mode = "readonly" if read_only == True else "readwrite"
        tabTrans = db.transaction(table_name, mode)
        tabObjectStore = tabTrans.objectStore(table_name)
        on_open(tabTrans, tabObjectStore)

    open_database(_on_open)


window.get_table = get_table


def get_list_from_table(table, on_open_list):
    """Retrieve all records from an object store as a list.

    Opens a cursor and iterates through all records, collecting them
    into an array.

    Args:
        table: Name of the object store.
        on_open_list: Callback receiving the list of all stored items.
    """

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
                RawJS("cursor.continue()")

        cursor_request.onsuccess = onsuccess

    get_table(table, on_open)


window.get_list_from_table = get_list_from_table


# =============================================================================
# Synchronization engine
# =============================================================================
# Sync structure format:
#   [ ['table_name', time_check_url, sync_function], ... ]
#   sync_function(on_success, on_error)
#
# 'sys' is a built-in sync entry that checks the application timestamp
# and clears the PYTIGON cache when outdated.


def on_sys_sync(fun):
    """Built-in system sync handler: clears PYTIGON cache and reports status.

    Args:
        fun: Callback receiving status string:
            'OK-refresh' if cache was deleted,
            'OK-no cache' if no cache existed.
    """

    def _fun(cache_deleted):
        if cache_deleted:
            fun("OK-refresh")
        else:
            fun("OK-no cache")

    caches.delete("PYTIGON_" + window.PRJ_NAME).then(_fun)


# Browser detection: MSIE doesn't support the Cache API properly,
# so we skip the system sync on those browsers.
_UA = window.navigator.userAgent
_MSIE = _UA.indexOf("MSIE ")
_MSIE2 = _UA.indexOf("Trident/")

if _MSIE > 0 or _MSIE2 > 0:
    SYNC_STRUCT = []
else:
    SYNC_STRUCT = [["sys", window.BASE_PATH + "schsys/app_time_stamp/", on_sys_sync]]


def init_sync(sync_struct):
    """Register additional synchronization entries.

    Each entry defines a table name, a server URL for timestamp checking,
    and a sync function to execute when the server has newer data.

    Args:
        sync_struct: List of sync entries to append to SYNC_STRUCT.
            Each entry: [table_name, url, sync_function]
    """
    global SYNC_STRUCT
    for pos in sync_struct:
        SYNC_STRUCT.append(pos)


window.init_sync = init_sync


def sync_and_run(tbl, fun):
    """Synchronize a specific table with the server and invoke callback.

    Fetches a timestamp from the server, compares it with the locally stored
    timestamp in IndexedDB, and runs the registered sync function if the
    server has newer data.

    Args:
        tbl: Table name to synchronize (must be registered in SYNC_STRUCT).
        fun: Callback receiving status:
            'OK' - already in sync,
            'OK-refresh' / 'OK-no cache' - from sync function,
            'offline' - no network connection,
            'timeout' - request timed out,
            'error - no reg function' - table not registered.
    """
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
            """Process the server timestamp response."""

            def _on_open_param(trans, db):
                """Check local timestamp against server timestamp in IndexedDB."""
                nonlocal tbl
                param_get_request = db.get("time_sync_" + tbl)

                def _on_param_error(event):
                    """No local timestamp yet - store and trigger sync."""
                    rec[2](fun)
                    db.add({"key": "time_sync_" + tbl, "value": time})

                def _on_param_success(event):
                    """Compare timestamps and update if server is newer."""
                    nonlocal param_get_request, db, time, rec, fun, tbl
                    param = param_get_request.result
                    if param:
                        time2 = param.value
                        if time2 < time:
                            # Server has newer data - update local timestamp
                            # and trigger the sync function
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
                        # No local timestamp - store and trigger sync
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

            # Parse the server response to extract the timestamp
            x = JSON.parse(responseText)
            time = x["TIME"]
            get_table("param", _on_open_param, False)

        def _on_request_init(request):
            """Configure a 2-second timeout for the sync request."""

            def _on_timeout(self, event):
                nonlocal fun
                fun("timeout")

            with contextlib.suppress(Exception):
                request.timeout = 2000
            request.ontimeout = _on_timeout

        ajax_get(rec[1], complete, _on_request_init)
    else:
        fun("offline")


window.sync_and_run = sync_and_run
