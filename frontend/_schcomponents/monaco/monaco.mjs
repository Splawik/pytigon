import { monaco, loadCss } from 'monaco-esm'
import { initMonaco } from 'monaco-esm'
import editorWorker from 'monaco-esm/workers/editor'
import htmlWorker from 'monaco-esm/workers/html'
import cssWorker from 'monaco-esm/workers/css'

export function load_monaco (editor_element, params) {
  initMonaco({
    workers: {
      editor: editorWorker,
      html: htmlWorker,
      css: cssWorker
    }
  })

  //loadCss()

  return monaco.editor.create(editor_element, params)
}
