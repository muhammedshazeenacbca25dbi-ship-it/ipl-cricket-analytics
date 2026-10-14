import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


st.set_page_config(page_title="IPL Matches Dashboard", page_icon="🏏", layout="wide")

st.markdown("""
<style>
:root {
    --page-bg: #05070d;
    --card-bg: #10182b;
    --ink: #e8eeff;
    --muted: #9aa8c7;
    --accent: #4169e1;
    --border: #263657;
}
.stApp { background: var(--page-bg); color: var(--ink); font-family: "Inter", "Segoe UI", sans-serif; }
.block-container { max-width: 1500px; padding-top: 1.5rem; padding-bottom: 2.2rem; }
h1 { font-size: 2.35rem !important; font-weight: 800 !important; color: var(--ink) !important; letter-spacing: -0.7px; }
h2 { font-size: 1.75rem !important; font-weight: 750 !important; color: var(--ink) !important; }
h3 { font-size: 1.25rem !important; font-weight: 700 !important; color: var(--ink) !important; }
p, label, .stMarkdown, .stCaption { font-size: 0.98rem; }
.subtitle { color: var(--muted); font-size: 1.05rem; font-style: italic; margin-top: -8px; margin-bottom: 20px; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #10182b, #17264a); border: 1px solid var(--border); border-top: 4px solid var(--accent);
    padding: 18px 20px; border-radius: 16px; box-shadow: 0 5px 18px rgba(0, 0, 0, .25);
}
div[data-testid="stMetricLabel"] { color: var(--muted); font-size: 0.9rem !important; font-weight: 700; }
div[data-testid="stMetricValue"] { color: var(--ink); font-size: 1.85rem !important; font-weight: 800; }
div[data-testid="stTabs"] button { font-size: 1.02rem !important; font-weight: 750 !important; border-radius: 10px 10px 0 0; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: var(--accent) !important; }
div[data-testid="stPopover"] button {
    border: 1px solid #4169e1; background: #10182b; color: #dbeafe;
    border-radius: 10px; font-weight: 700; padding: 0.35rem 0.75rem;
}
div[data-testid="stFileUploader"] section { background: #10182b; border: 1px dashed #4169e1; border-radius: 14px; }
div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div { border-radius: 10px; }
hr { border-color: var(--border); }
[data-testid="stWidgetLabel"] p { color: #cbd5e1; }
[data-testid="stMarkdownContainer"] p { color: #cbd5e1; }
[data-testid="stExpander"] {
    background: rgba(12, 22, 43, .94);
    border: 1px solid #4169e1;
    border-radius: 12px;
    transition: border-color .25s ease, box-shadow .25s ease, transform .25s ease;
    animation: filterBorderGlow 3s ease-in-out infinite;
}
[data-testid="stExpander"]:hover {
    border-color: #60a5fa;
    box-shadow: 0 0 0 1px rgba(65, 105, 225, .42), 0 0 22px rgba(37, 99, 235, .24);
    transform: translateY(-1px);
}
[data-testid="stExpander"] summary {
    color: #e8eeff !important;
    font-weight: 750 !important;
    min-height: 42px;
}
[data-testid="stExpander"] summary:hover { color: #93c5fd !important; }
[data-testid="stExpander"] [data-testid="stMultiSelect"] {
    background: rgba(5, 10, 22, .85);
    border-radius: 10px;
}
[data-testid="stBaseButton-secondary"] {
    background: #10182b;
    color: #e8eeff;
    border-color: #4169e1;
    border-radius: 9px;
}
@keyframes filterBorderGlow {
    0%, 100% { box-shadow: 0 0 0 rgba(65, 105, 225, 0); }
    50% { box-shadow: 0 0 13px rgba(65, 105, 225, .16); }
}
.small-note { color: var(--muted); font-size: 0.82rem; text-align: center; margin-top: 14px; }
</style>
""", unsafe_allow_html=True)

