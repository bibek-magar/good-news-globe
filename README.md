# Good News Globe — Instagram auto-poster

Carousels for [@good_newsglobe](https://instagram.com/good_newsglobe) are rendered by scheduled Claude runs and pushed here as `posts/<date>-<edition>/01.jpg…06.jpg` + `caption.txt`.

Pushing `caption.txt` (always uploaded last) triggers `.github/workflows/post.yml`, which runs `post_to_instagram.py` to publish the carousel through the Instagram Graph API. Images are served to Instagram from `raw.githubusercontent.com`, so they must be JPEG. After a successful post the workflow commits a `POSTED` marker in the folder.

Secrets: `IG_USER_ID`, `IG_ACCESS_TOKEN`. Manual re-run: Actions → "Post carousel to Instagram" → Run workflow → folder, e.g. `posts/2026-10-01-morning`.
