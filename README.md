# The Daily Globe — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/ninton822/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/ninton822/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

One image that sums up Tuesday 17 November 2026: a broadsheet front page
drawn with PIL, carrying 42 real stories from the day.

The lead is Ukraine's overnight strike that brought down an arch of the
Kerch Bridge, with Russia answering by hitting two bridges in Kyiv. Below
it: the US–Iran exchange of fire in the Gulf, Nvidia's record $115.8bn
quarter, Trump's Asia trip, the Gaza aid plea and the fourth tanker ablaze
near Hormuz — then a world map with numbered markers and a 36-item
day-in-brief list covering every region and beat, from Cabo Verde's
re-election to a dual-quasar discovery.

Every story was checked against reporting from 17 November 2026 (AP,
Reuters, AFP, USA Today, CNN, Kyiv Independent, Bloomberg, PANA, WHO,
WFP, ECOWAS, CDC, CENTCOM). Unverified claims are labelled as claims.

## How it was made

The page is drawn, not generated: `render.py` lays out the masthead, the
lead story, five illustrated panels, the world map and the story list with
PIL's vector and text drawing, so every letter is exact and legible. The
illustrations are simple geometric scenes — a bridge, a radar, a chip, a
summit, an aid camp, a tanker — never fake photographs of real people.

## Files

- `entry.png` — the entry image, 1024x1024 PNG
- `render.py` — the PIL script that draws the front page
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
- `LICENSE` — MIT
