# Türkiye Ekonomisi: Reel Döviz Kuru Baskılanması ve Seçim Senaryoları Simülasyonu (2026–2028)

Bu proje, Haziran 2023 sonrası uygulanan dezenflasyon programı kapsamında Türk Lirası'nın reel değerlenmesini (sürünen kur politikası) ve bu politikanın olası bir **Erken Seçim (Kasım 2027)** ile **Normal Seçim (Mayıs 2028)** tarihlerinde biriktireceği makroekonomik riskleri 3 farklı senaryo altında simüle etmektedir.

## 📌 Metodoloji ve Veri Entegrasyonu

- **Canlı Veri API:** Kod çalıştığında canlı USD/TRY kurunu API üzerinden otomatik çeker (Bağlantı olmaması durumunda baseline: 48.31 TL).
- **Baz Dönemi:** Haziran 2023 (Satın Alma Gücü Paritesi - SGP başlangıcı).
- **Simülasyon Dönemi:** Eylül 2026 – Mayıs 2028 (21 Ay).
* **Olması Gereken Kur (SGP / Adil Değer):** Türkiye TÜFE enflasyonu ile ABD TÜFE enflasyonu arasındaki farkın kura yansıtıldığı teorik adil değer:

  $$\text{Adil Kur}_t = \text{Adil Kur}_{t-1} \times (1 + \pi_{\text{TR}} - \pi_{\text{ABD}})$$
- **Birikimli Baskı / Sapma Endeksi (%):**
  $$\text{Baskı Oranı (\%)} = \left( \frac{\text{Olması Gereken Kur}}{\text{Olası Kur}} - 1 \right) \times 100$$

---

## 📊 Senaryo Analizi ve Seçim Karşılaştırması

| Senaryo Türü | Makroekonomik Varsayım | Kasım 2027 Adil Kur | Mayıs 2028 Adil Kur | Birikimli Kur Baskısı (%) |
| :--- | :--- | :--- | :--- | :--- |
| **İyimser** | Dezenflasyon hızlı (%1.4 &rarr; %0.5) | **69.31 TL** | **71.02 TL** | **%25.7 - %27.1** |
| **Temel** | Program patikası (%1.8 &rarr; %0.9) | **73.26 TL** | **76.90 TL** | **%34.7 - %36.0** |
| **Kötümser** | Katı enflasyon / Şok (%2.5 &rarr; %1.8) | **81.52 TL** | **90.13 TL** | **%49.8 - %59.4** |

*Not: Olası Piyasa Kuru Kasım 2027'de 54.39 TL, Mayıs 2028'de 56.55 TL olarak modellenmiştir.*

---

## 📂 Dosya Yapısı

- `dolar_baskilanma_raporu.py`: Canlı veri çeken ve 3 senaryoyu hesaplayan ana simülasyon kodu.
- `simulasyon_tam_veri.csv` / `dolar_baskilanma_raporu.csv`: 21 aylık zaman serisi verileri.
- `tum_degerler_zaman_serisi.png`: 3 senaryolu zaman serisi grafiği.
- `secim_karsilastirma.png`: Seçim senaryoları karşılaştırma bar grafiği.
- `Policy_Brief_TUR_FX.pdf`: Dünya Bankası formatında hazırlanmış 2 sayfalık Türkçe Politika Raporu.
