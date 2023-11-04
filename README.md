<div align="center">

# Harfang 🦉

## A [Hacker News](https://news.ycombinator.com/) clone

</div>

Built with Django, [htmx](https://htmx.org/), [alpine.js](https://alpinejs.dev/) and Tailwind CSS.

Uses SQLite for storage.

## Nix Quick Start

Optional dev environment set up with [`nix`](https://nixos.org/) (via `devenv`) to ensure reproducibility across machines.

install [`devenv`](https://devenv.sh/getting-started/)

install [`direnv`](https://devenv.sh/automatic-shell-activation/) with the shell hook

clone the repo and run `direnv allow` in the directory to enable automatic shell (and virtualenv) activation

## Dev Quick Start

(if not using the devenv shell, you'll need to have [`just`](https://github.com/casey/just) to run the following convenience tasks.  
if you don't feel like installing it, you can take a look inside the `justfile` to see what commands you should run)

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
