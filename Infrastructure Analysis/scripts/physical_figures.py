"""Visualize independently reviewed project stages without implying net capacity."""
from pathlib import Path
import re
import pandas as pd
from analyze import style, save, BLUE, GOLD, GREY, INK, ROOT
import matplotlib.pyplot as plt


def build():
    style()
    timeline=pd.read_csv(ROOT/'research/physical/gaploop/project_timeline_audited.csv')
    selected=timeline.loc[timeline.first_observed_earlier_stage_year.notna()].copy()
    # Multi-stage bypass has two completion records; keep it in the ledger rather than
    # forcing those stages into one event on this selected illustration.
    selected=selected.loc[~selected.project.str.contains('Highway43X')]
    selected['earlier_year']=selected.first_observed_earlier_stage_year.str[:4].astype(int)
    selected['reported_status_year']=selected.first_reported_completed_status_fy.str[:4].astype(int)
    selected=selected.sort_values(['reported_status_year','earlier_year','project']).reset_index(drop=True)
    names={
        'Grande Prairie Regional Hospital phases 1 and 2':'Grande Prairie hospital: Phase 2',
        'Grande Prairie Regional Hospital Phase 2 (joint phase1/phase2 funding)':'Grande Prairie hospital (Phase 2 status)',
        'Misericordia Community Hospital emergency department':'Misericordia emergency department',
        'Rockyview General Hospital ICU CCU GI redevelopment':'Rockyview ICU / CCU / GI redevelopment',
        'Edmonton Anthony Henday Drive ring road':'Edmonton Anthony Henday Drive',
        'Highway63 twinning Grassland to Fort McMurray':'Highway 63 twinning corridor',
        'Calgary ring road final west stage':'Calgary ring road: final west stage',
        'Calgary ring road whole program (final western stage)':'Calgary ring-road program',
        'Highway15 twinning North Saskatchewan River bridge':'Highway 15 and North Saskatchewan bridge',
    }
    labels=[names.get(s,s) for s in selected.project]
    fig,ax=plt.subplots(figsize=(13,7.4))
    positions=list(range(len(selected)))
    ax.scatter(selected.earlier_year,positions,s=80,facecolor='white',edgecolor=GREY,
               linewidth=1.8,label='Earlier documented planning / work / spending',zorder=3)
    ax.scatter(selected.reported_status_year,positions,s=85,marker='s',facecolor=BLUE,
               edgecolor=BLUE,label='First recovered fiscal report listing completed status',zorder=4)
    for i,r in selected.iterrows():
        ax.text(r.earlier_year+.12,i+.13,r.first_observed_earlier_stage_year,
                color=GREY,fontsize=9,va='bottom')
        ax.text(r.reported_status_year+.12,i-.18,r.first_reported_completed_status_fy,
                color=BLUE,fontsize=9,va='top')
    ax.set_yticks(positions,labels)
    ax.invert_yaxis()
    ax.set_xticks(range(2015,2025))
    ax.set_xlim(2014.6,2025.15)
    ax.axvline(2018.5,color=GREY,linestyle=':',linewidth=1.3)
    ax.text(2018.6,-.65,'UCP takes office',fontsize=9,color=GREY)
    ax.set_title('Later completed-status reports follow work documented before 2019')
    ax.set_xlabel('Fiscal year beginning in April of the labelled calendar year')
    ax.grid(axis='x',color='#E5E9EC',linewidth=.7)
    ax.set_axisbelow(True)
    ax.legend(loc='upper center',bbox_to_anchor=(.45,-.13),frameon=False,fontsize=9,ncol=1)
    note=('Source: reviewed annual-report pages in research/physical/gaploop/project_timeline_audited.csv.\n'
          'Selected observations, not event dates. Most operational dates remain unverified; Anthony Henday opened in 2016.\n'
          'Earlier work can concern the whole program, not the later named phase. Dots do not imply continuous construction.')
    # Give the source note and legend separate vertical room.
    save(fig,'07_selected_project_stages',note,left=.36,bottom=.27)
    selected.to_csv(ROOT/'data/selected_project_stages.csv',index=False)
    print(f'Built selected physical-stage figure for {len(selected)} projects; no net-capacity inference.')


if __name__=='__main__':build()
