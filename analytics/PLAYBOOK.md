# Good News Globe — growth playbook

Every autoposter run reads this before picking stories and writing hooks. The growth-coach run rewrites it
twice a week from `analytics/posts.csv` and `analytics/REPORT.md`. Rules carry a confidence level, because the
sample is still small; a rule is only dropped when new data contradicts it.

_Last updated: 2026-10-07 (data: 10 Reels, 13 carousels, 2026-09-30 → 2026-10-05; no new Reel data since)._

## What the numbers say
- **Reels are the growth channel.** Reels averaged 56 reach; carousels averaged 2.5. Followers are still at 2,
  so carousels reach almost no one. Every edition is built around its Reel; carousels go out once a day (evening).
- **Reel reach is falling:** 114 → 104 → 101 → 76 → 55 → 37 over Oct 2–4, then Instagram blocked publishing.
  Average watch time fell with it (4.7 s → 1.9 s). Two causes fit the data: weaker opening lines, and posting
  6+ times a day from a new account. Both are now addressed (stronger hooks, fewer automated posts).
- **What held viewers longest** (avg watch 3.6–4.8 s):
  - "Moth swarms are back after a 99.5% crash" (114 reach, 4.8 s)
  - "A 'lost' bird was filmed for the 1st time ever" (104, 4.7 s)
  - "Tiny cave crocs filmed hunting bats for the 1st time" (101, 3.6 s)
  - "Archaeologists may have found Aristotle's classroom" (42, 3.8 s)
- **What lost viewers fastest** (1.9–2.3 s): "A gorilla saved from traffickers is now a mum in the wild",
  "These lemurs sing using an opera singer's trick". Pleasant, but no hard number, nothing "first", no stakes.
- **Only one Reel got shares (5):** "🌍 4 good things happening in the world right now." A roundup gives people
  a reason to send it on.

## Hook rules (Reel frame 1 = `reel_hook`, also guides `cover_hook`)
1. **Lead with a hard fact in the first 3 words:** a number, "1st time", a record, or a time span
   ("99.5% crash", "lost for 154 years", "1st time ever"). _Confidence: medium (4 of 4 top Reels; 0 of 2 bottom)._
2. **Stakes over charm.** Comeback, discovery, rescue or record beats "cute behaviour". _Confidence: medium._
3. **4–8 words, no setup.** The viewer must get it in under 1.5 s (frame 1 shows for 1.8 s).
4. **Say what they'll see.** Pair the hook with a photo of the real subject; a hook about an animal needs that animal.
5. **Never a question, never "you won't believe".** Never exaggerate; the number must be in the article.
6. **The highlight (gold) goes on the number or the "first".**

## Story selection
- Story #1 (the Reel) must have **buzz**: it is already spreading (top of r/UpliftingNews or r/science that day,
  covered by 3+ outlets, or trending on Google News), *and* it has a hard number or a "first".
- Best categories so far: nature/animals with a number, "lost/rediscovered", comebacks, ancient finds. Weakest:
  energy (avg score 50). _Confidence: low._
- Global spread still matters, but buzz comes first for story #1.

## Experiments to run next (one at a time, note the result here)
- [ ] Hook in the safe zone and no "Watch to the end" tag (shipped 2026-10-06). Watch: avg watch time up from ~2–3 s?
- [ ] 8.4 s Reel instead of ~10 s (shipped 2026-10-06). Watch: avg watch ÷ length (completion) up?
- [ ] A weekly "4 good things this week" roundup Reel (the only format that got shares). Try on Sunday.
- [ ] Evening-only carousel (shipped 2026-10-06). Watch: does Reel reach recover once the block lifts?

## Changelog
- 2026-10-07: no new Reel insights since 10-04 (Instagram blocked publishing 10-05 → 10-07), so no rule changes. Posting note, not engagement data: on 10-07 the evening Reel was accepted (1st since 10-04) while the carousel posted a minute later was blocked again (error 2207051). Its reach will be the first test of the new hook layout and 8.4 s length.
- 2026-10-06: first version, from 10 Reels and 13 carousels.
