#!/usr/bin/env python

from altair import *
import pandas  # http://pandas.pydata.org
import numpy
import datetime

from fileops import save
from filters import *
from logic import *

name = 'cuda89'

# begin user settings for this script
roots = ['../gunrock-output/cuda8', '../gunrock-output/cuda9']
fnFilterInputFiles = [fileEndsWithJSON,
                      ]
fnPreprocessDF = [selectAnyOfThese('engine', ['Gunrock']),
                  convertCtimeStringToDate,
                  DOBFStoBFS,
                  equateRGG,
                  normalizePRMTEPS,
                  addJSONDetailsLink,
                  gunrockVersionGPU,
                  ]
fnFilterDFRows = [deleteZeroMTEPS,
                  ]
fnPostprocessDF = []
# end user settings for this script

# actual program logic
# do not modify

# choose input files
df = filesToDF(roots=roots,
               fnFilterInputFiles=fnFilterInputFiles)

for fn in fnPreprocessDF:       # alter entries / compute new entries
    df = fn(df)
for fn in fnFilterDFRows:       # remove rows
    df = fn(df)
for fn in fnPostprocessDF:      # alter entries / compute new entries
    df = fn(df)

# end actual program logic

# now make the graph

chart = Chart(df).mark_point(opacity=0.5).encode(
    x=X('dataset:N',
        axis=Axis(
            title='Dataset',
        ),
        ),
    column=Column('algorithm:N',
                  axis=Axis(
                      title='Primitive',
                      orient='top',
                  )
                  ),
    y=Y('elapsed',
        axis=Axis(
            title='Elapsed time (ms)',
        ),
        scale=Scale(type='log'),
        ),
    color=Color('[gpuinfo.runtime_version]:N',
                legend=Legend(
                    title='GPU runtime',
                ),
                ),
    shape=Shape('[gpuinfo.runtime_version]:N',
                legend=Legend(
                    title='GPU runtime',
                ),
                ),
)
print chart.to_dict(data=False)

save(chart=chart,
     df=df,
     plotname=name,
     formats=['html', 'svg', 'png', 'pdf', 'tablehtml'],
     sortby=['algorithm',
             'dataset',
             'engine',
             'gunrock_version'],
     columns=['algorithm',
              'dataset',
              'm_teps',
              'elapsed',
              'gunrock_version',
              'gpuinfo.name',
              'gpuinfo.driver_version',
              'details'],
     )
