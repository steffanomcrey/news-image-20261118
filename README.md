# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/steffanomcrey/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/steffanomcrey/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A newspaper front page that sums up Wednesday 18 November 2026 in one image:
32 verified stories, three illustrated leads, a world map with numbered pins,
and a footer stating every story was checked against reporting published that
day. The image is drawn in code by `render.py` and shipped as `entry.png`;
`main.py` copies it to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-draw the front page (three layout variants, A/B/C):

```sh
python3 render.py A
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=7nh48qqg&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
