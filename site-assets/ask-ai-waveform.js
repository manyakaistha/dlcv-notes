/* Waveform controls for Ask AI: a spoken-signal stamp and per-heading "voice bars" that swell on hover. */
(() => {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const states = new Set(), moving = new Set();
  let frame = 0, serial = 0;
  const svg = (tag, attributes = {}) => {
    const el = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attributes)) el.setAttribute(k, v);
    return el;
  };
  function rng(seed) {
    return () => {
      seed = (seed + 0x6D2B79F5) | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = (t + Math.imul(t ^ t >>> 7, 61 | t)) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  // A speech-like amplitude envelope: tall in the middle, tapering at both ends.
  function bars(seed, count, maxHeight) {
    const random = rng(seed);
    return Array.from({length: count}, (_, i) => {
      const u = count === 1 ? .5 : i / (count - 1);
      const envelope = Math.sin(Math.PI * (.12 + .76 * u));
      return Math.max(.14, envelope * (.45 + .55 * random())) * maxHeight;
    });
  }
  function waveform(seed, count, width, maxHeight) {
    const g = svg('g', {'class': 'ai-wave'});
    const heights = bars(seed, count, maxHeight);
    const gap = width / count, barWidth = gap * .56;
    const rects = heights.map((h, i) => {
      const r = svg('rect', {'class': 'ai-wave-bar', x: (-width / 2 + i * gap + (gap - barWidth) / 2).toFixed(2), width: barWidth.toFixed(2), rx: (barWidth / 2).toFixed(2)});
      g.append(r);
      return r;
    });
    return {g, heights, rects};
  }
  function setBars(wave, v) {
    wave.rects.forEach((r, i) => {
      const h = 1.4 + (wave.heights[i] - 1.4) * v;
      r.setAttribute('height', h.toFixed(2));
      r.setAttribute('y', (-h / 2).toFixed(2));
    });
  }
  function apply(state, value) {
    const v = Math.max(-.08, Math.min(1.16, value));
    state.value = v;
    setBars(state.wave, Math.max(0, v));
  }
  function motionAllowed() { return !reduced.matches && document.documentElement.dataset.askAiMotion !== 'off' && !document.hidden; }
  function finish() {
    cancelAnimationFrame(frame); frame = 0;
    for (const s of moving) apply(s, s.target);
    moving.clear();
  }
  function tick(now) {
    frame = 0;
    if (!motionAllowed()) { finish(); return; }
    for (const s of moving) {
      const u = Math.min(1, (now - s.birth) / s.duration);
      // Finite damped spring toward the endpoint, snapping exactly on completion.
      const ease = s.target > 0 ? 1 - Math.exp(-7 * u) * Math.cos(11 * u) : 1 - Math.pow(1 - u, 3);
      apply(s, u === 1 ? s.target : s.from + (s.target - s.from) * ease);
      if (u === 1) moving.delete(s);
    }
    if (moving.size) frame = requestAnimationFrame(tick);
  }
  function to(state, target) {
    if (state.target === target && !moving.has(state)) return;
    state.from = state.value; state.target = target; state.birth = performance.now(); state.duration = target ? 760 : 440;
    if (!motionAllowed() || !state.visible) { apply(state, target); moving.delete(state); return; }
    moving.add(state);
    if (!frame) frame = requestAnimationFrame(tick);
  }
  const observer = new IntersectionObserver(entries => entries.forEach(e => {
    const s = [...states].find(s => s.button === e.target);
    if (s) { s.visible = e.isIntersecting; if (!s.visible) { moving.delete(s); apply(s, s.target); } }
  }), {threshold: .05});

  function decorateFlower(button, seed) {
    const icon = svg('svg', {viewBox: '0 0 64 64', 'class': 'ai-bloom-icon', 'aria-hidden': 'true', focusable: 'false'});
    const wave = waveform(seed, 9, 46, 40), position = svg('g', {transform: 'translate(32 32)'});
    position.append(svg('line', {'class': 'ai-wave-baseline', x1: -26, x2: 26, y1: 0, y2: 0}), wave.g);
    icon.append(position);
    const label = document.createElement('span');
    label.className = 'ai-bloom-label'; label.textContent = 'Ask AI';
    button.replaceChildren(icon, label);
    const state = {button, wave, value: 0, target: 0, from: 0, visible: true, hover: false, focus: false};
    states.add(state); apply(state, 0); observer.observe(button);
    const update = () => to(state, state.hover || state.focus ? 1 : 0);
    button.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') { state.hover = true; update(); } });
    button.addEventListener('pointerleave', () => { state.hover = false; update(); });
    button.addEventListener('pointercancel', () => { state.hover = false; update(); });
    button.addEventListener('focus', () => { state.focus = true; update(); });
    button.addEventListener('blur', () => { state.focus = false; update(); });
    return state;
  }
  function decorateStamp(button) {
    const icon = svg('svg', {viewBox: '0 0 128 128', 'class': 'ai-stamp', 'aria-hidden': 'true', focusable: 'false'});
    const id = 'ask-ai-rim-' + (++serial), defs = svg('defs');
    defs.append(svg('path', {id, d: 'M64 17.5 A46.5 46.5 0 1 1 63.999 17.5'}));
    icon.append(defs);
    // Scalloped edge, like the rim of a speaker cone.
    const edge = [];
    for (let i = 0; i <= 192; i++) {
      const a = i / 192 * Math.PI * 2, r = 59.5 + 1.1 * Math.sin(24 * a);
      edge.push([64 + Math.cos(a) * r, 64 + Math.sin(a) * r]);
    }
    const d = edge.map(([x, y], i) => (i ? 'L' : 'M') + x.toFixed(2) + ',' + y.toFixed(2)).join(' ') + 'Z';
    icon.append(svg('path', {d, 'class': 'ai-stamp-paper'}), svg('circle', {cx: 64, cy: 64, r: 55, 'class': 'ai-stamp-keyline'}));
    const orbit = svg('g', {'class': 'ai-stamp-orbit'});
    const lettering = svg('text', {'class': 'ai-stamp-lettering', textLength: 286, lengthAdjust: 'spacing'});
    const onPath = svg('textPath', {href: '#' + id, startOffset: '0%'});
    lettering.append(onPath); orbit.append(lettering); icon.append(orbit);
    const wave = waveform(2701, 13, 56, 30), position = svg('g', {transform: 'translate(64 58)', 'class': 'ai-stamp-wave'});
    setBars(wave, 1); position.append(wave.g); icon.append(position);
    const word = svg('text', {x: 64, y: 91, 'text-anchor': 'middle', 'class': 'ai-stamp-word'});
    word.textContent = 'Ask AI'; icon.append(word);
    const hint = document.createElement('span');
    hint.className = 'ai-stamp-hint'; hint.textContent = 'Explain this page';
    button.replaceChildren(icon, hint);
    setStamp(button, false);
  }
  function setStamp(button, selected) {
    button.dataset.selection = String(selected);
    button.querySelector('textPath').textContent = selected ? 'ASK AI  ·  EXPLAIN MY SELECTION  ·' : 'ASK AI  ·  TUNE IN TO THIS TOPIC  ·';
    button.querySelector('.ai-stamp-hint').textContent = selected ? 'Explain selected text' : 'Explain this page';
    button.setAttribute('aria-label', selected ? 'Ask AI about selected text' : 'Ask AI to explain this page. Select text to ask about a passage.');
  }
  function syncMotion() {
    const toggle = document.querySelector('.motion-toggle');
    document.documentElement.dataset.askAiMotion = reduced.matches || (toggle && toggle.getAttribute('aria-pressed') === 'false') ? 'off' : 'on';
    if (!motionAllowed()) finish();
  }
  const toggle = document.querySelector('.motion-toggle');
  if (toggle) new MutationObserver(syncMotion).observe(toggle, {attributes: true, attributeFilter: ['aria-pressed']});
  reduced.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', () => { document.documentElement.dataset.askAiHidden = String(document.hidden); if (document.hidden) finish(); });
  syncMotion();
  window.AskAIWaveforms = {decorateFlower, decorateStamp, setStamp};
})();
