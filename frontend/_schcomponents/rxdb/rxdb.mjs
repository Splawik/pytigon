import { createRxDatabase, addRxPlugin } from 'rxdb/plugins/core'
import { getRxStorageDexie } from 'rxdb/plugins/storage-dexie'
import { RxDBDevModePlugin } from 'rxdb/plugins/dev-mode'

export { createRxDatabase, addRxPlugin, getRxStorageDexie, RxDBDevModePlugin }

// 1. Enable DevMode plugin (helps with schema validation and debugging)
if (process.env.NODE_ENV !== 'production') {
  addRxPlugin(RxDBDevModePlugin)
}
