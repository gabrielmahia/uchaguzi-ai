import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Uchaguzi AI — Elimu ya Uchaguzi", page_icon="🗳️", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0a16;color:#e8eaf6}
.u-card{background:#0d0d30;border:1px solid #283593;border-radius:10px;padding:14px 18px;margin:8px 0}
.important{background:#1a1000;border:1px solid #f57f17;border-radius:8px;padding:10px;margin:8px 0}
.stButton>button{background:#1565c0;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = """Wewe ni mshauri wa uchaguzi na haki za kiraia Kenya.
Toa habari za elimu kuhusu mchakato wa uchaguzi, IEBC, haki za mpiga kura, na wajibu wa raia.
Kuwa na usawa wa kisiasa kabisa. Usichukue upande wowote wa kisiasa. Toa ukweli tu."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🗳️ Uchaguzi AI")
st.markdown("**Elimu ya Uchaguzi na Haki za Kiraia Kenya**")
st.markdown('<div class="important">⚖️ Zana hii ni ya elimu ya kiraia tu. Haichukui upande wowote wa kisiasa. Maudhui yote yanategemea habari rasmi za IEBC na katiba ya Kenya.</div>', unsafe_allow_html=True)

tab1,tab2,tab3,tab4 = st.tabs(["📋 Usajili wa Mpiga Kura","🗳️ Siku ya Uchaguzi","🏛️ Haki za Kiraia","🚨 Ufuatiliaji"])

with tab1:
    q_reg = st.selectbox("Swali lako:", [
        "Jinsi ya kusajiliwa kama mpiga kura",
        "Mahali pa kusajiliwa — vituo vya karibu",
        "Niangalie kama niko kwenye daftari la wapiga kura",
        "Nilikuwa nina usajili lakini sijui nipo wapi",
        "Wasajiliwe wangapi Kenya — takwimu",
        "Umri gani mtu anaweza kupiga kura Kenya?",
    ])
    if st.button("📋 Niambie", key="reg_btn"):
        with st.spinner("..."): result = ask(q_reg + " Kenya. Toa hatua sahihi na viungo vya rasmi (iebc.or.ke).")
        st.markdown(f'<div class="u-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    q_day = st.selectbox("Swali lako:", [
        "Ninachohitaji kwenda kupiga kura",
        "Saa ngapi vituo vya kupigia kura vinafungua/kufunga",
        "Nini kinatokea ikiwa hakuna jina langu kwenye daftari",
        "Ninaweza kupiga kura bila kadi ya mpiga kura?",
        "Uchaguzi kwa njia ya biometric unatendekaje",
        "Jinsi ya kupiga kura bila wasiwasi wa vitisho",
    ])
    if st.button("🗳️ Niambie", key="day_btn"):
        with st.spinner("..."): result = ask(q_day + " Kenya uchaguzi. Toa maelezo ya kisheria na vitendo.")
        st.markdown(f'<div class="u-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    q_rights = st.selectbox("Haki yako:", [
        "Haki zangu kama mpiga kura Kenya",
        "Ninaweza kufanya nini ikiwa kupiga kura kwangu kumezuiwa?",
        "Jinsi ya kulalamika kwa IEBC au mahakama ya uchaguzi",
        "Wabunge na madiwani — kazi zao ni nini?",
        "Jinsi ya kumhoji mbunge wangu kwa kazi anazofanya",
        "Petitioner — nini maana yake na jinsi inavyofanya kazi?",
    ])
    if st.button("✊ Niambie Haki Zangu", key="rights_btn"):
        with st.spinner("..."): result = ask(q_rights + " Kenya katiba na sheria za uchaguzi.")
        st.markdown(f'<div class="u-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### Ufuatiliaji wa Uchaguzi wa Kiraia")
    q_monitor = st.selectbox("Swali:", [
        "Jinsi ya kuwa mwangalizi wa uchaguzi Kenya",
        "Mashirika yanayofanya ufuatiliaji wa uchaguzi Kenya",
        "Jinsi ya kuripoti udhaifu wa uchaguzi",
        "ELOG, KNCHR, EU observers — wanafanya nini?",
    ])
    if st.button("🔍 Habari za Ufuatiliaji", key="mon_btn"):
        with st.spinner("..."): result = ask(q_monitor + " Kenya. Toa habari za vitendo na viungo vya rasmi.")
        st.markdown(f'<div class="u-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🗳️ Uchaguzi AI v1.0 | IEBC: iebc.or.ke | Habari za elimu tu — Si propaganda | CC BY-NC-ND 4.0")
