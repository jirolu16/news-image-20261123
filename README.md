# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/jirolu16/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/jirolu16/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

**The Strike at Benghazi.** One square page that tries to hold the whole of Monday 23 November 2026: a newspaper front page, drawn rather than photographed, for the make.fun one-day news-image contest. The date sits in red under the masthead, because the picture is meant to be read as that day and no other.

## The lead story

Kyiv confirmed on the Monday that seven Ukrainian naval drones had sunk the Russian corvette *Merkury* and damaged a Russian cargo ship in the port of Benghazi, Libya, roughly 1,500 miles from the front lines: the longest-range naval strike Ukraine has carried out in the war. The Kremlin's answer was to call it terrorist activity. The lead block gives the story a tinted panel of its own, with a small drawn motif of harbour water, a pale corvette sitting low, and three little drones running in at it.

## Around the lead

Four panels share the middle of the page:

- **Brussels.** NATO's North Atlantic Council sat in emergency session after three Russian Kh-101 cruise missiles came down in Poland during Friday's mass attack on Ukraine; Warsaw asked for stronger air defences on the eastern flank, and nobody in Poland was hurt.
- **Washington.** House Democrats locked in at least 258 seats as the last midterm results were confirmed, their biggest House majority since 1992, and started preparing oversight of the Trump administration.
- **New York.** Stock futures climbed about 2% early on Monday, bouncing after the AI sell-off handed the Nasdaq its worst week since March 2020, with the S&P 500 still more than 10% under its October record.
- **Seoul.** A surprise reshuffle from President Lee Jae Myung nominated former justice minister Kang Kum-sil to run the National Intelligence Service, which would make her South Korea's first woman spy chief.

Below them, a full-width panel covers Jakarta: President Prabowo Subianto came to the parliament complex in Senayan to hand the MPR two vice-presidential candidates, Andi Amran Sulaiman and Sugiono, ahead of the assembly's vote on 11 December. A black strip along the bottom, headed ALSO THAT DAY, carries four one-line briefs: Iran's vow against the US naval blockade on day 130, Jakarta stocks rising 1.59% as MSCI softened on a downgrade, Alcaraz beating Zverev in Turin for his first ATP Finals title, and the safety audit ordered for every factory in Serang after the Cikande fire.

## How the page is built

Three files do the work:

- `news.md` is the research record: every story that appears on the page, the wording chosen for it, and the sources it was checked against.
- `draw.py` renders the front page with Pillow: masthead, tinted lead block with its harbour motif, four panels, the wide Jakarta panel and the briefs strip, all laid out on a 1024 by 1024 page with hard assertions that no text overflows its box.
- `main.ts` is the entrypoint the grader runs. It copies the finished `entry.png` into the output directory (`MAKEFUN_OUTPUT_DIR`, or `/output` when the variable is unset), creating the directory if needed and checking the copy's size against the original before it reports success.

Nothing on the page is a photograph or a downloaded asset; every mark on it was drawn by `draw.py`.

## Sources and checking

No story reached the page on a single report. Each one was confirmed in at least two independent outlets before it was drawn, and `news.md` names them story by story: wire copy from AP and Reuters, the BBC, NBC and the Guardian on the Benghazi strike, NPR and RMF24 reporting on the NATO session, Korean outlets including the Korea JoongAng Daily and Yonhap on the Seoul reshuffle, and Indonesian reporting from Batavia News and RI News on the Jakarta panel, among others.

Two judgement calls are recorded in `news.md` as well. Stories from the Sunday were left off the page even when Monday commentary was still running hard on them, and a much-discussed mathematics story was dropped once its dates turned out to be 20 and 21 November rather than the Monday. The one follow-up that did stay, the Cikande safety audit, is a new decision taken on the Monday itself, and the page draws it as a follow-up rather than as fresh news.

## Run it

```sh
node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=77d34c9m&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
