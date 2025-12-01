import streamlit as st
from openai import OpenAI
import json

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Nano Banana Pro",
    page_icon="🍌",
    layout="centered"
)

# --- AYARLAR VE GÜVENLİK ---

# 1. MODEL ADI:
MODEL_ADI = "ft:gpt-4o-mini-2024-07-18:personal::Chf9BuQp" 

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Eğer lokalde çalışıyorsan veya secrets ayarlanmamışsa uyarı ver
    st.error("⚠️ API Key bulunamadı! Lütfen Streamlit Cloud ayarlarında 'Secrets' kısmına OPENAI_API_KEY ekleyin.")
    st.stop()

# --- ARAYÜZ TASARIMI ---
st.title("🍌 Nano Banana Pro")
st.subheader("Analog Fotoğraf Reçetesi Oluşturucu")
st.markdown("Fikrini yaz, **90'lar Estetiği** için gerekli JSON kodunu saniyeler içinde al.")

# Sol Menü (Sidebar)
with st.sidebar:
    st.header("Nasıl Çalışır?")
    st.info("Bu araç, fine-tune edilmiş özel bir GPT-4o-mini modeli kullanır.")
    st.success("Target: 90's Disposable Camera Style")
    st.markdown("---")
    st.caption("Nano Banana Project © 2025")

# Kullanıcı Giriş Alanı
user_input = st.text_area(
    "Fotoğraf fikrini buraya yaz:", 
    height=100, 
)

# Çalıştırma Butonu
if st.button("✨ Promptu Oluştur", type="primary"):
    if not user_input:
        st.warning("Lütfen önce kutucuğa bir fikir yazın.")
    else:
        client = OpenAI(api_key=api_key)

        with st.spinner('Üretiliyor...'):
            try:
                response = client.chat.completions.create(
                    model=MODEL_ADI,
                    messages=[
                        {
                            "role": "system", 
                            "content": "Sen, kullanıcı fikirlerini 90'lı yılların 'kullan-at kamera' estetiğine sahip, flaşlı, grenli ve nostaljik fotoğraf promptlarını JSON formatında üreten bir uzmansın."
                        },
                        {
                            "role": "user", 
                            "content": user_input
                        }
                    ],
                    response_format={ "type": "json_object" }
                )

                # Cevabı İşle
                raw_content = response.choices[0].message.content
                parsed_json = json.loads(raw_content)

                # Sonucu Göster
                st.success("Reçete Hazır!")

                st.subheader("📋 Kopyalanacak Kod")
                st.code(raw_content, language="json")
                
                st.caption("👆 Sağ üstteki ikona tıklayarak kopyala ve Muzlu Araca yapıştır.")

                # Detaylı Görünüm
                with st.expander("Detayları İncele (JSON Ağacı)"):
                    st.json(parsed_json)

            except Exception as e:

                st.error(f"Bir hata oluştu: {e}")
