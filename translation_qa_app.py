import streamlit as st
import json
import re
import csv
import io

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Translation QA · Thai Language Studio",
    page_icon="🔍",
    layout="wide",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Sans+Thai:wght@300;400;500&family=IBM+Plex+Mono&display=swap');

:root {
  --bg:       #0d0f14;
  --surface:  #161920;
  --surface2: #1d2028;
  --border:   #2a2d38;
  --accent:   #e8c96a;
  --accent2:  #6ae8c0;
  --danger:   #e86a6a;
  --ok:       #6ae8a0;
  --text:     #e8e6df;
  --muted:    #7a7d8a;
  --radius:   10px;
}

html, body, [class*="css"] {
  background: var(--bg);
  color: var(--text);
  font-family: 'IBM Plex Sans Thai', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

/* ── hero ── */
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

/* ── labels ── */
.sec-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.7rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 0.4rem;
  display: block;
}

/* ── glossary zone ── */
.glossary-zone {
  background: var(--surface);
  border: 1.5px dashed var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 1.8rem;
  margin-bottom: 1rem;
}
.glossary-loaded {
  background: var(--surface);
  border: 1.5px solid var(--accent2);
  border-radius: var(--radius);
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.gcount {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 900;
  color: var(--accent2);
  line-height: 1;
}
.gmeta { flex: 1; }
.gmeta-label {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
}

/* ── glossary table ── */
.g-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.g-table th {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  border-bottom: 1px solid var(--border);
  padding: 0.5rem 0.8rem;
  text-align: left;
}
.g-table td { padding: 0.45rem 0.8rem; border-bottom: 1px solid #1d2028; line-height: 1.5; }
.g-table tr:last-child td { border-bottom: none; }
.g-table tr:hover td { background: #1d2028; }
.en-term { font-family: 'IBM Plex Mono', monospace; color: var(--accent); }
.th-term { color: var(--text); }
.g-note  { color: var(--muted); font-size: 0.82rem; }

/* ── glossary check results ── */
.gcheck-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.4rem;
  margin-bottom: 0.7rem;
}
.gcheck-pass { border-left: 4px solid var(--ok); }
.gcheck-fail { border-left: 4px solid var(--danger); }
.gcheck-tag {
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.15rem 0.6rem;
  border-radius: 999px;
  margin-bottom: 0.5rem;
}
.tag-pass { background: #1a3d2b; color: var(--ok); }
.tag-fail { background: #3a1010; color: var(--danger); }
.gcheck-pair {
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
  flex-wrap: wrap;
}
.gcheck-en { font-family: 'IBM Plex Mono', monospace; color: var(--accent); font-size: 0.9rem; }
.gcheck-arrow { color: var(--muted); }
.gcheck-expected { color: var(--ok); font-weight: 500; }
.gcheck-context { font-size: 0.82rem; color: var(--muted); margin-top: 0.3rem; font-style: italic; }

/* ── stat chips ── */
.stat-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.stat-chip {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 0.8rem 1.2rem;
  flex: 1;
  min-width: 110px;
  text-align: center;
}
.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  font-weight: 900;
  line-height: 1;
}
.stat-lbl {
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 0.2rem;
}

/* ── score cards ── */
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
}
.score-card-label {
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'IBM Plex Mono', monospace;
}
.score-card-name { font-size: 1rem; font-weight: 500; color: var(--text); margin: 0.2rem 0 0.8rem; }
.score-pill {
  display: inline-block;
  padding: 0.25rem 0.9rem;
  border-radius: 999px;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 1rem;
  font-weight: 700;
}
.score-bar-bg { background: var(--border); border-radius: 999px; height: 5px; margin-top: 0.7rem; }
.score-bar    { height: 5px; border-radius: 999px; }

/* ── total ── */
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
.total-num { font-family: 'Playfair Display', serif; font-size: 3.5rem; font-weight: 900; color: var(--accent); line-height: 1; }
.total-meta { flex: 1; }
.total-label { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); font-family: 'IBM Plex Mono', monospace; }
.total-verdict { font-size: 1.1rem; font-weight: 500; margin-top: 0.2rem; }

/* ── comment / fix blocks ── */
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
.detail-block { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.2rem 1.5rem; margin-bottom: 0.8rem; }
.detail-header { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--accent); margin-bottom: 0.5rem; }

