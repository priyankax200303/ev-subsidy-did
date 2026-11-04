"""Shared loaders and a transparent Callaway-Sant'Anna estimator."""
import os, numpy as np, pandas as pd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START,END='2019-01-01','2023-12-01'

def load(root=ROOT,start=START,end=END,treat=('paid',),ctrl=('control',),alt_dates=False,override=None):
    p=pd.read_csv(f'{root}/data/processed/vahan_2w_panel.csv',parse_dates=['date'])
    c=pd.read_csv(f'{root}/data/policy/treatment_coding.csv')
    col='alt_treat_month' if alt_dates else 'treat_month'
    c['g']=pd.to_datetime(c[col].fillna(c.treat_month)+'-01',errors='coerce')
    for k,v in (override or {}).items(): c.loc[c.state==k,'g']=pd.Timestamp(v+'-01')
    c=c[c.group.isin(list(treat)+list(ctrl))]
    p=p[p.state.isin(c.state)&p.date.between(start,end)].copy()
    p=p.merge(c[['state','group','g']],on='state')
    p.loc[p.group.isin(ctrl),'g']=pd.NaT
    p['share']=np.where(p.regs_2w>0,100*p.regs_e2w/p.regs_2w.replace(0,np.nan),np.nan)
    p['logodds']=np.where(p.regs_2w>0,np.log((p.regs_e2w+.5)/(p.regs_2w-p.regs_e2w+.5)),np.nan)
    p['log_nonev']=np.log((p.regs_2w-p.regs_e2w).clip(lower=1))
    p['t']=(p.date.dt.year-2019)*12+p.date.dt.month-1
    p['post']=(p.g.notna()&(p.date>=p.g)).astype(int)
    p['gt']=(p.g.dt.year-2019)*12+p.g.dt.month-1
    return p

def wide(p,y):
    return p.pivot(index='state',columns='t',values=y).sort_index(axis=1)

def event_study(Y,g,ctrl,leads=18,lags=12,base_k=1):
    """Y: state x t array frame. g: dict state->treat t. ctrl: list of comparison states.
    ATT(g,t) uses g-1 as the base for every t, compared with the same change in ctrl.
    Each treated state counts equally. Returns event-time series and the mean of months 0..lags."""
    rows={}
    C=Y.loc[ctrl]
    es=range(-leads,lags+1)
    gs=pd.Series(g)
    tv=Y.columns.values
    out={e:[] for e in es}; post=[]
    for coh,sts in gs.groupby(gs).groups.items():
        base=coh-1
        bw=[c for c in range(coh-base_k,coh) if c in Y.columns]
        dT=Y.loc[list(sts)].sub(Y.loc[list(sts),bw].mean(axis=1),axis=0).mean(skipna=True)
        dC=C.sub(C[bw].mean(axis=1),axis=0).mean(skipna=True)
        a=dT-dC
        for e in es:
            if coh+e in a.index: out[e].extend([a[coh+e]]*len(sts))
        post.extend(list(np.repeat(a[a.index>=coh].mean(),len(sts))))
    s=pd.Series({e:np.nanmean(v) if len(v) else np.nan for e,v in out.items()})
    return s,s.loc[0:lags].mean(),float(np.mean(post))

def boot(Y,g,ctrl,n=999,seed=7,**k):
    """State cluster bootstrap, resampling treated and comparison states separately."""
    r=np.random.default_rng(seed); tr=list(g); res=[]; ev=[]
    for _ in range(n):
        ts=list(r.choice(tr,len(tr))); cs=list(r.choice(ctrl,len(ctrl)))
        names_t=[f'{s}#{i}' for i,s in enumerate(ts)]; names_c=[f'{s}#c{i}' for i,s in enumerate(cs)]
        Yb=pd.concat([Y.loc[ts+cs]]).copy(); Yb.index=names_t+names_c
        gb={n_:g[s] for n_,s in zip(names_t,ts)}
        s,a,b=event_study(Yb,gb,names_c,**k); ev.append(s.values); res.append((a,b))
    return np.array(ev),np.array(res)

def rand_inf(Y,g,ctrl,n=4999,seed=11,**k):
    """Reassign the actual treatment dates to random states from the pooled sample."""
    r=np.random.default_rng(seed); pool=list(g)+list(ctrl); dates=list(g.values()); res=[]
    for _ in range(n):
        ch=list(r.permutation(pool)); tg=dict(zip(ch[:len(dates)],dates))
        s,a,b=event_study(Y,tg,ch[len(dates):],**k); res.append((a,s.loc[:-2].mean(),b))
    return np.array(res)

def impute(p,y,trend=False):
    """Imputation DiD (Borusyak-Jaravel-Spiess style). Fit state and month effects, optionally
    state linear trends, on untreated cells only, predict Y(0) for treated cells, and return
    (t-level frame with tau, event time)."""
    from scipy import sparse
    from scipy.sparse.linalg import lsqr
    d=p.dropna(subset=[y]).copy().reset_index(drop=True)
    si=d.state.astype('category').cat.codes.values; ns=si.max()+1
    ti=d.t.astype('category').cat.codes.values; nt=ti.max()+1
    n=len(d); r=np.arange(n)
    cols=[sparse.csr_matrix((np.ones(n),(r,si)),shape=(n,ns)),sparse.csr_matrix((np.ones(n),(r,ti)),shape=(n,nt))]
    if trend: cols.append(sparse.csr_matrix(((d.t.values-30)/12,(r,si)),shape=(n,ns)))
    X=sparse.hstack(cols).tocsr(); u=d.post.values==0
    b=lsqr(X[u],d.loc[u,y].values,atol=1e-10,btol=1e-10,iter_lim=20000)[0]
    d['tau']=d[y]-X@b
    d['e']=d['t']-d['gt']
    return d

def imp_att(p,y,trend=False,lags=12):
    d=impute(p,y,trend); tr=d[d.post==1]; tr=tr[tr.e<=lags]
    return tr.groupby('state').tau.mean().mean(), tr.groupby('state').tau.mean()


def rand_imp(p,y,trend,n=499,seed=13,lags=12):
    """Randomisation inference for the imputation estimator."""
    r=np.random.default_rng(seed); s0=p.groupby('state').agg(g=('gt','first'));tr=s0.dropna()
    dates=tr.g.values; pool=s0.index.values; res=[]
    for _ in range(n):
        ch=r.permutation(pool)[:len(dates)]; m=dict(zip(ch,dates)); d=p.copy()
        d['gt']=d.state.map(m); d['post']=(d['gt'].notna()&(d.t>=d['gt'])).astype(int)
        res.append(imp_att(d,y,trend,lags)[0])
    return np.array(res)
