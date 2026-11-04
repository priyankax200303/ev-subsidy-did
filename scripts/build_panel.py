"""Parse the Vahan dashboard capture into a tidy state-month panel, with checks.
Input: data/raw/vahan_2w_state_month_capture.txt, captured 2026-11-04 from
vahan.parivahan.gov.in/vahan4dashboard (Y=State, X=Month Wise, calendar year, vehicle classes
M-CYCLE/SCOOTER and variants, MOPED, MOTORISED CYCLE; all fuels, then ELECTRIC(BOV)+PURE EV).
"""
import re, pandas as pd
MON='JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()
rows=[];bad=[];hdr=None
for ln in open('data/raw/vahan_2w_state_month_capture.txt'):
    ln=ln.rstrip('\n')
    if not ln: continue
    if ln.startswith('#'):
        p=ln[1:].split(); y,m=int(p[0]),p[1]; months=p[2:]; continue
    t=ln.split(); k=len(months)+1
    st=' '.join(t[:-k]); v=[int(x) for x in t[-k:]]
    if sum(v[:-1])!=v[-1]: bad.append((y,m,st,sum(v[:-1]),v[-1]))
    for mo,val in zip(months,v[:-1]):
        rows.append((y,MON.index(mo)+1,st,m,val))
d=pd.DataFrame(rows,columns=['year','month','state','series','regs'])
print('row-total mismatches',len(bad),bad[:5])
p=d.pivot_table(index=['state','year','month'],columns='series',values='regs',aggfunc='sum').reset_index()
g=pd.MultiIndex.from_product([sorted(d.state.unique()),range(2017,2027),range(1,13)],names=['state','year','month']).to_frame(index=False)
p=g.merge(p,how='left',on=['state','year','month'])
p['date']=pd.to_datetime(dict(year=p.year,month=p.month,day=1))
p=p[p.date<='2026-10-01'].copy()      # Nov 2026 is four days of data
assert p['all'].notna().all(),'missing total'
p['ev']=p.ev.fillna(0).astype(int); p['all']=p['all'].astype(int)
p=p.rename(columns={'all':'regs_2w','ev':'regs_e2w'})
print(p.shape,p.state.nunique(),p.date.min(),p.date.max())
p[['state','date','year','month','regs_2w','regs_e2w']].to_csv('data/processed/vahan_2w_panel.csv',index=False)
a=p.groupby('year')[['regs_2w','regs_e2w']].sum();a['share']=a.regs_e2w/a.regs_2w*100;print(a.round(2))
print('ev>all rows',(p.regs_e2w>p.regs_2w).sum())
print('zero-2W months by state',p[p.regs_2w==0].groupby('state').size().to_dict())
small=p[p.year==2019].groupby('state').regs_2w.sum().sort_values();print(small.head(10).to_dict())
