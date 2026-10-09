"""Show reported budget execution without mixing actual-report vintages."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import style, BLUE, GOLD, GREY, INK

ROOT=Path(__file__).resolve().parents[1]


def build():
    frame=pd.read_csv(ROOT/'research/capital/budget_execution_original_vintage.csv')
    if frame.fiscal_year.tolist()!=[f'{y}-{str(y+1)[-2:]}' for y in range(2015,2025)]:
        raise ValueError('Execution panel must contain ten ordered reported fiscal years')
    if frame[['budget_million','contemporary_actual_million']].isna().any().any():
        raise ValueError('Missing paired budget or actual; do not impute execution')
    frame['budget_execution_pct']=frame.contemporary_actual_million/frame.budget_million*100
    frame.to_csv(ROOT/'data/budget_execution_analysis.csv',index=False)
    style()
    fig,(ax,ratio_ax)=plt.subplots(2,1,figsize=(12,8),sharex=True,
        gridspec_kw={'height_ratios':[2,1]})
    x=np.arange(len(frame))
    ax.bar(x-.18,frame.budget_million/1000,width=.34,color=GREY,label='Budget column in each final-results report')
    ax.bar(x+.18,frame.contemporary_actual_million/1000,width=.34,color=BLUE,label='Actual in the same report')
    ax.set_ylabel('Nominal Capital Plan, CAD billions')
    ax.set_ylim(0,10.2)
    ratio_ax.plot(x,frame.budget_execution_pct,marker='o',color=GOLD)
    for i,value in enumerate(frame.budget_execution_pct):
        ratio_ax.text(i,value+2.3,f'{value:.1f}%',ha='center',fontsize=9)
    ratio_ax.set_ylabel('Actual / budget, %')
    ratio_ax.set_ylim(0,112)
    ratio_ax.axhline(100,color=GREY,linestyle='--',linewidth=1)
    ratio_ax.set_xticks(x,frame.fiscal_year)
    ratio_ax.set_xlabel('Fiscal year; contemporary actuals differ from the latest historical series')
    for axis in [ax,ratio_ax]:
        axis.grid(axis='y',color='#E5E9EC',linewidth=.7)
        axis.set_axisbelow(True)
        axis.axvline(3.5,linestyle=':',color=GREY,linewidth=1.2)
    fig.suptitle('Reported capital spending was below its paired budget in every year',y=.96,fontsize=16)
    fig.legend(loc='upper center',bbox_to_anchor=(.52,.93),frameon=False,fontsize=10)
    fig.text(.10,.025,
        'Sources: each local annual final-results fiscal summary; exact pages in the execution CSV.\n'
        'Budget columns may be restated. Execution is not a project-delivery score; the 2020–21 program changed substantially.\n'
        'Annual shortfalls cannot be summed as an infrastructure backlog or interpreted as permanent cancellations.',
        fontsize=9,color=GREY,va='bottom')
    fig.subplots_adjust(left=.10,right=.97,bottom=.22,top=.84,hspace=.15)
    for extension in ['png','svg']:
        fig.savefig(ROOT/'plots'/f'09_reported_budget_execution.{extension}',dpi=180,
            metadata={'Date':'2026-10-09','Creator':'Alberta infrastructure analysis'})
    plt.close(fig)
    print('Created paired contemporary budget-execution table and figure.')
    return frame


if __name__=='__main__':build()
