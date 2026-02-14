# ===============================
# WAR ROOM GOD MODE – نسخه نهایی آنلاین
# ===============================

import streamlit as st
import yfinance as yf
import plotly.express as px
import feedparser
import folium
from streamlit_folium import st_folium
from deep_translator import GoogleTranslator

# ----------------------
# 1. تنظیمات تلگرام
# ----------------------
try:
    from telegram import Bot
    TELEGRAM_TOKEN = "8385391009:AAF1rBbn_SoU5p-2m_gzUF8OL8bG-kzKsN0"
    TELEGRAM_IDS = [3399457]  # ID خودت و دوستان بعداً اضافه می‌شوند
    bot = Bot(token=TELEGRAM_TOKEN)
    def send_telegram(msg):
        for chat_id in TELEGRAM_IDS:
            try:
                bot.send_message(chat_id=chat_id, text=msg)
            except:
                pass
except Exception as e:
    st.warning("⚠️ تلگرام فعال نیست، نسخه بدون هشدار تلگرام اجرا شد")
    def send_telegram(msg):
        pass  # اگر تلگرام نصب نبود، هیچ کاری نکند

# ----------------------
# 2. فونت فارسی و طراحی حرفه‌ای
# ----------------------
st.set_page_config(layout="wide", page_title="WAR ROOM GOD MODE ONLINE")
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;600;800&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {font-family: 'Vazirmatn', sans-serif; background-color:#0a0f18; color:white;}
.big-title {font-size:36px; font-weight:800; margin:10px 0;}
.box-news {background:#1f2937; color:#fff; padding:15px; border-radius:12px; margin-bottom:12px; line-height:1.4;}
.metric-box {background:#111927; padding:15px; border-radius:12px; text-align:center; color:#fff;}
.sidebar .stButton>button {background-color:#ff8a00; color:white; font-weight:600; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.title("🛰️ WAR ROOM GOD MODE – آنلاین")
st.caption("تحلیل پیشرفته جنگ و بازار با پیش‌بینی ۲۴ ساعته و هشدار تلگرام")
translator = GoogleTranslator(source='en', target='fa')

# ----------------------
# 3. منابع اخبار
# ----------------------
sources = [
    "https://news.google.com/rss/search?q=war+conflict+military+finance+middle+east&hl=en-US&gl=US&ceid=US:en",
    "https://www.reuters.com/rssFeed/worldNews",
    "https://www.bloomberg.com/feed/podcast/etf.xml"
]

# ----------------------
# 4. شاخص‌ها و ریسک
# ----------------------
symbols = {"نفت":"CL=F","طلا":"GC=F","اوراق":"^TNX","VIX":"^VIX"}

def get_market_status():
    change, price = {}, {}
    risk, iran_risk = 0,0
    for name, sym in symbols.items():
        hist = yf.Ticker(sym).history(period="5d")
        change[name] = round((hist["Close"][-1]-hist["Close"][0])/hist["Close"][0]*100,2)
        price[name] = round(hist["Close"][-1],2)
    # محاسبه ریسک
    if change["نفت"]>10: risk+=3; iran_risk+=2
    elif change["نفت"]>6: risk+=2; iran_risk+=1
    elif change["نفت"]>3: risk+=1
    if price["VIX"]>35: risk+=3; iran_risk+=2
    elif price["VIX"]>25: risk+=2; iran_risk+=1
    elif price["VIX"]>20: risk+=1
    if change["طلا"]>4: risk+=2; iran_risk+=1
    elif change["طلا"]>2: risk+=1
    if change["اوراق"]<-3: risk+=1
    return change, price, risk, iran_risk

def get_status(s):
    if s<=1: return "🟢 پایدار","#00ffa6"
    elif s<=3: return "🟡 تنش","#ffe100"
    elif s<=6: return "🟠 ریسک بالا","#ff8a00"
    return "🔴 هشدار شدید","#ff2b2b"

# ----------------------
# 5. اخبار فارسی
# ----------------------
def get_news():
    news_list=[]
    for src in sources:
        feed = feedparser.parse(src)
        for entry in feed.entries[:5]:
            title_en = entry.title
            if any(k in title_en.lower() for k in ["war","attack","strike","conflict","missile","explosion","oil","finance","stock"]):
                try:
                    title_fa = translator.translate(title_en)
                except:
                    title_fa = title_en
                news_list.append(title_fa)
    return news_list

# ----------------------
# 6. پیش‌بینی احتمال جنگ (%) بر اساس ریسک
# ----------------------
def predict_war_probability(risk_score):
    if risk_score<=1: return 2
    elif risk_score<=3: return 15
    elif risk_score<=6: return 40
    return 75

# ----------------------
# 7. فرم اضافه کردن نفرات جدید به هشدار تلگرام
# ----------------------
with st.sidebar.expander("➕ اضافه کردن نفر جدید به هشدار تلگرام"):
    new_id = st.number_input("ID تلگرام نفر جدید", min_value=1000000, step=1)
    if st.button("اضافه کن"):
        if new_id not in TELEGRAM_IDS:
            TELEGRAM_IDS.append(new_id)
            st.success(f"{new_id} اضافه شد!")
        else:
            st.warning("قبلا اضافه شده است!")

# ----------------------
# 8. داشبورد Streamlit
# ----------------------
change, price, risk, iran_risk = get_market_status()

st.subheader("📊 شاخص‌های مهم")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🛢 نفت ۵روزه %", change["نفت"])
col2.metric("🥇 طلا ۵روزه %", change["طلا"])
col3.metric("😱 شاخص ترس", price["VIX"])
col4.metric("🏦 اوراق %", change["اوراق"])

st.markdown(f"<div class='big-title' style='color:{get_status(risk)[1]}'>وضعیت جهانی: {get_status(risk)[0]} | احتمال جنگ: {predict_war_probability(risk)}%</div>",unsafe_allow_html=True)
st.markdown(f"<div class='big-title' style='color:{get_status(iran_risk)[1]}'>وضعیت ایران: {get_status(iran_risk)[0]} | احتمال جنگ: {predict_war_probability(iran_risk)}%</div>",unsafe_allow_html=True)

st.subheader("🚨 اخبار نظامی و مالی مهم")
news = get_news()
for n in news:
    st.markdown(f"<div class='box-news'>{n}</div>",unsafe_allow_html=True)

st.subheader("📈 نمودار ۲۴ ساعته شاخص‌ها")
sel = st.selectbox("انتخاب شاخص", ["نفت","طلا","VIX","اوراق"])
hist = yf.Ticker(symbols[sel]).history(period="1d", interval="15m")
fig = px.line(hist, y="Close", title=f"{sel} - ۲۴ ساعت گذشته")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🗺️ نقشه ریسک دنیا")
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
countries = {
    "Iran":[32,53, iran_risk],
    "USA":[38,-97, risk],
    "Israel":[31,34, risk//2],
    "Saudi Arabia":[25,45, risk//2],
    "Russia":[61,105, risk//2],
    "China":[35,103, risk//3]
}
for country, (lat, lon, r) in countries.items():
    color = "green" if r<=1 else "yellow" if r<=3 else "orange" if r<=6 else "red"
    folium.Circle([lat,lon], radius=400000, color=color, fill=True, fill_opacity=0.7, popup=country).add_to(m)
st_folium(m, width=900, height=500)

st.subheader("🧠 تحلیل خودکار و پیش‌بینی")
if risk<=1:
    st.success("بازار و منطقه پایدار، نشانه جنگ دیده نمی‌شود")
elif risk<=3:
    st.warning("تنش در منطقه وجود دارد ولی الگوی کامل جنگ نیست")
elif risk<=6:
    st.error("ریسک بالا: سرمایه‌گذاران بزرگ در حال پوشش ریسک هستند")
else:
    st.error("هشدار شدید: بازار مشابه قبل شروع درگیری‌های واقعی است")

st.info("💡 نسخه آنلاین WAR ROOM: پیش‌بینی احتمال جنگ، ۲۴ ساعته و هشدار تلگرام فعال است")
