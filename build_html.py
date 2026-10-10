"""
build_html.py — injects the Homira AI chatbot into the existing website HTML.
Run: python build_html.py
"""
import os

SRC  = r"C:\Users\HP\.kiro\crew\uploads\179aa089bec442b6b0c6878716eb67f1_homira-website.html"
DEST = r"C:\Users\HP\homira-ai\homira-ai.html"

with open(SRC, encoding="utf-8") as f:
    original = f.read()

# ─── Chatbot CSS ───────────────────────────────────────────────────────────
CSS = """
<style>
/* ── Homira AI Chatbot Widget ── */
#ai-chat-btn{
  position:fixed;bottom:92px;right:28px;z-index:800;
  width:56px;height:56px;background:var(--navy);color:#fff;
  border:none;border-radius:50%;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 6px 20px rgba(30,42,56,0.35);
  transition:transform .2s,background .2s;
}
#ai-chat-btn:hover{background:var(--orange);transform:scale(1.08);}
#ai-chat-btn svg{width:26px;height:26px;}
#ai-chat-badge{
  position:absolute;top:-4px;right:-4px;
  width:18px;height:18px;background:var(--orange);
  color:#fff;border-radius:50%;font-size:10px;font-weight:700;
  display:none;align-items:center;justify-content:center;
}
#ai-chat-panel{
  position:fixed;bottom:158px;right:28px;z-index:801;
  width:380px;max-width:calc(100vw - 40px);
  background:#fff;border-radius:20px;
  box-shadow:0 20px 60px rgba(30,42,56,0.18);
  display:none;flex-direction:column;overflow:hidden;
  border:1px solid var(--border);max-height:520px;
  font-family:var(--font-body);
}
#ai-chat-panel.open{display:flex;}
.ai-header{
  background:var(--navy);color:#fff;
  padding:16px 20px;display:flex;align-items:center;justify-content:space-between;
  flex-shrink:0;
}
.ai-header-left{display:flex;align-items:center;gap:12px;}
.ai-avatar{
  width:38px;height:38px;background:var(--orange);
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:var(--font);font-weight:700;font-size:14px;flex-shrink:0;
}
.ai-header-info h4{font-size:14px;font-weight:600;margin-bottom:1px;}
.ai-header-info span{font-size:11px;opacity:.65;}
.ai-header button{
  background:rgba(255,255,255,0.12);border:none;color:#fff;
  width:28px;height:28px;border-radius:8px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:.2s;
}
.ai-header button:hover{background:rgba(255,255,255,0.22);}
.ai-header button svg{width:14px;height:14px;}
#ai-messages{
  flex:1;overflow-y:auto;padding:16px;display:flex;
  flex-direction:column;gap:12px;min-height:200px;
}
.ai-msg{display:flex;gap:8px;max-width:90%;}
.ai-msg.user{flex-direction:row-reverse;align-self:flex-end;}
.ai-msg.bot{align-self:flex-start;}
.ai-bubble{
  padding:10px 14px;border-radius:14px;font-size:13.5px;
  line-height:1.55;word-break:break-word;
}
.ai-msg.bot .ai-bubble{background:var(--grey);color:var(--text);border-bottom-left-radius:4px;}
.ai-msg.user .ai-bubble{background:var(--navy);color:#fff;border-bottom-right-radius:4px;}
.ai-estimate-card{
  margin-top:10px;background:var(--orange-soft);
  border:1px solid #FFD9B5;border-radius:12px;padding:14px;font-size:13px;
}
.ai-estimate-card .est-header{
  font-family:var(--font);font-weight:700;font-size:14px;
  color:var(--navy);margin-bottom:10px;
}
.ai-estimate-row{
  display:flex;justify-content:space-between;
  padding:4px 0;color:var(--charcoal);
}
.ai-estimate-row.total{
  border-top:1px solid #FFD9B5;margin-top:6px;padding-top:8px;
  font-weight:700;font-size:14px;color:var(--navy);
}
.ai-estimate-disclaimer{
  font-size:11px;color:var(--text-muted);margin-top:10px;
  padding-top:8px;border-top:1px solid #FFD9B5;line-height:1.5;
}
.ai-estimate-book{
  margin-top:10px;background:var(--orange);color:#fff;
  border:none;border-radius:99px;padding:8px 18px;
  font-size:13px;font-weight:600;cursor:pointer;
  transition:.2s;width:100%;
}
.ai-estimate-book:hover{background:var(--orange-light);}
.ai-safety-card{
  background:#FEF2F2;border:1px solid #FECACA;
  border-radius:12px;padding:14px;font-size:13px;
  color:#7F1D1D;line-height:1.6;
}
.ai-typing{display:flex;gap:4px;align-items:center;padding:10px 14px;}
.ai-typing span{
  width:7px;height:7px;background:var(--text-muted);
  border-radius:50%;animation:aiDot 1.2s infinite;
}
.ai-typing span:nth-child(2){animation-delay:.2s;}
.ai-typing span:nth-child(3){animation-delay:.4s;}
@keyframes aiDot{0%,60%,100%{transform:translateY(0);}30%{transform:translateY(-5px);}}
.ai-starters{
  padding:0 16px 12px;display:flex;flex-wrap:wrap;gap:6px;flex-shrink:0;
}
.ai-starter-chip{
  background:var(--grey);border:1px solid var(--border);
  color:var(--charcoal);padding:6px 12px;border-radius:99px;
  font-size:12px;font-weight:500;cursor:pointer;transition:.2s;white-space:nowrap;
}
.ai-starter-chip:hover{background:var(--orange-soft);border-color:var(--orange);color:var(--orange);}
.ai-input-area{
  padding:12px 14px;border-top:1px solid var(--border);
  display:flex;gap:8px;align-items:flex-end;flex-shrink:0;background:#fff;
}
#ai-input{
  flex:1;border:1.5px solid var(--border);border-radius:10px;
  padding:9px 12px;font-size:13.5px;font-family:var(--font-body);
  resize:none;outline:none;max-height:80px;line-height:1.4;
  color:var(--text);background:#fff;transition:.2s;
}
#ai-input:focus{border-color:var(--orange);}
#ai-send{
  background:var(--orange);color:#fff;border:none;
  width:36px;height:36px;border-radius:10px;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;transition:.2s;
}
#ai-send:hover{background:var(--orange-light);}
#ai-send:disabled{background:var(--grey2);cursor:not-allowed;}
#ai-send svg{width:16px;height:16px;}
.ai-error-banner{
  background:#FEF2F2;color:#991B1B;font-size:12px;
  padding:8px 14px;text-align:center;flex-shrink:0;
  border-top:1px solid #FECACA;display:none;
}
@media(max-width:600px){
  #ai-chat-panel{
    bottom:0;right:0;left:0;width:100%;max-width:100%;
    border-radius:20px 20px 0 0;max-height:80vh;
  }
  #ai-chat-btn{bottom:84px;}
}
</style>
"""