/* ── misc ── */
.rule { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

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
.stSpinner > div { border-top-color: var(--accent) !important; }
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

with st.expander("📋  ดู RUBRIC การตรวจคำแปล"):
    st.markdown("""
**1. Accuracy** · ความถูกต้องของความหมาย — แปลครบ ไม่ตกหล่น ไม่บิดเบือน

**2. Terminology** · การใช้คำศัพท์เฉพาะทาง — ใช้คำตาม glossary บริษัท / ราชบัณฑิต

**3. Register** · ระดับภาษา — ทางการ สุภาพ ใช้ "ท่าน" (ห้าม "คุณ") ห้ามคำลงท้าย "ค่ะ/ครับ/นะคะ"

**4. Fluency** · ความลื่นไหล — ภาษาไทยธรรมชาติ ≤40 คำ/ประโยค ลำดับคำแบบไทย

**เกณฑ์:** 5=ยอดเยี่ยม · 4=ดี · 3=พอใช้ · 2=ต้องแก้ · 1=ไม่ผ่าน
    """)


# ═══════════════════════════════════════════════
# GLOSSARY UPLOAD
# ═══════════════════════════════════════════════
st.markdown('<span class="sec-label">📚 Glossary · อัปโหลด glossary บริษัท (ไม่บังคับ)</span>',
            unsafe_allow_html=True)

glossary: dict = {}  # { "english_lower": {"thai": "...", "note": "...", "display_en": "..."} }

uploaded_glossary = st.file_uploader(
    "อัปโหลดไฟล์ glossary (.csv หรือ .tsv) — คอลัมน์: english, thai [, note]",
    type=["csv", "tsv"],
    label_visibility="collapsed",
)

if uploaded_glossary:
    try:
        raw_bytes = uploaded_glossary.read()
        try:
            content = raw_bytes.decode("utf-8-sig")
        except UnicodeDecodeError:
            content = raw_bytes.decode("cp874")

        dialect = "excel-tab" if uploaded_glossary.name.endswith(".tsv") else "excel"
        reader  = csv.DictReader(io.StringIO(content), dialect=dialect)

        for row in reader:
            keys_lower = {k.lower().strip(): v.strip() for k, v in row.items() if k}
            en_raw = (
                keys_lower.get("english") or keys_lower.get("en") or
                keys_lower.get("source")  or keys_lower.get("english term") or ""
            )
            th = (
                keys_lower.get("thai") or keys_lower.get("th") or
                keys_lower.get("target") or keys_lower.get("thai term") or ""
            )
            note = (
                keys_lower.get("note") or keys_lower.get("notes") or
                keys_lower.get("หมายเหตุ") or ""
            )
            if en_raw and th:
                glossary[en_raw.lower()] = {
                    "thai":       th,
                    "note":       note,
                    "display_en": en_raw,
                }

        if glossary:
            st.markdown(f"""
<div class="glossary-loaded">
  <div class="gcount">{len(glossary)}</div>
  <div class="gmeta">
    <div class="gmeta-label">คำศัพท์ใน glossary</div>
    <div style="font-size:0.85rem;color:var(--accent2);margin-top:0.1rem;">
      {uploaded_glossary.name} · โหลดสำเร็จ ✓
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

            with st.expander(f"🔎  ดู glossary ทั้งหมด ({len(glossary)} รายการ)"):
                rows_html = "".join(
                    f'<tr><td class="en-term">{d["display_en"]}</td>'
                    f'<td class="th-term">{d["thai"]}</td>'
                    f'<td class="g-note">{d["note"]}</td></tr>'
                    for d in list(glossary.values())[:200]
                )
                st.markdown(f"""
<div style="max-height:320px;overflow-y:auto;">
<table class="g-table">
  <thead><tr><th>English Term</th><th>คำแปลที่กำหนด</th><th>หมายเหตุ</th></tr></thead>
  <tbody>{rows_html}</tbody>
</table>
</div>
""", unsafe_allow_html=True)
                if len(glossary) > 200:
                    st.caption(f"แสดง 200 จาก {len(glossary)} รายการ")
        else:
            st.warning("ไม่พบข้อมูลใน glossary — ตรวจสอบชื่อคอลัมน์: english, thai [, note]")

    except Exception as e:
        st.error(f"ไม่สามารถอ่านไฟล์ glossary: {e}")
else:
    st.markdown("""
<div class="glossary-zone">
  <div style="font-size:0.85rem;color:var(--muted);text-align:center;">
    📂 &nbsp; ลาก&วางไฟล์ .csv/.tsv หรือกดปุ่มด้านบนเพื่ออัปโหลด glossary<br>
    <span style="font-size:0.75rem;font-family:'IBM Plex Mono',monospace;color:#3a3d4a;">
      คอลัมน์ที่รองรับ: english / thai / note &nbsp;·&nbsp;
      หากไม่อัปโหลด ระบบจะใช้ glossary ตัวอย่างแทน
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

    sample_csv = (
        "english,thai,note\n"
        "contract,สัญญา,\n"
        "invoice,ใบแจ้งหนี้,\n"
        "payment,การชำระเงิน,\n"
        "deadline,กำหนดเวลา,\n"
        "agreement,ข้อตกลง,\n"
        "party,คู่สัญญา,เฉพาะบริบทกฎหมาย\n"
        "clause,ข้อกำหนด,\n"
        "obligation,พันธะ,\n"
        "liability,ความรับผิด,\n"
        "confidential,ข้อมูลความลับ,\n"
    )
    st.download_button(
        "⬇️  ดาวน์โหลด glossary ตัวอย่าง (.csv)",
        data=sample_csv,
        file_name="glossary_sample.csv",
        mime="text/csv",
    )

st.markdown("<hr class='rule'>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# SOURCE / TARGET INPUT
# ═══════════════════════════════════════════════
col_src, col_tgt = st.columns(2, gap="large")

with col_src:
    st.markdown('<span class="sec-label">SOURCE · ต้นฉบับภาษาอังกฤษ</span>', unsafe_allow_html=True)
    source_text = st.text_area(
        label="source", label_visibility="collapsed",
        placeholder="Paste English source text here…",
        height=260, key="source",
    )

with col_tgt:
    st.markdown('<span class="sec-label">TRANSLATION · คำแปลภาษาไทย</span>', unsafe_allow_html=True)
    target_text = st.text_area(
        label="target", label_visibility="collapsed",
        placeholder="วางคำแปลภาษาไทยที่นี่…",
        height=260, key="target",
    )

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run_btn = st.button("🔍  ตรวจสอบคุณภาพการแปล", use_container_width=True)


# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════
SCORE_LABELS = {5: "ยอดเยี่ยม", 4: "ดี", 3: "พอใช้", 2: "ต้องแก้ไข", 1: "ไม่ผ่าน"}
SCORE_COLORS = {5: "#6ae8a0", 4: "#9de86a", 3: "#e8c96a", 2: "#e8996a", 1: "#e86a6a"}
SCORE_BG     = {5: "#1a3d2b", 4: "#1e3a1a", 3: "#3a3010", 2: "#3a1f10", 1: "#3a1010"}

RUBRIC_NAMES = {
    "accuracy":    ("01", "Accuracy",    "ความถูกต้องของความหมาย"),
    "terminology": ("02", "Terminology", "การใช้คำศัพท์เฉพาะทาง"),
    "register":    ("03", "Register",    "ระดับภาษา"),
    "fluency":     ("04", "Fluency",     "ความลื่นไหล"),
}


def score_pill_html(score: int) -> str:
    c = SCORE_COLORS.get(score, "#e8c96a")
    b = SCORE_BG.get(score, "#3a3010")
    l = SCORE_LABELS.get(score, "")
    return (f'<span class="score-pill" style="background:{b};color:{c};border:1px solid {c};">'
            f'{score}/5 · {l}</span>')


def bar_html(score: int) -> str:
    pct = score / 5 * 100
    c   = SCORE_COLORS.get(score, "#e8c96a")
    return (f'<div class="score-bar-bg">'
            f'<div class="score-bar" style="width:{pct}%;background:{c};"></div></div>')


def render_score_card(key: str, data: dict) -> str:
    num, en, th = RUBRIC_NAMES[key]
    s = data["score"]
    return (f'<div class="score-card">'
            f'<div class="score-card-label">{num} · {en}</div>'
            f'<div class="score-card-name">{th}</div>'
            f'{score_pill_html(s)}{bar_html(s)}</div>')


def verdict(avg: float) -> str:
    if avg >= 4.5: return "🏆 งานแปลคุณภาพสูงมาก"
    if avg >= 3.5: return "✅ งานแปลผ่านเกณฑ์ มีจุดปรับปรุงเล็กน้อย"
    if avg >= 2.5: return "⚠️ งานแปลพอใช้ ควรแก้ไขก่อนส่งมอบ"
    if avg >= 1.5: return "❌ งานแปลต้องแก้ไขมาก"
    return "🚫 งานแปลไม่ผ่านเกณฑ์ ต้องแปลใหม่"


# ═══════════════════════════════════════════════
# GLOSSARY PRE-CHECK (deterministic, rule-based)
# ═══════════════════════════════════════════════
def glossary_precheck(source: str, target: str, glossary: dict) -> list[dict]:
    """
    For every glossary term found in the source text,
    verify the required Thai equivalent appears in the target.
    """
    results = []
    source_lower = source.lower()

    for en_lower, data in glossary.items():
        # word-boundary match in source
        pattern = r'(?<![a-z])' + re.escape(en_lower) + r'(?![a-z])'
        if not re.search(pattern, source_lower):
            continue

        found_in_target = data["thai"] in target
        results.append({
            "en":            data["display_en"],
            "expected_thai": data["thai"],
            "found":         found_in_target,
            "note":          data["note"],
        })

    return results


# ═══════════════════════════════════════════════
# API
# ═══════════════════════════════════════════════
def get_api_key() -> str:
    import os
    try:
        return st.secrets["anthropic"]["api_key"]
    except Exception:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            st.error("ไม่พบ API Key — ตั้งค่า Streamlit Secrets หรือ env var ANTHROPIC_API_KEY")
            st.stop()
        return key


def build_system_prompt(glossary: dict) -> str:
    if glossary:
        gl_lines = "\n".join(
            f'  - "{d["display_en"]}" → "{d["thai"]}"' + (f' ({d["note"]})' if d["note"] else "")
            for d in list(glossary.values())[:100]
        )
        gl_block = f"Glossary บริษัท (ต้องใช้คำเหล่านี้เสมอ):\n{gl_lines}"
    else:
        gl_block = (
            'Glossary บริษัท (ตัวอย่าง): "contract"=สัญญา, "invoice"=ใบแจ้งหนี้, '
            '"payment"=การชำระเงิน, "deadline"=กำหนดเวลา, "agreement"=ข้อตกลง, '
            '"party"=คู่สัญญา, "clause"=ข้อกำหนด, "obligation"=พันธะ, '
            '"liability"=ความรับผิด, "confidential"=ข้อมูลความลับ'
        )

    return f"""คุณคือผู้เชี่ยวชาญตรวจสอบคุณภาพการแปล (Translation QA Specialist) สำหรับบริษัทแปลภาษาไทยชั้นนำ

{gl_block}

ตรวจสอบตาม RUBRIC 4 ด้าน:
1. Accuracy — แปลครบ ไม่ตกหล่น ไม่เพิ่มเนื้อหา ความหมายตรง
2. Terminology — ใช้คำตาม glossary ข้างต้น / ราชบัณฑิต ห้ามทับศัพท์ที่มีคำไทยแทนได้
3. Register — ทางการ สุภาพ ใช้ "ท่าน" (ห้าม "คุณ") ห้ามคำลงท้าย "ค่ะ/ครับ/นะคะ"
4. Fluency — ภาษาไทยธรรมชาติ ≤40 คำ/ประโยค ลำดับคำแบบไทย

เกณฑ์คะแนน 1–5: 5=ยอดเยี่ยม 4=ดี 3=พอใช้ 2=ต้องแก้ 1=ไม่ผ่าน

ตอบเป็น JSON เท่านั้น ไม่มี backticks ไม่มีข้อความอื่น:
{{
  "accuracy":    {{"score":<1-5>,"comment":"<2-4 ประโยค>","issues":["..."],"suggestions":["..."]}},
  "terminology": {{"score":<1-5>,"comment":"<2-4 ประโยค>","issues":["..."],"suggestions":["..."]}},
  "register":    {{"score":<1-5>,"comment":"<2-4 ประโยค>","issues":["..."],"suggestions":["..."]}},
  "fluency":     {{"score":<1-5>,"comment":"<2-4 ประโยค>","issues":["..."],"suggestions":["..."]}},
  "overall_comment":    "<สรุปภาพรวม 3-5 ประโยค>",
  "revised_suggestion": "<ตัวอย่างการแก้ไข หรือ 'งานแปลอยู่ในเกณฑ์ดี'>"
}}"""


def call_claude(source: str, target: str, glossary: dict) -> dict:
    import urllib.request

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1800,
        "system": build_system_prompt(glossary),
        "messages": [{"role": "user", "content":
            f"ต้นฉบับภาษาอังกฤษ:\n{source}\n\n---\n\nคำแปลภาษาไทย:\n{target}"}],
    }

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type":      "application/json",
            "anthropic-version": "2023-06-01",
            "x-api-key":         get_api_key(),
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    raw = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    raw = re.sub(r"^```json\s*|```\s*$", "", raw.strip(), flags=re.MULTILINE).strip()
    return json.loads(raw)


# ═══════════════════════════════════════════════
# MAIN RUN
# ═══════════════════════════════════════════════
if run_btn:
    if not source_text.strip():
        st.warning("กรุณาใส่ต้นฉบับภาษาอังกฤษ")
    elif not target_text.strip():
        st.warning("กรุณาใส่คำแปลภาษาไทย")
    else:
        # Step 1 — Glossary pre-check (instant, no API)
        gcheck_results: list[dict] = []
        if glossary:
            gcheck_results = glossary_precheck(source_text, target_text, glossary)

        # Step 2 — Claude QA
        with st.spinner("กำลังวิเคราะห์งานแปล…"):
            try:
                result = call_claude(source_text, target_text, glossary)
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
                st.stop()

        st.markdown("<hr class='rule'>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # GLOSSARY CHECK RESULTS
        # ──────────────────────────────────────────
        if gcheck_results:
            st.markdown('<span class="sec-label">📚 ผลการตรวจ Glossary Compliance</span>',
                        unsafe_allow_html=True)

            n_total  = len(gcheck_results)
            n_pass   = sum(1 for r in gcheck_results if r["found"])
            n_fail   = n_total - n_pass
            pct      = int(n_pass / n_total * 100) if n_total else 0
            pct_color = "#6ae8a0" if n_fail == 0 else ("#e8c96a" if n_fail < 3 else "#e86a6a")

            st.markdown(f"""
<div class="stat-row">
  <div class="stat-chip">
    <div class="stat-num" style="color:#e8c96a;">{n_total}</div>
    <div class="stat-lbl">คำศัพท์ที่ตรวจ</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num" style="color:#6ae8a0;">{n_pass}</div>
    <div class="stat-lbl">ใช้ถูกต้อง</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num" style="color:#e86a6a;">{n_fail}</div>
    <div class="stat-lbl">ไม่ตรง Glossary</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num" style="color:{pct_color};">{pct}%</div>
    <div class="stat-lbl">Compliance Rate</div>
  </div>
</div>
""", unsafe_allow_html=True)

            # failures first
            for r in sorted(gcheck_results, key=lambda x: x["found"]):
                if r["found"]:
                    tag_cls = "tag-pass"
                    tag_txt = "✓ ถูกต้อง"
                    box_cls = "gcheck-pass"
                    status_html = (
                        f'พบ <span class="gcheck-expected">{r["expected_thai"]}</span> ในคำแปล ✓'
                    )
                else:
                    tag_cls = "tag-fail"
                    tag_txt = "✗ ไม่ตรง Glossary"
                    box_cls = "gcheck-fail"
                    status_html = (
                        f'ต้องใช้ <span class="gcheck-expected">{r["expected_thai"]}</span> '
                        f'— ไม่พบในคำแปล'
                    )
                note_html = (
                    f'<div class="gcheck-context">💡 {r["note"]}</div>' if r["note"] else ""
                )
                st.markdown(f"""
<div class="gcheck-box {box_cls}">
  <span class="gcheck-tag {tag_cls}">{tag_txt}</span>
  <div class="gcheck-pair">
    <span class="gcheck-en">{r["en"]}</span>
    <span class="gcheck-arrow">→</span>
    <span style="font-size:0.9rem;">{status_html}</span>
  </div>
  {note_html}
</div>
""", unsafe_allow_html=True)

            st.markdown("<hr class='rule'>", unsafe_allow_html=True)

        elif glossary:
            st.info("ℹ️  ไม่พบคำใน glossary ในต้นฉบับ — ข้ามการตรวจ glossary compliance")
            st.markdown("<hr class='rule'>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # RUBRIC QA RESULTS
        # ──────────────────────────────────────────
        st.markdown('<span class="sec-label">ผลการตรวจสอบ Rubric</span>', unsafe_allow_html=True)

        keys   = ["accuracy", "terminology", "register", "fluency"]
        scores = [result[k]["score"] for k in keys]
        avg    = sum(scores) / len(scores)

        st.markdown(f"""
<div class="total-box">
  <div class="total-num">{avg:.1f}</div>
  <div class="total-meta">
    <div class="total-label">คะแนนเฉลี่ยรวม (เต็ม 5.0)</div>
    <div class="total-verdict">{verdict(avg)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

        cards_html = '<div class="score-grid">' + "".join(
            render_score_card(k, result[k]) for k in keys
        ) + "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        st.markdown('<span class="sec-label" style="margin-top:1rem;display:block;">รายละเอียดแต่ละด้าน</span>',
                    unsafe_allow_html=True)

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
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;
                  text-transform:uppercase;color:#e86a6a;margin-bottom:0.4rem;">ปัญหาที่พบ</div>
      <ul style="margin:0;padding-left:1.2rem;">{issues_html}</ul>
    </div>
    <div>
      <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;letter-spacing:0.1em;
                  text-transform:uppercase;color:#e8c96a;margin-bottom:0.4rem;">ข้อแนะนำ</div>
      <ul style="margin:0;padding-left:1.2rem;">{sugg_html}</ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

        st.markdown('<span class="sec-label" style="margin-top:1.5rem;display:block;">สรุปภาพรวม</span>',
                    unsafe_allow_html=True)
        st.markdown(f'<div class="comment-block">{result["overall_comment"]}</div>',
                    unsafe_allow_html=True)

        st.markdown('<span class="sec-label">ตัวอย่างการแก้ไข</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="fix-block">{result["revised_suggestion"]}</div>',
                    unsafe_allow_html=True)


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
