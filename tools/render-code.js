// tools/code/code-X-Y.ts -> assets/img/code-X-Y.png: τα μπλοκ ζωγραφίζονται από το ίδιο το MakeCode, στα Ελληνικά.
// Χρήση: node tools/render-code.js [code-2-1 ...]   (χωρίς ορίσματα: όλα τα αρχεία του tools/code/)
// Θέλει internet και το playwright (το tools/render-code.sh τα στήνει όπως το make-pdf).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'tools', 'code');
const OUT = path.join(ROOT, 'assets', 'img');
const RENDER_URL = 'https://makecode.microbit.org/---docs?render=1&lang=el';
const MAX_PX = 2000;   // μεγαλύτερη πλευρά: ~300 dpi στο πλάτος της σελίδας
const GAP = 16;        // κενό ανάμεσα στα μπλοκ της κάθετης διάταξης, σε px του MakeCode

// Τα σχόλια στην αρχή του .ts είναι για ανθρώπους. Δύο γραμμές τα ρυθμίζουν:
//   «// extensions: ...»   ποια πακέτα φορτώνει το MakeCode («-» για κανένα)
//   «// διάταξη: κάθετα»   το «κατά την έναρξη» πάνω από τα υπόλοιπα, αντί για δίπλα (για πολύ φαρδύ κώδικα)
function readSource(file) {
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  let i = 0, ext = '', vertical = false;
  for (; i < lines.length && lines[i].startsWith('//'); i++) {
    const m = lines[i].match(/^\/\/\s*extensions:\s*(.*)$/);
    if (m && m[1].trim() !== '-') ext = m[1].split(',').map(s => s.trim()).filter(Boolean).join(',');
    if (/^\/\/\s*διάταξη:\s*κάθετα/.test(lines[i])) vertical = true;
  }
  return { code: lines.slice(i).join('\n').trim() + '\n', ext, vertical };
}

