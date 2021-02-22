// @ts-check

/**
 * @typedef ChatEntry
 * @property {String} username
 * @property {String[]} badges
 * @property {String} msg
 * @property {String[]} emojis
 * @property {Boolean} is_highlighted
 * @property {String[]} links
 */

/**
 * @param {string} uri
 * @param {import(".").Config} config
 */
const main = (uri, config) => new Promise((res, rej) => {
  /**
   * @param {WebSocket} ws 
   */
  const make_watcher = ws => {
    const state = {
      last : ""
    }
    /**
     * @type {MutationCallback}
     */
    const callback = (mutations, _obs) => {
      for (const m of mutations) {
        const root           = m.target.lastChild.lastChild.parentElement
        const badges         = [...root.querySelectorAll(`.chat-badge`)].map(b => b.getAttribute("alt"))
        const username       = root.querySelector(`[data-a-target="chat-message-username"]`).textContent.trim()
        const msg            = [...root.querySelectorAll(`[data-a-target="chat-message-text"]`)].reduce((s, f) => s += f.textContent.trim(), "")
        const emojis         = [...root.querySelectorAll(`img.chat-line__message--emote`)].map(e => e.getAttribute("alt"))
        const is_highlighted = !!root.querySelector(".chat-line__message-body--highlighted")
        const links          = [...root.querySelectorAll("a.link-fragment")].map(l => l.getAttribute("href"))

        // function closure in order to ensure proper data type
        const data = JSON.stringify(
          (() => {
            /**
              * @type {ChatEntry}
              */
            const d = {
              username,
              badges,
              msg,
              emojis,
              is_highlighted,
              links
            }
            return d
          })())

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
    // Send the streamer's nickname to create a named log file
    ws.send(location.pathname.slice(1))

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