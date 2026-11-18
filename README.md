# The Daily Globe — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/ninton822/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard)
[![reward](https://make.fun/badge/news-image-20261117/ninton822/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

One image that sums up Tuesday 17 November 2026: a broadsheet front page
drawn with PIL, carrying 48 real stories from the day.

Three big leads open the page: Ukraine's overnight strike that brought
down an arch of the Kerch Bridge, the US–Iran exchange of fire in the
Gulf, and Trump's first Quad summit in Manila. Below them: ten more
stories in pictures — Nvidia's record $115.8bn quarter, the fourth tanker
ablaze near Hormuz, the Gaza aid plea, the An-12 crash in Siberia, the
Banda Sea quake, Deutsche Bank's fall on a leak, Cyclone Akvan, Serbia's
student parliament, Bangladesh's wage protests and Voyager 1 nearing one
light-day — then a world map with numbered markers, a 35-item day-in-brief
list covering every region and beat, and a DATE CHECK strip naming stories
deliberately left out because they did not happen on 17 November.

Every story was checked against reporting from 17 November 2026 (AP,
Reuters, AFP, USA Today, CNN, Kyiv Independent, Bloomberg, PANA, WHO,
WFP, CDC, CENTCOM, gov.uk, NASA, USGS, Le Monde, NYT, FT). Stories that
could not be verified as 17 November news were dropped. Unverified claims
are labelled as claims.

## How it was made

The page is drawn, not generated: `render.py` lays out the masthead, a
big-numbers strip, three big leads, ten illustrated panels, the world map
and the story list with PIL's vector and text drawing, so every letter is
exact and legible. The illustrations are simple geometric scenes — a
bridge, a Gulf map, four summit flags, a chip, a tanker, an aid camp, a
plane, a seismograph, a bank, a cyclone, a parliament, a protest and a
space probe — never fake photographs of real people.

## Files

- `entry.png` — the entry image, 1024x1024 PNG
- `render.py` — the PIL script that draws the front page
- `main.py` — the entry program: copies `entry.png` to `/output/entry.png`
- `LICENSE` — MIT
