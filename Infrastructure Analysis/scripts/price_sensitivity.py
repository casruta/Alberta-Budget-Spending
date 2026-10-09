"""Hypothetical deflator sensitivity; does not estimate construction inflation."""
import numpy as np
import pandas as pd
from analyze import ROOT, load_primary, style, save, BLUE, GOLD, GREY, INK
import matplotlib.pyplot as plt


def build():
    data=load_primary()
    base=data.loc[data.calendar_year.eq(2018)].iloc[0]
    end=data.loc[data.calendar_year.eq(2024)].iloc[0]
    nominal_pc_factor=end.capital_nominal_per_resident_cad/base.capital_nominal_per_resident_cad
    hypothetical_growth=np.linspace(0,35,351)
    adjusted_change=(nominal_pc_factor/(1+hypothetical_growth/100)-1)*100
    threshold=(nominal_pc_factor-1)*100
    actual_cpi_growth=(end.cpi_index_2015_100/base.cpi_index_2015_100-1)*100
    cpi_adjusted_change=(nominal_pc_factor/(1+actual_cpi_growth/100)-1)*100
    style()
    fig,ax=plt.subplots(figsize=(11.8,6))
    ax.plot(hypothetical_growth,adjusted_change,color=BLUE)
    ax.axhline(0,color=INK,linewidth=1)
    ax.axvline(threshold,color=GREY,linestyle=':',linewidth=1.4)
    ax.scatter([threshold],[0],s=65,color=INK,zorder=4)
    ax.text(threshold+.6,1.2,f'Break-even price growth: {threshold:.1f}%',fontsize=11)
    ax.scatter([actual_cpi_growth],[cpi_adjusted_change],s=90,marker='s',color=GOLD,zorder=4)
    ax.annotate(f'Observed CPI chain: +{actual_cpi_growth:.1f}%\nCPI-adjusted per-resident change: {cpi_adjusted_change:.1f}%',
        xy=(actual_cpi_growth,cpi_adjusted_change),xytext=(13,-6),fontsize=10,
        arrowprops={'arrowstyle':'-','color':GREY,'linewidth':1})
    ax.set_title('A 5.0% cumulative price increase would erase the nominal per-resident gain')
    ax.set_xlabel('Hypothetical cumulative price growth, 2018 to 2024 (%)')
    ax.set_ylabel('Calculated price-adjusted spending\nper resident change (%)')
    ax.set_xlim(0,35)
    ax.set_ylim(-25,9)
    ax.grid(axis='y',color='#E5E9EC',linewidth=.7)
    ax.set_axisbelow(True)
    save(fig,'08_hypothetical_price_sensitivity',
        'Inputs: actual capital spending and July population, Alberta 2024–25 Final Results, pp. 13–14.\n'
        'The curve is an illustrative arithmetic scenario, not observed construction prices or construction-volume growth.\n'
        'The square uses observed consumer inflation; appropriate construction-price data remain unavailable.')
    pd.DataFrame({'assumed_cumulative_price_growth_pct':hypothetical_growth,
        'calculated_price_adjusted_spending_per_resident_growth_pct':adjusted_change,
        'scenario_status':'hypothetical; not observed construction inflation'}).to_csv(
            ROOT/'data/hypothetical_price_scenarios.csv',index=False)
    print(f'Illustrative threshold {threshold:.6f}%; construction inflation not estimated.')


if __name__=='__main__':build()
