import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =============================
# CONFIG
# =============================
st.set_page_config(page_title="Seismic Dashboard", layout="wide")
st.title("🌍 Global Seismic Insights Dashboard")

# =============================
# LOAD DATA
# =============================
@st.cache_data
def load_data():
    engine = create_engine(
        "mysql+mysqlconnector://root:12345@localhost/seismic_db"
    )
    return pd.read_sql("SELECT * FROM earthquakes", engine)

df = load_data()

# =============================
# MONTH NAME FIX
# =============================
month_map = {
    1:"January",2:"February",3:"March",4:"April",
    5:"May",6:"June",7:"July",8:"August",
    9:"September",10:"October",11:"November",12:"December"
}
df["month_name"] = df["month"].map(month_map)

# =============================
# HORIZONTAL BAR FUNCTION
# =============================
def horizontal_bar(series, title):
    chart_df = series.reset_index()
    chart_df.columns = ["Category", "Value"]

    fig = px.bar(
        chart_df,
        x="Value",
        y="Category",
        orientation="h",
        title=title
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# =============================
# SIDEBAR NAVIGATION
# =============================
section = st.sidebar.radio(
    "📌 Select Category",
    [
        "Magnitude & Depth",
        "Time Analysis",
        "Event Quality",
        "Tsunami & Alerts",
        "Seismic Pattern",
        "Location Analysis"
    ]
)

# =============================
# QUESTIONS
# =============================
if section == "Magnitude & Depth":
    q = st.sidebar.radio("Select Question", [
        "Q1 Strongest Earthquakes",
        "Q2 Deepest Earthquakes",
        "Q3 Dangerous Shallow Strong",
        "Q5 Avg Magnitude Type"
    ])

elif section == "Time Analysis":
    q = st.sidebar.radio("Select Question", [
        "Q6 Most Active Year",
        "Q7 Most Active Month",
        "Q8 Most Active Day",
        "Q9 Peak Hour",
        "Q10 Most Reporting Network"
    ])

elif section == "Event Quality":
    q = st.sidebar.radio("Select Question", [
        "Q11 Highest Impact Places",
        "Q13 Impact vs Alert",
        "Q14 Reviewed vs Auto",
        "Q15 Event Type Distribution",
        "Q16 Data Type Distribution",
        "Q18 High Station Coverage"
    ])

elif section == "Tsunami & Alerts":
    q = st.sidebar.radio("Select Question", [
        "Q19 Tsunami Trend",
        "Q20 Alert Distribution"
    ])

elif section == "Seismic Pattern":
    q = st.sidebar.radio("Select Question", [
        "Q21 Strongest Countries",
        "Q22 Mixed Depth Activity",
        "Q23 Yearly Growth",
        "Q24 Most Active Regions"
    ])

elif section == "Location Analysis":
    q = st.sidebar.radio("Select Question", [
        "Q25 Equator Depth Pattern",
        "Q26 Shallow vs Deep Ratio",
        "Q27 Tsunami vs Non Strength",
        "Q28 Low Reliability",
        "Q30 Deep Focus Regions"
    ])

st.divider()

# =====================================================
# MAGNITUDE & DEPTH
# =====================================================

if q == "Q1 Strongest Earthquakes":

    st.header("Top 10 Strongest Earthquakes")

    res = df.groupby("place")["mag"].max().sort_values(ascending=False)

    st.success(f"Answer: Highest Magnitude = {res.max()}")
    st.info("Justification: Shows strongest earthquake per unique location.")

    horizontal_bar(res.head(10), "Top Strongest Earthquakes")


elif q == "Q2 Deepest Earthquakes":

    st.header("Top 10 Deepest Earthquakes")

    res = df.groupby("place")["depth_km"].max().sort_values(ascending=False)

    st.success(f"Answer: Deepest Earthquake = {res.max()} km")
    st.info("Justification: Shows deepest earthquake per unique location.")

    horizontal_bar(res.head(10), "Top Deepest Earthquakes")


elif q == "Q3 Dangerous Shallow Strong":

    res = df[(df["depth_km"] < 50) & (df["mag"] > 7.5)]

    st.success(f"Answer: Dangerous Events Count = {len(res)}")
    st.info("Justification: Shallow + strong earthquakes cause maximum damage.")

    st.dataframe(res.head(20))


elif q == "Q5 Avg Magnitude Type":

    res = df.groupby("magType")["mag"].mean()

    st.success(f"Answer: Highest Avg Magnitude Type = {res.idxmax()}")
    st.info("Justification: Shows which measurement type records strongest average earthquakes.")

    horizontal_bar(res, "Average Magnitude by Type")


# =====================================================
# TIME
# =====================================================

elif q == "Q6 Most Active Year":

    res = df["year"].value_counts()

    st.success(f"Answer: Most Active Year = {res.idxmax()}")
    st.info("Justification: Shows year with highest earthquake frequency.")

    horizontal_bar(res.sort_index(), "Earthquakes per Year")


elif q == "Q7 Most Active Month":

    res = df["month_name"].value_counts()

    st.success(f"Answer: Most Active Month = {res.idxmax()}")
    st.info("Justification: Shows which month recorded highest earthquakes.")

    horizontal_bar(res, "Earthquakes per Month")


elif q == "Q8 Most Active Day":

    res = df["day_of_week"].value_counts()

    st.success(f"Answer: Peak Day = {res.idxmax()}")
    st.info("Justification: Shows weekday earthquake concentration.")

    horizontal_bar(res, "Earthquakes per Day")


elif q == "Q9 Peak Hour":

    res = df["hour"].value_counts()

    st.success(f"Answer: Peak Hour = {res.idxmax()}")
    st.info("Justification: Shows hour earthquake frequency highest.")

    horizontal_bar(res.sort_index(), "Earthquakes per Hour")


elif q == "Q10 Most Reporting Network":

    res = df["net"].value_counts()

    st.success(f"Answer: Most Reporting Network = {res.idxmax()}")
    st.info("Justification: Shows most active monitoring network.")

    horizontal_bar(res.head(10), "Top Networks")


# =====================================================
# EVENT QUALITY
# =====================================================

elif q == "Q11 Highest Impact Places":

    res = df.groupby("place")["sig"].sum().sort_values(ascending=False)

    st.success(f"Answer: Highest Impact Place = {res.index[0]}")
    st.info("Justification: Higher significance means higher impact.")

    horizontal_bar(res.head(10), "Impact by Place")


elif q == "Q13 Impact vs Alert":

    res = df.groupby("alert")["sig"].mean()

    st.success(f"Answer: Highest Impact Alert = {res.idxmax()}")
    st.info("Justification: Shows alert vs average impact.")

    horizontal_bar(res, "Impact by Alert")


elif q == "Q14 Reviewed vs Auto":

    res = df["status"].value_counts()

    st.success(f"Answer: Most Common Status = {res.idxmax()}")
    st.info("Justification: Shows verification level distribution.")

    horizontal_bar(res, "Status Distribution")


elif q == "Q15 Event Type Distribution":

    res = df["type"].value_counts()

    st.success(f"Answer: Most Common Event Type = {res.idxmax()}")
    st.info("Justification: Shows type classification distribution.")

    horizontal_bar(res, "Event Type Distribution")


elif q == "Q16 Data Type Distribution":

    res = df["types"].value_counts().head(10)

    st.success("Answer: Top data types shown in chart.")
    st.info("Justification: Shows available seismic metadata types.")

    horizontal_bar(res, "Top Data Types")


elif q == "Q18 High Station Coverage":

    res = df[df["nst"] > 50]

    st.success(f"Answer: High Coverage Events = {len(res)}")
    st.info("Justification: Higher station count → higher accuracy.")

    st.dataframe(res.head(20))


# =====================================================
# TSUNAMI
# =====================================================

elif q == "Q19 Tsunami Trend":

    res = df[df["tsunami"] == 1]["year"].value_counts()

    st.success("Answer: Tsunami yearly distribution shown.")
    st.info("Justification: Shows tsunami related earthquake trend.")

    horizontal_bar(res.sort_index(), "Tsunami Events by Year")


elif q == "Q20 Alert Distribution":

    res = df["alert"].value_counts()

    st.success(f"Answer: Most Common Alert = {res.idxmax()}")
    st.info("Justification: Shows alert severity distribution.")

    horizontal_bar(res, "Alert Distribution")


# =====================================================
# SEISMIC PATTERN
# =====================================================

elif q == "Q21 Strongest Countries":

    res = df.groupby("country")["mag"].mean().sort_values(ascending=False)

    st.success(f"Answer: Strongest Avg Magnitude Country = {res.index[0]}")
    st.info("Justification: Shows strongest earthquake countries.")

    horizontal_bar(res.head(10), "Top Countries by Avg Magnitude")


elif q == "Q22 Mixed Depth Activity":

    mix = df.groupby(["country","year","month"]).filter(
        lambda x: (x["depth_km"] < 70).any() and (x["depth_km"] > 300).any()
    )

    st.success(f"Answer: Countries Found = {mix['country'].nunique()}")
    st.info("Justification: Shows mixed tectonic depth activity.")

    st.dataframe(mix[["country","year","month"]].drop_duplicates().head(20))


elif q == "Q23 Yearly Growth":

    yearly = df["year"].value_counts().sort_index()

    st.success("Answer: Yearly growth shown in chart.")
    st.info("Justification: Shows increase/decrease yearly trend.")

    horizontal_bar((yearly.pct_change()*100).dropna(), "Yearly Growth %")


elif q == "Q24 Most Active Regions":

    res = df.groupby("place")["id"].count().sort_values(ascending=False)

    st.success(f"Answer: Most Active Region = {res.index[0]}")
    st.info("Justification: Shows highest earthquake frequency region.")

    horizontal_bar(res.head(10), "Most Active Regions")


# =====================================================
# LOCATION
# =====================================================

elif q == "Q25 Equator Depth Pattern":

    eq = df[(df["latitude"] >= -5) & (df["latitude"] <= 5)]
    res = eq.groupby("country")["depth_km"].mean()

    st.success("Answer: Equator depth distribution shown.")
    st.info("Justification: Shows seismic depth near equator.")

    horizontal_bar(res.head(10), "Equator Avg Depth by Country")


elif q == "Q26 Shallow vs Deep Ratio":

    shallow = df[df["depth_km"] < 70].groupby("country").size()
    deep = df[df["depth_km"] > 300].groupby("country").size()
    res = (shallow/deep).fillna(0)

    st.success(f"Answer: Highest Ratio Country = {res.idxmax()}")
    st.info("Justification: Shows shallow vs deep dominance.")

    horizontal_bar(res.sort_values(ascending=False).head(10), "Shallow/Deep Ratio")


elif q == "Q27 Tsunami vs Non Strength":

    tsunami_avg = df[df["tsunami"] == 1]["mag"].mean()
    non_avg = df[df["tsunami"] == 0]["mag"].mean()

    diff = tsunami_avg - non_avg

    st.success(f"Answer: Magnitude Difference = {round(diff,2)}")
    st.info("Justification: Compares average magnitude of tsunami vs non-tsunami earthquakes.")

    compare_series = pd.Series({
        "Tsunami EQ": tsunami_avg,
        "Non Tsunami EQ": non_avg
    })

    horizontal_bar(compare_series, "Avg Magnitude Comparison")


elif q == "Q28 Low Reliability":

    df["error"] = df["gap"] + df["rms"]

    st.success("Answer: Lowest reliability events shown.")
    st.info("Justification: Higher gap + rms → Lower reliability.")

    st.dataframe(df.sort_values("error", ascending=False).head(20))


elif q == "Q30 Deep Focus Regions":

    res = df[df["depth_km"] > 300]["place"].value_counts()

    st.success(f"Answer: Most Deep Focus Region = {res.index[0]}")
    st.info("Justification: Shows deep tectonic activity zones.")

    horizontal_bar(res.head(10), "Deep Focus Regions")
