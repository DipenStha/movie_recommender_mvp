import streamlit as st
from data_loader import load_data
from recommender import build_similarity_matrix, recommend
import pandas as pd
# --- Page Config ---
st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🍿", layout="centered")

# --- Custom CSS ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 12px;
    }
    .title {
        text-align: center;
        font-size: 42px;
        color: #1e3a8a;
        font-weight: bold;
        padding: 20px 0 10px 0;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #374151;
        margin-bottom: 30px;
    }
    .stButton > button {
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        padding: 10px 18px;
        border-radius: 10px;
        border: none;
    }
    .stSelectbox > div, .stSlider > div {
        background-color: #eff6ff;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)


# --- Title ---
st.markdown('<div class="title">🍿 Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find movies similar to your favorite titles!</div>', unsafe_allow_html=True)



data_source = st.sidebar.radio("Choose Data Source", ["Use Default Dataset", "Upload Your Own"])

# --- Load Data ---
if data_source == "Use Default Dataset":
    with st.spinner("📡 Loading default MovieLens dataset..."):
        ratings = load_data()
else:
    uploaded_file = st.sidebar.file_uploader("📂 Upload your ratings CSV", type=["csv"])
    if uploaded_file:
        try:
            ratings = pd.read_csv(uploaded_file)
            st.success("✅ Custom dataset loaded!")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
            st.stop()
    else:
        st.warning("⚠️ Please upload a CSV file.")
        st.stop()



# --- Build Similarity Matrix ---
sim_df = build_similarity_matrix(ratings)

# --- Movie Recommendation Interface ---
movie_list = sim_df.columns.tolist()
selected_movie = st.selectbox("🎬 Choose a movie", movie_list)
num_recs = st.slider("🔢 Number of similar movies to recommend", min_value=1, max_value=10, value=5)

# --- Recommend Button + Display Table ---
if st.button("🚀 Get Recommendations"):
    recs = recommend(selected_movie, sim_df, num_recs)
    if not recs.empty:
        st.success(f"📽️ Top {num_recs} movies similar to *{selected_movie}*")

        recs_df = recs.reset_index()
        recs_df.columns = ['🎞️ Movie Title', '📊 Similarity Score']
        recs_df['📊 Similarity Score'] = recs_df['📊 Similarity Score'].round(2)

        st.table(recs_df)
    else:
        st.warning("😕 No similar movies found. Try another title.")


# with st.spinner("🎥 Loading movie data..."):
#     ratings = load_data()
#     sim_df = build_similarity_matrix(ratings)

# # --- Movie Picker ---
# movie_list = sim_df.columns.tolist()
# selected_movie = st.selectbox("🎬 Choose a movie", movie_list)
# num_recs = st.slider("🔢 Number of similar movies to recommend", min_value=1, max_value=10, value=5)

# # --- Generate Recommendations ---
# if st.button("🚀 Get Recommendations"):
#     recs = recommend(selected_movie, sim_df, num_recs)
#     if not recs.empty:
#         st.success(f"✅ Top {num_recs} movies similar to *{selected_movie}*")

    #     # Create a styled and sortable table
    #     recs_df = recs.reset_index()
    #     recs_df.columns = ['🎞️ Movie Title', '📊 Similarity Score']
    #     recs_df['📊 Similarity Score'] = recs_df['📊 Similarity Score'].round(2)

    #     st.dataframe(
    #         recs_df.style
    #         .background_gradient(cmap='Reds', subset=['📊 Similarity Score'])
    #         .set_properties(**{'text-align': 'left'}),
    #         use_container_width=True
    #     )
    # else:
    #     st.warning("No similar movies found. Try another movie.")

