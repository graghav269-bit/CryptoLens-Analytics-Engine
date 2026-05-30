import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    
    /* ===== REMOVE BLUE TABLE COMPLETELY ===== */
[data-testid="stDataFrame"] {
    background: #0a0a0a !important;
}

[data-testid="stDataFrame"] table {
    background: #0a0a0a !important;
}

[data-testid="stDataFrame"] th {
    background: #111 !important;
    color: #ccc !important;
    border-bottom: 1px solid #222 !important;
}

[data-testid="stDataFrame"] td {
    background: #0a0a0a !important;
    color: #fff !important;
    border-bottom: 1px solid #111 !important;
}
/* ===== CLEAN PROFESSIONAL TABLE ===== */

.custom-table {
    width: 100%;
    border-collapse: collapse;
    background: #0a0a0a;
    color: #fff;
    border: 1px solid #222;
    border-radius: 10px;
    overflow: hidden;
    font-size: 14px;
}

.custom-table th {
    background: #111;
    color: #aaa;
    padding: 14px;
    text-align: center;
    border-bottom: 1px solid #222;
}

.custom-table td {
    padding: 14px;
    text-align: center;
    border-bottom: 1px solid #111;
}

.custom-table tr:hover {
    background: #1a1a1a;
}

/* remove weird left gap */
.custom-table td:first-child,
.custom-table th:first-child {
    text-align: left;
    padding-left: 20px;
}

/* remove blue hover */
[data-testid="stDataFrame"] tr:hover {
    background: #1a1a1a !important;
}

/* ===== REMOVE BLUE FROM DROPDOWN ===== */
div[data-baseweb="select"] {
    background: #111 !important;
    border: 1px solid #333 !important;
}

div[data-baseweb="select"] * {
    background: #111 !important;
    color: #fff !important;
}

/* dropdown menu */
ul {
    background: #111 !important;
}

li {
    background: #111 !important;
    color: #fff !important;
}

li:hover {
    background: #1a1a1a !important;
}

/* ===== REMOVE BLUE INPUT HIGHLIGHT ===== */
div[data-baseweb="select"]:focus-within {
    border-color: #888 !important;
}

/* ===== REMOVE BLUE DIVIDERS / LINES ===== */
hr {
    border: 1px solid #222 !important;
}

/* vertical column divider (this is your "vertical blue line") */
[data-testid="column"] {
    border: none !important;
}

    /* ===== BACKGROUND (Mac style) ===== */
    .stApp {
        background: radial-gradient(circle at top, #111 0%, #0a0a0a 60%);
        color: #e5e5e5;
    }

    /* ===== REMOVE TOP BLUE BAR ===== */
    header[data-testid="stHeader"] {
        background: #0a0a0a !important;
        border-bottom: 1px solid #222 !important;
    }

    .stApp > header {
        background: #0a0a0a !important;
    }

    /* ===== REMOVE DEPLOY / TOOLBAR BLUE ===== */
    [data-testid="stToolbar"] {
        background: #0a0a0a !important;
    }

    button[kind="header"] {
        background: transparent !important;
        color: white !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #0f0f0f !important;
        border-right: 1px solid #222;
    }

    /* Active sidebar item */
    section[data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #1a1a1a !important;
        border-left: 3px solid #888 !important;
        color: #fff !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebarNav"] a:hover {
        background: #1a1a1a !important;
    }

    /* ===== REMOVE ALL BLUE FOCUS ===== */
    *:focus, *:active {
        outline: none !important;
        box-shadow: none !important;
    }

    /* ===== TEXT ===== */
    h1, h2, h3 {
        color: #ffffff;
    }

    p {
        color: #b5b5b5;
    }

    /* ===== CARDS ===== */
    .glass-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 22px;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border: 1px solid rgba(255,255,255,0.2);
        transform: translateY(-3px);
    }

    /* ===== BUTTON ===== */
    .stButton button {
        background: #111;
        border: 1px solid #333;
        color: #fff;
    }

    .stButton button:hover {
        background: #1a1a1a;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: 1px solid #222;
    }

    </style>
    """, unsafe_allow_html=True)