# Good News Globe — growth playbook

Every autoposter run reads this before picking stories and writing hooks. The growth-coach run rewrites it
twice a week from `analytics/posts.csv` and `analytics/REPORT.md`. Rules carry a confidence level, because the
sample is still small; a rule is only dropped when new data contradicts it.

_Last updated: 2026-10-31 (data: 42 Reels, 2026-09-30 → 2026-10-31). 9 new Reels since the last update
(10-28 → 10-31 morning). 10-30 midday failed to upload (Instagram processing error); 10-31 midday and evening
are not in the data yet; 10-31 morning (~14 h old, 120 reach) is still growing and is shown but not used in
the comparisons below._

## What the numbers say
- **Followers: 2 → 2** over both the last 3 and the last 7 days (2 for all 31 days on record). Reach per Reel
  is flat-to-up, but nobody follows yet. Shares and saves are still 0 on every Reel since 10-02.
- **Reels-only still means no blocks.** Every Reel since 10-24 went out with no Instagram block; the only miss
  was one upload processing error (10-30 midday), not a block.
- **The evening slot collapsed this week (new, the clearest pattern in the data).** Last 7 days, first-run
  Reels by slot: morning 48 / 100 / 17 / 104 / 105 / 108 (avg 80), midday 103 / 99 / 80 / 33 / 115 (avg 86),
  evening 46 / 11 / 13 / 71 / 17 (avg 32, n=5). It is not the hooks: the evening losers include arc hooks
  ("25 years after it was dug up…" 11, "66M years ago…" 13) and the 17-reach bamboo Reel held 3.2 s. The
  10-25 evening weekly re-run (124) is the exception. Before 10-26 the evening slot was not weaker.
- **Last 3 days (10-28 → 10-30), 8 mature Reels:** reach 104 / 33 / 13 / 105 / 115 / 71 / 108 / 17 (avg 71);
  avg watch 4.0 / 2.2 / 1.8 / 4.8 / 2.2 / 1.7 / 1.2 / 3.2 s (avg 2.6 s, completion ~31%).
- **Last 7 days (10-24 → 10-30), 17 mature Reels:** avg reach 70, avg watch 2.4 s (completion 11–57%,
  avg ~28%). Top third by watch: "Born once every 3 years, now caught on camera" 4.8 s, cassowary re-run 4.2 s,
  "1,600 years later, Rome's colour-changing glass is back" 4.0 s, bamboo 3.2 s, Starry Night 2.2 s/lynx 2.6 s
  next. Bottom third: dolphins 0.9 s, "700,000 years ago, elephants…" 1.2 s, "25 years after it was dug up"
  1.4 s, barreleye 1.7 s, ants 1.8 s, orangutans 1.8 s.
- **"X years ago" is not an arc.** Deep-time spans with nothing coming back held least: "700,000 years ago"
  1.2 s, "66M years ago" 1.8 s (n=2). Spans that end in a return or a payoff held best: "1,600 years later,
  … is back" 4.0 s, "34 years later" 4.2 s, "Born once every 3 years, now caught on camera" 4.8 s (n=3).
- **Animals no longer clearly lead reach once slot is accounted for:** morning non-animal Reels (glass 104,
  elephant fossils 108) matched morning animal Reels (~105). The low non-animal Reels were evening ones.
- **Rarity-count hooks** ("Seen 11 times in 40 years", "Found 7 times in 65 years"): 71 reach / 1.7 s
  (evening) and 120+ / 2.8 s (morning, still growing). Middle of the pack on watch; n=2.

## Hook rules (Reel frame 1 = `reel_hook`, also guides `cover_hook`)
1. **Lead with a hard fact in the first 3 words:** a number, "1st time", a record, or a time span
   ("99.5% crash", "lost for 154 years", "7 years"). _Confidence: medium-high (needed, not enough: the Mars record
   and penguin "1st" had one and were watched least; the number-last orangutan hook was bottom third)._
   No wordplay or puns in front of the fact ("From wildfire to wild again…").
