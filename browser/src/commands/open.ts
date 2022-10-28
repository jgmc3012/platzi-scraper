import {Command, Flags} from '@oclif/core'
import { new_puppetter } from '../packages/my_puppetter/main'

export default class Open extends Command {
  static description = 'Open Browser'

  static examples = [
    '<%= config.bin %> <%= command.id %>',
  ]

  static flags = {
    // flag with a value (-a, --args=VALUE)
    name: Flags.string({char: 'a', description: 'extra arguments'}),
    // flag with no value (-g, --gui)
    force: Flags.boolean({char: 'g', description: 'use a graphical user interface'}),
  }

  static args = []

  public async run(): Promise<void> {
    const {args, flags} = await this.parse(Open)

    let puppetter = await new_puppetter()
    const page = await puppetter.browser.newPage();
    await page.goto('https://platzi.com/clases/1669-pentesting/22415-instalacion-y-configuracion-de-maquinas-virtuales-/');
    await page.screenshot({path: 'google.png'});
    await puppetter.browser.close();
  }
}
