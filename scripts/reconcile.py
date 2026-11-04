"""Rebuilds the headline numbers from raw inputs, independently of the notebooks, and asserts them."""
import json,sys,numpy as np,pandas as pd
sys.path.insert(0,'scripts')
m=json.load(open('outputs/metrics.json'))
p=pd.read_csv('data/processed/vahan_2w_panel.csv',parse_dates=['date'])
assert p.state.nunique()==36 and p.date.nunique()==118 and len(p)==4248
assert (p.regs_e2w<=p.regs_2w).all()
y=p.groupby('year')[['regs_e2w','regs_2w']].sum();assert abs(100*y.regs_e2w[2023]/y.regs_2w[2023]-m['panel']['share_2023'])<.01
c=pd.read_csv('data/policy/treatment_coding.csv')
assert c.group.value_counts().to_dict()=={'control':17,'paid':7,'excluded':7,'paper':5}
# Plain pandas re-derivation of the headline CS estimate, no shared code
w=p[(p.date>='2019-01-01')&(p.date<='2023-12-01')].copy();w=w[w.regs_2w>0]
w['s']=100*w.regs_e2w/w.regs_2w;W=w.pivot(index='state',columns='date',values='s')
tr=c[(c.group=='paid')&(c.state!='CHANDIGARH')];ctrl=c[c.group=='control'].state.tolist();eff=[]
for _,r in tr.iterrows():
    g=pd.Timestamp(r.treat_month+'-01');b=g-pd.DateOffset(months=1)
    for k in range(13):
        t=g+pd.DateOffset(months=k)
        eff.append((k,r.state,(W.loc[r.state,t]-W.loc[r.state,b])-(W.loc[ctrl,t]-W.loc[ctrl,b]).mean()))
e=pd.DataFrame(eff,columns=['k','s','v']);att=e.groupby('k').v.mean().mean()
print('headline',round(att,3),m['main']['att']);assert abs(att-m['main']['att'])<.002
assert abs(m['csdid']['lib']-m['csdid']['own'])<.005
assert m['main']['lo_ci'][0]<0<m['main']['lo_ci'][1]
assert m['large_controls']['ri_p']>.1
print('all reconciled')
