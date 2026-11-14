(() => {
  'use strict';
  const root = document.documentElement;
  const themes = ['paper', 'midnight', 'scope', 'spectro', 'butter', 'mono'];
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let motion = !reduced.matches;
  try { motion = localStorage.getItem('speech-lab-motion') !== 'off' && !reduced.matches; } catch {}
  let repaint = () => {};
  const toggle = document.querySelector('.motion-toggle');
  function updateControls() {
    document.querySelectorAll('.theme-option').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.palette === root.dataset.theme)));
    if (!toggle) return;
    toggle.textContent = reduced.matches ? 'Motion off (system preference)' : motion ? 'Pause header motion' : 'Enable header motion';
    toggle.setAttribute('aria-pressed', String(motion));
    toggle.disabled = reduced.matches;
  }
  document.querySelectorAll('.theme-option').forEach(b => b.addEventListener('click', () => {
    if (!themes.includes(b.dataset.palette)) return;
    root.dataset.theme = b.dataset.palette;
    try { localStorage.setItem('speech-lab-theme', root.dataset.theme); } catch {}
    updateControls(); repaint();
  }));
  if (toggle) toggle.addEventListener('click', () => {
    motion = !motion;
    try { localStorage.setItem('speech-lab-motion', motion ? 'on' : 'off'); } catch {}
    updateControls(); repaint();
  });
  reduced.addEventListener('change', () => { motion = !reduced.matches; updateControls(); repaint(); });
  updateControls();

  const progress = document.querySelector('.reading-progress');
  const updateProgress = () => {
    if (!progress) return;
    const total = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${total > 0 ? Math.min(100, scrollY / total * 100) : 0}%`;
  };
  addEventListener('scroll', updateProgress, {passive: true});
  addEventListener('resize', updateProgress); updateProgress();

  // Hero: a sampled speech-like waveform over a drifting spectrogram.
  const canvas = document.querySelector('.speech-hero canvas');
  const ctx = canvas && canvas.getContext('2d');
  if (ctx) {
    let width = 0, height = 0, visible = true, frame = 0, birth = performance.now(), palette;
    const rng = seed => () => {
      seed = (seed + 0x6D2B79F5) | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = (t + Math.imul(t ^ t >>> 7, 61 | t)) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
    const rand = rng(260310);
    // Syllable-like energy bursts and formant tracks, fixed by seed for a stable picture.
    const bursts = Array.from({length: 5}, (_, i) => ({c: .08 + i * .2 + rand() * .06, w: .045 + rand() * .035, a: .55 + rand() * .45}));
    const formants = [{r: .78, wob: .05, ph: rand() * 6}, {r: .52, wob: .07, ph: rand() * 6}, {r: .27, wob: .05, ph: rand() * 6}];
    const noise = Array.from({length: 40 * 9}, () => rand());
    function colors() {
      const css = getComputedStyle(root);
      palette = Object.fromEntries(['ink', 'line', 'stem', 'flower', 'flower-line'].map(k => [k, css.getPropertyValue('--' + k).trim()]));
    }
    function size() {
      const r = canvas.getBoundingClientRect(); width = r.width; height = r.height;
      const dpr = Math.min(devicePixelRatio || 1, 2.5);
      canvas.width = Math.round(width * dpr); canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); colors(); repaint();
    }
    const envelope = u => bursts.reduce((s, b) => s + b.a * Math.exp(-Math.pow((u - b.c) / b.w, 2)), 0);
    const signal = (u, phase) => envelope(u) * (Math.sin(u * 190 + phase) + .45 * Math.sin(u * 410 + phase * 1.7) + .2 * Math.sin(u * 760 - phase));
    function draw(now) {
      frame = 0; ctx.clearRect(0, 0, width, height);
      const animate = motion && !reduced.matches;
      const u = animate ? Math.max(0, Math.min(1, (now - birth) / 1300)) : 1;
      const grow = 1 - Math.pow(1 - u, 3), time = animate ? now : 0;
      const overview = document.body.dataset.overview === 'true';
      const x0 = width * (overview ? .58 : .46), w = width - x0, mid = height * .5, amp = height * .34;
      // Axis lines.
      ctx.strokeStyle = palette.line; ctx.lineWidth = .6; ctx.globalAlpha = .55;
      for (let i = 0; i < 5; i++) { ctx.beginPath(); ctx.moveTo(x0, height * (.18 + i * .16)); ctx.lineTo(width, height * (.18 + i * .16)); ctx.stroke(); }
      // Spectrogram cells: formant bands that glide with the speech bursts.
      const cols = 40, rows = 9, cw = w / cols, ch = height * .78 / rows;
      ctx.fillStyle = palette.stem;
      for (let c = 0; c < cols; c++) {
        const t = c / (cols - 1);
        if (t > grow) break;
        const e = Math.min(1, envelope(t));
        for (let r = 0; r < rows; r++) {
          const yr = 1 - r / (rows - 1);
          let v = 0;
          for (const f of formants) v += Math.exp(-Math.pow((yr - (f.r + f.wob * Math.sin(t * 9 + f.ph + time * .0004))) / .13, 2));
          const a = Math.min(1, v * e * (.65 + .35 * noise[c * rows + r]));
          if (a < .06) continue;
          ctx.globalAlpha = .08 + a * .5;
          ctx.fillRect(x0 + c * cw + 1, height * .1 + r * ch + 1, cw - 2, ch - 2);
        }
      }
      // Waveform trace.
      const phase = animate ? time * .0011 : 0;
      ctx.globalAlpha = 1; ctx.strokeStyle = palette.stem; ctx.lineWidth = 1.5; ctx.lineJoin = 'round';
      ctx.beginPath();
      const steps = Math.max(80, Math.round(w / 2));
      for (let i = 0; i <= steps; i++) {
        const t = i / steps; if (t > grow) break;
        const x = x0 + t * w, y = mid - signal(t, phase) * amp * .62;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
      // Discrete samples: the lollipops of x[n].
      const n = Math.max(24, Math.round(w / 13));
      ctx.lineWidth = 1;
      for (let i = 0; i <= n; i++) {
        const t = i / n; if (t > grow) break;
        const x = x0 + t * w, y = mid - signal(t, phase) * amp * .62;
        ctx.globalAlpha = .8; ctx.strokeStyle = palette.flower;
        ctx.beginPath(); ctx.moveTo(x, mid); ctx.lineTo(x, y); ctx.stroke();
        ctx.globalAlpha = 1; ctx.fillStyle = palette.flower;
        ctx.beginPath(); ctx.arc(x, y, 2.3, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = palette['flower-line']; ctx.lineWidth = .6; ctx.stroke(); ctx.lineWidth = 1;
      }
      ctx.globalAlpha = .6; ctx.strokeStyle = palette.ink; ctx.lineWidth = .7;
      ctx.beginPath(); ctx.moveTo(x0, mid); ctx.lineTo(width, mid); ctx.stroke(); ctx.globalAlpha = 1;
      if (animate && visible && !document.hidden) frame = requestAnimationFrame(draw);
    }
    repaint = () => { if (frame) cancelAnimationFrame(frame); frame = 0; colors(); draw(performance.now()); };
    new ResizeObserver(size).observe(canvas);
    new IntersectionObserver(entries => { visible = entries[0].isIntersecting; if (visible) repaint(); else if (frame) { cancelAnimationFrame(frame); frame = 0; } }, {threshold: 0}).observe(canvas);
    document.addEventListener('visibilitychange', () => { if (document.hidden) { cancelAnimationFrame(frame); frame = 0; } else if (visible) repaint(); });
    size();
  }

  // Load the Ask AI helper and the collapsible sidebar relative to this script.
  const current = document.currentScript;
  if (!current) return;
  const assetURL = name => new URL(name, current.src).href;
  const css = document.createElement('link'); css.rel = 'stylesheet'; css.href = assetURL('ask-ai.css');
  const decoration = document.createElement('script'); decoration.src = assetURL('ask-ai-waveform.js');
  decoration.onload = () => { const s = document.createElement('script'); s.src = assetURL('ask-ai.js'); document.head.append(s); };
  document.head.append(css, decoration);
  const sidebar = document.createElement('script'); sidebar.src = assetURL('sidebar.js'); document.head.append(sidebar);
})();
