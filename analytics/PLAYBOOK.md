# Good News Globe — growth playbook

Every autoposter run reads this before picking stories and writing hooks. The growth-coach run rewrites it
twice a week from `analytics/posts.csv` and `analytics/REPORT.md`. Rules carry a confidence level, because the
sample is still small; a rule is only dropped when new data contradicts it.

_Last updated: 2026-10-21 (data: 23 Reels, 2026-09-30 → 2026-10-20). 4 new Reels since the last update
(10-18 ×3, 10-20 evening). 10-19 → 10-22 editions are held by the cooldowns after the 5th and 6th carousel
blocks (10-18 weekly, 10-20 evening); hand-posted editions are not in the data._

## What the numbers say
- **Reels are the growth channel.** Reels average ~55 reach; carousels ~2. Followers: 2 → 2 this week, and
  2 for all 22 days on record. Nothing has converted viewers into followers yet.
- **Last 3 days (10-18 → 10-21):** 4 Reels. "Under 1,000 then, 183,000 giant tortoises now" (weekly re-run)
  100 reach / 2.9 s (35%); "At 99, she rode on top of a flying plane" 54 / 2.3 s (27%); "165 years later, a bike
  beat the Pony Express" 44 / 3.1 s (37%); "45 km on Mars: a new off-world driving record" 37 / 1.5 s (18%).
- **Last 7 days (10-14 → 10-21), 7 Reels:** reach 100 / 67 / 55 / 54 / 44 / 37 / 35 (avg 56); avg watch
  1.5–4.7 s (completion 18–55%, avg 33%).
- **Top third by watch time** (4.7 s tortoises, 3.7 s sea turtle, 3.1 s Pony Express) are again all
  **before/after hooks with a time span or then/now numbers**. Bottom third (1.5 s Mars record, 1.7 s penguin
  "1st", 2.3 s wing-walker age) have a number, a "1st" or a record, but no arc. Since 10-07 (8.4 s Reels):
  before/after hooks 6 of 7 held ≥ 3 s, avg 3.6 s (n=7); all others avg 1.8 s, 0 of 7 reached 2.5 s (n=7).
- **A bare record is the weakest #1 so far:** "45 km on Mars… record" 1.5 s, tied for the lowest watch on record.
- **The same hook can reach 3x more on a second run:** tortoises reached 35 (10-15 evening) and 100 as the
  10-18 weekly Reel. n=1, but it is the clearest reach signal we have; reach is still mostly distribution luck.
- **Slot:** 7-day reach by slot: morning 67 / 54, midday 55 / 44, evening 35 / 37, weekly 100. No slot rule; n is
  too small, but evening Reels have been lowest twice in a row.
- **Shares and saves are still ~0 on Reels** (1 save this week: Pony Express). The only Reel shares ever (5) came
  from the 09-30 "4 good things" roundup.
- **Carousels trigger Instagram blocks: now 6 of 6** (10-07, 10-10, 10-12, 10-15, 10-18 weekly, 10-20 evening).
  Each one stopped all posting for 48 h; since 10-07 that cost roughly half of all editions. It is still the
  main reason reach and followers stalled. Carousels themselves reach ~2.

## Hook rules (Reel frame 1 = `reel_hook`, also guides `cover_hook`)
1. **Lead with a hard fact in the first 3 words:** a number, "1st time", a record, or a time span
   ("99.5% crash", "lost for 154 years", "7 years"). _Confidence: medium (needed, not enough: the Mars record
   and penguin "1st" both had one and were watched least)._
2. **Before/after beats a bare fact.** When the story honestly has it, frame it as an arc: a time span ("7 years,
   7 surgeries: …goes home", "165 years later, …") or then/now numbers ("Under 1,000 then, 183,000 now").
   _Confidence: medium-high (since 10-07: 6 of 7 arc hooks held ≥ 3 s, avg 3.6 s, vs avg 1.8 s for 7 others)._
   Never invent an arc the article does not give; if there is none, use rule 1.
3. **Stakes over charm.** Comeback, rescue, discovery or record beats "cute behaviour". _Confidence: medium._
   A living subject alone does not hold viewers (orangutans 1.8 s); the arc does.
4. **4–8 words, no setup.** The viewer must get it in under 1.5 s (frame 1 shows for 1.8 s).
5. **Say what they'll see.** Pair the hook with a photo of the real subject; a hook about an animal needs that animal.
6. **Never a question, never "you won't believe".** Never exaggerate; the number must be in the article.
7. **The highlight (gold) goes on the number, the time span or the "first".**

## Story selection
- Story #1 (the Reel) must have **buzz**: it is already spreading (top of r/UpliftingNews or r/science that day,
  covered by 3+ outlets, or trending on Google News), *and* it has a hard number or a "first".
