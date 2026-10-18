import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path';
const R = new URL('..', import.meta.url).pathname; const O = R + 'sites';
const files = fs.readdirSync(O).filter(f => /^\d\d_.*\.html$/.test(f)).sort();
const b = await chromium.launch({ channel: 'chrome', args: ['--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
const out = {};
async function one(f) {
  const n = f.replace('.html',''); const r = { errors: [] };
  for (const [tag, vp] of [['desk',{width:1440,height:900}],['phone',{width:390,height:844}]]) {
    const ctx = await b.newContext({ viewport: vp, deviceScaleFactor: 1, isMobile: tag==='phone', hasTouch: tag==='phone' });
    const p = await ctx.newPage();
    p.on('pageerror', e => r.errors.push(`${tag} pageerror: ${e.message}`.slice(0,200)));
    p.on('console', m => { if (m.type()==='error') r.errors.push(`${tag} console: ${m.text()}`.slice(0,200)); });
    await p.goto('file://' + path.join(O,f), { waitUntil: 'load', timeout: 30000 }).catch(e => r.errors.push(`${tag} goto: ${e.message}`.slice(0,150)));
    await p.waitForTimeout(2500);
    await p.screenshot({ path: `${R}screenshots/${n}_${tag}.png` });
    r[`${tag}_hscroll`] = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    if (tag==='desk') {
      r.height = await p.evaluate(() => document.documentElement.scrollHeight);
      await p.mouse.move(700, 400); await p.mouse.wheel(0, 2200); await p.waitForTimeout(1800);
      await p.screenshot({ path: `${R}screenshots/${n}_desk_scroll.png` });
    }
    await ctx.close();
  }
  out[n] = r; console.log(n, JSON.stringify({e:r.errors.length, h:r.height, hs:[r.desk_hscroll,r.phone_hscroll]}));
}
for (let i = 0; i < files.length; i += 5) await Promise.all(files.slice(i,i+5).map(one));
fs.writeFileSync(`${R}results/browser_check.json`, JSON.stringify(out, null, 1));
await b.close();