# ─── Chatbot HTML ──────────────────────────────────────────────────────────
HTML = """
<!-- Homira AI Chat Button -->
<button id="ai-chat-btn" onclick="toggleAIChat()" aria-label="Open Homira AI Assistant" title="Chat with Homira AI">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
    <line x1="8" y1="9" x2="16" y2="9" stroke-width="1.5"/>
    <line x1="8" y1="13" x2="13" y2="13" stroke-width="1.5"/>
  </svg>
  <span id="ai-chat-badge">1</span>
</button>

<!-- Homira AI Chat Panel -->
<div id="ai-chat-panel" role="dialog" aria-modal="true" aria-label="Homira AI Assistant">
  <div class="ai-header">
    <div class="ai-header-left">
      <div class="ai-avatar">AI</div>
      <div class="ai-header-info">
        <h4>Homira AI</h4>
        <span id="ai-status-text">Home services assistant</span>
      </div>
    </div>
    <button onclick="toggleAIChat()" aria-label="Close chat">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
    </button>
  </div>
  <div id="ai-messages" role="log" aria-live="polite" aria-label="Chat messages"></div>
  <div class="ai-starters" id="ai-starters">
    <button class="ai-starter-chip" data-msg="Leaking tap in my kitchen" tabindex="0">Leaking tap</button>
    <button class="ai-starter-chip" data-msg="Electrical switch not working in my room" tabindex="0">Switch problem</button>
    <button class="ai-starter-chip" data-msg="I need a ceiling fan installed" tabindex="0">Fan installation</button>
    <button class="ai-starter-chip" data-msg="My AC is not cooling properly" tabindex="0">AC not cooling</button>
  </div>
  <div class="ai-error-banner" id="ai-error-banner"></div>
  <div class="ai-input-area">
    <textarea id="ai-input" rows="1" placeholder="Describe your home problem..." aria-label="Type your home problem" maxlength="1000"></textarea>
    <button id="ai-send" aria-label="Send message" title="Send (Enter)">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" y1="2" x2="11" y2="13"/>
        <polygon points="22 2 15 22 11 13 2 9 22 2"/>
      </svg>
    </button>
  </div>
</div>
"""

