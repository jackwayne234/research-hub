// Scientific Calculator Widget - Reusable Component
(function() {
  if (document.getElementById('calc-widget-toggle')) return;

  const STORAGE_KEY = 'calc-widget-state';
  const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');

  const css = document.createElement('style');
  css.textContent = `
    #calc-widget-toggle {
      position: fixed; bottom: 24px; right: 24px; z-index: 99999;
      width: 48px; height: 48px; border-radius: 50%;
      background: linear-gradient(135deg, #6366f1, #a855f7);
      border: none; font-size: 22px; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 20px rgba(99,102,241,0.4);
      transition: transform 0.2s;
    }
    #calc-widget-toggle:hover { transform: scale(1.1); }

    #calc-widget {
      position: fixed; z-index: 100000;
      width: 320px; min-height: 420px;
      background: #111128; border: 1px solid #1a1a3a;
      border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.6);
      font-family: 'JetBrains Mono', monospace; color: #e0e0f0;
      display: none; flex-direction: column; overflow: hidden;
      user-select: none;
    }
    #calc-widget.visible { display: flex; }

    #calc-widget .calc-titlebar {
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 12px; background: #0d0d22; cursor: move;
      border-bottom: 1px solid #1a1a3a; flex-shrink: 0;
    }
    #calc-widget .calc-titlebar span { font-size: 12px; font-weight: 600; color: #8888aa; }
    #calc-widget .calc-titlebar .calc-controls button {
      background: none; border: none; color: #8888aa; cursor: pointer;
      font-size: 14px; margin-left: 8px; padding: 2px 4px;
    }
    #calc-widget .calc-titlebar .calc-controls button:hover { color: #e0e0f0; }

    #calc-widget .calc-display {
      padding: 12px; background: #0a0a1a; margin: 8px; border-radius: 8px;
      border: 1px solid #1a1a3a; flex-shrink: 0;
      display: flex; flex-direction: column; position: relative;
    }
    #calc-widget .calc-display-row {
      display: flex; align-items: center; gap: 6px;
    }
    #calc-widget .calc-input {
      width: 100%; background: transparent; border: none; outline: none;
      font-family: 'JetBrains Mono', monospace; color: #e0e0f0;
      font-size: 22px; font-weight: 600; text-align: right;
      caret-color: #a855f7; min-height: 30px;
    }
    #calc-widget .calc-input::placeholder { color: #444466; }
    #calc-widget .calc-expr {
      font-size: 13px; color: #8888aa; min-height: 18px;
      word-break: break-all; text-align: right;
    }
    #calc-widget .calc-copy-btn {
      background: none; border: 1px solid #252550; color: #8888aa;
      border-radius: 4px; cursor: pointer; font-size: 13px;
      padding: 2px 6px; flex-shrink: 0; transition: all 0.2s;
      font-family: 'JetBrains Mono', monospace;
    }
    #calc-widget .calc-copy-btn:hover { color: #e0e0f0; border-color: #6366f1; }
    #calc-widget .calc-copy-btn.copied { color: #22c55e; border-color: #22c55e; }

    #calc-widget .calc-buttons {
      display: grid; grid-template-columns: repeat(5, 1fr);
      gap: 4px; padding: 4px 8px 8px; flex-shrink: 0;
    }
    #calc-widget .calc-buttons button {
      background: #1a1a3a; border: 1px solid #252550; color: #e0e0f0;
      border-radius: 6px; padding: 10px 0; font-size: 13px;
      font-family: 'JetBrains Mono', monospace; cursor: pointer;
      transition: background 0.15s;
    }
    #calc-widget .calc-buttons button:hover { background: #252550; }
    #calc-widget .calc-buttons button.op {
      background: linear-gradient(135deg, rgba(236,72,153,0.35), rgba(168,85,247,0.3));
      border-color: rgba(236,72,153,0.5);
      color: #f472b6;
      font-size: 18px;
      font-weight: 700;
    }
    #calc-widget .calc-buttons button.op:hover { background: rgba(236,72,153,0.5); color: #fff; }
    #calc-widget .calc-buttons button.eq {
      background: linear-gradient(135deg, #6366f1, #a855f7); color: #fff; border: none;
    }
    #calc-widget .calc-buttons button.eq:hover { filter: brightness(1.15); }
    #calc-widget .calc-buttons button.wide { grid-column: span 2; }
    #calc-widget .calc-buttons button.formula-btn {
      background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(168,85,247,0.2));
      border-color: rgba(99,102,241,0.5); color: #a78bfa; font-size: 11px;
    }
    #calc-widget .calc-buttons button.formula-btn:hover { background: rgba(99,102,241,0.5); color: #fff; }

    #calc-widget .calc-history {
      max-height: 100px; overflow-y: auto; padding: 4px 8px 8px;
      border-top: 1px solid #1a1a3a; flex-shrink: 0;
    }
    #calc-widget .calc-history-title {
      font-size: 10px; color: #6366f1; text-transform: uppercase;
      letter-spacing: 1px; margin-bottom: 4px;
    }
    #calc-widget .calc-history-item {
      font-size: 11px; color: #8888aa; padding: 2px 0; cursor: pointer;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    #calc-widget .calc-history-item:hover { color: #e0e0f0; }

    /* Formula Panel */
    #calc-formula-panel {
      position: absolute; top: 0; left: 0; right: 0; bottom: 0;
      background: #111128; z-index: 10; display: none;
      flex-direction: column; overflow: hidden;
      border-radius: 12px;
    }
    #calc-formula-panel.visible { display: flex; }
    #calc-formula-panel .fp-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 10px 12px; background: #0d0d22; border-bottom: 1px solid #1a1a3a;
      flex-shrink: 0;
    }
    #calc-formula-panel .fp-header span { font-size: 15px; font-weight: 700; color: #e0e0f0; }
    #calc-formula-panel .fp-close {
      background: none; border: none; color: #8888aa; cursor: pointer;
      font-size: 16px; padding: 2px 6px;
    }
    #calc-formula-panel .fp-close:hover { color: #e0e0f0; }
    #calc-formula-panel .fp-body {
      flex: 1; overflow-y: auto; padding: 8px;
    }
    #calc-formula-panel .fp-presets {
      display: flex; gap: 4px; padding: 0 8px 8px; flex-wrap: wrap; flex-shrink: 0;
      border-bottom: 1px solid #1a1a3a; margin-bottom: 4px; padding-bottom: 8px;
    }
    #calc-formula-panel .fp-presets button { font-size: 13px;
      background: #1a1a3a; border: 1px solid #252550; color: #8888aa;
      border-radius: 4px; padding: 3px 8px; font-size: 10px; cursor: pointer;
      font-family: 'JetBrains Mono', monospace; transition: all 0.15s;
    }
    #calc-formula-panel .fp-presets button:hover { color: #e0e0f0; border-color: #6366f1; }
    #calc-formula-panel .fp-card {
      background: #0a0a1a; border: 1px solid #1a1a3a; border-radius: 8px;
      padding: 10px; margin-bottom: 8px;
    }
    #calc-formula-panel .fp-card-title {
      font-size: 15px; font-weight: 700; color: #f472b6; margin-bottom: 4px;
    }
    #calc-formula-panel .fp-card-eq {
      font-size: 13px; color: #c0c0d8; margin-bottom: 8px;
    }
    #calc-formula-panel .fp-fields {
      display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
      gap: 6px; margin-bottom: 8px;
    }
    #calc-formula-panel .fp-field label {
      display: block; font-size: 12px; color: #a78bfa; text-transform: uppercase;
      font-weight: 600; letter-spacing: 0.5px; margin-bottom: 3px;
    }
    #calc-formula-panel .fp-field input {
      width: 100%; background: #111128; border: 1px solid #353560; color: #e0e0f0;
      border-radius: 4px; padding: 7px 8px; font-size: 13px;
      font-family: 'JetBrains Mono', monospace; outline: none;
      box-sizing: border-box;
    }
    #calc-formula-panel .fp-field input:focus { border-color: #6366f1; }
    #calc-formula-panel .fp-compute {
      background: linear-gradient(135deg, #6366f1, #a855f7); color: #fff;
      border: none; border-radius: 4px; padding: 5px 12px; font-size: 11px;
      font-family: 'JetBrains Mono', monospace; cursor: pointer;
      transition: filter 0.15s;
    }
    #calc-formula-panel .fp-compute:hover { filter: brightness(1.15); }

    @media (max-width: 480px) {
      #calc-widget { width: calc(100vw - 16px); left: 8px !important; right: 8px; }
      #calc-widget-toggle { bottom: 16px; right: 16px; }
    }
  `;
  document.head.appendChild(css);

  // Toggle button
  const toggle = document.createElement('button');
  toggle.id = 'calc-widget-toggle';
  toggle.innerHTML = '🧮';
  toggle.title = 'Scientific Calculator';
  document.body.appendChild(toggle);

  // Calculator window
  const widget = document.createElement('div');
  widget.id = 'calc-widget';
  widget.style.left = (saved.x || 100) + 'px';
  widget.style.top = (saved.y || 100) + 'px';

  const buttons = [
    ['sin','cos','tan','π','C'],
    ['log','ln','√','(', ')'],
    ['7','8','9','^','⌫'],
    ['4','5','6','×','÷'],
    ['1','2','3','+','−'],
    ['0','.','e','=','📐'],
  ];

  let btnHtml = '';
  for (const row of buttons) {
    for (const b of row) {
      if (!b) continue;
      const cls = b === '=' ? 'eq' : b === '📐' ? 'formula-btn' : ['+','−','×','÷','^','sin','cos','tan','log','ln','√','π','C','⌫','(', ')'].includes(b) ? 'op' : '';
      btnHtml += `<button class="${cls}" data-v="${b}">${b}</button>`;
    }
  }

  // Formula definitions
  const formulas = [
    {
      name: 'Escape Velocity',
      eq: 'v = √(2GM/r)',
      fields: [
        { id: 'G', label: 'G', default: '6.674e-11' },
        { id: 'M', label: 'M', default: '' },
        { id: 'r', label: 'r', default: '' },
      ],
      compute: (v) => Math.sqrt(2 * v.G * v.M / v.r),
    },
    {
      name: 'Beta (river velocity)',
      eq: 'β = √(r_s / r)',
      fields: [
        { id: 'r_s', label: 'r_s', default: '' },
        { id: 'r', label: 'r', default: '' },
      ],
      compute: (v) => Math.sqrt(v.r_s / v.r),
    },
    {
      name: 'Clock Rate',
      eq: '√(1 − β²)',
      fields: [
        { id: 'beta', label: 'β', default: '' },
      ],
      compute: (v) => Math.sqrt(1 - v.beta * v.beta),
    },
    {
      name: 'Schwarzschild Radius',
      eq: 'r_s = 2GM/c²',
      fields: [
        { id: 'G', label: 'G', default: '6.674e-11' },
        { id: 'M', label: 'M', default: '' },
        { id: 'c', label: 'c', default: '2.998e8' },
      ],
      compute: (v) => 2 * v.G * v.M / (v.c * v.c),
    },
  ];

  const presets = [
    { label: '🌍 Earth', values: { M: '5.972e24', r: '6.371e6', r_s: '8.87e-3', beta: '3.731e-5' } },
    { label: '🔴 Mars', values: { M: '6.39e23', r: '3.3895e6', r_s: '9.46e-4', beta: '1.67e-5' } },
    { label: '☀️ Sun', values: { M: '1.989e30', r: '6.957e8', r_s: '2.954e3', beta: '6.514e-6' } },
  ];

  let formulaCardsHtml = '';
  for (const f of formulas) {
    const fieldsHtml = f.fields.map(fd =>
      `<div class="fp-field"><label>${fd.label}</label><input data-fid="${fd.id}" value="${fd.default}" placeholder="0"></div>`
    ).join('');
    formulaCardsHtml += `
      <div class="fp-card" data-formula="${f.name}">
        <div class="fp-card-title">${f.name}</div>
        <div class="fp-card-eq">${f.eq}</div>
        <div class="fp-fields">${fieldsHtml}</div>
        <button class="fp-compute">Compute</button>
      </div>`;
  }

  const presetsHtml = presets.map(p =>
    `<button data-preset='${JSON.stringify(p.values)}'>${p.label}</button>`
  ).join('');

  widget.innerHTML = `
    <div class="calc-titlebar">
      <span>⚡ CALCULATOR</span>
      <div class="calc-controls">
        <button id="calc-minimize" title="Minimize">−</button>
        <button id="calc-close" title="Close">×</button>
      </div>
    </div>
    <div class="calc-display">
      <div class="calc-expr"></div>
      <div class="calc-display-row">
        <input class="calc-input" type="text" value="0" placeholder="0">
        <button class="calc-copy-btn" title="Copy result">📋</button>
      </div>
    </div>
    <div class="calc-buttons">${btnHtml}</div>
    <div class="calc-history">
      <div class="calc-history-title">History</div>
    </div>
    <div id="calc-formula-panel">
      <div class="fp-header">
        <span>📐 Formulas</span>
        <button class="fp-close">×</button>
      </div>
      <div class="fp-presets">${presetsHtml}</div>
      <div class="fp-body">${formulaCardsHtml}</div>
    </div>
  `;
  document.body.appendChild(widget);

  const exprEl = widget.querySelector('.calc-expr');
  const inputEl = widget.querySelector('.calc-input');
  const copyBtn = widget.querySelector('.calc-copy-btn');
  const historyEl = widget.querySelector('.calc-history');
  const formulaPanel = widget.querySelector('#calc-formula-panel');
  let expr = '';
  let history = saved.history || [];

  function saveState() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      x: parseInt(widget.style.left), y: parseInt(widget.style.top), history
    }));
  }

  function renderHistory() {
    const items = history.map(h =>
      `<div class="calc-history-item" data-expr="${h.expr}">${h.expr} = ${h.result}</div>`
    ).join('');
    historyEl.innerHTML = `<div class="calc-history-title">History</div>${items}`;
    historyEl.querySelectorAll('.calc-history-item').forEach(el => {
      el.addEventListener('click', () => { expr = el.dataset.expr; syncToInput(); update(); });
    });
  }

  function evaluate(e) {
    try {
      let s = e
        .replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-')
        .replace(/π/g, `(${Math.PI})`)
        .replace(/e(\d)/g, 'e$1')
        .replace(/(\d)e([+-]?\d)/g, '$1e$2')
        .replace(/sin\(/g, 'Math.sin(').replace(/cos\(/g, 'Math.cos(').replace(/tan\(/g, 'Math.tan(')
        .replace(/log\(/g, 'Math.log10(').replace(/ln\(/g, 'Math.log(')
        .replace(/√\(/g, 'Math.sqrt(')
        .replace(/\^/g, '**');
      return new Function('return ' + s)();
    } catch { return 'Error'; }
  }

  function syncToInput() {
    inputEl.value = expr || '0';
  }

  function syncFromInput() {
    const v = inputEl.value.trim();
    expr = (v === '0' || v === '') ? '' : v;
  }

  function update() {
    exprEl.textContent = '';
    // Don't auto-evaluate while typing — just keep display in sync
  }

  function input(v) {
    syncFromInput();
    switch(v) {
      case 'C': expr = ''; break;
      case '⌫': expr = expr.slice(0, -1); break;
      case '=':
        syncFromInput();
        const r = evaluate(expr);
        if (r !== 'Error' && expr) {
          history.unshift({ expr, result: r });
          if (history.length > 5) history.pop();
          renderHistory();
          exprEl.textContent = expr + ' =';
          expr = String(r);
          syncToInput();
          saveState();
          return;
        }
        break;
      case '📐':
        formulaPanel.classList.toggle('visible');
        return;
      case 'sin': case 'cos': case 'tan': case 'log': case 'ln': case '√':
        expr += v + '('; break;
      default: expr += v;
    }
    syncToInput();
    update();
  }

  // Editable input: handle Enter to evaluate
  inputEl.addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      e.preventDefault();
      input('=');
    }
  });

  // Copy button
  copyBtn.addEventListener('click', () => {
    const text = inputEl.value;
    navigator.clipboard.writeText(text).then(() => {
      copyBtn.textContent = '✓';
      copyBtn.classList.add('copied');
      setTimeout(() => { copyBtn.textContent = '📋'; copyBtn.classList.remove('copied'); }, 1200);
    }).catch(() => {
      // Fallback
      const ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta);
      ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
      copyBtn.textContent = '✓';
      copyBtn.classList.add('copied');
      setTimeout(() => { copyBtn.textContent = '📋'; copyBtn.classList.remove('copied'); }, 1200);
    });
  });

  // Formula panel interactions
  formulaPanel.querySelector('.fp-close').addEventListener('click', () => {
    formulaPanel.classList.remove('visible');
  });

  // Presets
  formulaPanel.querySelectorAll('.fp-presets button').forEach(btn => {
    btn.addEventListener('click', () => {
      const vals = JSON.parse(btn.dataset.preset);
      // Fill matching fields across all formula cards
      formulaPanel.querySelectorAll('.fp-field input').forEach(inp => {
        if (vals[inp.dataset.fid] !== undefined) {
          inp.value = vals[inp.dataset.fid];
        }
      });
    });
  });

  // Compute buttons
  formulaPanel.querySelectorAll('.fp-compute').forEach((btn, i) => {
    btn.addEventListener('click', () => {
      const card = btn.closest('.fp-card');
      const f = formulas[i];
      const vals = {};
      card.querySelectorAll('.fp-field input').forEach(inp => {
        vals[inp.dataset.fid] = parseFloat(inp.value);
      });
      try {
        const result = f.compute(vals);
        if (isNaN(result) || !isFinite(result)) {
          inputEl.value = 'Error';
        } else {
          expr = String(result);
          inputEl.value = result;
          exprEl.textContent = f.eq + ' =';
        }
        formulaPanel.classList.remove('visible');
      } catch {
        inputEl.value = 'Error';
      }
    });
  });

  // Stop click events on formula panel inputs from propagating
  formulaPanel.querySelectorAll('input').forEach(inp => {
    inp.addEventListener('mousedown', e => e.stopPropagation());
  });

  // Button clicks
  widget.querySelector('.calc-buttons').addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (btn) input(btn.dataset.v);
  });

  // Keyboard (only when input not focused)
  document.addEventListener('keydown', e => {
    if (!widget.classList.contains('visible')) return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.isContentEditable) return;
    const map = { Enter: '=', Backspace: '⌫', Escape: 'C', '*': '×', '/': '÷', '-': '−' };
    const v = map[e.key] || (/[\d+.()^e]/.test(e.key) ? e.key : null);
    if (v) { e.preventDefault(); input(v); }
  });

  // Drag
  let dragging = false, dx, dy;
  widget.querySelector('.calc-titlebar').addEventListener('mousedown', e => {
    e.preventDefault(); e.stopPropagation();
    dragging = true; dx = e.clientX - widget.offsetLeft; dy = e.clientY - widget.offsetTop;
  });
  widget.querySelector('.calc-titlebar').addEventListener('touchstart', e => {
    e.preventDefault(); e.stopPropagation();
    dragging = true; const t = e.touches[0];
    dx = t.clientX - widget.offsetLeft; dy = t.clientY - widget.offsetTop;
  });
  const onMove = (cx, cy) => {
    if (!dragging) return;
    widget.style.left = Math.max(0, cx - dx) + 'px';
    widget.style.top = Math.max(0, cy - dy) + 'px';
  };
  document.addEventListener('mousemove', e => onMove(e.clientX, e.clientY));
  document.addEventListener('touchmove', e => { if (dragging) onMove(e.touches[0].clientX, e.touches[0].clientY); }, { passive: true });
  document.addEventListener('mouseup', () => { if (dragging) { dragging = false; saveState(); } });
  document.addEventListener('touchend', () => { if (dragging) { dragging = false; saveState(); } });

  // Toggle / close / minimize
  toggle.addEventListener('click', () => widget.classList.toggle('visible'));
  widget.querySelector('#calc-close').addEventListener('click', () => widget.classList.remove('visible'));
  widget.querySelector('#calc-minimize').addEventListener('click', () => widget.classList.remove('visible'));

  renderHistory();
})();
