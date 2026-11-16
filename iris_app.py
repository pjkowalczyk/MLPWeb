import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Streamlit Selections Tutorial", layout="wide")

st.title("🌱 Interactive Data Explorer")
st.write("Welcome! Use the sidebar selections below to filter and analyze the dataset.")

# Load sample dataset
@st.cache_data
def load_data():
    # Using a classic dataset via Plotly
    df = px.data.iris()
    return df

df = load_data()

# --- SIDEBAR SELECTIONS ---
st.sidebar.header("Filter Controls")

# 1. Multiselect for categorical filtering (Species)
available_species = df['species'].unique().tolist()
selected_species = st.sidebar.multiselect(
    label="Select Species to Display",
    options=available_species,
    default=available_species
)

# 2. Slider for numerical threshold filtering (Sepal Length)
min_sepal, max_sepal = float(df['sepal_length'].min()), float(df['sepal_length'].max())
sepal_range = st.sidebar.slider(
    label="Sepal Length Range (cm)",
    min_value=min_sepal,
    max_value=max_sepal,
    value=(min_sepal, max_sepal)
)

# 3. Selectbox for choosing chart axes
numeric_columns = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
x_axis = st.sidebar.selectbox("Choose X-axis metric", numeric_columns, index=0)
y_axis = st.sidebar.selectbox("Choose Y-axis metric", numeric_columns, index=1)

# --- APPLY FILTERS ---
filtered_df = df[
    (df['species'].isin(selected_species)) & 
    (df['sepal_length'] >= sepal_range[0]) & 
    (df['sepal_length'] <= sepal_range[1])
]

# Display summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Records", len(df))
col2.metric("Filtered Records", len(filtered_df))
col3.metric("Retention Rate", f"{(len(filtered_df) / len(df)) * 100:.1f}%")

st.divider()

# --- DATA VISUALIZATION ---
st.subheader("📊 Interactive Scatter Plot")

if filtered_df.empty:
    st.warning("No data matches your selected filters. Please adjust the sidebar controls.")
else:
    fig = px.scatter(
        filtered_df,
        x=x_axis,
        y=y_axis,
        color="species",
        size="petal_width",
        hover_data=['petal_length'],
        title=f"{y_axis.title()} vs {x_axis.title()}"
    )
    
    # Render plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# --- RAW DATA VIEW ---
with st.expander("🔍 View Raw Filtered Data"):
    st.dataframe(filtered_df, use_container_width=True)