- Among buzzing candidates, **prefer the one with an honest before/after arc** (recovery, homecoming, comeback
  after X years, then/now numbers) for story #1. _Confidence: medium-high (rule 2)._
- **Don't lead with a bare record or a bare age** ("45 km on Mars: a record", "At 99, she…") unless it can be
  framed as an honest arc. _Confidence: low-medium (n=2: 1.5 s and 2.3 s)._
- Avoid leading with a big count about a place or project ("3 million mangroves", "15,000 crossings").
  _Confidence: low-medium (n=2, both bottom third)._
- A "1st ever / 1st in 100 years" discovery without a before/after: fine as stories 2–4; as #1 only when nothing
  with an arc is buzzing. _Confidence: low (penguin 1.7 s; the 10-02 "lost bird" held 4.7 s)._
- Best categories so far: nature/animals with a recovery arc, ancient finds. Weakest: energy. _Confidence: low._
- Global spread still matters, but buzz comes first for story #1.

## Experiments to run next (one at a time, note the result here)
- [x] Hook in the safe zone, no "Watch to the end" tag (10-06). Kept; completion since then 18–55%, avg ~30%.
- [x] 8.4 s Reel instead of ~10 s (10-06). Completion avg ~30% vs ~35% before; inconclusive. Keep.
- [x] Evening-only carousel (10-06). Result: 6 of 6 carousels were followed by a 48 h block.
      Recommendation for the user: Reels only, or let a carousel block pause carousels only (user decision,
      not changed here).
- [ ] A weekly "4 good things this week" roundup Reel (the only format that got shares). Not run yet: the
      10-11 weekly was held by the cooldown and the 10-18 weekly Reel was built on one story (tortoises).
- [x] Living-subject Reel #1 (10-10). Target ≥ 3.5 s not met (3.1 / 1.8 / 1.7 s). Closed.
- [x] Time-span before/after hook on Reel #1 (10-14). Target avg ≥ 3 s met; now 6 of 7 since 10-07. Rule 2.
- [ ] Then/now numbers vs time span alone in frame 1. So far then/now 4.7 / 2.9 s (avg 3.8, n=2) vs time span
      3.0 / 3.7 / 4.3 / 3.1 s (avg 3.5, n=4). No ≥ 1 s lead yet; keep both, keep tracking.
- [ ] Re-run the week's best-watched arc Reel story as the Sunday weekly Reel #1 (tortoises: 35 → 100 reach on
      a second run). Measure the weekly Reel's reach vs that story's first run; keep if ≥ 2x over 2 weeks.

## Changelog
- 2026-10-21: 4 new Reels (10-18 ×3, 10-20 evening); 10-19 → 10-22 held by cooldowns after carousel blocks 5 and 6. Before/after rule raised to medium-high (6 of 7 arc hooks ≥ 3 s vs 1.8 s avg for others); added a low-medium "don't lead with a bare record or age" note (Mars 1.5 s, wing-walker 2.3 s); new experiment: re-run the week's best arc story as the weekly Reel (tortoises 35 → 100). Followers still 2.
- 2026-10-17: 3 new Reels (all 10-15); 10-16 → 10-17 held by the cooldown after the 4th carousel block. Time-span/before-after experiment met its target (3.7 s, 4.7 s vs 1.7 s) → promoted to hook rule 2 (medium) and to story #1 selection; dropped the evening-slot lead (10-15 evening lowest reach); added low-confidence note on bare "1st" hooks; new then/now experiment. Followers still 2.
- 2026-10-14: 3 new Reels measured (10-10 midday/evening, 10-12 evening); 10-11 → 10-14 held by the cooldown after the 3rd carousel block. Replaced the "living subject" note with a low-confidence "time span + before/after" rule, added "avoid big counts about a place/project", noted the evening-slot lead, closed the living-subject experiment (target not met). Followers still 2.
- 2026-10-10: 3 new Reels measured (10-07 eve, 10-09 eve, 10-10 morning). Rule 1 raised to medium-high (lava Reel 102 reach); added low-confidence "living subject" note; recorded the 10-06 experiments (inconclusive) and that carousels triggered both blocks. Followers still 2.
- 2026-10-07: no new Reel insights since 10-04 (Instagram blocked publishing 10-05 → 10-07), so no rule changes. Posting note, not engagement data: on 10-07 the evening Reel was accepted (1st since 10-04) while the carousel posted a minute later was blocked again (error 2207051). Its reach will be the first test of the new hook layout and 8.4 s length.
- 2026-10-06: first version, from 10 Reels and 13 carousels.
