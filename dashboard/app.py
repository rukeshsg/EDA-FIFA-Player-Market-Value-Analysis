import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# -------------------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.data_loader import load_data
from src.utils import ensure_dir

DATA_PATH = BASE_DIR / "datasets" / "fifa_players.csv"
IMAGE_DIR = BASE_DIR / "images" / "dashboard"
ensure_dir(str(IMAGE_DIR))

# -------------------------------------------------------------------
# STREAMLIT CONFIG
# -------------------------------------------------------------------
st.set_page_config(
    page_title="FIFA Player Market Value Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

sns.set_theme(style="whitegrid", context="talk")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        [data-testid="metric-container"] {
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 16px;
            padding: 8px 12px;
            background: rgba(255,255,255,0.03);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚽ FIFA Player Market Value Dashboard")
st.caption("Interactive exploratory analysis of player rating, age, position, and market value.")

# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------
def pick_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def save_and_show(fig, filename: str):
    save_path = IMAGE_DIR / filename
    fig.savefig(save_path, bbox_inches="tight", dpi=220)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


@st.cache_data(show_spinner=False)
def load_dataset():
    return load_data(str(DATA_PATH))


# -------------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------------
try:
    df = load_dataset()
except FileNotFoundError:
    st.error(f"Dataset not found at: {DATA_PATH}")
    st.stop()
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

# -------------------------------------------------------------------
# AUTO-DETECT IMPORTANT COLUMNS
# -------------------------------------------------------------------
age_col = pick_column(df, ["age", "player_age"])
rating_col = pick_column(df, ["overall_rating", "rating", "overall"])
value_col = pick_column(df, ["market_value_million_eur", "market_value", "value", "market_value_eur"])
position_col = pick_column(df, ["position", "player_position"])

missing_required = []
if age_col is None:
    missing_required.append("age")
if rating_col is None:
    missing_required.append("overall rating")
if value_col is None:
    missing_required.append("market value")

if missing_required:
    st.error(
        "Required columns not found: "
        + ", ".join(missing_required)
        + f"\n\nAvailable columns: {list(df.columns)}"
    )
    st.stop()

# Convert important columns to numeric safely
for col in [age_col, rating_col, value_col]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if position_col is not None:
    df[position_col] = df[position_col].astype("string").fillna("Unknown")

df = df.dropna(subset=[age_col, rating_col, value_col]).copy()

# -------------------------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------------------------
st.sidebar.header("Filters")

age_min, age_max = int(df[age_col].min()), int(df[age_col].max())
rating_min, rating_max = int(df[rating_col].min()), int(df[rating_col].max())

default_age_max = min(age_min + 10, age_max)
default_rating_min = max(rating_min, int(df[rating_col].quantile(0.25)))
default_rating_max = min(rating_max, int(df[rating_col].quantile(0.75)))

age_range = st.sidebar.slider(
    "Select Age Range",
    min_value=age_min,
    max_value=age_max,
    value=(age_min, default_age_max),
)

rating_range = st.sidebar.slider(
    "Select Rating Range",
    min_value=rating_min,
    max_value=rating_max,
    value=(default_rating_min, default_rating_max),
)

selected_positions = None
if position_col is not None:
    all_positions = sorted(df[position_col].dropna().unique().tolist())
    selected_positions = st.sidebar.multiselect(
        "Select Position(s)",
        options=all_positions,
        default=all_positions,
    )

filtered_df = df[
    (df[age_col] >= age_range[0])
    & (df[age_col] <= age_range[1])
    & (df[rating_col] >= rating_range[0])
    & (df[rating_col] <= rating_range[1])
].copy()

if position_col is not None and selected_positions:
    filtered_df = filtered_df[filtered_df[position_col].isin(selected_positions)].copy()

if filtered_df.empty:
    st.warning("No data matches the selected filters. Try widening the filter ranges.")
    st.stop()

# -------------------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Players", f"{len(filtered_df):,}")
col2.metric("Average Rating", f"{filtered_df[rating_col].mean():.2f}")
col3.metric("Average Market Value", f"€{filtered_df[value_col].mean():.2f}M")
col4.metric("Median Age", f"{filtered_df[age_col].median():.0f}")

st.divider()

# -------------------------------------------------------------------
# TABS
# -------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Visual Analysis", "🔥 Correlation", "🚨 Outliers", "🏆 Top Players"]
)

# -------------------------------------------------------------------
# TAB 1: VISUAL ANALYSIS
# -------------------------------------------------------------------
with tab1:
    left, right = st.columns(2)

    with left:
        st.subheader("Rating vs Market Value")

        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.regplot(
            data=filtered_df,
            x=rating_col,
            y=value_col,
            scatter_kws={"alpha": 0.65, "s": 45},
            line_kws={"color": "crimson", "linewidth": 2},
            ax=ax1,
        )
        ax1.set_title("Overall Rating vs Market Value")
        ax1.set_xlabel("Overall Rating")
        ax1.set_ylabel("Market Value (Million EUR)")
        save_and_show(fig1, "rating_vs_value.png")

    with right:
        st.subheader("Market Value Distribution")

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.histplot(filtered_df[value_col], bins=30, kde=True, ax=ax2)
        ax2.set_title("Market Value Distribution")
        ax2.set_xlabel("Market Value (Million EUR)")
        ax2.set_ylabel("Count")
        save_and_show(fig2, "market_value_distribution.png")

    if position_col is not None:
        st.subheader("Average Market Value by Position")

        position_summary = (
            filtered_df.groupby(position_col, as_index=False)[value_col]
            .mean()
            .sort_values(value_col, ascending=False)
            .head(10)
        )

        fig_pos, ax_pos = plt.subplots(figsize=(10, 5))
        sns.barplot(data=position_summary, x=position_col, y=value_col, ax=ax_pos)
        ax_pos.set_title("Top 10 Positions by Average Market Value")
        ax_pos.set_xlabel("Position")
        ax_pos.set_ylabel("Average Market Value (Million EUR)")
        ax_pos.tick_params(axis="x", rotation=30)
        save_and_show(fig_pos, "position_market_value.png")

# -------------------------------------------------------------------
# TAB 2: CORRELATION
# -------------------------------------------------------------------
with tab2:
    st.subheader("Correlation Heatmap")

    numeric_df = filtered_df.select_dtypes(include="number")
    corr = numeric_df.corr()

    fig3, ax3 = plt.subplots(figsize=(11, 7))
    mask = pd.DataFrame(False, index=corr.index, columns=corr.columns)
    sns.heatmap(
        corr,
        mask=mask,
        cmap="coolwarm",
        center=0,
        linewidths=0.4,
        ax=ax3,
    )
    ax3.set_title("Correlation Heatmap")
    save_and_show(fig3, "correlation_heatmap.png")

    st.info(
        f"Market value is evaluated using {value_col}. "
        "Look for strong positive or negative relationships with rating, age, and other numeric features."
    )

# -------------------------------------------------------------------
# TAB 3: OUTLIERS
# -------------------------------------------------------------------
with tab3:
    st.subheader("Market Value Outliers")

    q1 = filtered_df[value_col].quantile(0.25)
    q3 = filtered_df[value_col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier_count = filtered_df[(filtered_df[value_col] < lower_bound) | (filtered_df[value_col] > upper_bound)].shape[0]

    fig4, ax4 = plt.subplots(figsize=(9, 4.8))
    sns.boxplot(x=filtered_df[value_col], ax=ax4)
    ax4.set_title("Market Value Outliers")
    ax4.set_xlabel("Market Value (Million EUR)")
    save_and_show(fig4, "market_value_outliers.png")

    st.warning(f"Detected outliers: {outlier_count}")

# -------------------------------------------------------------------
# TAB 4: TOP PLAYERS
# -------------------------------------------------------------------
with tab4:
    st.subheader("Top 10 Players by Market Value")

    display_cols = [c for c in [age_col, rating_col, value_col, position_col] if c is not None]
    top_players = (
        filtered_df.sort_values(by=value_col, ascending=False)
        .head(10)[display_cols]
        .copy()
    )

    st.dataframe(top_players, use_container_width=True)

# -------------------------------------------------------------------
# INSIGHTS + DOWNLOAD
# -------------------------------------------------------------------
st.subheader("💡 Key Insights")
st.success(
    f"""
- Higher-rated players generally show higher market value.
- Market value is right-skewed, meaning a few players are much more valuable than most.
- Age and rating together influence player valuation.
- Position can also affect average market value.
"""
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_fifa_players.csv",
    mime="text/csv",
)

st.caption(f"Dashboard visuals are saved in: {IMAGE_DIR}")