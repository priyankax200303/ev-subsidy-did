"""Generates and executes the analysis notebooks. Run from the repo root."""
import nbformat as nbf, sys, os
from nbclient import NotebookClient
SETUP='''import sys,json,os,warnings
warnings.filterwarnings('ignore')
sys.path.insert(0,'../scripts')
import numpy as np,pandas as pd,matplotlib.pyplot as plt,matplotlib.dates as mdates
from common import *
ACC="#20808D";MUTE="#9a9a94";INK="#2b2b2b";BAD="#C8452F"
plt.rcParams.update({'axes.spines.top':False,'axes.spines.right':False,'font.size':10,'axes.edgecolor':MUTE,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'axes.titlesize':11.5,'axes.titleweight':'bold','axes.titlelocation':'left','figure.dpi':130,'savefig.bbox':'tight','lines.linewidth':2})
M='../outputs/metrics.json'
def save_metrics(k,v):
    d=json.load(open(M)) if os.path.exists(M) else {}
    d[k]=v;json.dump(d,open(M,'w'),indent=1,default=float)
pd.set_option('display.width',160)
'''
def nb(cells,path):
    n=nbf.v4.new_notebook();n.cells=[nbf.v4.new_code_cell(SETUP)]
    for c in cells:
        n.cells.append(nbf.v4.new_markdown_cell(c[3:]) if c.startswith('MD:') else nbf.v4.new_code_cell(c))
    NotebookClient(n,timeout=1800,kernel_name='python3',resources={'metadata':{'path':'notebooks'}}).execute()
    nbf.write(n,path);print('ok',path)

N1=["MD:# 1. Panel and coverage\nVahan state by month, two-wheeler classes, all fuels versus ELECTRIC(BOV) plus PURE EV. The check here is whether the panel can carry the design at all.",
'''p=pd.read_csv('../data/processed/vahan_2w_panel.csv',parse_dates=['date'])
c=pd.read_csv('../data/policy/treatment_coding.csv')
a=p.groupby('year')[['regs_2w','regs_e2w']].sum();a['e2w_share_pct']=(100*a.regs_e2w/a.regs_2w).round(2)
a.to_csv('../outputs/tables/national_by_year.csv');print(a)
print(p.state.nunique(),p.date.nunique(),len(p),p.regs_2w.isna().sum())
save_metrics('panel',{'states':p.state.nunique(),'months':p.date.nunique(),'rows':len(p),'share_2019':a.e2w_share_pct[2019],'share_2023':a.e2w_share_pct[2023],'share_2026_ytd':a.e2w_share_pct[2026]})''',
"MD:## Independent cross-check\nA separate public copy of Vahan EV counts, pulled in early 2024, is compared month by month. Vahan revises old months slightly, so exact equality is not expected.",
'''o=pd.read_csv('../data/raw/crosscheck_github_copy_2024.csv',parse_dates=['date'])
m=p.merge(o,on=['state','date']);m=m[m.date<'2024-01-01']
x={'rows':len(m),'states':m.state.nunique(),'corr':m.regs_e2w.corr(m.e2w_2024_copy),'sum_ours':int(m.regs_e2w.sum()),'sum_copy':int(m.e2w_2024_copy.sum()),'exact_match_share':(m.regs_e2w==m.e2w_2024_copy).mean()}
print(x);save_metrics('crosscheck',x)''',
"MD:## Size floor and thin cells",
'''b=p[p.year==2019].groupby('state').regs_2w.sum().sort_values();print(b.head(9))
w=p[(p.date>='2019-01-01')&(p.date<='2023-12-01')]
print('zero-denominator cells in window',w[w.regs_2w==0][['state','date']].values.tolist())
print('cells under 100 two-wheelers, excluding the seven small units:',(w[~w.state.isin(c[c.group=='excluded'].state)].regs_2w<100).sum())''',
"MD:## The Chandigarh problem\nChandigarh's policy also capped petrol two-wheeler registrations, and the yearly cap ran out in early 2023. Registrations collapse in February and March 2023 and reset in April, so the share spikes from the denominator. That is a petrol ban, not a subsidy effect. See `docs/DATA_QUALITY_LOG.md`.",
'''ch=p[(p.state=='CHANDIGARH')&(p.date>='2022-01-01')&(p.date<='2023-12-01')].copy();ch['s']=100*ch.regs_e2w/ch.regs_2w
fig,ax=plt.subplots(figsize=(7,2.8));ax.plot(ch.date,ch.s,color=BAD);ax.set_ylabel('Electric share, %')
ax.set_title('Chandigarh: a petrol cap, not a subsidy, made the 54% spike');ax.annotate('Mar 2023: 358 of 660',(pd.Timestamp('2023-03-01'),54.2),xytext=(8,-6),textcoords='offset points',fontsize=9)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'));plt.savefig('../outputs/charts/chandigarh_spike.png');plt.show()
save_metrics('chandigarh',{'mar23_regs':660,'mar23_ev':358,'mar23_share':54.2})''',
"MD:## Raw comparison",
'''P=load(end='2026-10-01');P=P[P.state!='CHANDIGARH']
q=P.groupby([P.group,'date'])[['regs_e2w','regs_2w']].sum().reset_index();q['s']=100*q.regs_e2w/q.regs_2w
q['s3']=q.groupby('group').s.transform(lambda v:v.rolling(3).mean())
fig,ax=plt.subplots(figsize=(7.5,3.4))
for g_,col,lab in [('paid',ACC,'Subsidy states with money paid (6)'),('control',MUTE,'No subsidy in window (17)')]:
    d=q[q.group==g_];ax.plot(d.date,d.s3,color=col,label=lab)
ax.set_ylabel('Electric share, %, 3-month average');ax.set_title('Pooled by registrations, the two groups track closely (descriptive)');ax.legend(frameon=False,loc='upper left')
plt.savefig('../outputs/charts/raw_share_by_group.png');plt.show()
y=q.assign(y=q.date.dt.year).groupby(['group','y'])[['regs_e2w','regs_2w']].sum();y=(100*y.regs_e2w/y.regs_2w).unstack(0).round(2);print(y);y.to_csv('../outputs/tables/share_by_group_year.csv')
m_=P.assign(y=P.date.dt.year).groupby(['group','state','y'])[['regs_e2w','regs_2w']].sum().reset_index();m_['s']=100*m_.regs_e2w/m_.regs_2w
med=m_.groupby(['y','group']).s.median().unstack().round(2);print(med);med.to_csv('../outputs/tables/median_share_by_year.csv')
save_metrics('median_2023',med.loc[2023].to_dict())
save_metrics('raw',{'paid_2023':y.loc[2023,'paid'],'ctrl_2023':y.loc[2023,'control'],'paid_2019':y.loc[2019,'paid'],'ctrl_2019':y.loc[2019,'control']})'''
]

