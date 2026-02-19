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
    }
    #calc-widget .calc-expr {
      font-size: 13px; color: #8888aa; min-height: 18px;
      word-break: break-all; text-align: right;
    }
    #calc-widget .calc-result {
      font-size: 22px; font-weight: 600; color: #e0e0f0;
      text-align: right; min-height: 30px; word-break: break-all;
    }

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
    ['0','.','e','=',''],
  ];

  let btnHtml = '';
  for (const row of buttons) {
    for (const b of row) {
      if (!b) continue;
      const cls = '='.includes(b) ? 'eq' : ['+','−','×','÷','^','sin','cos','tan','log','ln','√','π','C','⌫','(', ')'].includes(b) ? 'op' : '';
      const wide = b === '0' ? '' : '';
      btnHtml += `<button class="${cls} ${wide}" data-v="${b}">${b}</button>`;
    }
  }

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
      <div class="calc-result">0</div>
    </div>
    <div class="calc-buttons">${btnHtml}</div>
    <div class="calc-history">
      <div class="calc-history-title">History</div>
    </div>
  `;
  document.body.appendChild(widget);

  const exprEl = widget.querySelector('.calc-expr');
  const resultEl = widget.querySelector('.calc-result');
  const historyEl = widget.querySelector('.calc-history');
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
      el.addEventListener('click', () => { expr = el.dataset.expr; update(); });
    });
  }

  function evaluate(e) {
    try {
      let s = e
        .replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-')
        .replace(/π/g, `(${Math.PI})`)
        .replace(/e(\d)/g, 'e$1') // keep scientific notation
        .replace(/(\d)e([+-]?\d)/g, '$1e$2')
        .replace(/sin\(/g, 'Math.sin(').replace(/cos\(/g, 'Math.cos(').replace(/tan\(/g, 'Math.tan(')
        .replace(/log\(/g, 'Math.log10(').replace(/ln\(/g, 'Math.log(')
        .replace(/√\(/g, 'Math.sqrt(')
        .replace(/\^/g, '**');
      return new Function('return ' + s)();
    } catch { return 'Error'; }
  }

  function update() {
    exprEl.textContent = expr || '';
    if (expr) {
      const r = evaluate(expr);
      resultEl.textContent = r === 'Error' ? '' : r;
    } else {
      resultEl.textContent = '0';
    }
  }

  function input(v) {
    switch(v) {
      case 'C': expr = ''; break;
      case '⌫': expr = expr.slice(0, -1); break;
      case '=':
        const r = evaluate(expr);
        if (r !== 'Error' && expr) {
          history.unshift({ expr, result: r });
          if (history.length > 5) history.pop();
          renderHistory();
          resultEl.textContent = r;
          exprEl.textContent = expr + ' =';
          expr = String(r);
          saveState();
          return;
        }
        break;
      case 'sin': case 'cos': case 'tan': case 'log': case 'ln': case '√':
        expr += v + '('; break;
      default: expr += v;
    }
    update();
  }

  // Button clicks
  widget.querySelector('.calc-buttons').addEventListener('click', e => {
    const btn = e.target.closest('button');
    if (btn) input(btn.dataset.v);
  });

  // Keyboard
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
    dragging = true; dx = e.clientX - widget.offsetLeft; dy = e.clientY - widget.offsetTop;
  });
  widget.querySelector('.calc-titlebar').addEventListener('touchstart', e => {
    dragging = true; const t = e.touches[0];
    dx = t.clientX - widget.offsetLeft; dy = t.clientY - widget.offsetTop;
  }, { passive: true });
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