# Animated cricket stadium background (inline SVG; no separate image required)
st.markdown("""
<style>
.stApp { background: #030712 !important; color: #e8eeff; font-family: "Inter", "Segoe UI", sans-serif; overflow-x: hidden; }
[data-testid="stAppViewContainer"] { background: transparent !important; position: relative; }
[data-testid="stHeader"] { background: rgba(3, 7, 18, .30) !important; }
[data-testid="stMain"], .main, .block-container { position: relative; z-index: 2; }
.stadium-bg { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
  background: radial-gradient(ellipse at 50% 65%, rgba(22,163,74,.22), transparent 42%), linear-gradient(180deg,#020617 0%,#071426 48%,#052e25 100%); }
.stadium-bg svg { position:absolute; width:100%; height:100%; min-width:1000px; min-height:650px; left:50%; top:50%; transform:translate(-50%,-50%); }
.stadium-beam { transform-origin:720px 100px; animation:beamSweep 12s ease-in-out infinite alternate; opacity:.14; }
.stadium-beam.beam-two { animation-delay:-6s; }
.stadium-lamp { animation:lampPulse 3.8s ease-in-out infinite; }
.stadium-lamp.delay { animation-delay:1.9s; }
.stadium-stars { animation:crowdTwinkle 5s ease-in-out infinite; }
.stadium-screen { animation:screenGlow 4s ease-in-out infinite; }
.pitch-glow { animation:pitchPulse 6s ease-in-out infinite; }
@keyframes beamSweep { from { transform:rotate(-12deg); opacity:.07; } to { transform:rotate(12deg); opacity:.22; } }
@keyframes lampPulse { 0%,100% { opacity:.55; } 50% { opacity:1; } }
@keyframes crowdTwinkle { 0%,100% { opacity:.42; } 50% { opacity:.78; } }
@keyframes screenGlow { 0%,100% { filter:brightness(.85); } 50% { filter:brightness(1.25); } }
@keyframes pitchPulse { 0%,100% { opacity:.4; } 50% { opacity:.7; } }
.stadium-title-card { position:relative; z-index:2; padding:22px 26px; margin:4px 0 18px; border:1px solid #29466b; border-radius:20px;
  background:linear-gradient(115deg,rgba(3,7,18,.88),rgba(15,32,58,.82)); backdrop-filter:blur(8px); }
.stadium-title-card h1 { color:#e8eeff; font-size:clamp(1.7rem,3vw,2.4rem); font-weight:800; line-height:1.15; margin:0; }
.stadium-title-card p { color:#a9c4eb; margin:8px 0 0; font-size:1rem; }
@media (prefers-reduced-motion: reduce) { .stadium-beam,.stadium-lamp,.stadium-stars,.stadium-screen,.pitch-glow { animation:none; } }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stadium-bg" aria-hidden="true">
<svg viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
<defs>
 <radialGradient id="nightSky"><stop offset="0%" stop-color="#173c60" stop-opacity=".45"/><stop offset="100%" stop-color="#020617" stop-opacity="0"/></radialGradient>
 <linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#0b513d"/><stop offset="100%" stop-color="#031b19"/></linearGradient>
 <linearGradient id="screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0ea5e9"/><stop offset="100%" stop-color="#1d4ed8"/></linearGradient>
 <filter id="stadiumGlow"><feGaussianBlur stdDeviation="13" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="1440" height="900" fill="url(#nightSky)"/>
<g class="stadium-stars" fill="#dbeafe"><circle cx="110" cy="110" r="2"/><circle cx="205" cy="145" r="2"/><circle cx="340" cy="95" r="2"/><circle cx="490" cy="130" r="2"/><circle cx="950" cy="110" r="2"/><circle cx="1100" cy="90" r="2"/><circle cx="1270" cy="140" r="2"/><circle cx="1360" cy="105" r="2"/></g>
<path class="stadium-beam" d="M170 115 L0 650 L440 650 Z" fill="#bfdbfe"/>
<path class="stadium-beam beam-two" d="M1270 115 L1000 650 L1440 650 Z" fill="#bfdbfe"/>
<g class="stadium-lamp" filter="url(#stadiumGlow)"><circle cx="170" cy="115" r="35" fill="#93c5fd" opacity=".32"/><circle cx="170" cy="115" r="13" fill="#eff6ff"/></g>
<g class="stadium-lamp delay" filter="url(#stadiumGlow)"><circle cx="1270" cy="115" r="35" fill="#93c5fd" opacity=".32"/><circle cx="1270" cy="115" r="13" fill="#eff6ff"/></g>
<path d="M40 365 Q720 180 1400 365 L1400 540 Q720 385 40 540 Z" fill="#071426" stroke="#193653" stroke-width="4"/>
<path d="M40 405 Q720 235 1400 405" fill="none" stroke="#234b70" stroke-width="12"/><path d="M40 455 Q720 295 1400 455" fill="none" stroke="#102b46" stroke-width="28"/>
<g class="stadium-stars" fill="#60a5fa"><circle cx="90" cy="390" r="3"/><circle cx="135" cy="420" r="3"/><circle cx="185" cy="380" r="3"/><circle cx="270" cy="415" r="3"/><circle cx="330" cy="370" r="3"/><circle cx="410" cy="400" r="3"/><circle cx="515" cy="365" r="3"/><circle cx="600" cy="405" r="3"/><circle cx="700" cy="370" r="3"/><circle cx="790" cy="405" r="3"/><circle cx="890" cy="375" r="3"/><circle cx="990" cy="415" r="3"/><circle cx="1080" cy="380" r="3"/><circle cx="1180" cy="410" r="3"/><circle cx="1300" cy="390" r="3"/><circle cx="1360" cy="430" r="3"/></g>
<g class="stadium-screen"><rect x="590" y="260" width="260" height="112" rx="8" fill="#071426" stroke="#3b82f6" stroke-width="4"/><rect x="604" y="274" width="232" height="84" rx="4" fill="url(#screen)" opacity=".75"/><text x="720" y="310" text-anchor="middle" fill="#eff6ff" font-size="19" font-weight="800">IPL NIGHT</text><text x="720" y="340" text-anchor="middle" fill="#ffffff" font-size="24" font-weight="900">T20</text></g>
<path d="M0 600 Q720 420 1440 600 L1440 900 L0 900 Z" fill="url(#grass)"/>
<ellipse cx="720" cy="760" rx="570" ry="170" fill="#0c6847" stroke="#22c55e" stroke-width="5" opacity=".55"/>
<ellipse class="pitch-glow" cx="720" cy="760" rx="360" ry="100" fill="none" stroke="#4ade80" stroke-width="4"/>
<path d="M650 900 L690 645 L750 645 L790 900 Z" fill="#b9a57a" opacity=".75"/><path d="M680 675 H760 M670 700 H770" stroke="#f8fafc" stroke-width="4" opacity=".65"/>
<path d="M70 675 Q720 500 1370 675" fill="none" stroke="#bfdbfe" stroke-width="4" opacity=".65"/>
<text x="720" y="865" text-anchor="middle" fill="#dbeafe" font-size="18" font-weight="700" letter-spacing="5" opacity=".5">CRICKET STADIUM • IPL</text>
</svg>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="stadium-title-card"><h1>🏏 IPL Matches Dashboard</h1>'
    '<p>Explore IPL seasons, team performance, match scorecards and innings trends.</p></div>',
    unsafe_allow_html=True,
)

def find_col(df, candidates):
    if df.empty:
        return None
    lookup = {str(c).lower().strip().replace(" ", "_"): c for c in df.columns}
    for item in candidates:
        key = item.lower().strip().replace(" ", "_")
        if key in lookup:
            return lookup[key]
    for c in df.columns:
        normalized = str(c).lower().strip().replace(" ", "_")
        if any(item.lower().replace(" ", "_") in normalized for item in candidates):
            return c
    return None

def numeric(df, col):
    if col and col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series(index=df.index, dtype=float)

def chart_filter(label, key, options, default=None):
    """Visible per-chart filters in an animated expander (more reliable than popovers)."""
    if not options:
        return []
    if default is None:
        default = options

    # Use a visible Streamlit expander so the filter control cannot disappear behind
    # the animated background or fail to render as a popover.
    with st.expander(f"🎛️ {label} filters  ·  click to open", expanded=False):
        picked = st.multiselect(
            f"Filter {label.lower()}",
            options,
            default=default,
            key=key,
            placeholder="Choose options",
        )
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("↺ Reset", key=f"{key}_reset", use_container_width=True):
                st.session_state[key] = list(options)
                st.rerun()
        with c2:
            st.caption(f"{len(picked)} of {len(options)} options selected")

    return picked

with st.expander("📂 Upload matches CSV", expanded=True):
    uploaded = st.file_uploader("Upload one IPL match-level CSV", type=["csv"])
    local_path = st.text_input("Or local CSV filename (same folder as this app)", value="matches(1).csv")

df = pd.DataFrame()
try:
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    elif local_path and Path(local_path).exists():
        df = pd.read_csv(local_path)
except Exception as e:
    st.error(f"Unable to read CSV: {e}")

if df.empty:
    st.info("Upload your matches CSV to see charts based on your real match data. No ball-by-ball file is needed.")
    st.stop()

# Detect common match-level fields.
season_col = find_col(df, ["season", "year", "season_year"])
date_col = find_col(df, ["date", "match_date"])
if season_col is None and date_col:
    parsed = pd.to_datetime(df[date_col], errors="coerce")
    if parsed.notna().any():
        df["Detected season"] = parsed.dt.year
        season_col = "Detected season"

winner_col = find_col(df, ["winner", "match_winner"])
team1_col = find_col(df, ["team1", "home_team"])
team2_col = find_col(df, ["team2", "away_team"])
team_col = winner_col or find_col(df, ["team", "batting_team"])
toss_winner_col = find_col(df, ["toss_winner"])
toss_decision_col = find_col(df, ["toss_decision", "decision"])
venue_col = find_col(df, ["venue", "stadium", "ground"])
match_id_col = find_col(df, ["match_id", "id"])
result_col = find_col(df, ["result", "result_description"])
win_runs_col = find_col(df, ["win_by_runs", "runs_margin", "run_margin"])
win_wickets_col = find_col(df, ["win_by_wickets", "wickets_margin", "wicket_margin"])
target_col = find_col(df, ["target_runs", "target", "first_innings_runs", "total_runs"])

if season_col:
    df[season_col] = pd.to_numeric(df[season_col], errors="coerce")
seasons = sorted(df[season_col].dropna().unique().tolist()) if season_col else []
teams = sorted(df[winner_col].dropna().astype(str).unique().tolist()) if winner_col else []
venues = sorted(df[venue_col].dropna().astype(str).unique().tolist()) if venue_col else []

tab1, tab2 = st.tabs(["📊 Tab 1: Overview", "🏏 Tab 2: Match Analysis"])

with tab1:
    st.subheader("Overview")
    st.caption("Top filters affect the overview. Use ⚙️ Chart filters to filter each chart separately.")
    a, b, c = st.columns(3)
    with a:
        selected_seasons = st.multiselect("Season", seasons, default=seasons, key="global_seasons") if seasons else []
    with b:
        selected_teams = st.multiselect("Winning team", teams, default=[], key="global_winners") if teams else []
    with c:
        selected_venues = st.multiselect("Venue", venues, default=[], key="global_venues") if venues else []

    view = df.copy()
    if season_col and selected_seasons:
        view = view[numeric(view, season_col).isin(selected_seasons)]
    if winner_col and selected_teams:
        view = view[view[winner_col].astype(str).isin(selected_teams)]
    if venue_col and selected_venues:
        view = view[view[venue_col].astype(str).isin(selected_venues)]

    match_count = view[match_id_col].nunique() if match_id_col else len(view)
    season_count = int(view[season_col].nunique()) if season_col else "—"
    winners_count = int(view[winner_col].notna().sum()) if winner_col else "—"
    m1, m2, m3 = st.columns(3)
    m1.metric("TOTAL MATCHES", f"{match_count:,}")
    m2.metric("SEASONS", f"{season_count}")
    m3.metric("MATCHES WITH WINNER", f"{winners_count:,}" if isinstance(winners_count, int) else winners_count)
    st.divider()

    # Match count by season
    left, right = st.columns(2)
    with left:
        st.markdown("### Matches played by season · Trend line")
        if season_col:
            opts = sorted(numeric(view, season_col).dropna().unique().tolist())
            picked = chart_filter("Season", "matches_by_season_filter", opts)
            src = view[numeric(view, season_col).isin(picked)] if picked else view.iloc[0:0]
            summary = src.groupby(season_col).size().reset_index(name="Matches")
            fig = px.line(
                summary, x=season_col, y="Matches", markers=True,
                color_discrete_sequence=["#38bdf8"],
                line_shape="spline",
            )
            fig.update_traces(line=dict(width=4), marker=dict(size=8))
            fig.update_layout(height=340, xaxis_title="Season", yaxis_title="Matches", margin=dict(l=5,r=5,t=10,b=10))
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No season/year or date column found in this CSV.")

    with right:
        st.markdown("### Wins by team · Ranking")
        if winner_col:
            opts = sorted(view[winner_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Winning team", "wins_by_team_filter", opts)
            src = view[view[winner_col].astype(str).isin(picked)] if picked else view.iloc[0:0]
            summary = src[winner_col].astype(str).value_counts().rename_axis("Team").reset_index(name="Wins")
            summary = summary.sort_values("Wins", ascending=True)
            fig = px.bar(
                summary, x="Wins", y="Team", orientation="h",
                color="Wins", color_continuous_scale=["#1d4ed8", "#38bdf8"]
            )
            fig.update_layout(height=340, xaxis_title="Wins", yaxis_title="Team", coloraxis_showscale=False, margin=dict(l=5,r=5,t=10,b=10))
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No winner/match_winner column found in this CSV.")

    left2, right2 = st.columns(2)
    with left2:
        st.markdown("### Toss decisions by season")
        if toss_decision_col:
            opts = sorted(view[toss_decision_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Toss decision", "toss_decision_filter", opts)
            src = view[view[toss_decision_col].astype(str).isin(picked)] if picked else view.iloc[0:0]
            if season_col:
                src = src.copy()
                src["_season_for_chart"] = numeric(src, season_col)
                summary = src.groupby(["_season_for_chart", toss_decision_col]).size().reset_index(name="Matches")
                fig = px.bar(
                    summary, x="_season_for_chart", y="Matches",
                    color=toss_decision_col, barmode="group",
                    color_discrete_sequence=["#38bdf8", "#f59e0b", "#a78bfa"]
                )
                fig.update_layout(xaxis_title="Season", yaxis_title="Matches")
            else:
                summary = src[toss_decision_col].astype(str).value_counts().rename_axis("Decision").reset_index(name="Matches")
                fig = px.pie(summary, names="Decision", values="Matches", hole=.5)
            fig.update_layout(height=320, margin=dict(l=5,r=5,t=10,b=10))
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No toss_decision/decision column found in this CSV.")

    with right2:
        st.markdown("### Win margin")
        if win_runs_col or win_wickets_col:
            margin_options = [name for name, col in [("Runs", win_runs_col), ("Wickets", win_wickets_col)] if col]
            picked = chart_filter("Margin type", "margin_type_filter", margin_options)
            rows = []
            if "Runs" in picked:
                values = numeric(view, win_runs_col).dropna()
                rows.extend([{"Margin type":"Runs", "Margin":float(v)} for v in values if v > 0])
            if "Wickets" in picked:
                values = numeric(view, win_wickets_col).dropna()
                rows.extend([{"Margin type":"Wickets", "Margin":float(v)} for v in values if v > 0])
            if rows:
                fig = px.histogram(pd.DataFrame(rows), x="Margin", color="Margin type", barmode="overlay", nbins=20)
                fig.update_layout(height=320, xaxis_title="Winning margin", yaxis_title="Matches", margin=dict(l=5,r=5,t=10,b=10))
                fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
                fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
                fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No positive winning margins available for this selection.")
        elif result_col:
            opts = sorted(view[result_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Result", "result_filter", opts)
            src = view[view[result_col].astype(str).isin(picked)] if picked else view.iloc[0:0]
            summary = src[result_col].astype(str).value_counts().head(10).rename_axis("Result").reset_index(name="Matches")
            fig = px.pie(
                summary, names="Result", values="Matches", hole=0.58,
                color_discrete_sequence=["#38bdf8", "#f59e0b", "#a78bfa", "#34d399", "#fb7185"]
            )
            fig.update_layout(height=320, margin=dict(l=5,r=5,t=10,b=10))
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No win_by_runs, win_by_wickets or result column found in this CSV.")

with tab2:
    st.subheader("Match Analysis")
    st.caption("All charts below are built from match-level columns in the same CSV.")
    if date_col:
        df["_match_label_date"] = df[date_col].astype(str)
    else:
        df["_match_label_date"] = [f"Match row {i+1}" for i in range(len(df))]
    label_cols = [c for c in [team1_col, team2_col, winner_col, venue_col] if c]
    labels = df["_match_label_date"].astype(str)
    for col in label_cols:
        labels = labels + " | " + df[col].fillna("Unknown").astype(str)
    # Add index to ensure duplicate labels remain selectable.
    options = [f"{label}  [row {idx}]" for label, idx in zip(labels.tolist(), df.index.tolist())]
    label_to_idx = dict(zip(options, df.index.tolist()))
    selected = st.selectbox("Choose a match", options, key="match_picker")
    row = df.loc[label_to_idx[selected]]

    result_value = str(row[result_col]) if result_col and pd.notna(row[result_col]) else (f"{row[winner_col]} won" if winner_col and pd.notna(row[winner_col]) else "Result not available")
    team1_name = str(row[team1_col]) if team1_col and pd.notna(row[team1_col]) else "Team 1"
    team2_name = str(row[team2_col]) if team2_col and pd.notna(row[team2_col]) else "Team 2"
    score_cols = [
        find_col(df, ["team1_score", "first_innings_score", "innings1_score", "score1", "first_innings_runs"]),
        find_col(df, ["team2_score", "second_innings_score", "innings2_score", "score2", "second_innings_runs"]),
    ]
    s1, s2, s3 = st.columns(3)
    s1.metric("RESULT", result_value)
    if score_cols[0] and pd.notna(row[score_cols[0]]):
        s2.metric(f"1ST INNINGS — {team1_name}", str(row[score_cols[0]]))
    else:
        s2.metric("TEAM 1", team1_name)
    if score_cols[1] and pd.notna(row[score_cols[1]]):
        s3.metric(f"2ND INNINGS — {team2_name}", str(row[score_cols[1]]))
    else:
        s3.metric("TEAM 2", team2_name)

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("### Team performance · Win share")
        if winner_col:
            opts = sorted(df[winner_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Teams", "match_tab_team_filter", opts)
            src = df[df[winner_col].astype(str).isin(picked)] if picked else df.iloc[0:0]
            summary = src[winner_col].astype(str).value_counts().rename_axis("Team").reset_index(name="Wins")
            fig = px.pie(
                summary, names="Team", values="Wins", hole=0.52,
                color_discrete_sequence=["#38bdf8", "#2563eb", "#a78bfa", "#34d399", "#f59e0b", "#fb7185"]
            )
            fig.update_layout(height=330, margin=dict(l=5,r=5,t=10,b=10), legend_title_text="Team")
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("A winner column is needed for this chart.")

    with p2:
        st.markdown("### Matches by venue · Treemap")
        if venue_col:
            opts = sorted(df[venue_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Venue", "match_tab_venue_filter", opts)
            src = df[df[venue_col].astype(str).isin(picked)] if picked else df.iloc[0:0]
            summary = src[venue_col].astype(str).value_counts().head(15).rename_axis("Venue").reset_index(name="Matches")
            fig = px.treemap(
                summary, path=["Venue"], values="Matches", color="Matches",
                color_continuous_scale=["#172554", "#2563eb", "#67e8f9"]
            )
            fig.update_layout(height=330, margin=dict(l=5,r=5,t=10,b=10), coloraxis_showscale=False)
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No venue/stadium/ground column found in this CSV.")

    p3, p4 = st.columns(2)
    with p3:
        st.markdown("### Toss winner vs match winner · Heatmap")
        if toss_winner_col and winner_col:
            toss_opts = sorted(df[toss_winner_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Toss winner", "toss_winner_match_filter", toss_opts)
            src = df[df[toss_winner_col].astype(str).isin(picked)] if picked else df.iloc[0:0]
            src = src.copy()
            src["_match_winner_label"] = src[winner_col].astype(str)
            summary = src.groupby([toss_winner_col, "_match_winner_label"]).size().reset_index(name="Matches")
            fig = px.density_heatmap(
                summary, x=toss_winner_col, y="_match_winner_label", z="Matches",
                histfunc="sum", color_continuous_scale=["#0b132b", "#2563eb", "#67e8f9"]
            )
            fig.update_layout(height=330, xaxis_title="Toss winner", yaxis_title="Match winner", margin=dict(l=5,r=5,t=10,b=10), coloraxis_showscale=False)
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("This chart needs both toss_winner and winner columns.")

    with p4:
        st.markdown("### Toss decision breakdown")
        if toss_decision_col:
            opts = sorted(df[toss_decision_col].dropna().astype(str).unique().tolist())
            picked = chart_filter("Toss decision", "match_tab_toss_decision_filter", opts)
            src = df[df[toss_decision_col].astype(str).isin(picked)] if picked else df.iloc[0:0]
            summary = src[toss_decision_col].astype(str).value_counts().rename_axis("Decision").reset_index(name="Matches")
            fig = px.pie(summary, names="Decision", values="Matches", hole=.55)
            fig.update_layout(height=330, margin=dict(l=5,r=5,t=10,b=10))
            fig.update_layout(paper_bgcolor="#05070d", plot_bgcolor="#10182b", font_color="#e8eeff")
            fig.update_xaxes(gridcolor="#263657", zerolinecolor="#263657")
            fig.update_yaxes(gridcolor="#263657", zerolinecolor="#263657")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No toss_decision/decision column found in this CSV.")

st.markdown('<div class="small-note">One matches CSV only. Charts appear when the required match-level columns exist; unavailable charts are explained instead of showing fake data.</div>', unsafe_allow_html=True)