N2=["MD:# 2. Event study\nCallaway-Sant'Anna ATT against never-subsidised states, each treated state counted equally. `Pre-specified` is the plan as written, with Chandigarh. `Headline` drops Chandigarh because its treatment is a petrol cap plus a subsidy.",
'''p=load();pn=p[p.state!='CHANDIGARH']
gm=lambda d:d.dropna(subset=['gt']).groupby('state')['gt'].first().astype(int).to_dict()
c=sorted(p[p.group=='control'].state.unique());g=gm(p);gh=gm(pn)
rows=[];store={}
for nm,d,gg in [('Pre-specified, 7 states',p,g),('Headline, without Chandigarh',pn,gh)]:
  for y in ['share','logodds']:
    W=wide(d,y);s,a,b=event_study(W,gg,c);ev,r=boot(W,gg,c,n=999);lo,hi=np.nanpercentile(r[:,0],[2.5,97.5])
    R=rand_inf(W,gg,c,n=1999);ri=(np.abs(R[:,0])>=abs(a)).mean()
    rows.append(dict(run=nm,outcome=y,att_0_12=a,ci_lo=lo,ci_hi=hi,ri_p=ri,pre_m12_m2=s.loc[-12:-2].mean(),all_post=b))
    store[(nm,y)]=(s,np.nanpercentile(ev,[2.5,97.5],axis=0))
T=pd.DataFrame(rows).round(3);T.to_csv('../outputs/tables/main_results.csv',index=False);print(T.to_string())
h=T.iloc[2];l=T.iloc[3]
save_metrics('main',{'prespec_att':T.iloc[0].att_0_12,'att':h.att_0_12,'ci':[h.ci_lo,h.ci_hi],'ri_p':h.ri_p,'pre':h.pre_m12_m2,'lo_att':l.att_0_12,'lo_ci':[l.ci_lo,l.ci_hi],'lo_ri_p':l.ri_p,'lo_pre':l.pre_m12_m2})''',
'''fig,axs=plt.subplots(1,2,figsize=(10,3.6))
for ax,y,t,yl in [(axs[0],'share','Points: a rise after the start, wide bands','Change in electric share, points'),(axs[1],'logodds','Proportional: nothing separable from zero','Change in log-odds')]:
    s,ci=store[('Headline, without Chandigarh',y)]
    ax.fill_between(s.index,ci[0],ci[1],color=ACC,alpha=.15,lw=0);ax.plot(s.index,s.values,color=ACC,marker='o',ms=3.5)
    ax.axhline(0,color=MUTE,lw=1);ax.axvline(-.5,color=INK,lw=1,ls=':');ax.set_title(t);ax.set_ylabel(yl);ax.set_xlabel('Months from subsidy start')
plt.tight_layout();plt.savefig('../outputs/charts/event_study.png',dpi=170);plt.show()
s,ci=store[('Headline, without Chandigarh','share')];pd.DataFrame({'event_month':s.index,'att':s.values,'lo':ci[0],'hi':ci[1]}).round(3).to_csv('../outputs/tables/event_study_share.csv',index=False)''',
"MD:## State by state\nThe average hides the spread. Each state is compared with the 17 controls on its own.",
'''W=wide(pn,'share');L=wide(pn,'logodds');rs=[]
for k,v in gh.items():
    s,a,_=event_study(W,{k:v},c,leads=12);s2,a2,_=event_study(L,{k:v},c,leads=12)
    rs.append(dict(state=k,start=str(pn[pn.state==k].g.iloc[0])[:7],att_points=a,pre_points=s.loc[-12:-2].mean(),att_logodds=a2))
S=pd.DataFrame(rs).sort_values('att_points').round(2);S.to_csv('../outputs/tables/by_state.csv',index=False);print(S.to_string(index=False))
fig,ax=plt.subplots(figsize=(6.5,2.8));ax.barh(S.state.str.title(),S.att_points,color=[BAD if v<0 else ACC for v in S.att_points],height=.55)
ax.axvline(0,color=MUTE,lw=1);ax.set_xlabel('Effect on electric share, points, months 0 to 12');ax.set_title('Wide spread by state: Goa +4.2 to UP -1.0');plt.savefig('../outputs/charts/by_state.png');plt.show()
save_metrics('by_state',S.set_index('state').att_points.to_dict())''',
"MD:## Weighted by registrations\nThe headline counts each state equally, so Goa, about 1% of treated registrations, gets a sixth of the weight. This is the same state-level estimate weighted by two-wheeler registrations over months 0 to 12.",
'''wt={k:pn[(pn.state==k)&(pn['t']>=v)&(pn['t']<=v+12)].regs_2w.sum() for k,v in gh.items()}
Sb=S.set_index('state');ws=pd.Series(wt)
wa=(Sb.att_points*ws).sum()/ws.sum();wa6=sum(event_study(W,{k:v},c,leads=12,base_k=6)[1]*wt[k] for k,v in gh.items())/ws.sum()
print(round(wa,3),round(wa6,3),(ws/ws.sum()).round(3).to_dict());save_metrics('weighted',{'att':wa,'att_base6':wa6,'goa_weight':ws['GOA']/ws.sum()})''',
"MD:## Chandigarh without the two cap months\nThe spike could be removed without losing the state: February and March 2023 are blanked.",
'''pb=p.copy();pb.loc[(pb.state=='CHANDIGARH')&(pb.date.isin(pd.to_datetime(['2023-02-01','2023-03-01']))),'share']=np.nan
Wb=wide(pb,'share');_s,ab,_=event_study(Wb,g,c);sc,ac,_=event_study(Wb,{'CHANDIGARH':g['CHANDIGARH']},c,leads=12);print(round(ab,3),round(ac,3));save_metrics('chandigarh_blanked',{'seven_state':ab,'alone':ac})''',
"MD:## Counterfactual scale\nWhat share would treated states have had, on the estimate?",
'''W=wide(pn,'share');vals=[]
for k,v in gh.items(): vals.append(W.loc[k,[t for t in W.columns if v<=t<=v+12]].mean())
ob=np.mean(vals);save_metrics('scale',{'treated_mean_share_0_12':ob});print(round(ob,2))''',
"MD:## Two-way fixed effects, for comparison\nBiased under staggered timing and growing effects. Shown because reviewers expect it.",
'''import pyfixest as pf
r=[]
for nm,d in [('Pre-specified',p),('Headline',pn)]:
  for y in ['share','logodds']:
    f=pf.feols(f'{y}~post|state+t',data=d.dropna(subset=[y]),vcov={'CRV1':'state'});r.append(dict(run=nm,y=y,coef=f.coef().iloc[0],se=f.se().iloc[0]))
for y in ['share']:
    q=pn[(pn['gt'].isna())|(pn['t']<=pn['gt']+12)].dropna(subset=[y]);f=pf.feols(f'{y}~post|state+t',data=q,vcov={'CRV1':'state'});r.append(dict(run='Headline, months 0 to 12 only',y=y,coef=f.coef().iloc[0],se=f.se().iloc[0]))
r=pd.DataFrame(r).round(3);r.to_csv('../outputs/tables/twfe.csv',index=False);print(r);save_metrics('twfe',r.to_dict('records'))''',
"MD:## Library cross-check\nThe hand-written estimator is checked against the `csdid` package on group-time effects.",
'''from csdid.att_gt import ATTgt
d=pn.copy();d['id']=d.state.astype('category').cat.codes;d['gv']=d['gt'].fillna(0).astype(int)+d['gt'].notna().astype(int);d['tt']=d['t']+1
d['share']=d.share.fillna(0)
o=ATTgt(yname='share',gname='gv',idname='id',tname='tt',data=d[['share','gv','id','tt']],control_group='nevertreated',est_method='reg').fit(est_method='reg',base_period='universal',bstrap=False)
res=o.summ_attgt().summary2
res=res.rename(columns=lambda x:x.strip())
gc=[c_ for c_ in res.columns if c_.lower() in('group',)][0];tc=[c_ for c_ in res.columns if c_.lower() in('time',)][0];ac=[c_ for c_ in res.columns if 'att' in c_.lower()][0]
res=res[[gc,tc,ac]].astype(float);res=res[(res[tc]>=res[gc])&(res[tc]<=res[gc]+12)]
lib=res.groupby(gc)[ac].mean();w=d.groupby('gv').id.nunique();w=w[w.index>0]
lib_att=(lib*w.reindex(lib.index)).sum()/w.reindex(lib.index).sum()
Y0=wide(pn.assign(share=pn.share.fillna(0)),'share');own=event_study(Y0,gh,c)[1]
print(round(lib_att,3),round(own,3));save_metrics('csdid',{'lib':lib_att,'own':own})'''
]

