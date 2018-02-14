#!/usr/bin/env python
import os,sys,pdb,scipy,glob
from pylab import *
from strolger_util import util as u
from scipy.integrate import simps
from stsci.convolve import boxcar
rcParams['figure.figsize']=15.3, 18.75
rcParams['font.size']=18.0



if __name__=='__main__':



    metals = glob.glob('../SN_SFH/*/*.dat')
    lbu = 9.5
    lbl = 0.003
    bxsmooth=3
    
    fig = plt.figure()
    fig.suptitle = ('test')
    fig.text(0.5,0.04,'Lookback Time (Gyr)',ha='center',va='center')
    fig.text(0.06,0.5,r'Average Metallicity ($Z/Z_{\odot}$)',ha='center',va='center',rotation='vertical')
    

    
    ax1=subplot(221)
    composite = 0
    for metal in metals:
        data = loadtxt(metal)[1:]
        ii = where((data[:,0]>lbl)&(data[:,0]<=lbu))
        data = data[ii]
        composite+=data[:,3]
        ax1.plot(data[:,0], data[:,3], '-', color='0.65',alpha=0.3)
    ax1.plot(data[:,0],composite/len(metals),'k-', label='%d SNe Hosts' %len(metals))

    codex = []
    f = open('../SN_SFH/goodsn_match_idcand.dat')
    lines=f.readlines()
    f.close()
    for line in lines:
        if line.startswith('#'): continue
        c = line.split()
        codex.append(c[:2])
    f = open('../SN_SFH/goodss_match_idcand.dat')
    lines=f.readlines()
    f.close()
    for line in lines:
        if line.startswith('#'): continue
        c = line.split()
        codex.append(c[:2])
    codex=array(codex)

    f = open('goods_1as.csv')
    lines = f.readlines()
    f.close()
    ias = []
    for line in lines:
        if line.startswith('#'): continue
        ias.append(line.split(',')[0])

    goods_composite_ia=0
    misses = 0
    for ia in ias:
        idx = where(codex[:,1]==ia)
        if not codex[idx][:,0]: misses+=1; continue
        index = '%05d' %int(codex[idx][:,0][0])
        metal = glob.glob('../SN_SFH/*/%s.dat'%index)
        if not metal: continue
        data = loadtxt(metal[0])[1:]
        ii = where((data[:,0]>lbl)&(data[:,0]<=lbu))
        data = data[ii]
        goods_composite_ia += data[:,3]
    norm1=len(ias)-misses
    ax3 = subplot(222)
    ax31 = twinx(ax3)
    ax3.plot(data[:,0],goods_composite_ia/norm1,'b-',label='%d GOODS SNe Ia' %norm1)
    ax3.plot(data[:,0],composite/len(metals),'k',label='All SNe')
    test1 = goods_composite_ia/composite*(len(metals)/norm1)
    ax31.plot(data[:,0], test1,'r-', label='GOODS Quotient')
    ax3.axvspan(2.2,2.8,color='red',alpha=0.1)



    f = open('candels_guesses.csv')
    lines = f.readlines()
    f.close()
    ias = []
    for line in lines:
        if line.startswith('#'): continue
        if float(line.split(',')[-1]>0.5):
            ias.append(line.split(',')[0])

    candels_composite_ia=0
    misses = 0
    for ia in ias:
        idx = where(codex[:,1]==ia)
        if not codex[idx][:,0]: misses+=1; continue
        index = '%05d' %int(codex[idx][:,0][0])
        metal = glob.glob('../SN_SFH/*/%s.dat'%index)
        if not metal: continue
        data = loadtxt(metal[0])[1:]
        ii = where((data[:,0]>lbl)&(data[:,0]<=lbu))
        data = data[ii]
        candels_composite_ia += data[:,3]
    norm2=len(ias)-misses
    ax4 = subplot(223)
    ax41 = twinx(ax4)
    ax4.plot(data[:,0],candels_composite_ia/norm2,'b-',label='%d CANDELS SNe Ia' %norm2)
    ax4.plot(data[:,0],composite/len(metals),'k',label='All SNe')
    test2 = candels_composite_ia/composite*(len(metals)/norm2)
    ax41.plot(data[:,0], test2,'r-', label='CANDELS Quotient')


    ax5 = subplot(224)
    ax51 = twinx(ax5)
    ax5.plot(data[:,0],(candels_composite_ia+goods_composite_ia)/(norm1+norm2),
             'b-',label='%d SNe Ia' %(norm1+norm2))
    ax5.plot(data[:,0], composite/len(metals), 'k',label='All SNe')
    ax51.plot(data[:,0],(candels_composite_ia+goods_composite_ia)/composite*(len(metals)/(norm1+norm2)),
              'r-',label='SNe Ia Quotient')




    u.adjust_spines(ax1, ['bottom','left'])
    u.adjust_spines(ax3, ['bottom'])
    u.adjust_spines(ax31,['bottom'])
    u.adjust_spines(ax4, ['bottom','left'])
    u.adjust_spines(ax41,['bottom'])
    u.adjust_spines(ax5, ['bottom'])
    u.adjust_spines(ax51, ['bottom'])

    ylims = (-100,10)
    xlims = (lbl,lbu)
    ax1.set_ylim(ylims)
    ax3.set_ylim(ylims)
    ax4.set_ylim(ylims)
    ax5.set_ylim(ylims)
    ax31.set_ylim(0,1)
    ax41.set_ylim(0,3)
    ax51.set_ylim(0,1)

    ax1.set_xlim(xlims)
    ax3.set_xlim(xlims)
    ax4.set_xlim(xlims)
    ax5.set_xlim(xlims)

    ax1.legend(loc=1,frameon=False)
    ax3.legend(loc=1,frameon=False)#, fontsize=10)
    ax4.legend(loc=1,frameon=False)#, fontsize=10)
    ax5.legend(loc=1,frameon=False)#, fontsize=10)
    

    plt.subplots_adjust(wspace=0.01,hspace=0.01)
    #show()
    savefig('plot3.png',transparent=True)
        
