// @ts-check

/**
 * @param {string} uri
 * @param {import(".").Config} config
 */
const main = (uri, config) => new Promise((res, rej) => {
  /**
 * @param {WebSocket} ws 
 */
  const make_watcher = ws =>  
  /**
   * @param {MutationRecord[]} mutations
   * @param {any} _obs
   */
  {
    const state = {
      last : undefined
    }
    /**
     * @type {MutationCallback}
     */
    const callback = (mutations, _obs) => {
      for (const m of mutations) {
        let data = m.target.lastChild.textContent
        if(data === state.last) continue

        ws.send(data)
        console.dir(data)

        state.last = data
      }
    }

    return callback
  }

  const ws = new WebSocket(uri)

  ws.addEventListener("open", () => {
    const watcher = make_watcher(ws)
    const obs     = new MutationObserver(watcher)
    const target  = document.querySelector(config.target)

    obs.observe(target, {
      childList: true
    })

    ws.addEventListener("close", () => {
      console.log("disconnecting the observer")
      obs.disconnect()
      res()
    })

    ws.addEventListener("error", rej)
  })
})

module.exports = {
  main
}