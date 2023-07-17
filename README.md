# A [Hacker News](https://news.ycombinator.com/) clone

Built with Django, [htmx](https://htmx.org/), [alpine.js](https://alpinejs.dev/) and Tailwind CSS.

Uses SQLite

## Dev Quick Start

install nix:
```shell
sh <(curl -L https://nixos.org/nix/install) --no-daemon
```

install [direnv](https://direnv.net/docs/installation.html#from-system-packages)

install [devenv](https://devenv.sh/getting-started/)

clone the repo and `direnv allow`


```shell
# install requirements
just setup
# create mock data
just populate 
# run the dev server
just serve 
```

if you're editing styles, then, in another terminal:

```shell
# run tailwind binary to watch for changes & update the output.css
just css
```
