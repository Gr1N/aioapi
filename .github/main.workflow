workflow "run linters and tests" {
  on = "push"
  resolves = ["notify build succeeded"]
}

action "py3.7 linting and testing" {
  uses = "docker://python:3.7.2"
  runs = ["sh", "-c", "make ci-quality"]
}

action "notify build succeeded" {
  needs = "py3.7 linting and testing"
  uses = "docker://gr1n/the-telegram-action:master"
  env = {
    TELEGRAM_MESSAGE = "`aioapi` build succeeded"
  }
  secrets = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
  ]
}

workflow "notify about new star" {
  on = "watch"
  resolves = ["notify project starred"]
}

action "notify project starred" {
  uses = "docker://gr1n/the-telegram-action:master"
  env = {
    TELEGRAM_MESSAGE = "`aioapi` starred!"
  }
  secrets = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
  ]
}

workflow "publish" {
  on = "release"
  resolves = ["notify project published"]
}

action "py37 publish" {
  uses = "docker://python:3.7.2"
  runs = ["sh", "-c", "make ci-publish"]
  secrets = [
    "PYPI_USERNAME",
    "PYPI_PASSWORD",
  ]
}

action "notify project published" {
  uses = "docker://gr1n/the-telegram-action:master"
  needs = ["py37 publish"]
  env = {
    TELEGRAM_MESSAGE = "`aioapi` published to PyPI"
  }
  secrets = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
  ]
}