2. **Before/after beats a bare fact.** When the story honestly has it, frame it as an arc: a time span ("7 years,
   7 surgeries: …goes home", "165 years later, …") or then/now numbers ("Under 1,000 then, 183,000 now").
   _Confidence: medium-high for reach (slot now explains more of reach than hook type), medium-high for watch
   (since 10-07: 11 of 21 arc/time-span hooks ≥ 3 s vs 1 of 12 others)._ The arc must end in a payoff: something is
   back, found, born, freed or seen again ("1,600 years later, … is back", "34 years later"). A bare
   "X years ago" deep-time span is not an arc (700,000 years ago 1.2 s, 66M years ago 1.8 s).
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
  after X years, then/now numbers) for story #1. _Confidence: high (rule 2)._ If nothing buzzing has an arc,
  look one level deeper in the candidate's article for an honest time span ("first in 34 years") before settling
  for a bare count.
- **Don't lead with a bare record or a bare age** ("45 km on Mars: a record", "At 99, she…") unless it can be
  framed as an honest arc. _Confidence: low-medium (n=2: 1.5 s and 2.3 s)._
- Avoid leading with a big count about a place, project or herd ("3 million mangroves", "15,000 crossings",
  "6 new calves… to 118"). _Confidence: medium (n=3, all bottom third; dolphins 17 reach / 0.9 s)._
- A "1st ever / 1st in 100 years" discovery without a before/after: fine as stories 2–4; as #1 only when nothing
  with an arc is buzzing. _Confidence: low (penguin 1.7 s; the 10-02 "lost bird" held 4.7 s)._
- Best categories so far: nature/animals with a recovery arc, ancient finds with a "back after X years"
  payoff. Weakest: energy. _Confidence: low (lowered: in the morning slot non-animal Reels matched animal
  ones this week; the weak non-animal Reels were all evening)._
- An ancient find leads only with a payoff arc ("…is back", "recreated after 1,600 years"), not with its age
  ("700,000 years ago…"). _Confidence: low-medium (n=3)._
- Global spread still matters, but buzz comes first for story #1.

## Experiments to run next (one at a time, note the result here)
- [x] Hook in the safe zone, no "Watch to the end" tag (10-06). Kept; completion since then 18–55%, avg ~30%.
- [x] 8.4 s Reel instead of ~10 s (10-06). Completion avg ~30% vs ~35% before; inconclusive. Keep.
- [x] Evening-only carousel (10-06). Result: 7 of 7 carousels were followed by a 48 h block.
      Recommendation for the user: Reels only, or let a carousel block pause carousels only (user decision,
      not changed here).
- [ ] A weekly "4 good things this week" roundup Reel (the only format that got shares). Not run yet: the
      10-11 weekly was held by the cooldown and the 10-18 weekly Reel was built on one story (tortoises).
- [x] Living-subject Reel #1 (10-10). Target ≥ 3.5 s not met (3.1 / 1.8 / 1.7 s). Closed.
- [x] Time-span before/after hook on Reel #1 (10-14). Target avg ≥ 3 s met; now 6 of 7 since 10-07. Rule 2.
- [ ] Then/now numbers vs time span alone in frame 1. So far then/now 4.7 / 2.9 s (avg 3.8, n=2) vs time span
      3.0 / 3.7 / 4.3 / 3.1 / 4.1 s (avg 3.6, n=5). No ≥ 1 s lead; keep both, keep tracking.
- [x] Re-run the week's best-watched arc Reel story as the Sunday weekly Reel #1. Result over 2 weeks:
      tortoises 35 → 100 (2.9x), cassowary 104 → 124 (1.2x). Avg ~2x but only 1 of 2 hit 2x. Keep doing it
      (it never lost reach and the re-run held 4.2 s), but it is not a reach multiplier on its own.
- [x] Exact time span vs vague "100+ / 25+ years" in frame 1. Result: no vague hooks ran this week (exact was
      used whenever the article had it); exact spans held 1.2–4.8 s (avg 2.5 s, n=8) vs vague 1.9 / 2.6 s
      (n=2). No ≥ 1 s lead: exactness alone is not what holds viewers, the payoff is (see rule 2). Closed;
      still prefer exact numbers because they are more accurate.
