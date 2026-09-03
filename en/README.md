# Real Exchange Rate Suppression and Election Horizon Risks in Turkey (2026–2028)

This project simulates the macroeconomic risks and Purchasing Power Parity (PPP) fair value deviations of the USD/TRY exchange rate under **3 different scenarios** (Base, Optimistic, Pessimistic) across a 21-month projection period (September 2026 – May 2028).

---

## 📌 Key Features & Methodology

- **Live API Data Pipeline:** Automatically fetches live USD/TRY exchange rates via financial APIs (Fallback baseline: 48.31 TRY).
- **PPP Fair Value Calculation:** Uses differential inflation rates between Turkey and the United States relative to the June 2023 baseline.
- **Election Horizon Analysis:** Evaluates accumulated rate suppression gaps at two critical dates:
  - **Snap Election:** November 2027
  - **Regular Election:** May 2028
- **Policy Brief:** Generates publication-ready HTML/PDF policy briefs for institutional evaluation.

---

## 📊 Scenario Comparison Matrix

| Scenario | Nov 2027 Fair Rate | May 2028 Fair Rate | Cumulative Risk Gap (%) |
| :--- | :--- | :--- | :--- |
| **Optimistic** | **69.31 TRY** | **71.02 TRY** | **25.7% – 27.1%** |
| **Base** | **73.26 TRY** | **76.90 TRY** | **34.7% – 36.0%** |
| **Pessimistic** | **81.52 TRY** | **90.13 TRY** | **49.8% – 59.4%** |

*Note: Projected exchange rate path assumes 54.39 TRY by Nov 2027 and 56.55 TRY by May 2028.*

---

## 📂 Project Structure

- `fx_suppression_simulation.py`: Main Python simulation script with live API pipeline.
- `simulation_full_data.csv`: Complete 21-month dataset across all scenarios.
- `time_series_charts.png`: Time-series projection and gap visualization.
- `election_comparison_chart.png`: Election horizon scenario comparison bar chart.
- `Turkey_FX_Policy_Brief.pdf`: Institutional 2-page Policy Brief document.

---

- Disclaimer: This repository and the associated policy brief are created strictly for academic research, econometric modeling, and portfolio demonstration purposes. Nothing contained herein constitutes financial, investment, or legal advice. Projections are theoretical outputs based on Purchase Power Parity (PPP) models under hypothetical scenario parameters.
