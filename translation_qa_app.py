import streamlit as st
import json
import re

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Translation QA · Thai Language Studio",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────
# Custom CSS  (editorial / refined dark theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Sans+Thai:wght@300;400;500&family=IBM+Plex+Mono&display=swap');

/* ── root palette ── */
:root {
  --bg:        #0d0f14;
  --surface:   #161920;
  --border:    #2a2d38;
  --accent:    #e8c96a;
  --accent2:   #6ae8c0;
  --danger:    #e86a6a;
  --text:      #e8e6df;
  --muted:     #7a7d8a;
  --radius:    10px;
}

/* ── global ── */
html, body, [class*="css"] {
  background: var(--bg);
  color: var(--text);
  font-family: 'IBM Plex Sans Thai', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── hero banner ── */
.hero {
  background: linear-gradient(135deg, #161920 0%, #0d1520 60%, #0d0f14 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2.5rem 3rem;
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: "";
  position: absolute;
  top: -60px; right: -60px;
  width: 220px; height: 220px;
  background: radial-gradient(circle, rgba(232,201,106,0.12) 0%, transparent 70%);
  border-radius: 50%;
}
.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.6rem;
  font-weight: 900;
  color: var(--accent);
  line-height: 1.1;
  margin: 0;
}
.hero-sub {
  font-size: 0.95rem;
  color: var(--muted);
  margin-top: 0.5rem;
  letter-spacing: 0.04em;
}

/* ── section labels ── */
.sec-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.4rem;
  display: block;
}

