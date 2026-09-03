import datetime
import json
import typing
import urllib.error
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ==========================================
# 1. LIVE DATA PIPELINE (API WITH FALLBACK)
# ==========================================
def fetch_live_usd_try(default_rate: float = 48.31) -> float:
  urls = [
      'https://open.er-api.com/v6/latest/USD',
      'https://api.exchangerate-api.com/v4/latest/USD',
  ]
  for url in urls:
    try:
      req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      with urllib.request.urlopen(req, timeout=3) as resp:
        data = json.loads(resp.read().decode())
        if 'rates' in data and 'TRY' in data['rates']:
          return float(data['rates']['TRY'])
    except Exception:
      pass
  return default_rate


current_usd = fetch_live_usd_try(48.31)
print(f'Baseline USD/TRY Rate: {current_usd:.2f} TRY')

# ==========================================
# 2. 3-SCENARIO 21-MONTH SIMULATION
# ==========================================
start_date = datetime.date(2026, 9, 1)
months_count = 21

initial_fair_usd = current_usd * (61.46 / 48.31)
us_inflation = 0.002  # 0.2% monthly US inflation

scenarios = {
    'Base': {
        'inf_path': np.linspace(0.018, 0.009, months_count),
        'fx_path': np.linspace(0.010, 0.006, months_count),
    },
    'Optimistic': {
        'inf_path': np.linspace(0.014, 0.005, months_count),
        'fx_path': np.linspace(0.011, 0.005, months_count),
    },
    'Pessimistic': {
        'inf_path': np.linspace(0.025, 0.018, months_count),
        'fx_path': np.linspace(0.008, 0.005, months_count),
    },
}

sim_data: list[dict[str, typing.Any]] = []

for idx in range(months_count):
  m_date = (start_date + pd.DateOffset(months=idx)).strftime('%Y-%m')
  row: dict[str, typing.Any] = {'date': m_date}

  for sc_name, sc_params in scenarios.items():
    inf = float(sc_params['inf_path'][idx])
    fx = float(sc_params['fx_path'][idx])

    if idx == 0:
      act = current_usd
      fair = initial_fair_usd
    else:
      prev_act = float(sim_data[idx - 1][f'{sc_name.lower()}_projected_rate'])
      prev_fair = float(sim_data[idx - 1][f'{sc_name.lower()}_fair_rate'])
      act = prev_act * (1.0 + fx)
      fair = prev_fair * (1.0 + (inf - us_inflation))

    gap = ((fair / act) - 1.0) * 100.0

    sc_key = sc_name.lower()
    row[f'{sc_key}_monthly_inf_pct'] = round(inf * 100.0, 2)
    row[f'{sc_key}_monthly_fx_pct'] = round(fx * 100.0, 2)
    row[f'{sc_key}_projected_rate'] = round(act, 2)
    row[f'{sc_key}_fair_rate'] = round(fair, 2)
    row[f'{sc_key}_gap_pct'] = round(gap, 2)

  sim_data.append(row)

df_all = pd.DataFrame(sim_data)

# Save CSVs
df_all.to_csv('simulation_full_data.csv', index=False)
df_all.to_csv('fx_suppression_report.csv', index=False)

# ==========================================
# 3. VISUALIZATION 1: TIME SERIES (ENGLISH)
# ==========================================
plt.style.use(
    'seaborn-v0_8-whitegrid'
    if 'seaborn-v0_8-whitegrid' in plt.style.available
    else 'default'
)
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), sharex=True)

colors = {'Base': '#0275d8', 'Optimistic': '#5cb85c', 'Pessimistic': '#d9534f'}

for sc in ['Base', 'Optimistic', 'Pessimistic']:
  sc_k = sc.lower()
  ax1.plot(
      df_all['date'],
      df_all[f'{sc_k}_projected_rate'],
      label=f'{sc} Scenario (Projected Rate)',
      color=colors[sc],
      linewidth=2,
      marker='o' if sc == 'Base' else None,
  )
  ax1.plot(
      df_all['date'],
      df_all[f'{sc_k}_fair_rate'],
      label=f'{sc} Scenario (PPP Fair Rate)',
      color=colors[sc],
      linestyle='--',
  )

ax1.set_ylabel('USD / TRY Rate', fontweight='bold')
ax1.set_title(
    'USD/TRY Exchange Rate Projection: 3 Scenarios (Sep 2026 - May 2028)',
    fontweight='bold',
    fontsize=12,
)
ax1.legend(loc='upper left', frameon=True, facecolor='white')

for sc in ['Base', 'Optimistic', 'Pessimistic']:
  sc_k = sc.lower()
  ax2.plot(
      df_all['date'],
      df_all[f'{sc_k}_gap_pct'],
      label=f'{sc} Scenario Gap (%)',
      color=colors[sc],
      linewidth=2,
  )

ax2.set_ylabel('Cumulative Rate Gap (%)', fontweight='bold')
ax2.set_xlabel('Date (Year-Month)', fontweight='bold')
ax2.set_title(
    'Cumulative Devaluation / Adjustment Risk Gap (%)',
    fontweight='bold',
    fontsize=12,
)
plt.xticks(rotation=45)
ax2.legend(loc='upper left', frameon=True, facecolor='white')

fig1.tight_layout()
fig1.savefig('time_series_charts.png', dpi=300)
plt.close(fig1)

# ==========================================
# 4. VISUALIZATION 2: ELECTION COMPARISON
# ==========================================
erken_row = df_all[df_all['date'] == '2027-11'].iloc[0]
normal_row = df_all[df_all['date'] == '2028-05'].iloc[0]

