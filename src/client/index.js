// @ts-check
const ppt = require("puppeteer")
const scraper = require('./scraper')
const fs = require('fs/promises')
const { announce_pr } = require("./helpers")

/**
 * @typedef Config
 * @property {String} host
 * @property {Number} port
 * @property {String} protocol
 * @property {Boolean} headless
 * @property {String} target
 */

/**
 * @param {ppt.Browser} b
 */
const setup_events = async (b) => {
  process.on("beforeExit", () => {
    b.close()
    console.log("Closing the scraper")
  })
}

/**
 * @param {string} path
 * @returns {Promise<Config>}
 */
const read_config = (path) => {
  /**
   * @type {Config}
   */
  const default_config = {
    host     : "0.0.0.0",
    port     : 9001,
    headless : false,
    protocol : "wss",
    target   : "[role=log]"
  }

  return fs.readFile(path, {
    encoding: 'utf-8'
  })
    .then(JSON.parse)
    .then(d => {
      for (const k in default_config) {
        if (!(k in d)) d[k] = default_config[k]
      }
      return d
    })
}

/**
 * @param {Config} cfg 
 */
const main = async (cfg) => {
  const socket_uri = `${cfg.protocol}://${cfg.host}:${cfg.port}`
  const [, , url]  = process.argv
  const browser    = await ppt.launch({
    headless : !!cfg.headless,
    args     : ["-ignore-certificate-errors"]
  })

  await setup_events(browser)

  const page = await browser.newPage()
  await page.setViewport({
    width  : 1920,
    height : 1080
  })
  await page.setUserAgent("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")
  await page.goto(url, {
    waitUntil : 'networkidle2'
  })

  await page.waitForSelector(cfg.target)
  await page.evaluate(scraper.main, socket_uri, cfg)
}

read_config("./config.json")
  .then(announce_pr)
  .then(main)