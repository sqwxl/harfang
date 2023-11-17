<div align="center">

# 🪶 Harfang

A social network/forum inspired by Hacker News and Reddit.\
Built with Django, HTMX, Alpine.js, Tailwind CSS

</div>

Features so far:

- Posts ("Top" and "Latest" views)
- Threaded comment system (i.e. nested comments)
- Votes and points system for posts and comments
- User profiles
- Admin operations (moderation)

Next up:

- Public API (for bot accounts)
- Optimize accessibility
- Media Posts
- User DMs/Chat
- Host an MVP
- Email system

## Dev Quick Start

Use [`just`](https://github.com/casey/just).\
If you don't feel like installing it, you can take a look inside the [justfile](justfile) to see what commands you should run)

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

## Nix Quick Start

Optional dev environment set up with [`nix`](https://nixos.org/) (via `devenv`) to ensure reproducibility across machines.

install [`devenv`](https://devenv.sh/getting-started/)

install [`direnv`](https://devenv.sh/automatic-shell-activation/) with the shell hook

clone the repo and run `direnv allow` in the directory to enable automatic shell (and virtualenv) activation
