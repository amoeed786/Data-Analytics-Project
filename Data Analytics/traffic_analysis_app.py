import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title="Traffic Accident Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    data = pd.read_csv('DataSet/road-accidents.csv', skiprows=9, delimiter='|')
    data.columns = ["state", "drvr_fatl_col_bmiles", "perc_fatl_speed", "perc_fatl_alcohol", "perc_fatl_1st_time"]
    return data

data = load_data()

st.markdown(
    """
    <style>
        .main { background-color: #f9f9f9; padding: 20px; font-family: 'Arial', sans-serif; }
        .sidebar .sidebar-content { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); }
        h1 { color: #2c3e50; font-size: 28px; font-weight: bold; margin-bottom: 10px; }
        h2, h3 { color: #34495e; font-weight: bold; }
        p { font-size: 16px; color: #555555; }
        .footer { margin-top: 20px; text-align: center; font-size: 14px; color: #777777; }
        .card { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
        .metric { display: flex; justify-content: space-around; margin-bottom: 20px; }
        .metric > div { text-align: center; padding: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚗 Traffic Accident Analysis")
st.write("Explore insights and statistics on road accidents across the U.S.")

st.sidebar.header("Explore Analysis")
options = [
    "Overview",
    "Accident Severity by State",
    "Impact of Speed",
    "Alcohol Influence",
    "First-Time Offender",
    "High-Risk States"
]
selected_option = st.sidebar.radio("Choose an analysis:", options)

if selected_option == "Overview":
    st.header("🗂️ Dataset Overview")
    total_states = data['state'].nunique()
    avg_fatal_collisions = round(data['drvr_fatl_col_bmiles'].mean(), 2)
    avg_fatal_speed = round(data['perc_fatl_speed'].mean(), 2)
    avg_fatal_alcohol = round(data['perc_fatl_alcohol'].mean(), 2)
    
    st.markdown("<div class='metric'>", unsafe_allow_html=True)
    st.metric(label="🛣️ Total States", value=total_states)
    st.metric(label="⚠️ Avg Fatal Collisions", value=avg_fatal_collisions)
    st.metric(label="🏎️ Avg Fatal Speed (%)", value=f"{avg_fatal_speed}%")
    st.metric(label="🍸 Avg Fatal Alcohol (%)", value=f"{avg_fatal_alcohol}%")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.subheader("📊 Full Dataset Preview")
    st.write(data.head(10))

elif selected_option == "Accident Severity by State":
    st.header("Accident Severity by State")
    selected_state = st.selectbox("Select a State:", options=["All"] + sorted(data['state'].unique().tolist()))
    if selected_state != "All":
        data = data[data['state'] == selected_state]
    
    state_summary = data.groupby('state')[['drvr_fatl_col_bmiles', 'perc_fatl_speed']].mean().sort_values(by='drvr_fatl_col_bmiles', ascending=False)
    fig = px.bar(state_summary, x=state_summary.index, y='drvr_fatl_col_bmiles', title="Accident Severity by State", labels={'drvr_fatl_col_bmiles': 'Fatal Collisions'})
    st.plotly_chart(fig)

elif selected_option == "Impact of Speed":
    st.header("Impact of Speed on Fatalities")
    min_speed, max_speed = st.slider("Select Fatal Speed Range (%):", int(data['perc_fatl_speed'].min()), int(data['perc_fatl_speed'].max()), (int(data['perc_fatl_speed'].min()), int(data['perc_fatl_speed'].max())))
    filtered_data = data[(data['perc_fatl_speed'] >= min_speed) & (data['perc_fatl_speed'] <= max_speed)]
    
    fig = px.scatter(filtered_data, x='perc_fatl_speed', y='drvr_fatl_col_bmiles', title="Impact of Speed on Fatalities", color='perc_fatl_speed', labels={'perc_fatl_speed': 'Fatal Speed (%)', 'drvr_fatl_col_bmiles': 'Fatal Collisions'})
    st.plotly_chart(fig)

elif selected_option == "Alcohol Influence":
    st.header("Alcohol Influence on Accident Severity")
    min_alcohol, max_alcohol = st.slider("Select Alcohol Fatalities Range (%):", int(data['perc_fatl_alcohol'].min()), int(data['perc_fatl_alcohol'].max()), (int(data['perc_fatl_alcohol'].min()), int(data['perc_fatl_alcohol'].max())))
    filtered_data = data[(data['perc_fatl_alcohol'] >= min_alcohol) & (data['perc_fatl_alcohol'] <= max_alcohol)]
    
    fig = px.histogram(filtered_data, x='state', y='perc_fatl_alcohol', title="Alcohol Influence by State", color='perc_fatl_alcohol', labels={'perc_fatl_alcohol': 'Alcohol Fatalities (%)'})
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

elif selected_option == "First-Time Offender":
    st.header("First-Time Offender Impact on Fatalities")
    min_first_time, max_first_time = st.slider("Select First-Time Offender Range (%):", int(data['perc_fatl_1st_time'].min()), int(data['perc_fatl_1st_time'].max()), (int(data['perc_fatl_1st_time'].min()), int(data['perc_fatl_1st_time'].max())))
    filtered_data = data[(data['perc_fatl_1st_time'] >= min_first_time) & (data['perc_fatl_1st_time'] <= max_first_time)]
    
    fig = px.scatter(filtered_data, x='perc_fatl_1st_time', y='drvr_fatl_col_bmiles', title="First-Time Offender Impact on Fatal Collisions", color='perc_fatl_1st_time')
    st.plotly_chart(fig)

elif selected_option == "High-Risk States":
    st.header("High-Risk States with High Speed and Alcohol-Related Fatalities")
    speed_median = data['perc_fatl_speed'].median()
    alcohol_median = data['perc_fatl_alcohol'].median()
    
    selected_state = st.selectbox("Select a State:", options=["All"] + sorted(data['state'].unique().tolist()))
    high_risk_data = data[(data['perc_fatl_speed'] > speed_median) & (data['perc_fatl_alcohol'] > alcohol_median)]
    if selected_state != "All":
        high_risk_data = high_risk_data[high_risk_data['state'] == selected_state]

    st.write(high_risk_data[['state', 'perc_fatl_speed', 'perc_fatl_alcohol', 'drvr_fatl_col_bmiles']])
    
    fig = px.bar(high_risk_data, x='state', y='drvr_fatl_col_bmiles', title="High-Risk States Fatal Collisions", color='drvr_fatl_col_bmiles', labels={'drvr_fatl_col_bmiles': 'Fatal Collisions'})
    st.plotly_chart(fig)

st.markdown(
    """
    <hr style='border: 1px solid #e0e0e0;'>
    <footer class='footer'>
        <p>🚗 Traffic Accident Analysis App - Created by Abdul Moeed</p>
    </footer>
    """,
    unsafe_allow_html=True
)