// Κάθετη διάταξη: ο κώδικας χωρίζεται στο «κατά την έναρξη» (ό,τι είναι στο πρώτο επίπεδο) και σε ένα
// κομμάτι για κάθε γεγονός (basic.forever(...), input.onButtonPressed(...)). Οι δηλώσεις «let» μπαίνουν
// μόνο στα γεγονότα, για να μεταγλωττίζονται μόνα τους· στην έναρξη θα έβγαζαν ένα επιπλέον «ορισμός i σε 0».
function splitTopLevel(code) {
  const lines = code.split('\n'), start = [], lets = [], events = [];
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (/^[\w.]+\(.*function\s*\(/.test(l)) {
      const ev = [l];
      while (++i < lines.length && lines[i] !== '})') ev.push(lines[i]);
      ev.push('})');
      events.push(ev.join('\n'));
    } else if (/^let\s/.test(l)) {
      lets.push(l);
    } else if (l.trim()) {
      start.push(l);
    }
  }
  const pre = lets.length ? lets.join('\n') + '\n' : '';
  return [...(start.length ? [start.join('\n')] : []), ...events.map(e => pre + e)];
}

(async () => {
  const want = process.argv.slice(2).map(a => a.replace(/\.ts$/, ''));
  const files = fs.readdirSync(SRC).filter(f => /^code-.*\.ts$/.test(f))
    .filter(f => !want.length || want.includes(f.replace(/\.ts$/, ''))).sort();
  if (!files.length) { console.error('Κανένα αρχείο στο tools/code/.'); process.exit(1); }

  const b = await chromium.launch();
  let failed = 0;
  const renderOne = async (name, parts, ext) => {
    // νέο context για κάθε αρχείο: αλλιώς οι μεταφράσεις ενός extension «περνούν» στο επόμενο αρχείο
    const ctx = await b.newContext();
    try {
      // ο Chromium χάνει κάποια αιτήματα του MakeCode (ERR_SOCKET_NOT_CONNECTED) και τότε τα μπλοκ βγαίνουν
      // μισά στα Αγγλικά· τα περνάμε από το playwright με επανάληψη
      await ctx.route(/makecode\.(com|microbit\.org)|github(usercontent)?\.com/, async route => {
        for (let k = 0; k < 6; k++) {
          try { return await route.fulfill({ response: await route.fetch() }); }
          catch (e) { await new Promise(r => setTimeout(r, 500 * (k + 1))); }
        }
        console.error('  αποτυχία: ' + route.request().url());
        return route.abort();
      });
      const p = await ctx.newPage();
      await p.setContent('<!doctype html><html><body></body></html>');
      await p.evaluate((url) => new Promise((resolve, reject) => {
        window.__done = {};
        window.addEventListener('message', ev => {
          const m = ev.data || {};
          if (m.type === 'renderready') resolve();
          if (m.type === 'renderblocks') window.__done[m.id] = m;
        });
        const fr = document.createElement('iframe');
        fr.id = 'mc'; fr.src = url;
        document.body.appendChild(fr);
        setTimeout(() => reject(new Error('το MakeCode δεν απάντησε σε 2 λεπτά')), 120000);
      }), RENDER_URL);

      return await p.evaluate(async ({ id, parts, ext, max, gap }) => {
        const render = (pid, code) => new Promise((resolve, reject) => {
          document.getElementById('mc').contentWindow.postMessage(
            { type: 'renderblocks', id: pid, code, options: { package: ext } }, '*');
          const t0 = Date.now();
          const poll = () => {
            const m = window.__done[pid];
            if (!m) return Date.now() - t0 > 120000 ? reject(new Error('timeout')) : setTimeout(poll, 200);
            if (!m.uri) return reject(new Error(m.error || 'χωρίς εικόνα'));
            const img = new Image();
            img.onload = () => resolve({ img, k: img.width / m.width });   // k: κλίμακα της PNG του MakeCode
            img.onerror = () => reject(new Error('η εικόνα δεν διαβάστηκε'));
            img.src = m.uri;
          };
          poll();
        });
        try {
          const imgs = [];
          for (let i = 0; i < parts.length; i++) imgs.push(await render(id + '-' + i, parts[i]));
          // τα κομμάτια το ένα κάτω από το άλλο, στοιχισμένα αριστερά (ένα κομμάτι: η εικόνα όπως είναι)
          const sp = gap * imgs[0].k;
          const W = Math.max(...imgs.map(x => x.img.width));
          const H = imgs.reduce((s, x) => s + x.img.height, 0) + sp * (imgs.length - 1);
          // σμίκρυνση σε λευκό φόντο: χωρίς διαφάνεια και χωρίς metadata
          const k = Math.min(1, max / Math.max(W, H));
          const c = document.createElement('canvas');
          c.width = Math.round(W * k); c.height = Math.round(H * k);
          const g = c.getContext('2d');
          g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height);
          g.imageSmoothingQuality = 'high';
          let y = 0;
          for (const x of imgs) {
            g.drawImage(x.img, 0, y * k, x.img.width * k, x.img.height * k);
            y += x.img.height + sp;
          }
          return { png: c.toDataURL('image/png').split(',')[1], w: c.width, h: c.height };
        } catch (e) { return { err: e.message }; }
      }, { id: name, parts, ext, max: MAX_PX, gap: GAP });
    } finally { await ctx.close(); }
  };

  for (const f of files) {
    const name = f.replace(/\.ts$/, '');
    const { code, ext, vertical } = readSource(path.join(SRC, f));
    const parts = vertical ? splitTopLevel(code) : [code];
    let res;
    for (let k = 0; k < 2; k++) {
      res = await renderOne(name, parts, ext).catch(e => ({ err: e.message || String(e) }));
      if (!res.err) break;
    }
    if (res.err) { failed++; console.error(`  ${name}: ΑΠΟΤΥΧΙΑ (${res.err})`); continue; }
    fs.writeFileSync(path.join(OUT, name + '.png'), Buffer.from(res.png, 'base64'));
    console.log(`  ${name}.png  ${res.w}×${res.h}${vertical ? '  (κάθετα)' : ''}`);
  }
  await b.close();
  process.exit(failed ? 2 : 0);
})().catch(e => { console.error(e.message || e); process.exit(1); });
