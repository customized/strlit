
import streamlit as st
import pandas as pd
import numpy as np
import math


import altair as alt
from vega_datasets import data

st.title("""
Dashboard
""")
#
# st.sidebar.header('Menu')
# st.sidebar.write(["Plot, Altair, Plotly"])


### KPI
from streamlit_metrics import metric, metric_row

# st.write("## Here's a single figure")
metric("Revenue $M (YTD)", 500)

# st.write("## ... and here's a row of them")
metric_row(
    {
        "Asia": 250,
        "SE Asia": 120,
        "Singapore": 80
    }
)



### Line chart


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)



col1,col2 = st.beta_columns([1,2])

### Slope graph

with col1:
    source = data.barley()

    s = alt.Chart(source).mark_line().encode(
        x='year:O',
        y='median(yield)',
        color='site'
    )
    st.altair_chart(s, use_container_width=True)


### Parallel Coordinates

with col2:
    source = data.iris()

    p = alt.Chart(source).transform_window(
        index='count()'
    ).transform_fold(
        ['petalLength', 'petalWidth', 'sepalLength', 'sepalWidth']
    ).mark_line().encode(
        x='key:N',
        y='value:Q',
        color='species:N',
        detail='index:N',
        opacity=alt.value(0.5)
    ).properties(width=50)

    st.altair_chart(p, use_container_width=True)


### Sorted Trellis plot
source = data.stocks()

t = alt.Chart(source).transform_filter(
    alt.datum.symbol != 'GOOG'
).mark_area().encode(
    x='date:T',
    y='price:Q',
    color='symbol:N',
    row=alt.Row('symbol:N', sort=['MSFT', 'AAPL', 'IBM', 'AMZN'])
).properties(height=50, width=400)

st.altair_chart(t, use_container_width=False)



    ### Horizontal plot
my_expander = st.beta_expander(label='Contribution')
with my_expander:

    source = data.wheat()

    bars = alt.Chart(source).mark_bar().encode(
        x='wheat:Q',
        y="year:O"
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='wheat:Q'
    )

    (bars + text).properties(height=900)


    st.altair_chart(bars+text, use_container_width=True)



### Scatter

my_expander = st.beta_expander(label='Customer Overview')
with my_expander:

    df = pd.DataFrame(
        np.random.randn(200, 3),
        columns=['a', 'b', 'c'])

    c = alt.Chart(df).mark_circle().encode(
        x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

    st.altair_chart(c, use_container_width=True)




### layered histogram
np.random.seed(42)

my_expander = st.beta_expander(label='Distribution')
with my_expander:

    # Generating Data
    source = pd.DataFrame({
        'Trial A': np.random.normal(0, 0.8, 1000),
        'Trial B': np.random.normal(-2, 1, 1000),
        'Trial C': np.random.normal(3, 2, 1000)
    })

    h = alt.Chart(source).transform_fold(
        ['Trial A', 'Trial B', 'Trial C'],
        as_=['Experiment', 'Measurement']
        ).mark_area(
        opacity=0.3,
        interpolate='step'
        ).encode(
        alt.X('Measurement:Q', bin=alt.Bin(maxbins=100)),
        alt.Y('count()', stack=None),
        alt.Color('Experiment:N'))

    st.altair_chart(h, use_container_width=True)
