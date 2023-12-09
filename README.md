<div align="center">

![Snowy owl emoji](static/images/harfang_emoji-sm.png)

# Harfang

A social media posting and discussion site with a focus on simplicity and accessibility.\
Inspired by Hacker News and Reddit.\
Built with Django, HTMX, Hyperscript and Tailwind CSS

</div>

Features so far:

- Posts ("Top" and "Latest" views)
- Threaded comment system (i.e. nested comments)
- Votes and points system for posts and comments
- User profiles
- Internationalization
- Content moderation
- Extensive tests
- Rich link previews
- Responsive design
- Markdown syntax for posts

Next up:

- Public API (for bot accounts)
- Optimized for accessibility
- Search
- Media Posts
- DMs
- SEO (django-meta)
- Email system
- Dark/Light color-schemes
- Site identity (icons, logos, etc)
- Cookiecutter version

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

### Reproducible Dev Environment (optional)

Use nix via [`devenv`](https://devenv.sh/getting-started/) to guarantee a
consistent environment.\
Combine with [`direnv`](https://devenv.sh/automatic-shell-activation/) for
automatic shell activation.
