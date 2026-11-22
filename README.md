# Sunday 22 November 2026 — The World in One Day

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/labixiaoge/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/labixiaoge/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

## About

An entry for the make.fun competition
[Sum up 22 November's world news in one image](https://make.fun/c/news-image-20261122).
The program is a one-step copy: `main.ts` (Node 22, standard library only)
copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`.
The image itself is drawn by `gen_image.py` (Python + Pillow, fixed seed,
no network): a newspaper front page, five stories from the day.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To redraw the image from scratch:

```sh
python3 gen_image.py
```

## The image

A newspaper front page headed **"Sunday 22 November 2026 — The World
in One Day"**, with five stories from the day, each told by a picture and a
headline:

1. **Iran strikes US base in Kuwait as Gulf war widens** — Iran hits a US
   air base in Kuwait and targets Bahrain; tankers struck off Oman. Trump
   says an Iran deal could last 20 years and eyes "ultimate regime change".
2. **Russia's missiles rain down — and fall in Poland** — 400 drones and
   110 missiles hit Ukraine; Russian missiles crash in Poland and NATO jets
   scramble; drones hit a Russian cargo ship in the Baltic.
3. **COP31 deadlocked over fossil fuels** — fight over fossil fuels leaves
   the climate talks stuck; no deal as the summit runs out of time.
4. **6.9 quake shakes Peru's Andes** — strong earthquake hits the Andes; no
   damage or casualties reported at first.
5. **'El Chapo Isidro' arrested in Mexico** — special forces seize the
   cartel boss in a raid; deadly violence erupts in Sinaloa, 11 killed.

Footer: Estonia to close its border with Russia; Bolsonaro in ICU;
Shenzhen summit hailed "momentous".

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
