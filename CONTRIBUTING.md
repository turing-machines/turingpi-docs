# Suggesting a fix

Found a mistake or something out of date on docs.turingpi.com? Thank you for fixing it!

1. On the page, click **Suggest an edit** at the bottom.
2. GitHub opens the page source in its editor. If you don't have write access, GitHub offers to fork the repository; accept it.
3. Make the change and click **Commit changes…** / **Propose changes**, then **Create pull request**. Add a line saying what was wrong.

A maintainer reviews the pull request. Once it's merged, the site updates within a few minutes.

## Format tips

Pages are Markdown. A few things specific to this site:

- Callouts:

  ```md
  :::note[Optional title]
  Text
  :::
  ```

  Types: `note`, `tip`, `caution`, `danger`.
- Links to other pages: `/docs/<page-slug>`, e.g. `[BMC UI](/docs/turing-pi2-bmc-ui)`.
- Images live in `src/assets/img/`. To add a screenshot, upload it there and reference it as `![](../../../assets/img/name.png)`.

Bigger changes (new pages, restructuring)? Open an issue first so we can agree on the approach.
