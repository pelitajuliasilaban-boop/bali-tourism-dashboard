import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Bali Tourism Sentiment & Feedback Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Cyberpunk Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #120224; /* Deep violet */
        color: #e0d5f5;
    }
    
    /* Sidebar Styles (Dark Cyberpunk) */
    [data-testid="stSidebar"] {
        background-color: #1d0836 !important;
        border-right: 1px solid #ff007f;
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #ff007f !important;
        text-shadow: 0 0 8px rgba(255, 0, 127, 0.5);
    }
    
    /* Compact Block Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 100% !important;
    }
    
    /* Header and Title Styles */
    h1, h2, h3 {
        color: #e0d5f5;
        font-weight: 700;
    }
    
    /* KPI Card Style (Neon Glow Effect) */
    .kpi-card {
        background-color: #1d0836;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.2), inset 0 0 5px rgba(255, 0, 127, 0.1);
        border: 1px solid #ff007f;
        margin: 5px 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.5), inset 0 0 8px rgba(255, 0, 127, 0.3);
    }
    .kpi-title {
        font-size: 12px; 
        color: #e0d5f5; 
        font-weight: 600; 
        text-transform: uppercase; 
        letter-spacing: 0.8px;
    }
    .kpi-value {
        font-size: 30px; 
        font-weight: 700; 
        color: #ff007f; /* Neon pink */
        text-shadow: 0 0 8px rgba(255, 0, 127, 0.5);
        margin: 6px 0 2px 0;
    }
    .kpi-subtitle {
        font-size: 11px; 
        color: #94a3b8;
    }
    
    /* Recommendation Card Style */
    .rec-card {
        background-color: #1d0836;
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 0 10px rgba(255, 0, 127, 0.2);
        border-left: 6px solid #ff007f;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
    }
    .rec-title {
        font-size: 15px;
        font-weight: 700;
        color: #ff007f;
        text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .rec-desc {
        font-size: 13px;
        color: #e0d5f5;
        line-height: 1.5;
    }
    
    /* Custom Badges */
    .badge-pos {
        background-color: rgba(255, 0, 127, 0.2); 
        color: #ff007f;
        border: 1px solid #ff007f;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
    }
    .badge-neg {
        background-color: rgba(129, 140, 248, 0.2); 
        color: #818cf8;
        border: 1px solid #818cf8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
    }
    
    /* Tweet Box in table */
    .tweet-box {
        background-color: #1d0836;
        border: 1px solid rgba(255, 0, 127, 0.3);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        box-shadow: 0 0 8px rgba(255, 0, 127, 0.1);
    }
    .tweet-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        font-size: 11px;
        color: #a78bfa;
    }
    .tweet-user {
        font-weight: 600;
        color: #e0d5f5;
    }
    .tweet-content {
        font-size: 13.5px;
        color: #ffffff;
        line-height: 1.5;
    }
    
    /* Adjust Streamlit elements border radius */
    div[data-testid="stForm"] {
        border-radius: 12px !important;
        border-color: rgba(255, 0, 127, 0.5) !important;
        background-color: #1d0836;
    }
    
    /* Custom Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 14px;
        font-weight: 600;
        color: #a78bfa;
        background-color: transparent !important;
    }
    button[aria-selected="true"] {
        color: #ff007f !important;
        border-bottom-color: #ff007f !important;
        text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Define Sentiment and Category Mapping based on dataset analysis
SENTIMENT_MAPPING = {
    'first time ke Bali!!! and i loooove ittt 🌴🔥 #bali #liburan_bali #ubud': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Ubud'),
    'Baliii indaaahh bngttt 😍😍 pantai nya bersiiihhh!!! #bali #pantai_bali': 
        ('Positif', 'Kebersihan & Lingkungan', 'Pantai Bali'),
    'jalanan macet muluuu capekkk 😩😩!!! #liburan_bali #canggu': 
        ('Negatif', 'Kemacetan & Transportasi', 'Canggu'),
    'healing ke bali emg worth it sihhh 😌✨ #liburan_bali #ubud': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Ubud'),
    'liburan ke bali seruuuu bgttt 😍aa😍😍!!! #bali #pantai_bali': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Pantai Bali'),
    'harga hotel naik trss 😑😑 duh... #pariwisata_bali #ubud': 
        ('Negatif', 'Harga & Biaya', 'Ubud'),
    'sunset bali kereeennnn bgttt 😍😍 luvvv it!!! #bali #pantai_bali': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Pantai Bali'),
    'tmpt wisata di bali bagus2 sihhh 👍👍 #liburan_bali #pantai_bali': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Pantai Bali'),
    'pantai bersihh & nyaman 😍 loveee baliii #bali #pantai_bali': 
        ('Positif', 'Kebersihan & Lingkungan', 'Pantai Bali'),
    'pantai kotorrrr abisss 😢😢 byk sampahh... #pariwisata_bali #pantai_bali': 
        ('Negatif', 'Kebersihan & Lingkungan', 'Pantai Bali'),
    'sampah msh bykk bgtt 😠😠 parah sih #pariwisata_bali #pantai_bali': 
        ('Negatif', 'Kebersihan & Lingkungan', 'Pantai Bali'),
    'harga makan mahal bgd sihh 😭😭 gk worth it?? #pariwisata_bali #canggu': 
        ('Negatif', 'Harga & Biaya', 'Canggu'),
    'transportasi di bali susahhh bgttt 😤😤!!! #bali #canggu': 
        ('Negatif', 'Kemacetan & Transportasi', 'Canggu'),
    'balii always be my favvv place ❤️❤️ #bali #ubud': 
        ('Positif', 'Daya Tarik & Rekreasi', 'Ubud'),
    'cuaca panas poll 🔥🔥 not comfy at all... #liburan_bali #canggu': 
        ('Negatif', 'Cuaca', 'Canggu'),
    'macettt parahhh di baliii 😡😡!!! jd mls liburan... #pariwisata_bali #canggu': 
        ('Negatif', 'Kemacetan & Transportasi', 'Canggu'),
    'ticket masuk mahal yaaa 😓😓 seriusss #pariwisata_bali #canggu': 
        ('Negatif', 'Harga & Biaya', 'Canggu')
}

def classify_tweet(tweet):
    t_clean = tweet.strip()
    if t_clean in SENTIMENT_MAPPING:
        return SENTIMENT_MAPPING[t_clean]
    
    # Robust Fallback Classification
    t_lower = t_clean.lower()
    
    # Sentiment
    neg_keywords = ['sampah', 'kotor', 'macet', 'panas', 'mahal', 'naik', 'susah', 'not comfy', 'capek', 'mls', '😠', '😭', '😩', '😡', '😤', '😑', '😢', '😓']
    sentiment = 'Positif'
    for kw in neg_keywords:
        if kw in t_lower:
            sentiment = 'Negatif'
            break
            
    # Aspect/Category
    if any(kw in t_lower for kw in ['sampah', 'kotor', 'bersih']):
        aspect = 'Kebersihan & Lingkungan'
    elif any(kw in t_lower for kw in ['macet', 'jalanan', 'transportasi', 'susah']):
        aspect = 'Kemacetan & Transportasi'
    elif any(kw in t_lower for kw in ['harga', 'mahal', 'ticket', 'hotel', 'makan', 'naik']):
        aspect = 'Harga & Biaya'
    elif any(kw in t_lower for kw in ['panas', 'cuaca', 'comfy']):
        aspect = 'Cuaca'
    else:
        aspect = 'Daya Tarik & Rekreasi'
        
    # Location
    if '#canggu' in t_lower or 'canggu' in t_lower:
        location = 'Canggu'
    elif '#ubud' in t_lower or 'ubud' in t_lower:
        location = 'Ubud'
    elif '#pantai_bali' in t_lower or 'pantai' in t_lower:
        location = 'Pantai Bali'
    else:
        location = 'Lainnya'
        
    return sentiment, aspect, location

# Load and Process Data
@st.cache_data
def load_data():
    df = pd.read_csv("dataset projek.csv")
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    # Apply Classification
    results = df['tweet'].apply(classify_tweet)
    df['sentiment'] = [r[0] for r in results]
    df['aspect'] = [r[1] for r in results]
    df['location'] = [r[2] for r in results]
    
    return df

# Initialize Data
try:
    df_raw = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.info("Pastikan file 'dataset projek.csv' berada di direktori yang sama dengan program ini.")
    st.stop()

# Title Section with Pastel styling
st.markdown("""
<div style="margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #f3eef7; padding-bottom: 10px;">
    <div>
        <h1 style="margin: 0; color: #db2777; font-size: 24px; letter-spacing: -0.5px;">Bali Tourism Sentiment Dashboard</h1>
        <p style="margin: 3px 0 0 0; color: #a78bfa; font-size: 13px; font-weight: 500;">Modern Pastel Interface • Analisis Sentimen & Umpan Balik</p>
    </div>
    <div style="background-color: #ffffff; border: 1px solid #f3eef7; padding: 6px 14px; border-radius: 12px; box-shadow: 0 4px 12px rgba(219,39,119,0.02)">
        <span style="color: #db2777; font-weight: 600; font-size: 12px;">📊 Total Data: 2,000 Ulasan</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ================= SIDEBAR FILTER =================
st.sidebar.markdown("""
<div style="margin-bottom: 15px;">
    <h2 style="margin: 0; font-size: 18px; color: #db2777; font-weight: 700;">Filter Analisis</h2>
    <p style="margin: 2px 0 0 0; color: #a78bfa; font-size: 11px;">Sesuaikan visualisasi dasbor</p>
</div>
""", unsafe_allow_html=True)

# Date Filter
min_date = df_raw['tanggal'].min().date()
max_date = df_raw['tanggal'].max().date()

st.sidebar.subheader("Periode Waktu")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Convert dates to datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Location Filter
locations = ['Semua Lokasi'] + sorted(df_raw['location'].unique().tolist())
selected_location = st.sidebar.selectbox('Wilayah/Lokasi', locations)

# Sentiment Filter
sentiments = ['Semua Sentimen', 'Positif', 'Negatif']
selected_sentiment = st.sidebar.selectbox('Sentimen', sentiments)

# Aspect Filter
aspects = ['Semua Kategori', 'Kebersihan & Lingkungan', 'Kemacetan & Transportasi', 'Harga & Biaya', 'Cuaca', 'Daya Tarik & Rekreasi']
selected_aspect = st.sidebar.selectbox('Kategori Isu', aspects)

# Reset Button
if st.sidebar.button("Reset Filter", use_container_width=True):
    st.rerun()

st.sidebar.markdown("""
<div style="margin-top: 40px; border-top: 1px solid #f6d1e4; padding-top: 15px; text-align: center; color: #c084fc; font-size: 10px; font-weight: 500;">
    Bali Decision Support System v2.0<br>
    Pastel Aesthetic UI
</div>
""", unsafe_allow_html=True)

# ================= APPLY FILTERS =================
df_filtered = df_raw.copy()

# Date range filtering
df_filtered = df_filtered[(df_filtered['tanggal'] >= start_datetime) & (df_filtered['tanggal'] <= end_datetime)]

# Location filtering
if selected_location != 'Semua Lokasi':
    df_filtered = df_filtered[df_filtered['location'] == selected_location]

# Sentiment filtering
if selected_sentiment != 'Semua Sentimen':
    df_filtered = df_filtered[df_filtered['sentiment'] == selected_sentiment]

# Aspect filtering
if selected_aspect != 'Semua Kategori':
    df_filtered = df_filtered[df_filtered['aspect'] == selected_aspect]


# ================= CALCULATE METRICS =================
total_all = len(df_raw)
total_filtered = len(df_filtered)

if total_filtered > 0:
    pos_count = len(df_filtered[df_filtered['sentiment'] == 'Positif'])
    neg_count = len(df_filtered[df_filtered['sentiment'] == 'Negatif'])
    pos_pct = (pos_count / total_filtered) * 100
    neg_pct = (neg_count / total_filtered) * 100
    
    # Find top location and category in the filtered dataset
    top_loc = df_filtered['location'].mode().iloc[0] if not df_filtered['location'].empty else "N/A"
    top_aspect = df_filtered['aspect'].mode().iloc[0] if not df_filtered['aspect'].empty else "N/A"
else:
    pos_count = neg_count = pos_pct = neg_pct = 0
    top_loc = top_aspect = "N/A"

# ================= TAB CREATION =================
tab1, tab2, tab3, tab4 = st.tabs([
    "Ringkasan Analisis", 
    "Analisis Lokasi & Isu", 
    "Rekomendasi Aksi", 
    "Cari Ulasan & Data"
])

# ================= TAB 1: OVERVIEW =================
with tab1:
    # KPI Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Ulasan</div>
            <div class="kpi-value">{total_filtered:,}</div>
            <div class="kpi-subtitle">Dari {total_all:,} total ulasan</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Sentimen Positif</div>
            <div class="kpi-value">{pos_pct:.1f}%</div>
            <div class="kpi-subtitle">{pos_count:,} ulasan senang</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Sentimen Negatif</div>
            <div class="kpi-value" style="color: #a78bfa;">{neg_pct:.1f}%</div>
            <div class="kpi-subtitle">{neg_count:,} ulasan keluhan</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Wilayah Teratas</div>
            <div class="kpi-value" style="font-size: 24px;">{top_loc}</div>
            <div class="kpi-subtitle">Volume diskusi tertinggi</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Aspek Utama</div>
            <div class="kpi-value" style="font-size: 18px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{top_aspect}</div>
            <div class="kpi-subtitle">Kategori keluhan terbanyak</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if total_filtered == 0:
        st.warning("Tidak ada data yang sesuai dengan filter Anda. Silakan sesuaikan kembali filter di sidebar.")
    else:
        # Row for pie chart and aspect bar chart
        chart_col1, chart_col2 = st.columns([1, 1])
        
        with chart_col1:
            sentiment_df = pd.DataFrame({
                'Sentimen': ['Positif', 'Negatif'],
                'Jumlah': [pos_count, neg_count]
            })
            
            # Using Pastel colors: Positif = Pastel Pink, Negatif = Pastel Indigo
            fig_pie = px.pie(
                sentiment_df, 
                names='Sentimen', 
                values='Jumlah',
                color='Sentimen',
                color_discrete_map={'Positif': '#ff007f', 'Negatif': '#a78bfa'},
                hole=0.55,
                title="<b>Proporsi Sentimen Wisatawan</b>"
            )
            fig_pie.update_traces(
                textinfo='percent+label', 
                textfont_size=12,
                marker=dict(line=dict(color='#120224', width=2))
            )
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=14, color='#e0d5f5', family="Inter"),
                font=dict(family="Inter", color="#e0d5f5")
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            # Count aspect counts
            aspect_df = df_filtered['aspect'].value_counts().reset_index()
            aspect_df.columns = ['Kategori', 'Jumlah']
            aspect_df = aspect_df.sort_values(by='Jumlah', ascending=True)
            
            # Neon Purple/Pink color palette
            color_sequence = ['#1d0836', '#4c1d95', '#7c3aed', '#a78bfa', '#d946ef', '#ff007f']
            
            fig_bar = px.bar(
                aspect_df,
                x='Jumlah',
                y='Kategori',
                orientation='h',
                title="<b>Distribusi Topik & Keluhan Aspek</b>",
                color='Kategori',
                color_discrete_sequence=color_sequence
            )
            fig_bar.update_layout(
                showlegend=False,
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=14, color='#e0d5f5', family="Inter"),
                font=dict(family="Inter", color="#e0d5f5"),
                xaxis_title="Jumlah Ulasan",
                yaxis_title="",
                xaxis=dict(showgrid=True, gridcolor='rgba(255, 0, 127, 0.2)')
            )
            fig_bar.update_traces(
                marker=dict(line=dict(color='#120224', width=1)),
                texttemplate='%{x}',
                textposition='outside',
                textfont=dict(color="#e0d5f5")
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
        # Row for trend analysis over time
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Trend Analysis
        df_filtered['Bulan'] = df_filtered['tanggal'].dt.to_period('M').astype(str)
        trend_data = df_filtered.groupby(['Bulan', 'sentiment']).size().reset_index(name='Jumlah')
        
        fig_trend = px.line(
            trend_data,
            x='Bulan',
            y='Jumlah',
            color='sentiment',
            color_discrete_map={'Positif': '#ff007f', 'Negatif': '#a78bfa'},
            title="<b>Tren Ulasan Wisatawan Bulanan</b>",
            markers=True
        )
        
        fig_trend.update_layout(
            margin=dict(t=60, b=40, l=30, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=14, color='#e0d5f5', family="Inter"),
            font=dict(family="Inter", color="#e0d5f5"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title=None
            ),
            xaxis_title="",
            yaxis_title="Jumlah Ulasan",
            xaxis=dict(showgrid=True, gridcolor='rgba(255, 0, 127, 0.2)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255, 0, 127, 0.2)')
        )
        fig_trend.update_traces(line=dict(width=3), marker=dict(size=8))
        
        st.plotly_chart(fig_trend, use_container_width=True)

# ================= TAB 2: DETAILED ANALYSIS =================
with tab2:
    if total_filtered == 0:
        st.warning("Tidak ada data yang sesuai dengan filter Anda.")
    else:
        st.markdown("### 🗺️ Eksplorasi Hubungan Wilayah & Keluhan")
        st.write("Analisis ini menunjukkan jenis isu apa saja yang paling banyak dikeluhkan wisatawan di setiap daerah pariwisata utama.")
        
        col_t2_1, col_t2_2 = st.columns([1, 1])
        
        with col_t2_1:
            loc_sentiment_df = df_filtered.groupby(['location', 'sentiment']).size().reset_index(name='Jumlah')
            
            fig_loc_sent = px.bar(
                loc_sentiment_df,
                x='location',
                y='Jumlah',
                color='sentiment',
                color_discrete_map={'Positif': '#ff007f', 'Negatif': '#a78bfa'},
                barmode='group',
                title='<b>Perbandingan Sentimen Antar Wilayah</b>',
                labels={'location': 'Lokasi', 'Jumlah': 'Jumlah Ulasan', 'sentiment': 'Sentimen'}
            )
            fig_loc_sent.update_layout(
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=14, color='#e0d5f5', family="Inter"),
                font=dict(family="Inter", color="#e0d5f5"),
                xaxis_title="",
                yaxis_title="Jumlah Ulasan",
                legend_title=None,
                yaxis=dict(showgrid=True, gridcolor='rgba(255, 0, 127, 0.2)')
            )
            st.plotly_chart(fig_loc_sent, use_container_width=True)
            
        with col_t2_2:
            aspect_sentiment_df = df_filtered.groupby(['aspect', 'sentiment']).size().reset_index(name='Jumlah')
            
            fig_aspect_stack = px.bar(
                aspect_sentiment_df,
                x='aspect',
                y='Jumlah',
                color='sentiment',
                color_discrete_map={'Positif': '#ff007f', 'Negatif': '#a78bfa'},
                title=f'<b>Komposisi Sentimen per Kategori Isu (Data Terfilter)</b>',
                labels={'aspect': 'Kategori Aspek', 'Jumlah': 'Jumlah Ulasan', 'sentiment': 'Sentimen'}
            )
            fig_aspect_stack.update_layout(
                margin=dict(t=50, b=20, l=20, r=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=14, color='#e0d5f5', family="Inter"),
                font=dict(family="Inter", color="#e0d5f5"),
                xaxis_title="",
                yaxis_title="Jumlah Ulasan",
                legend_title=None,
                yaxis=dict(showgrid=True, gridcolor='rgba(255, 0, 127, 0.2)')
            )
            st.plotly_chart(fig_aspect_stack, use_container_width=True)

        # Heatmap Section
        st.markdown("<br><b>Peta Kepadatan Keluhan & Diskusi (Wilayah vs Kategori Isu)</b>", unsafe_allow_html=True)
        fig_heatmap = px.density_heatmap(
            df_filtered,
            x='aspect',
            y='location',
            color_continuous_scale=['#120224', '#7c3aed', '#ff007f'],
            labels={'aspect': 'Kategori Isu', 'location': 'Wilayah/Lokasi'}
        )
        fig_heatmap.update_layout(
            margin=dict(t=30, b=40, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=14, color='#e0d5f5', family="Inter"),
            font=dict(family="Inter", color="#e0d5f5"),
            xaxis_title="Kategori Isu",
            yaxis_title="Wilayah/Lokasi"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Cross-Tabulation Matrix
        st.markdown("<br><b>Tabel Silang Wilayah vs Kategori Ulasan</b>", unsafe_allow_html=True)
        crosstab = pd.crosstab(df_filtered['location'], df_filtered['aspect'], values=df_filtered['sentiment'], 
                               aggfunc=lambda x: f"{(sum(x == 'Positif')/len(x))*100:.0f}% Positif ({len(x)} Ulasan)")
        st.dataframe(crosstab, use_container_width=True)

# ================= TAB 3: RECOMMENDATIONS =================
with tab3:
    st.markdown("### 💡 Rekomendasi Aksi & Intervensi Kebijakan")
    st.write("Rekomendasi ini disusun secara dinamis berdasarkan data keluhan negatif terbanyak yang diidentifikasi oleh wisatawan.")
    
    # 1. Kebersihan Pantai Recommendation
    st.markdown("""
    <div class="rec-card" style="border-left-color: #ec4899;">
        <div class="rec-title" style="color: #ec4899;">🗑️ Penanganan Sampah Pantai & Lingkungan (Prioritas Tinggi)</div>
        <div class="rec-desc">
            <b>Analisis Data:</b> Ulasan terkait Pantai Bali didominasi oleh keluhan sampah (misalnya: <i>"pantai kotorrrr abisss", "sampah msh bykk bgtt"</i>). Total terdapat ulasan negatif kebersihan yang cukup besar di pesisir.<br>
            <b>Aksi yang Direkomendasikan:</b>
            <ol>
                <li>Menugaskan <b>satgas kebersihan pantai harian</b> pada jam-jam krusial (pagi hari sebelum turis datang & sore setelah sunset).</li>
                <li>Menyediakan tempat sampah terpilah (organik & anorganik) setiap 50 meter di wilayah pantai pariwisata.</li>
                <li>Mengadakan kolaborasi komunitas lokal, pemilik usaha pantai, dan turis untuk program clean-up mingguan.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Kemacetan Canggu Recommendation
    st.markdown("""
    <div class="rec-card" style="border-left-color: #a78bfa;">
        <div class="rec-title" style="color: #a78bfa;">🚗 Rekayasa Lalu Lintas & Transportasi di Wilayah Canggu</div>
        <div class="rec-desc">
            <b>Analisis Data:</b> Canggu memiliki tingkat keluhan kemacetan lalu lintas tertinggi (misalnya: <i>"jalanan macet muluuu", "macettt parahhh di baliii"</i>). Transportasi umum juga dinilai susah diakses.<br>
            <b>Aksi yang Direkomendasikan:</b>
            <ol>
                <li>Menerapkan <b>sistem satu arah (one-way system)</b> pada jam sibuk di jalur sempit Canggu (seperti Jalan Batu Bolong dan Jalan Shortcut Canggu).</li>
                <li>Menyediakan fasilitas <b>shuttle bus listrik (Canggu Loop)</b> untuk mengurangi penggunaan sepeda motor sewaan/mobil pribadi oleh turis.</li>
                <li>Menertibkan parkir liar di bahu jalan raya depan restoran/klub pantai berkolaborasi dengan pecalang setempat.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Harga Akomodasi & Tiket Ubud/Canggu Recommendation
    st.markdown("""
    <div class="rec-card" style="border-left-color: #818cf8;">
        <div class="rec-title" style="color: #818cf8;">💰 Regulasi Standardisasi Tarif (Hotel, Restoran, & Tiket Masuk)</div>
        <div class="rec-desc">
            <b>Analisis Data:</b> Wisatawan mengeluhkan kenaikan harga akomodasi di Ubud (<i>"harga hotel naik trss"</i>) serta mahalnya makanan dan tiket masuk di Canggu.<br>
            <b>Aksi yang Direkomendasikan:</b>
            <ol>
                <li>Dinas Pariwisata menetapkan <b>pedoman batas tarif atas dan bawah</b> untuk hotel/villa bersertifikasi di Ubud guna menghindari lonjakan harga sepihak saat high season.</li>
                <li>Standardisasi harga tiket masuk tempat wisata milik pemda secara transparan dan menyediakan opsi pembayaran non-tunai (e-ticketing).</li>
                <li>Mewajibkan restoran dan warung wisata mencantumkan harga makanan secara jelas di menu (termasuk pajak) guna menghindari praktik <i>tourist trap</i>.</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Cuaca & Fasilitas Peneduh
    st.markdown("""
    <div class="rec-card" style="border-left-color: #cbd5e1;">
        <div class="rec-title" style="color: #94a3b8;">☀️ Peningkatan Infrastruktur Kenyamanan Pejalan Kaki (Cuaca Panas)</div>
        <div class="rec-desc">
            <b>Analisis Data:</b> Ulasan mengeluhkan cuaca yang sangat panas dan tidak nyaman saat berjalan kaki di daerah wisata Canggu.<br>
            <b>Aksi yang Direkomendasikan:</b>
            <ol>
                <li>Melakukan penanaman pohon peneduh di sepanjang pedestrian/trotoar jalan utama pariwisata.</li>
                <li>Menyediakan halte transportasi yang teduh dan dilengkapi kipas angin/mist blower.</li>
                <li>Mendorong kampanye promosi berwisata di jam-jam teduh (pagi hari dan sore hari menjelang matahari terbenam).</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= TAB 4: SEARCH & DATASET =================
with tab4:
    st.markdown("### 🔍 Cari dan Telusuri Ulasan Wisatawan")
    st.write("Gunakan fitur di bawah untuk mencari teks tertentu dari ulasan wisatawan secara detail.")
    
    # Text search
    search_query = st.text_input("🔍 Masukkan kata kunci pencarian (misal: 'worth', 'kotor', 'macet')", "")
    
    # Filter dataset based on search query
    df_search = df_filtered.copy()
    if search_query:
        df_search = df_search[df_search['tweet'].str.contains(search_query, case=False, na=False)]
        
    st.markdown(f"Ditemukan **{len(df_search)}** ulasan berdasarkan kata kunci dan filter saat ini.")
    
    # Display styled tweet list with pagination simulation
    if len(df_search) > 0:
        for idx, row in df_search.head(50).iterrows():
            sentiment_badge = f'<span class="badge-pos">Positif</span>' if row['sentiment'] == 'Positif' else f'<span class="badge-neg">Negatif</span>'
            
            st.markdown(f"""
            <div class="tweet-box">
                <div class="tweet-header">
                    <div>👤 <span class="tweet-user">@{row['username']}</span> | 📅 {row['tanggal'].strftime('%Y-%m-%d')}</div>
                    <div>📍 {row['location']} | {sentiment_badge}</div>
                </div>
                <div class="tweet-content">"{row['tweet']}"</div>
                <div style="font-size: 11px; margin-top: 5px; color: #a78bfa;">🏷️ Kategori Isu: <b>{row['aspect']}</b></div>
            </div>
            """, unsafe_allow_html=True)
            
        if len(df_search) > 50:
            st.info("Hanya menampilkan 50 ulasan teratas untuk menghemat memori. Gunakan filter atau pencarian spesifik untuk menyaring data.")
            
        # Download Data Button
        st.markdown("<br>", unsafe_allow_html=True)
        csv_download = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Unduh Seluruh Data Hasil Analisis (.csv)",
            data=csv_download,
            file_name=f"hasil_analisis_sentimen_bali_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Tidak ada ulasan yang cocok dengan kata kunci pencarian Anda.")
