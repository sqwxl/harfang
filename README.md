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
- Admin operations (content moderation)

Next up:

- Public API (for bot accounts)
- Extensive tests
- Optimized accessibility
- Search
- Media Posts
- Markdown syntax for posts
- User DMs
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
just runserver
```

### Reproducible Dev Environment

To ensure consistency, you can optionally use [`devenv`](https://devenv.sh/getting-started/)
and [`direnv`](https://devenv.sh/automatic-shell-activation/).
