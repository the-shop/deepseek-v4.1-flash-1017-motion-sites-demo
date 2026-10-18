# DeepSeek-V4.1-Flash-1017 Motion Sites Demo

Twenty one-page websites, each written by **DeepSeek-V4.1-Flash** in a single API call while prompted to act as a senior motion designer. The model output was not edited: every file in [`sites/`](sites) is exactly what came out of the model.

Open [`index.html`](index.html) for a gallery, or open any file in `sites/` directly in a browser.

## Model tested

All sites were generated on **2026-10-18** via the DeepSeek API model alias `deepseek-flash` (reported by the API as *DeepSeek-V4.1-Flash*). This was one day after DeepSeek announced **DeepSeek-V4.1-Flash-1017** as live on its website, app and API, so it is the latest Flash release at the time of testing. See X for the release:

- Release announcement: [@deepseek_ai on X](https://x.com/deepseek_ai/status/2111375640717033777)
- Open weights (Hugging Face, ModelScope): [@deepseek_ai on X](https://x.com/deepseek_ai/status/2111375653069259247)

The API response names only the alias, not a dated checkpoint, so the exact checkpoint is inferred from the release date.

## Method

- **No agent harness.** One plain `/chat/completions` request per site: the [system prompt](prompts/system.txt) plus one [brief](prompts/briefs). No tools, no retries, no follow-up turns, default reasoning effort, `max_tokens` 64000.
- **20 different briefs.** Each brief names a fictional brand and a motion signature: a Sun shader, a Web Audio synth, a playable canvas mini-game, a 3D globe, a variable-font tester, a replay of the 1851 Immortal Game, and so on.
- **Allowed resources.** Google Fonts and libraries from cdnjs or jsDelivr only. No images, video or audio files, so every visual is CSS, SVG, canvas or WebGL. The model chose GSAP + ScrollTrigger for 18 sites, Lenis for 17 and three.js for 3.
- **Browser check.** Playwright with Chrome. Each site was loaded at 1440×900 and at a 390×844 phone viewport, then screenshotted after 2.5 s and again after scrolling. The check recorded console errors, page errors and horizontal overflow ([`results/browser_check.json`](results/browser_check.json)).

## Results

All 20 sites loaded with **0 console errors and 0 page errors**. The only horizontal overflow was `08_festival` at desktop width (30 px). In total the 20 calls produced 984,369 output tokens, 132–207 s per site.

| Site | Output tokens | Of which reasoning | Seconds | Console errors |
| --- | ---: | ---: | ---: | ---: |
| [01_coffee](sites/01_coffee.html) | 48,790 | 26,968 | 174 | 0 |
| [02_space](sites/02_space.html) | 58,144 | 38,102 | 207 | 0 |
| [03_fashion](sites/03_fashion.html) | 39,717 | 23,223 | 142 | 0 |
| [04_synth](sites/04_synth.html) | 48,708 | 26,542 | 164 | 0 |
| [05_ocean](sites/05_ocean.html) | 48,657 | 30,954 | 173 | 0 |
| [06_architect](sites/06_architect.html) | 52,776 | 35,495 | 194 | 0 |
| [07_fintech](sites/07_fintech.html) | 43,196 | 19,145 | 141 | 0 |
| [08_festival](sites/08_festival.html) | 42,988 | 24,631 | 148 | 0 |
| [09_tea](sites/09_tea.html) | 46,378 | 28,795 | 171 | 0 |
| [10_ai](sites/10_ai.html) | 51,178 | 30,719 | 180 | 0 |
| [11_bakery](sites/11_bakery.html) | 57,024 | 36,210 | 199 | 0 |
| [12_watch](sites/12_watch.html) | 55,559 | 33,391 | 197 | 0 |
| [13_game](sites/13_game.html) | 49,891 | 26,001 | 170 | 0 |
| [14_travel](sites/14_travel.html) | 54,271 | 32,308 | 189 | 0 |
| [15_type](sites/15_type.html) | 37,608 | 21,405 | 132 | 0 |
| [16_climate](sites/16_climate.html) | 47,595 | 31,748 | 178 | 0 |
| [17_skate](sites/17_skate.html) | 57,128 | 35,018 | 201 | 0 |
| [18_meditation](sites/18_meditation.html) | 46,454 | 28,511 | 159 | 0 |
| [19_agency](sites/19_agency.html) | 42,707 | 23,106 | 142 | 0 |
| [20_chess](sites/20_chess.html) | 55,600 | 38,289 | 204 | 0 |

Observations from the screenshots:

- `09_tea` is still mostly blank on desktop at 2.5 s because its brush-stroke reveal is slow; the phone layout is fine.
- `17_skate`: the board graphic and the title read as a jumbled collage.
- `16_climate`: the temperature counter showed +0.00 in the scrolled screenshot, so its scroll trigger may not have fired in headless Chrome.

Interactive features were **not** tested automatically: dragging stickers, synth audio, the mini-game, globe pins, the chess replay and the breathing session. Try them by hand.

## Reproduce

```sh
DEEPSEEK_API_KEY=... python3 bench/generate.py            # rewrites sites/ and results/usage.json
npm install playwright && node bench/check.mjs             # needs Google Chrome; writes PNG screenshots
```

Model output is not deterministic, so a new run will produce different sites.

## License

MIT, see [LICENSE](LICENSE). The pages are model output published as-is; brand names in the briefs are fictional.