- [ ] Follow prompt in the Reel caption's first line ("Follow for 3 good-news wins a day"), running since
      10-29 morning. Interim: 8 Reels posted, followers 2 → 2. Keep to the full week (through 11-04); target: any
      follower gain.
- [ ] Payoff verb in frame 1: when story #1 honestly has one, put the payoff word ("is back", "returns",
      "freed", "born", "seen again") inside the first 6 words. Target over the next 5 Reels: avg watch
      ≥ 3.2 s (this week's arc hooks with a payoff avg 4.3 s, n=3; all Reels 2.4 s).

## Changelog
- 2026-10-31: 9 new Reels (10-28 → 10-31 morning), 0 blocks. Biggest finding: the evening slot fell to avg 32 reach over 5 Reels vs ~80–86 for morning and midday, across all hook types (recommended to the user; schedule not changed here). Rule 2 now requires a payoff ("…is back", "…later, found") and says a bare "X years ago" is not an arc; animal-category note lowered to low; exact-vs-vague experiment closed (no ≥ 1 s lead); follow-prompt experiment interim 0 followers; new experiment: payoff verb in frame 1. Followers still 2.
- 2026-10-28: 11 new Reels (10-25 → 10-28), first full week of Reels only and 0 Instagram blocks. Arc hooks led reach (avg 96 vs 47); rule 2 split into high for reach, medium-high for watch (only 2 of 6 arc hooks ≥ 3 s this week); rule 1 raised to medium-high and "no puns before the fact" added; "big count" note raised to medium (dolphins 17 / 0.9 s); weekly re-run experiment closed (2.9x, 1.2x); new experiments: exact vs vague time span, follow prompt in caption. Followers still 2.
- 2026-10-24: 1 new Reel (10-22 evening, cassowary "34 years later…" 104 reach / 4.1 s); 10-23 → 10-24 held by the cooldown after carousel block 7. Before/after rule raised to high (7 of 8 arc hooks ≥ 3 s); added "dig for an honest time span" to story #1 selection; dropped the evening-slot note (evening Reel had the week's top reach). Followers still 2.
- 2026-10-21: 4 new Reels (10-18 ×3, 10-20 evening); 10-19 → 10-22 held by cooldowns after carousel blocks 5 and 6. Before/after rule raised to medium-high (6 of 7 arc hooks ≥ 3 s vs 1.8 s avg for others); added a low-medium "don't lead with a bare record or age" note (Mars 1.5 s, wing-walker 2.3 s); new experiment: re-run the week's best arc story as the weekly Reel (tortoises 35 → 100). Followers still 2.
- 2026-10-17: 3 new Reels (all 10-15); 10-16 → 10-17 held by the cooldown after the 4th carousel block. Time-span/before-after experiment met its target (3.7 s, 4.7 s vs 1.7 s) → promoted to hook rule 2 (medium) and to story #1 selection; dropped the evening-slot lead (10-15 evening lowest reach); added low-confidence note on bare "1st" hooks; new then/now experiment. Followers still 2.
- 2026-10-14: 3 new Reels measured (10-10 midday/evening, 10-12 evening); 10-11 → 10-14 held by the cooldown after the 3rd carousel block. Replaced the "living subject" note with a low-confidence "time span + before/after" rule, added "avoid big counts about a place/project", noted the evening-slot lead, closed the living-subject experiment (target not met). Followers still 2.
- 2026-10-10: 3 new Reels measured (10-07 eve, 10-09 eve, 10-10 morning). Rule 1 raised to medium-high (lava Reel 102 reach); added low-confidence "living subject" note; recorded the 10-06 experiments (inconclusive) and that carousels triggered both blocks. Followers still 2.
- 2026-10-07: no new Reel insights since 10-04 (Instagram blocked publishing 10-05 → 10-07), so no rule changes. Posting note, not engagement data: on 10-07 the evening Reel was accepted (1st since 10-04) while the carousel posted a minute later was blocked again (error 2207051). Its reach will be the first test of the new hook layout and 8.4 s length.
- 2026-10-06: first version, from 10 Reels and 13 carousels.
