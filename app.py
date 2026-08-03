import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF
import time

st.set_page_config(page_title="Osmanlıca - Türkçe Çevirmen", page_icon="📜")

st.title("📜 Osmanlıca - Günümüz Türkçesi Çeviri Aracı")
st.write("Latin harflerine aktarılmış Osmanlıca PDF dosyalarınızı yükleyin, yapay zeka günümüz Türkçesine çevirsin.")

# API Anahtarı Girişi
api_key = st.text_input("Gemini API Anahtarınızı Girin:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')

    # PDF Yükleme Alanı
    uploaded_file = st.file_uploader("Çevrilecek PDF Dosyasını Seçin", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Çeviriyi Başlat 🚀"):
            # PDF'i okuma
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            toplam_sayfa = len(doc)
            
            st.success(f"PDF yüklendi! Toplam {toplam_sayfa} sayfa bulundu. Çeviri başlıyor...")
            
            ilerleme_cubugu = st.progress(0)
            durum_metni = st.empty()
            
            tam_cevap = ""

            # Sayfa sayfa çeviri döngüsü
            for sayfa_no in range(toplam_sayfa):
                sayfa = doc.load_page(sayfa_no)
                metin = sayfa.get_text("text")
                
                if len(metin.strip()) > 20: # Sadece yazılı sayfaları çevir
                    prompt = f"Aşağıdaki metin Latin harflerine aktarılmış Osmanlıca bir kitaba aittir. Lütfen anlamını bozmadan, okuyucunun rahat anlayabileceği günümüz akıcı Türkçesine çevir:\n\n{metin}"
                    
                    try:
                        cevap = model.generate_content(prompt)
                        tam_cevap += f"\n\n--- Sayfa {sayfa_no + 1} ---\n\n"
                        tam_cevap += cevap.text
                    except Exception as e:
                        tam_cevap += f"\n\n--- Sayfa {sayfa_no + 1} ÇEVİRİLEMEDİ: Hata oluştu ---\n\n"
                    
                    # Ücretsiz API kotası için bekleme süresi
                    time.sleep(4)
                
                # İlerlemeyi güncelle
                ilerleme = (sayfa_no + 1) / toplam_sayfa
                ilerleme_cubugu.progress(ilerleme)
                durum_metni.text(f"Çevriliyor: Sayfa {sayfa_no + 1} / {toplam_sayfa}")
                
            st.success("🎉 Çeviri Başarıyla Tamamlandı!")
            
            # İndirme Butonu
            st.download_button(
                label="📥 Çeviriyi İndir (.txt formatında)",
                data=tam_cevap,
                file_name="cevirilmis_kitap.txt",
                mime="text/plain"
            )
