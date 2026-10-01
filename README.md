# Good News Globe — Instagram auto-poster

Carousels for [@good_newsglobe](https://instagram.com/good_newsglobe) are rendered by scheduled Claude runs and pushed here as `posts/<date>-<edition>/01.jpg…06.jpg` + `caption.txt`, plus `reel/r1.jpg…r4.jpg` (9:16 frames for a single-story Reel), `reel_caption.txt`, optional `first_comment.txt` and the `stories.json` they were made from.

Pushing `caption.txt` (always uploaded last) triggers `.github/workflows/post.yml`, which runs `post_to_instagram.py` to publish the carousel through the Instagram Graph API. Images are served to Instagram from `raw.githubusercontent.com`, so they must be JPEG. After a successful post the workflow commits a `POSTED` marker in the folder.

Secrets: `IG_USER_ID`, `IG_ACCESS_TOKEN`. Manual re-run: Actions → "Post carousel to Instagram" → Run workflow → folder, e.g. `posts/2026-10-01-morning`.

After the carousel, the same workflow builds `reel.mp4` with `make_reel.py` (animated single-story Reel from `reel/`, or a slideshow of the carousel if there are no Reel frames), publishes it to the Reels tab (`post_reel.py`, caption from `reel_caption.txt`) and shares it to the Story (`post_story.py`). If `first_comment.txt` exists, `post_to_instagram.py` posts it under the carousel (best effort).

## Analytics
`.github/workflows/insights.yml` runs `insights.py` daily (06:05 Nepal time). It pulls reach, shares, saves, likes and comments for the last 30 days of posts plus follower count and audience data, and commits `analytics/posts.csv`, `analytics/account.csv` and `analytics/REPORT.md`. The scheduled Claude runs read `REPORT.md` before choosing stories and hooks. Insights need the token to include the `instagram_manage_insights` permission; missing data is listed under "Problems" in the report.