N3=["MD:# 3. Robustness\nEach row changes one thing against the headline run: CS, 6 treated states, 17 controls, Jan 2019 to Dec 2023. Effect is the mean over months 0 to 12.",
'''p=load();pn=p[p.state!='CHANDIGARH']
gm=lambda d:d.dropna(subset=['gt']).groupby('state')['gt'].first().astype(int).to_dict()
c=sorted(p[p.group=='control'].state.unique());g=gm(pn)
def run(lbl,d=pn,gg=g,cc=c,**k):
    A=[]
    for y in ['share','logodds']:
        W=wide(d,y);s,a,_=event_study(W,gg,cc,**k);A+= [a,s.loc[-12:-2].mean()]
    return dict(check=lbl,points=A[0],pre_points=A[1],logodds=A[2],pre_logodds=A[3])
R=[run('Headline')]
R.append(run('Base is mean of last 6 months, not month -1',base_k=6))
for k_ in g:
    R.append(run(f'Drop {k_.title()}',gg={a:b for a,b in g.items() if a!=k_}))
R.append(run('Drop Karnataka, Tamil Nadu from controls',cc=[x for x in c if x not in('KARNATAKA','TAMIL NADU')]))
big=p[p.year==2019].groupby('state').regs_2w.sum();cb=[x for x in c if big[x]>=300000]
R.append(run(f'Controls over 3 lakh 2W a year ({len(cb)})',cc=cb))
a=load(alt_dates=True);a=a[a.state!='CHANDIGARH'];R.append(run('Chhattisgarh start Aug 2022',d=a,gg=gm(a)))
o=load(override={'CHHATTISGARH':'2022-04'});o=o[o.state!='CHANDIGARH'];R.append(run('Chhattisgarh start Apr 2022, as first planned',d=o,gg=gm(o)))
gc=pn.copy();gc.loc[(gc.state=='GOA')&(gc.date>'2022-07-01'),['share','logodds']]=np.nan;R.append(run('Goa cut at end of first scheme, Jul 2022',d=gc))
b=load(treat=('paid','paper'));b=b[b.state!='CHANDIGARH'];R.append(run('Add 5 on-paper states (11), months 0 to 10',d=b,gg=gm(b),cc=c,lags=10))
e=load(treat=('paper',));R.append(run('On-paper states only (5), months 0 to 10',d=e,gg=gm(e),cc=c,lags=10))
Wb=wide(pn[pn.state.isin(list(g)+cb)],'share');_x,ab,_y=event_study(Wb,g,cb);Rb=rand_inf(Wb,g,cb,n=1999);pb=(np.abs(Rb[:,0])>=abs(ab)).mean();print('large-control RI p',pb);save_metrics('large_controls',{'att':ab,'ri_p':pb,'n':len(cb),'names':cb})
T=pd.DataFrame(R).round(3);T.to_csv('../outputs/tables/robustness.csv',index=False);print(T.to_string(index=False))
save_metrics('robust',T.set_index('check').to_dict('index'))''',
"MD:## Imputation estimator, with and without state trends\nFits state and month effects on untreated cells only, then predicts what treated states would have done. State trends absorb any steady gap in growth.",
'''rows=[]
for y in ['share','logodds']:
  for tr in [False,True]:
    a_,st=imp_att(pn,y,tr);Rr=rand_imp(pn,y,tr,n=499);rows.append(dict(outcome=y,state_trends=tr,att=a_,ri_p=(np.abs(Rr)>=abs(a_)).mean()))
I=pd.DataFrame(rows).round(3);I.to_csv('../outputs/tables/imputation.csv',index=False);print(I);save_metrics('impute',I.to_dict('records'))''',
"MD:## Estimator grid\nThe same question through each estimator, with randomisation p-values, so no single choice carries the verdict. Pre-trend uses months -12 to -7, which do not overlap the six-month base.",
'''rows=[]
for y in ['share','logodds']:
    W=wide(pn,y)
    for lbl,k_,ix in [('CS, base month -1',1,0),('CS, base last 6 months',6,0),('CS, all post months',1,2)]:
        s_,a_,b_=event_study(W,g,c,base_k=k_);v=a_ if ix==0 else b_;Rr=rand_inf(W,g,c,n=999,base_k=k_)
        rows.append(dict(outcome=y,spec=lbl,att=v,ri_p=(np.abs(Rr[:,ix])>=abs(v)).mean(),pre_m12_m7=s_.loc[-12:-7].mean(),pre_m6_m2=s_.loc[-6:-2].mean()))
G=pd.DataFrame(rows).round(3);G.to_csv('../outputs/tables/estimator_grid.csv',index=False);print(G.to_string(index=False));save_metrics('grid',G.to_dict('records'))''',
"MD:## Placebo dates\nEvery treated state is moved 12 months early, and data from its real start onward is deleted. A real design shows nothing here.",
'''def placebo(y):
    d=pn.copy();d=d[~(d.g.notna()&(d.date>=d.g))]
    gg={k:v-12 for k,v in g.items() if v-12>=7};W=wide(d,y)
    s,a,_=event_study(W,gg,c,leads=6,lags=11);R_=rand_inf(W,gg,c,n=1999,leads=6,lags=11)
    return a,(np.abs(R_[:,0])>=abs(a)).mean(),np.percentile(R_[:,0],[2.5,97.5])
P={y:placebo(y) for y in ['share','logodds']};print(P)
save_metrics('placebo',{y:{'att':P[y][0],'ri_p':P[y][1]} for y in P})''',
"MD:## Placebo outcome\nThe subsidy should not move non-electric registrations much. A large shift would point to a demand shock.",
'''W=wide(pn,'log_nonev');s,a,_=event_study(W,g,c);R_=rand_inf(W,g,c,n=1999);pv=(np.abs(R_[:,0])>=abs(a)).mean();print(a,pv);save_metrics('placebo_outcome',{'att':a,'ri_p':pv})''',
"MD:## Randomisation distribution\nThe actual dates are dealt to random states 1,999 times.",
'''W=wide(pn,'share');_,a,_b=event_study(W,g,c);RR=rand_inf(W,g,c,n=1999)
sm=(RR[:,0]>=a).mean();two=(np.abs(RR[:,0])>=abs(a)).mean()
fig,ax=plt.subplots(figsize=(6.5,2.8));ax.hist(RR[:,0],bins=40,color=MUTE);ax.axvline(a,color=BAD);ax.set_xlabel('Fake effect, points');ax.set_title('The real estimate against random assignments');ax.set_yticks([]);plt.savefig('../outputs/charts/randomisation.png');plt.show()
print(sm,two);save_metrics('ri',{'two_sided':two})''',
"MD:## Does the gap survive?\nDescriptive only: the window is extended to October 2026. Several subsidies ended and other states began, so this is not a causal estimate.",
'''P=load(end='2026-10-01');P=P[P.state!='CHANDIGARH']
s=P.groupby([P.date.dt.year,'state']).agg(g=('group','first'),e=('regs_e2w','sum'),n=('regs_2w','sum'));s['sh']=100*s.e/s.n
t=s.reset_index().groupby(['date','g']).sh.median().unstack().round(2);print(t);t.to_csv('../outputs/tables/median_share_by_year.csv');save_metrics('median_2026',t.loc[2026].to_dict())''',
"MD:## Cost per additional EV\nThe plan set this to run only if the effect survives. It does not clearly survive, so this is a conditional range. It takes each state's own estimate at face value. Spending has a low and a high case because the Maharashtra early-bird add-on may or may not stack, its base subsidy stopped sometime in 2022, and Goa's scheme had a unit cap. Battery size of 3 kWh is an assumption. Chhattisgarh is left out: its terms have no clear two-wheeler cap.",
'''bs=pd.read_csv('../outputs/tables/by_state.csv').set_index('state').att_points
rows=[];win={k:pn[(pn.state==k)&(pn['t']>=v)&(pn['t']<=v+12)] for k,v in g.items()}
mh=win['MAHARASHTRA'];mh_a=mh[mh.date<='2022-03-01'].regs_e2w.sum();mh_b=mh[mh.date>'2022-03-01'].regs_e2w.sum()
goa=win['GOA'];goa_live=goa[goa.date<='2022-07-01'].regs_e2w.sum()
low={'DELHI':win['DELHI'].regs_e2w.sum()*15000,'MAHARASHTRA':mh_a*10000,'ODISHA':win['ODISHA'].regs_e2w.sum()*5000,'GOA':5.5e7,'UTTAR PRADESH':win['UTTAR PRADESH'].regs_e2w.sum()*5000}
high={**low,'MAHARASHTRA':mh_a*25000+mh_b*10000,'GOA':min(goa_live,3000)*30000}
C=pd.DataFrame({'spend_low':low,'spend_high':high});C['all2w']=[win[k].regs_2w.sum() for k in C.index];C['e2w']=[win[k].regs_e2w.sum() for k in C.index];C['att']=bs.reindex(C.index)
C['extra']=C.att/100*C.all2w;C['extra_floored']=C.extra.clip(lower=0);C.round(1).to_csv('../outputs/tables/cost_inputs.csv');print(C)
lo,hi=C.spend_low.sum(),C.spend_high.sum();ef,eu=C.extra_floored.sum(),C.extra.sum()
out=dict(spend_low_cr=lo/1e7,spend_high_cr=hi/1e7,extra_floored=ef,extra_unfloored=eu,rs_low=lo/ef,rs_high=(hi/eu if eu>0 else None),avg_low=lo/C.e2w.sum(),avg_high=hi/C.e2w.sum(),additional_share_floored=ef/C.e2w.sum(),additional_share_unfloored=eu/C.e2w.sum(),goa_live_ev=int(goa_live))
print(out);save_metrics('cost',out)'''
]
os.makedirs('notebooks',exist_ok=True)
which=sys.argv[1:] or ['1','2','3']
if '1' in which: nb(N1,'notebooks/01_panel_and_coverage.ipynb')
if '2' in which: nb(N2,'notebooks/02_event_study.ipynb')
if '3' in which: nb(N3,'notebooks/03_robustness.ipynb')
