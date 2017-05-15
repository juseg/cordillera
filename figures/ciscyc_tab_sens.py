#!/usr/bin/env python2
# coding: utf-8

import util as ut
import numpy as np

res = '10km'
rec = 'grip'

# latex header and footer
header=r'''\documentclass[border=2.5mm]{standalone}
\newcommand\tophline{\hline\noalign{\vspace{1mm}}}
\newcommand\middlehline{\noalign{\vspace{1mm}}\hline\noalign{\vspace{1mm}}}
\newcommand\bottomhline{\noalign{\vspace{1mm}}\hline}
\newcommand{\unit}[1]{\ensuremath{\mathrm{#1}}}

\begin{document}

  \begin{tabular}{l|ccc|ccc|ccc}
    \tophline
             & \multicolumn{3}{c|}{Age (ka)}
             & \multicolumn{3}{c|}{Ice extent (\unit{10^6\,km^2})}
             & \multicolumn{3}{c}{Ice volume (m\,s.l.e.)} \\
    Config.  &  MIS~4 &  MIS~3 &  MIS~2
             &  MIS~4 &  MIS~3 &  MIS~2
             &  MIS~4 &  MIS~3 &  MIS~2 \\
    \middlehline
'''
footer=r'''    \bottomhline
  \end{tabular}

\end{document}
'''

# latex table line (curly braces need to be doubled to escape)
tabline = (' '*4 + '{title:8}' + ' &{:7.2f}'*3 + '\n'+
           ' '*12 + ' &{:7.2f}'*3 + '\n'+
           ' '*12 + ' &{:7.2f}'*3 + r' \\' + '\n')
errline = (' '*4 + '{title:8}' + r' &{:5.0f}\,\unit{{\%}}'*3 + '\n'+
           ' '*12 + r' &{:5.0f}\,\unit{{\%}}'*3 + '\n'+
           ' '*12 + r' &{:5.0f}\,\unit{{\%}}'*3 + r' \\' + '\n')

# initialize array
results = np.zeros((5, 9), dtype=float)

# open latex file to write in
with open('ciscyc_tab_sens.tex', 'w') as f:

    # write header
    f.write(header)

    # loop on records
    for i, conf in enumerate(ut.sens.configs):
        dt = ut.sens.offsets[i]
        label = ut.sens.labels[i]

        # get MIS times
        mis_idces, mis_times = ut.io.get_mis_times(res, rec, dt, config=conf)

        # compute area from extra file
        nc = ut.io.open_extra_file(res, rec, dt, config=conf)
        ex_thk = nc.variables['thk']
        ex_time = nc.variables['time']
        ex_mask = nc.variables['mask']
        ex_idces = [(np.abs(ex_time[:]-t*ut.a2s)).argmin() for t in mis_times]
        mis_gareas = ((ex_thk[ex_idces] >= ut.thkth)*
                      (ex_mask[ex_idces] == 2)).sum(axis=(1,2))*1e-4
        nc.close()

        # load output time series
        nc = ut.io.open_ts_file(res, rec, dt, config=conf)
        ts_time = nc.variables['time'][:]*ut.s2ka
        ts_ivol = nc.variables['slvol'][:]
        nc.close()
        mis_slvols = ts_ivol[mis_idces]

        # write info in table
        results[i] = np.concatenate((-mis_times/1e3, mis_gareas, mis_slvols))
        f.write(tabline.format(title=label, *results[i]))

        # compute relative errors
        if i in (2, 4):
            relerr = 100*np.abs(results[i]-results[i-1])/results[0]
            f.write(errline.format(title='R. diff.', *relerr))

        # add horizontal lines
        if i in (0, 2):
            f.write('    \cline{1-10}\n')

    # write footer
    f.write(footer)

# close latex file
f.close()