labels = ['Snap Election (Nov 2027)', 'Regular Election (May 2028)']
x = np.arange(len(labels))
width = 0.22

fig2, ax_secim = plt.subplots(figsize=(10, 6))

base_olasi = [
    erken_row['base_projected_rate'],
    normal_row['base_projected_rate'],
]
iy_adil = [erken_row['optimistic_fair_rate'], normal_row['optimistic_fair_rate']]
kot_adil = [
    erken_row['pessimistic_fair_rate'],
    normal_row['pessimistic_fair_rate'],
]

rects1 = ax_secim.bar(
    x - width,
    base_olasi,
    width,
    label='Projected Rate (Base Path)',
    color='#0275d8',
)
rects2 = ax_secim.bar(
    x, iy_adil, width, label='PPP Fair Rate (Optimistic)', color='#5cb85c'
)
rects3 = ax_secim.bar(
    x + width, kot_adil, width, label='PPP Fair Rate (Pessimistic)', color='#d9534f'
)

ax_secim.set_ylabel('USD / TRY Level', fontweight='bold')
ax_secim.set_title(
    'Projected Rate vs. PPP Fair Value at Election Horizons',
    fontweight='bold',
    fontsize=12,
)
ax_secim.set_xticks(x)
ax_secim.set_xticklabels(labels, fontweight='bold')

# Y ekseni tavanını 105 yaparak üstteki lejant kutusuna yeterli boşluk bırakıyoruz:
ax_secim.set_ylim(0, 105)

ax_secim.legend(
    loc='upper center',
    frameon=True,
    facecolor='white',
    framealpha=0.9,
    ncol=3,
)

ax_secim.bar_label(rects1, padding=3, fmt='%.2f TRY')
ax_secim.bar_label(rects2, padding=3, fmt='%.2f TRY')
ax_secim.bar_label(rects3, padding=3, fmt='%.2f TRY')

fig2.tight_layout()
fig2.savefig('election_comparison_chart.png', dpi=300)
plt.show()

# ==========================================
# 5. ENGLISH POLICY BRIEF (HTML REPORT)
# ==========================================
html_content_en = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Policy Brief - Real Exchange Rate Suppression in Turkey</title>
<style>
    body {{ font-family: 'Arial', sans-serif; margin: 30px; color: #1e293b; line-height: 1.6; background-color: #f8fafc; }}
    .container {{ max-width: 800px; margin: auto; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    .header {{ background-color: #0f172a; color: #ffffff; padding: 20px; border-radius: 6px; border-bottom: 4px solid #b91c1c; }}
    .header h1 {{ font-size: 16pt; margin: 0 0 5px 0; }}
    .header .sub {{ font-size: 10pt; color: #94a3b8; }}
    .exec-box {{ background: #f1f5f9; border-left: 4px solid #0275d8; padding: 15px; margin: 20px 0; border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    th, td {{ padding: 10px; border: 1px solid #cbd5e1; text-align: left; font-size: 10pt; }}
    th {{ background-color: #1e293b; color: white; }}
    .badge-red {{ background: #fee2e2; color: #991b1b; padding: 3px 6px; border-radius: 3px; font-weight: bold; }}
    .badge-green {{ background: #dcfce7; color: #166534; padding: 3px 6px; border-radius: 3px; font-weight: bold; }}
    .badge-blue {{ background: #dbeafe; color: #1e40af; padding: 3px 6px; border-radius: 3px; font-weight: bold; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>POLICY BRIEF: REAL EXCHANGE RATE SUPPRESSION IN TURKEY</h1>
        <div class="sub">Purchasing Power Parity (PPP) Macroeconomic Risk Projection (2026–2028)</div>
    </div>

    <div class="exec-box">
        <h3>EXECUTIVE SUMMARY</h3>
        <p>Based on September 2026 baseline data (<strong>1 USD = {current_usd:.2f} TRY</strong>), a 21-month macroeconomic simulation across 3 scenarios was executed. Even if disinflation targets are achieved, the accumulated exchange rate adjustment risk reaches <strong>25.7% – 49.8%</strong> by the Snap Election horizon (Nov 2027) and <strong>27.1% – 59.4%</strong> by the Regular Election horizon (May 2028).</p>
    </div>

    <h2>Scenario Comparison Matrix</h2>
    <table>
        <thead>
            <tr>
                <th>Scenario</th>
                <th>Nov 2027 Fair Rate</th>
                <th>May 2028 Fair Rate</th>
                <th>Cumulative Risk Gap (%)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Optimistic</strong></td>
                <td>69.31 TRY</td>
                <td>71.02 TRY</td>
                <td><span class="badge-green">25.7% - 27.1%</span></td>
            </tr>
            <tr>
                <td><strong>Base</strong></td>
                <td>73.26 TRY</td>
                <td>76.90 TRY</td>
                <td><span class="badge-blue">34.7% - 36.0%</span></td>
            </tr>
            <tr>
                <td><strong>Pessimistic</strong></td>
                <td>81.52 TRY</td>
                <td>90.13 TRY</td>
                <td><span class="badge-red">49.8% - 59.4%</span></td>
            </tr>
        </tbody>
    </table>

    <h2>Policy Recommendations</h2>
    <ul>
        <li><strong>Gradual FX Flexibility:</strong> FX rate growth should be gradually aligned with disinflation to preserve export competitiveness.</li>
        <li><strong>Structural Reforms:</strong> Support productivity-driven, high-value-added export sectors rather than relying solely on exchange rate advantages.</li>
    </ul>
</div>
</body>
</html>
"""

with open("Turkey_FX_Policy_Brief.html", "w", encoding="utf-8") as f:
  f.write(html_content_en)

print("English code execution complete. All output files generated.")