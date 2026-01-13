import streamlit as st
from src.pipeline.pipeline import run_pipeline

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Live Meeting Summarizer",
    layout="wide",
)

st.title("🎙️ Live Meeting Summarizer")
st.caption("System audio → Whisper → Diarization → AI Summary")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "final_text" not in st.session_state:
    st.session_state.final_text = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
with st.sidebar:
    st.header("Controls")

    duration = st.slider(
        "Recording duration (seconds)",
        min_value=5,
        max_value=120,
        value=10,
        step=5
    )

    start_btn = st.button("▶️ Start Recording & Process", type="primary")

# -------------------------------
# PIPELINE EXECUTION
# -------------------------------
if start_btn and not st.session_state.running:
    st.session_state.running = True

    with st.status("Running pipeline...", expanded=True) as status:
        st.write("🎧 Recording system audio...")
        st.write("🧠 Transcribing with Whisper...")
        st.write("🧑‍🤝‍🧑 Performing speaker diarization...")
        st.write("📝 Merging transcript with speakers...")
        st.write("✨ Generating meeting summary...")


        final_text, summary = run_pipeline(duration)

        st.session_state.final_text = final_text
        st.session_state.summary = summary

        status.update(label="✅ Pipeline completed", state="complete")

    st.session_state.running = False

# -------------------------------
# OUTPUT DISPLAY
# -------------------------------
tabs = st.tabs(["📜 Transcript", "🧠 Summary"])

with tabs[0]:
    if st.session_state.final_text:
        st.text_area(
            "Speaker-wise Transcript",
            st.session_state.final_text,
            height=400
        )
    else:
        st.info("Transcript will appear here after processing.")

with tabs[1]:
    if st.session_state.summary:
        st.text_area(
            "Meeting Summary",
            st.session_state.summary,
            height=300
        )
    else:
        st.info("Summary will appear here after processing.")
