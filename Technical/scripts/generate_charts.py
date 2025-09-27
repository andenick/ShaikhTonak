#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')

OUTPUT_IMG_DIR = os.path.join('Technical', 'docs', 'latex')
os.makedirs(OUTPUT_IMG_DIR, exist_ok=True)


def save_plot(fig, filename: str) -> None:
    path = os.path.join(OUTPUT_IMG_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


def generate_profit_rate_plot() -> None:
    candidates = [
        os.path.join('Technical', 'data', 'modern', 'final_results', 'shaikh_tonak_extended_1958_2025_FINAL.csv'),
        os.path.join('Technical', 'data', 'modern', 'results', 'phase2_profit_rates_corrected_1958_2025.csv'),
        os.path.join('Technical', 'data', 'modern', 'results', 'phase2_profit_rates_1958_2025.csv'),
    ]
    df = None
    for p in candidates:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
    if df is None or not {'year', 'profit_rate'}.issubset(df.columns):
        return
    df = df.dropna(subset=['year', 'profit_rate']).sort_values('year')
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(df['year'], df['profit_rate'], label='Profit rate (r)')
    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_title('Profit Rate, 1958–2025')
    ax.set_xlabel('Year')
    ax.set_ylabel('r (unitless)')
    ax.legend()
    save_plot(fig, 'profit_rate_series.png')


def generate_surplus_components_plot() -> None:
    spi = os.path.join('Technical', 'data', 'modern', 'integrated', 'complete_st_timeseries_1958_2025.csv')
    if not os.path.exists(spi):
        return
    d = pd.read_csv(spi)
    if 'year' not in d.columns:
        return
    cand_sp = 'original_SP' if 'original_SP' in d.columns else None
    cand_s = 'original_S' if 'original_S' in d.columns else None
    cand_v = None
    for vcol in ('original_v', 'original_V', 'original_vt', 'original_variable'):
        if vcol in d.columns:
            cand_v = vcol
            break
    if not any([cand_sp, cand_s, cand_v]):
        return
    fig, ax = plt.subplots(figsize=(9, 4))
    if cand_sp:
        ax.plot(d['year'], d[cand_sp], label='SP (original)')
    if cand_s:
        ax.plot(d['year'], d[cand_s], label='S (original)')
    if cand_v:
        ax.plot(d['year'], d[cand_v], label='V (original)')
    ax.set_title('Surplus Components (original, integrated)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Level (original units)')
    ax.legend()
    save_plot(fig, 'surplus_components.png')


def generate_capital_utilization_plot() -> None:
    spi = os.path.join('Technical', 'data', 'modern', 'integrated', 'complete_st_timeseries_1958_2025.csv')
    if not os.path.exists(spi):
        return
    d = pd.read_csv(spi)
    if 'year' not in d.columns:
        return
    cap_col = None
    for c in ('original_K', 'original_KK', 'original_K g', 'original_gK'):
        if c in d.columns:
            cap_col = c
            break
    u_col = 'original_u' if 'original_u' in d.columns else None
    if not any([cap_col, u_col]):
        return
    fig, ax = plt.subplots(figsize=(9, 4))
    if cap_col:
        ax.plot(d['year'], d[cap_col], label=cap_col)
    if u_col:
        ax.plot(d['year'], d[u_col], label='u (original)')
    ax.set_title('Capital Stock and Capacity Utilization (original, integrated)')
    ax.set_xlabel('Year')
    ax.set_ylabel('Level / fraction')
    ax.legend()
    save_plot(fig, 'capital_utilization.png')


if __name__ == '__main__':
    generate_profit_rate_plot()
    generate_surplus_components_plot()
    generate_capital_utilization_plot()
    print('charts_done')
