import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Breast Cancer Prediction",
    page_icon="🩺",
    layout="wide"
)

# ---------------- PAGE STYLING ---------------- #
st.markdown("""
<style>

.hero-section{
    width:100%;
    height:350px;
    background-image:url("https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=1600&auto=format&fit=crop");
    background-size:cover;
    background-position:center;
    border-radius:25px;

    display:flex;
    align-items:center;
    padding-left:60px;

    margin-bottom:40px;
}

.hero-content{
    background:rgba(0,0,0,0.55);
    padding:40px;
    border-radius:20px;
    width:60%;
}

.hero-content h1{
    color:white;
    font-size:60px;
    margin-bottom:15px;
}

.hero-content p{
    color:#e5e5e5;
    font-size:22px;
    line-height:1.6;
}

</style>

""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

col1, col2 = st.columns([1,2])

with col1:
    from PIL import Image
    import streamlit as st
    image = Image.open("static/breast_cancer.jpg")
    st.image(image, width='stretch')

with col2:
    st.markdown('<p class="main-title">🩺 Breast Cancer Prediction System</p>', unsafe_allow_html=True)

    st.markdown("""
    <p class="subtitle">
    AI-powered Machine Learning system for breast cancer prediction using medical diagnostic features.
    </p>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ---------------- #

st.subheader("📋 Patient Diagnostic Details")

col1, col2, col3 = st.columns(3)

with col1:
    radius_mean = st.number_input("Radius Mean", 0.0, 50.0)
    texture_mean = st.number_input("Texture Mean", 0.0, 50.0)
    perimeter_mean = st.number_input("Perimeter Mean", 0.0, 200.0)

with col2:
    area_mean = st.number_input("Area Mean", 0.0, 3000.0)
    smoothness_mean = st.number_input("Smoothness Mean", 0.0, 1.0)
    compactness_mean = st.number_input("Compactness Mean", 0.0, 1.0)

with col3:
    concavity_mean = st.number_input("Concavity Mean", 0.0, 1.0)
    symmetry_mean = st.number_input("Symmetry Mean", 0.0, 1.0)
    fractal_dimension = st.number_input("Fractal Dimension", 0.0, 1.0)

st.markdown("")

# ---------------- PREDICT BUTTON ---------------- #

predict_button = st.button("🔍 Predict Cancer", use_container_width=True)

# ---------------- PREDICTION SECTION ---------------- #

if predict_button:

    # Dummy Prediction
    prediction = "Benign"

    st.divider()

    st.subheader("📊 Prediction Result")

    if prediction == "Malignant":
        st.error("⚠️ High Risk of Malignant Cancer Detected")
    else:
        st.success("✅ Benign Tumor Detected")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Model Accuracy</h3>
            <h2>96%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Confidence Score</h3>
            <h2>92%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Prediction</h3>
            <h2>Benign</h2>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------------- FOOTER ---------------- #

st.caption("Built with Machine Learning + Streamlit 🚀")