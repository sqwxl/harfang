<div align="center">

![Snowy owl emoji](static/images/harfang_emoji-sm.png)

# Harfang

A social media posting and discussion site with a focus on simplicity and accessibility.\
Inspired by Hacker News and Reddit.\
Built with Django, HTMX, Hyperscript & Tailwind CSS

</div>

Features so far:

- Posts ("Top" and "Latest" views)
- Threaded comment system (i.e. nested comments)
- Votes and points system for posts and comments
- User profiles
- Internationalization

Next up:

- Admin operations (moderation)
- Public API (for bot accounts)
- Optimize accessibility
- Search
- Media Posts
- Gracefully degrades for JS-less clients
- User DMs/Chat
- Host an MVP
- SEO (w/ microdata?)
- Email system
- Dark/Light color-schemes
- Site identity (icons, logos, etc)

## Dev Quick Start

"[`just`](https://github.com/casey/just)" use the taskrunner.\
Or take a look inside [the justfile](justfile) to see the actual commands.

```shell
# install requirements
just setup
# create mock data
just populate
# run the dev server
just serve
# If you're editing styles, the tailwind binary can watch for changes
just css
```

### Reproducible Dev Environment

To ensure consistency, you can optionally use [`devenv`](https://devenv.sh/getting-started/)
and [`direnv`](https://devenv.sh/automatic-shell-activation/).