/* ── score card ── */
.score-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.score-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  position: relative;
  overflow: hidden;
}
.score-card-label {
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
}
.score-card-name {
  font-size: 1rem;
  font-weight: 500;
  color: var(--text);
  margin: 0.2rem 0 0.8rem;
}
.score-pill {
  display: inline-block;
  padding: 0.25rem 0.9rem;
  border-radius: 999px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 700;
}
.pill-5 { background: #1a3d2b; color: #6ae8a0; border: 1px solid #6ae8a0; }
.pill-4 { background: #1e3a1a; color: #9de86a; border: 1px solid #9de86a; }
.pill-3 { background: #3a3010; color: var(--accent); border: 1px solid var(--accent); }
.pill-2 { background: #3a1f10; color: #e8996a; border: 1px solid #e8996a; }
.pill-1 { background: #3a1010; color: var(--danger); border: 1px solid var(--danger); }

.score-bar-bg {
  background: var(--border);
  border-radius: 999px;
  height: 5px;
  margin-top: 0.7rem;
}
.score-bar {
  height: 5px;
  border-radius: 999px;
  transition: width 0.6s ease;
}

/* ── total score ── */
.total-box {
  background: var(--surface);
  border: 1px solid var(--accent);
  border-radius: var(--radius);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}
.total-num {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--accent);
  line-height: 1;
}
.total-meta { flex: 1; }
.total-label {
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
}
.total-verdict {
  font-size: 1.1rem;
  font-weight: 500;
  margin-top: 0.2rem;
}

/* ── comment block ── */
.comment-block {
  background: var(--surface);
  border-left: 3px solid var(--accent2);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 1.2rem 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  line-height: 1.8;
}
.fix-block {
  background: var(--surface);
  border-left: 3px solid var(--accent);
  border-radius: 0 var(--radius) var(--radius) 0;
  padding: 1.2rem 1.5rem;
  margin-bottom: 1rem;
  font-size: 0.95rem;
  line-height: 1.8;
}
.detail-block {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.2rem 1.5rem;
  margin-bottom: 0.8rem;
}
.detail-header {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.5rem;
}

/* ── divider ── */
.rule { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── button ── */
div.stButton > button {
  background: var(--accent);
  color: #0d0f14;
  font-family: 'IBM Plex Sans Thai', sans-serif;
  font-weight: 700;
  font-size: 1rem;
  padding: 0.7rem 2rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  width: 100%;
  transition: opacity 0.2s;
}
div.stButton > button:hover { opacity: 0.85; }

/* ── text areas ── */
textarea {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  font-family: 'IBM Plex Sans Thai', sans-serif !important;
  font-size: 0.95rem !important;
  line-height: 1.7 !important;
}
textarea:focus { border-color: var(--accent) !important; box-shadow: none !important; }

/* ── spinner override ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── expander ── */
details { background: var(--surface) !important; border-radius: var(--radius) !important; }
summary { color: var(--accent) !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Hero
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title">Translation QA</p>
  <p class="hero-sub">ระบบตรวจสอบคุณภาพการแปล · Thai Language Studio · Powered by Claude AI</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Rubric reference (collapsible)
# ─────────────────────────────────────────────
with st.expander("📋  ดู RUBRIC การตรวจคำแปล"):
    st.markdown("""
**1. Accuracy (ความถูกต้องของความหมาย)**
- แปลครบทุกประโยค ไม่มีตกหล่น
- ไม่เพิ่มเนื้อหาที่ไม่มีในต้นฉบับ
- ความหมายตรงกับต้นฉบับ ไม่บิดเบือน

**2. Terminology (การใช้คำศัพท์เฉพาะทาง)**
- ใช้คำศัพท์ตรงตาม glossary บริษัท
- คำที่อยู่ใน glossary ต้องใช้คำไทยที่กำหนด ห้ามทับศัพท์
- คำเฉพาะทางที่ไม่อยู่ใน glossary ให้ใช้ตามมาตรฐานราชบัณฑิต

**3. Register (ระดับภาษา)**
- ใช้ภาษาทางการ สุภาพ
- ใช้สรรพนาม "ท่าน" สำหรับเอกสารถึงลูกค้า (ห้ามใช้ "คุณ")
- ห้ามใช้คำลงท้าย "ค่ะ/ครับ/นะคะ" ในเอกสารทางการ
- ห้ามใช้คำทับศัพท์ที่มีคำไทยใช้แทนได้

**4. Fluency (ความลื่นไหล)**
- อ่านเป็นภาษาไทยธรรมชาติ ไม่เป็นภาษาแปล
- ประโยคไม่ยาวเกิน 40 คำต่อประโยค
- ลำดับคำเป็นแบบไทย ไม่ใช่ลำดับคำแบบอังกฤษ

**เกณฑ์คะแนน:** 5=ยอดเยี่ยม · 4=ดี · 3=พอใช้ · 2=ต้องแก้ไข · 1=ไม่ผ่าน
    """)


# ─────────────────────────────────────────────
# Input area
# ─────────────────────────────────────────────
col_src, col_tgt = st.columns(2, gap="large")

with col_src:
    st.markdown('<span class="sec-label">SOURCE · ต้นฉบับภาษาอังกฤษ</span>', unsafe_allow_html=True)
    source_text = st.text_area(
        label="source",
        label_visibility="collapsed",
        placeholder="Paste English source text here…",
        height=280,
        key="source",
    )

with col_tgt:
    st.markdown('<span class="sec-label">TRANSLATION · คำแปลภาษาไทย</span>', unsafe_allow_html=True)
    target_text = st.text_area(
        label="target",
        label_visibility="collapsed",
        placeholder="วางคำแปลภาษาไทยที่นี่…",
        height=280,
        key="target",
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run_btn = st.button("🔍  ตรวจสอบคุณภาพการแปล", use_container_width=True)


# ─────────────────────────────────────────────
# Claude API call
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """คุณคือผู้เชี่ยวชาญตรวจสอบคุณภาพการแปล (Translation QA Specialist) สำหรับบริษัทแปลภาษาไทยชั้นนำ
คุณต้องตรวจสอบตามเกณฑ์ RUBRIC 4 ด้านต่อไปนี้อย่างละเอียดและเป็นกลาง:

1. Accuracy (ความถูกต้องของความหมาย)
   - แปลครบทุกประโยค ไม่มีตกหล่น
   - ไม่เพิ่มเนื้อหาที่ไม่มีในต้นฉบับ
   - ความหมายตรงกับต้นฉบับ ไม่บิดเบือน

2. Terminology (การใช้คำศัพท์เฉพาะทาง)
   - ใช้คำศัพท์ตรงตาม glossary บริษัท (ตัวอย่าง: "contract" = "สัญญา", "invoice" = "ใบแจ้งหนี้", "payment" = "การชำระเงิน", "deadline" = "กำหนดเวลา", "agreement" = "ข้อตกลง", "party" = "คู่สัญญา", "clause" = "ข้อกำหนด", "obligation" = "พันธะ", "liability" = "ความรับผิด", "confidential" = "ข้อมูลความลับ")
   - คำที่อยู่ใน glossary ต้องใช้คำไทยที่กำหนด ห้ามทับศัพท์
   - คำเฉพาะทางที่ไม่อยู่ใน glossary ให้ใช้ตามมาตรฐานราชบัณฑิต

3. Register (ระดับภาษา)
   - ใช้ภาษาทางการ สุภาพ
   - ใช้สรรพนาม "ท่าน" สำหรับเอกสารถึงลูกค้า (ห้ามใช้ "คุณ")
   - ห้ามใช้คำลงท้าย "ค่ะ/ครับ/นะคะ" ในเอกสารทางการ
   - ห้ามใช้คำทับศัพท์ที่มีคำไทยใช้แทนได้

4. Fluency (ความลื่นไหล)
   - อ่านเป็นภาษาไทยธรรมชาติ ไม่เป็นภาษาแปล
   - ประโยคไม่ยาวเกิน 40 คำต่อประโยค
   - ลำดับคำเป็นแบบไทย ไม่ใช่ลำดับคำแบบอังกฤษ

เกณฑ์คะแนน (1-5):
5 = ยอดเยี่ยม ไม่มีจุดต้องแก้
4 = ดี มีจุดเล็กน้อยที่ปรับได้
3 = พอใช้ มีจุดที่ควรแก้บ้าง
2 = ต้องแก้ไข มีปัญหาชัดเจน
1 = ไม่ผ่าน ต้องแปลใหม่

ตอบกลับเป็น JSON เท่านั้น โดยไม่มี markdown backticks หรือข้อความอื่นใด ใช้โครงสร้างนี้:
{
  "accuracy": {
    "score": <int 1-5>,
    "comment": "<วิเคราะห์ด้าน accuracy อย่างละเอียด 2-4 ประโยค>",
    "issues": ["<ปัญหาที่พบ 1>", "<ปัญหาที่พบ 2>"],
    "suggestions": ["<ข้อแนะนำ 1>", "<ข้อแนะนำ 2>"]
  },
  "terminology": {
    "score": <int 1-5>,
    "comment": "<วิเคราะห์ด้าน terminology อย่างละเอียด 2-4 ประโยค>",
    "issues": ["<ปัญหาที่พบ 1>"],
    "suggestions": ["<ข้อแนะนำ 1>"]
  },
  "register": {
    "score": <int 1-5>,
    "comment": "<วิเคราะห์ด้าน register อย่างละเอียด 2-4 ประโยค>",
    "issues": ["<ปัญหาที่พบ 1>"],
    "suggestions": ["<ข้อแนะนำ 1>"]
  },
  "fluency": {
    "score": <int 1-5>,
    "comment": "<วิเคราะห์ด้าน fluency อย่างละเอียด 2-4 ประโยค>",
    "issues": ["<ปัญหาที่พบ 1>"],
    "suggestions": ["<ข้อแนะนำ 1>"]
  },
  "overall_comment": "<สรุปภาพรวมงานแปล 3-5 ประโยค>",
  "revised_suggestion": "<ตัวอย่างส่วนที่ควรแก้ไข หรือ 'งานแปลอยู่ในเกณฑ์ดี ไม่จำเป็นต้องแก้ไขมาก' ถ้าคะแนนสูง>"
}"""


def get_api_key() -> str:
    """Read API key from Streamlit secrets or environment variable."""
    import os
    try:
        return st.secrets["anthropic"]["api_key"]
    except Exception:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            st.error("ไม่พบ API Key — กรุณาตั้งค่า Streamlit Secrets หรือ environment variable ANTHROPIC_API_KEY")
            st.stop()
        return key


def call_claude(source: str, target: str) -> dict:
    import urllib.request

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1500,
        "system": SYSTEM_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": f"ต้นฉบับภาษาอังกฤษ:\n{source}\n\n---\n\nคำแปลภาษาไทย:\n{target}"
            }
        ]
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key": get_api_key(),
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    raw = "".join(
        block.get("text", "") for block in data.get("content", [])
        if block.get("type") == "text"
    )
    # strip possible ```json fences
    raw = re.sub(r"^```json\s*|```\s*$", "", raw.strip(), flags=re.MULTILINE).strip()
    return json.loads(raw)


# ─────────────────────────────────────────────
# Helpers for rendering
# ─────────────────────────────────────────────
SCORE_LABELS = {5: "ยอดเยี่ยม", 4: "ดี", 3: "พอใช้", 2: "ต้องแก้ไข", 1: "ไม่ผ่าน"}
SCORE_COLORS = {5: "#6ae8a0", 4: "#9de86a", 3: "#e8c96a", 2: "#e8996a", 1: "#e86a6a"}
SCORE_BG     = {5: "#1a3d2b", 4: "#1e3a1a", 3: "#3a3010", 2: "#3a1f10", 1: "#3a1010"}

RUBRIC_NAMES = {
    "accuracy":    ("01", "Accuracy", "ความถูกต้องของความหมาย"),
    "terminology": ("02", "Terminology", "การใช้คำศัพท์เฉพาะทาง"),
    "register":    ("03", "Register", "ระดับภาษา"),
    "fluency":     ("04", "Fluency", "ความลื่นไหล"),
}


def score_pill_html(score: int) -> str:
    color = SCORE_COLORS.get(score, "#e8c96a")
    bg    = SCORE_BG.get(score, "#3a3010")
    label = SCORE_LABELS.get(score, "")
    return (
        f'<span class="score-pill" '
        f'style="background:{bg};color:{color};border:1px solid {color};">'
        f'{score}/5 · {label}</span>'
    )


def bar_html(score: int) -> str:
    pct   = score / 5 * 100
    color = SCORE_COLORS.get(score, "#e8c96a")
    return (
        f'<div class="score-bar-bg">'
        f'<div class="score-bar" style="width:{pct}%;background:{color};"></div>'
        f'</div>'
    )


def render_score_card(key: str, data: dict) -> str:
    num, en, th = RUBRIC_NAMES[key]
    score = data["score"]
    return f"""
<div class="score-card">
  <div class="score-card-label">{num} · {en}</div>
  <div class="score-card-name">{th}</div>
  {score_pill_html(score)}
  {bar_html(score)}
</div>"""


def verdict(avg: float) -> str:
    if avg >= 4.5: return "🏆 งานแปลคุณภาพสูงมาก"
    if avg >= 3.5: return "✅ งานแปลผ่านเกณฑ์ มีจุดปรับปรุงเล็กน้อย"
    if avg >= 2.5: return "⚠️ งานแปลพอใช้ ควรแก้ไขก่อนส่งมอบ"
    if avg >= 1.5: return "❌ งานแปลต้องแก้ไขมาก"
    return "🚫 งานแปลไม่ผ่านเกณฑ์ ต้องแปลใหม่"


# ─────────────────────────────────────────────
# Main logic
# ─────────────────────────────────────────────
if run_btn:
    if not source_text.strip():
        st.warning("กรุณาใส่ต้นฉบับภาษาอังกฤษ")
    elif not target_text.strip():
        st.warning("กรุณาใส่คำแปลภาษาไทย")
    else:
        with st.spinner("กำลังวิเคราะห์งานแปล…"):
            try:
                result = call_claude(source_text, target_text)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
                st.stop()

        keys  = ["accuracy", "terminology", "register", "fluency"]
        scores = [result[k]["score"] for k in keys]
        avg    = sum(scores) / len(scores)

        st.markdown("<hr class='rule'>", unsafe_allow_html=True)
        st.markdown('<span class="sec-label">ผลการตรวจสอบ</span>', unsafe_allow_html=True)

        # ── Total score ──
        st.markdown(f"""
<div class="total-box">
  <div class="total-num">{avg:.1f}</div>
  <div class="total-meta">
    <div class="total-label">คะแนนเฉลี่ยรวม (เต็ม 5.0)</div>
    <div class="total-verdict">{verdict(avg)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Score cards grid ──
        cards_html = '<div class="score-grid">' + "".join(
            render_score_card(k, result[k]) for k in keys
        ) + "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        # ── Detail per dimension ──
        st.markdown('<span class="sec-label" style="margin-top:1rem;display:block;">รายละเอียดแต่ละด้าน</span>', unsafe_allow_html=True)

        for k in keys:
            num, en, th = RUBRIC_NAMES[k]
            d = result[k]
            issues_html = "".join(
                f'<li style="color:#e86a6a;margin-bottom:0.3rem;">{i}</li>'
                for i in (d.get("issues") or [])
            ) or '<li style="color:#6ae8a0;">ไม่พบปัญหา</li>'
            sugg_html = "".join(
                f'<li style="color:#e8c96a;margin-bottom:0.3rem;">{s}</li>'
                for s in (d.get("suggestions") or [])
            ) or '<li style="color:#7a7d8a;">ไม่มีข้อแนะนำเพิ่มเติม</li>'

            st.markdown(f"""
<div class="detail-block">
  <div class="detail-header">{num} · {en} · {th} &nbsp; {score_pill_html(d["score"])}</div>
  <p style="margin:0.5rem 0 0.8rem;line-height:1.8;font-size:0.95rem;">{d['comment']}</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
    <div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#e86a6a;margin-bottom:0.4rem;">ปัญหาที่พบ</div>
      <ul style="margin:0;padding-left:1.2rem;">{issues_html}</ul>
    </div>
    <div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;color:#e8c96a;margin-bottom:0.4rem;">ข้อแนะนำ</div>
      <ul style="margin:0;padding-left:1.2rem;">{sugg_html}</ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        # ── Overall comment ──
        st.markdown('<span class="sec-label" style="margin-top:1.5rem;display:block;">สรุปภาพรวม</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="comment-block">{result["overall_comment"]}</div>', unsafe_allow_html=True)

        # ── Revision suggestion ──
        st.markdown('<span class="sec-label">ตัวอย่างการแก้ไข</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="fix-block">{result["revised_suggestion"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #2a2d38;
            text-align:center;font-family:'IBM Plex Mono',monospace;
            font-size:0.7rem;color:#3a3d4a;letter-spacing:0.08em;">
  TRANSLATION QA · THAI LANGUAGE STUDIO · POWERED BY CLAUDE AI
</div>
""", unsafe_allow_html=True)
