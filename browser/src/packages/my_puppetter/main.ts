import { launch } from 'puppeteer'
import { PuppeteerLaunchOptions, Browser } from 'puppeteer/lib/types'
import { createInterface } from 'readline'

const readline = createInterface({ input: process.stdin, output: process.stdout });

class MyPuppeteer {

  browser: Browser
  webSocket: (string | null) = null

  constructor(browser: Browser) {
    this.browser = browser
  }

  static async launch(args: string[]): Promise<Browser> {
    // TODO: Add Flags https://github.com/GoogleChrome/chrome-launcher/blob/master/docs/chrome-flags-for-tools.md
    let parameters: PuppeteerLaunchOptions = { headless: true }
    // TODO: Add profile-directory
    // if (profile_dir) {
    //   args.unshift(`--profile-directory=${Path(self.get_profile_dir()).name}`)
    //   parameters.userDataDir = str(Path(this.profile_dir).parent)
    // }
    args.unshift('--no-sandbox')
    return launch({ executablePath: '/usr/bin/google-chrome', ...parameters, args })
      .then(browser => browser)
      .catch(error => {
        // if (error instanceof errors.BrowserError && !parameters.headless) {
        // TODO: Apply this logic 
        //   console.error(
        //     `Not is posible to launch the browser. Is you try to open browser in a 
        //     environment without graphical interface?`
        //   )
        // }
        debugger
        throw error
      }
      )
  }

  async get_connection(daemom: boolean): Promise<void> {
    if (!this.webSocket) { this.webSocket = this.browser.wsEndpoint() }
    if (!daemom) { return }

    readline.question('Press Enter to close browser!', _ => {
      console.log('Goodbye crack!');
      readline.close();
    });
    await this.browser.close()
  }
}

export async function new_puppetter(args: string[] = []): Promise<MyPuppeteer> {
  return new MyPuppeteer(await MyPuppeteer.launch(args))
}
