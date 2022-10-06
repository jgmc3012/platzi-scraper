oclif-hello-world
=================

oclif example Hello World CLI

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/oclif-hello-world.svg)](https://npmjs.org/package/oclif-hello-world)
[![CircleCI](https://circleci.com/gh/oclif/hello-world/tree/main.svg?style=shield)](https://circleci.com/gh/oclif/hello-world/tree/main)
[![Downloads/week](https://img.shields.io/npm/dw/oclif-hello-world.svg)](https://npmjs.org/package/oclif-hello-world)
[![License](https://img.shields.io/npm/l/oclif-hello-world.svg)](https://github.com/oclif/hello-world/blob/main/package.json)

<!-- toc -->
* [Usage](#usage)
* [Commands](#commands)
<!-- tocstop -->
# Usage
<!-- usage -->
```sh-session
$ npm install -g platzi-scraper
$ pltz-scraper COMMAND
running command...
$ pltz-scraper (--version)
platzi-scraper/0.0.0 linux-x64 node-v16.17.0
$ pltz-scraper --help [COMMAND]
USAGE
  $ pltz-scraper COMMAND
...
```
<!-- usagestop -->
# Commands
<!-- commands -->
* [`pltz-scraper hello PERSON`](#pltz-scraper-hello-person)
* [`pltz-scraper hello world`](#pltz-scraper-hello-world)
* [`pltz-scraper help [COMMAND]`](#pltz-scraper-help-command)
* [`pltz-scraper plugins`](#pltz-scraper-plugins)
* [`pltz-scraper plugins:install PLUGIN...`](#pltz-scraper-pluginsinstall-plugin)
* [`pltz-scraper plugins:inspect PLUGIN...`](#pltz-scraper-pluginsinspect-plugin)
* [`pltz-scraper plugins:install PLUGIN...`](#pltz-scraper-pluginsinstall-plugin-1)
* [`pltz-scraper plugins:link PLUGIN`](#pltz-scraper-pluginslink-plugin)
* [`pltz-scraper plugins:uninstall PLUGIN...`](#pltz-scraper-pluginsuninstall-plugin)
* [`pltz-scraper plugins:uninstall PLUGIN...`](#pltz-scraper-pluginsuninstall-plugin-1)
* [`pltz-scraper plugins:uninstall PLUGIN...`](#pltz-scraper-pluginsuninstall-plugin-2)
* [`pltz-scraper plugins update`](#pltz-scraper-plugins-update)

## `pltz-scraper hello PERSON`

Say hello

```
USAGE
  $ pltz-scraper hello [PERSON] -f <value>

ARGUMENTS
  PERSON  Person to say hello to

FLAGS
  -f, --from=<value>  (required) Who is saying hello

DESCRIPTION
  Say hello

EXAMPLES
  $ oex hello friend --from oclif
  hello friend from oclif! (./src/commands/hello/index.ts)
```

_See code: [dist/commands/hello/index.ts](https://github.com/jmillandev/platzi-scraper/blob/v0.0.0/dist/commands/hello/index.ts)_

## `pltz-scraper hello world`

Say hello world

```
USAGE
  $ pltz-scraper hello world

DESCRIPTION
  Say hello world

EXAMPLES
  $ pltz-scraper hello world
  hello world! (./src/commands/hello/world.ts)
```

## `pltz-scraper help [COMMAND]`

Display help for pltz-scraper.

```
USAGE
  $ pltz-scraper help [COMMAND] [-n]

ARGUMENTS
  COMMAND  Command to show help for.

FLAGS
  -n, --nested-commands  Include all nested commands in the output.

DESCRIPTION
  Display help for pltz-scraper.
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v5.1.14/src/commands/help.ts)_

## `pltz-scraper plugins`

List installed plugins.

```
USAGE
  $ pltz-scraper plugins [--core]

FLAGS
  --core  Show core plugins.

DESCRIPTION
  List installed plugins.

EXAMPLES
  $ pltz-scraper plugins
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v2.1.1/src/commands/plugins/index.ts)_

## `pltz-scraper plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ pltz-scraper plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.

  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.

ALIASES
  $ pltz-scraper plugins add

EXAMPLES
  $ pltz-scraper plugins:install myplugin 

  $ pltz-scraper plugins:install https://github.com/someuser/someplugin

  $ pltz-scraper plugins:install someuser/someplugin
```

## `pltz-scraper plugins:inspect PLUGIN...`

Displays installation properties of a plugin.

```
USAGE
  $ pltz-scraper plugins:inspect PLUGIN...

ARGUMENTS
  PLUGIN  [default: .] Plugin to inspect.

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Displays installation properties of a plugin.

EXAMPLES
  $ pltz-scraper plugins:inspect myplugin
```

## `pltz-scraper plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ pltz-scraper plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.

  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.

ALIASES
  $ pltz-scraper plugins add

EXAMPLES
  $ pltz-scraper plugins:install myplugin 

  $ pltz-scraper plugins:install https://github.com/someuser/someplugin

  $ pltz-scraper plugins:install someuser/someplugin
```

## `pltz-scraper plugins:link PLUGIN`

Links a plugin into the CLI for development.

```
USAGE
  $ pltz-scraper plugins:link PLUGIN

ARGUMENTS
  PATH  [default: .] path to plugin

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Links a plugin into the CLI for development.

  Installation of a linked plugin will override a user-installed or core plugin.

  e.g. If you have a user-installed or core plugin that has a 'hello' command, installing a linked plugin with a 'hello'
  command will override the user-installed or core plugin implementation. This is useful for development work.

EXAMPLES
  $ pltz-scraper plugins:link myplugin
```

## `pltz-scraper plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ pltz-scraper plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ pltz-scraper plugins unlink
  $ pltz-scraper plugins remove
```

## `pltz-scraper plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ pltz-scraper plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ pltz-scraper plugins unlink
  $ pltz-scraper plugins remove
```

## `pltz-scraper plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ pltz-scraper plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ pltz-scraper plugins unlink
  $ pltz-scraper plugins remove
```

## `pltz-scraper plugins update`

Update installed plugins.

```
USAGE
  $ pltz-scraper plugins update [-h] [-v]

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Update installed plugins.
```
<!-- commandsstop -->
