# A [Hacker News](https://news.ycombinator.com/) clone

Built with Django, [htmx](https://htmx.org/), [alpine.js](https://alpinejs.dev/) and Tailwind CSS.

Uses SQLite for storage.

Optional dev environment set up with [nix](https://nixos.org/) (via [devenv](https://devenv.sh/getting-started/)) to ensure reproducibility across machines.

## Nix Quick Start

install [nix](https://nixos.org/download.html#download-nix)

install [direnv](https://direnv.net/docs/installation.html#from-system-packages) with the shell hook.

install [devenv](https://devenv.sh/getting-started/)

clone the repo and `direnv allow` in the directory.

## Dev Setup

```shell
# install requirements
just setup
# create mock data
just populate 
# run the dev server
just serve 
```

if you're editing styles, run the following in another terminal:

```shell
# run tailwind binary to watch for changes & update the output.css
just css
```