# ─── Chatbot JS ────────────────────────────────────────────────────────────
JS = """
<script>
/* =====================================================
   HOMIRA AI CHATBOT
   Backend: FastAPI at BACKEND_URL
   Model:   llama3.2:3b via Ollama
   ===================================================== */
var AI_BACKEND = 'http://localhost:8000';
var aiHistory  = [];
var aiOpen     = false;
var aiLoading  = false;
var aiGreeted  = false;

/* ── toggle ── */
function toggleAIChat() {
  aiOpen = !aiOpen;
  var panel = document.getElementById('ai-chat-panel');
  var badge = document.getElementById('ai-chat-badge');
  panel.classList.toggle('open', aiOpen);
  if (aiOpen) {
    badge.style.display = 'none';
    document.getElementById('ai-input').focus();
    if (!aiGreeted) {
      aiGreeted = true;
      addAIBotMsg(
        "Hi! I am Homira AI, your home-services assistant.\\n\\n" +
        "Tell me about a problem at home — like a leaking tap, a broken switch, " +
        "or an AC that is not cooling — and I will help you understand the service and get an estimate.\\n\\n" +
        "I support English and Roman Urdu.",
        null, false
      );
    }
  }
}

/* ── render helpers ── */
function aiEscape(t) {
  return t
    .replace(/&/g,'\\u0026amp;')
    .replace(/</g,'\\u0026lt;')
    .replace(/>/g,'\\u0026gt;')
    .replace(/\\*\\*(.*?)\\*\\*/g,'<strong>$1</strong>')
    .replace(/_(.*?)_/g,'<em>$1</em>')
    .replace(/\\n/g,'<br>');
}

function addAIBotMsg(text, estimateData, isSafety) {
  var msgs = document.getElementById('ai-messages');
  var d = document.createElement('div');
  d.className = 'ai-msg bot';

  var inner = '';
  if (isSafety) {
    inner = '<div class="ai-bubble" style="padding:0;background:transparent;">'
          + '<div class="ai-safety-card">' + aiEscape(text) + '</div>'
          + '</div>';
  } else {
    inner = '<div class="ai-bubble">' + aiEscape(text) + '</div>';
  }

  if (estimateData && !isSafety) {
    inner += buildAIEstCard(estimateData);
  }
  d.innerHTML = inner;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function buildAIEstCard(est) {
  var priceLabel = est.is_estimate ? 'Starting from' : 'Fixed price';
  var totalLabel = est.is_estimate ? 'Estimate total' : 'Total';
  var h = '<div class="ai-estimate-card">';
  h += '<div class="est-header">Price Estimate</div>';
  h += '<div class="ai-estimate-row"><span>' + aiEscape(est.service_name) + '</span><span></span></div>';
  h += '<div class="ai-estimate-row"><span>' + priceLabel + '</span>'
     + '<span>Rs ' + est.base_price.toLocaleString() + '</span></div>';
  if (est.quantity > 1) {
    h += '<div class="ai-estimate-row"><span>Quantity</span><span>x ' + est.quantity + '</span></div>';
  }
  h += '<div class="ai-estimate-row total"><span>' + totalLabel + '</span>'
     + '<span>Rs ' + est.subtotal.toLocaleString() + '</span></div>';
  if (est.notes) {
    h += '<div style="font-size:12px;color:var(--text-muted);margin-top:6px;">' + aiEscape(est.notes) + '</div>';
  }
  h += '<div class="ai-estimate-disclaimer">This is an estimate based on the information provided. '
     + 'The final price may change after inspection.</div>';
  // Determine category for booking prefill
  var cat = est.category === 'plumbing' ? 'Plumbing'
          : est.category === 'electrician' ? 'Electrician'
          : 'AC Services';
  h += '<button class="ai-estimate-book" onclick="aiGoBook(\'' + cat + '\')">'
     + 'Book This Service</button>';
  h += '</div>';
  return h;
}

function addAIUserMsg(text) {
  var msgs = document.getElementById('ai-messages');
  var d = document.createElement('div');
  d.className = 'ai-msg user';
  d.innerHTML = '<div class="ai-bubble">' + aiEscape(text) + '</div>';
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function aiShowTyping() {
  var msgs = document.getElementById('ai-messages');
  var d = document.createElement('div');
  d.className = 'ai-msg bot';
  d.id = 'ai-typing-indicator';
  d.innerHTML = '<div class="ai-bubble ai-typing"><span></span><span></span><span></span></div>';
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function aiHideTyping() {
  var el = document.getElementById('ai-typing-indicator');
  if (el) el.remove();
}

function aiSetError(msg) {
  var b = document.getElementById('ai-error-banner');
  if (msg) { b.textContent = msg; b.style.display = 'block'; }
  else { b.style.display = 'none'; }
}

function aiHideStarters() {
  var s = document.getElementById('ai-starters');
  if (s) s.style.display = 'none';
}

function aiGoBook(cat) {
  showPage('booking');
  toggleAIChat();
  bookService(cat);
  toast('Service pre-selected — complete your booking below.', 'success');
}

/* ── send ── */
function aiSend() {
  if (aiLoading) return;
  var input = document.getElementById('ai-input');
  var msg = input.value.trim();
  if (!msg) { input.focus(); return; }
  if (msg.length > 1000) { aiSetError('Message too long (max 1000 characters).'); return; }

  aiHideStarters();
  addAIUserMsg(msg);
  aiHistory.push({role:'user', content:msg});
  input.value = '';
  input.style.height = 'auto';
  aiSetError('');
  aiLoading = true;
  document.getElementById('ai-send').disabled = true;
  input.disabled = true;
  document.getElementById('ai-status-text').textContent = 'Thinking...';
  aiShowTyping();

  var payload = JSON.stringify({message: msg, history: aiHistory.slice(-10)});
  var xhr = new XMLHttpRequest();
  xhr.open('POST', AI_BACKEND + '/api/chat', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.timeout = 70000;

  xhr.onload = function() {
    aiHideTyping();
    try {
      var data = JSON.parse(xhr.responseText);
      if (!data.success) {
        addAIBotMsg(data.error ||
          'Sorry, I ran into an issue. Please contact us via WhatsApp: 0331-4447719.', null, false);
      } else if (data.is_safety_alert) {
        addAIBotMsg(data.reply, null, true);
      } else {
        addAIBotMsg(data.reply, data.estimate, false);
        if (data.reply) aiHistory.push({role:'assistant', content:data.reply});
      }
    } catch(e) {
      addAIBotMsg('Something went wrong parsing the response. Please try again.', null, false);
    }
    aiDone();
  };
  xhr.ontimeout = function() {
    aiHideTyping();
    addAIBotMsg(
      'The AI took too long to respond. Please try rephrasing your question '
      + 'or contact us via WhatsApp: 0331-4447719.', null, false
    );
    aiDone();
  };
  xhr.onerror = function() {
    aiHideTyping();
    addAIBotMsg(
      'Cannot connect to the AI backend. Make sure it is running: '
      + 'cd backend && python -m uvicorn main:app --reload', null, false
    );
    aiSetError('Backend offline. Run: cd backend && python -m uvicorn main:app');
    aiDone();
  };
  xhr.send(payload);
}

function aiDone() {
  aiLoading = false;
  document.getElementById('ai-send').disabled = false;
  document.getElementById('ai-input').disabled = false;
  document.getElementById('ai-status-text').textContent = 'Home services assistant';
  document.getElementById('ai-input').focus();
}

/* ── init ── */
document.addEventListener('DOMContentLoaded', function() {
  /* auto-resize textarea */
  var inp = document.getElementById('ai-input');
  if (!inp) return;
  inp.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 80) + 'px';
  });
  inp.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); aiSend(); }
  });
  document.getElementById('ai-send').addEventListener('click', aiSend);

  /* starter chips */
  document.querySelectorAll('.ai-starter-chip').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var msg = btn.getAttribute('data-msg');
      if (msg) {
        inp.value = msg;
        aiSend();
      }
    });
    btn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
    });
  });

  /* badge hint */
  setTimeout(function() {
    if (!aiOpen) {
      var badge = document.getElementById('ai-chat-badge');
      if (badge) { badge.style.display = 'flex'; }
    }
  }, 4000);
});
</script>
"""

injection = "\n<!-- ══ HOMIRA AI CHATBOT ══ -->\n" + CSS + "\n" + HTML + "\n" + JS + "\n"

# Inject before </body>
injection_point = original.rfind('</body>')
if injection_point == -1:
    raise RuntimeError("</body> not found in source HTML")

modified = original[:injection_point] + injection + original[injection_point:]

os.makedirs(os.path.dirname(DEST), exist_ok=True)
with open(DEST, 'w', encoding='utf-8') as f:
    f.write(modified)

print(f"Done. Output: {DEST} ({len(modified):,} chars)")
