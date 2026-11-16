import base64
import json
import math
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Official Ghost Foundation Logo SVG
GHOST_LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" id="Full_White_logo" data-name="Full White logo" viewBox="0 0 977.95 396.85"><defs><style>.cls-1{fill:#302f2f;}.cls-2{fill:#fff;}</style></defs><g><path class="cls-2" d="M487.01,186.4h-39.94c-.36,0-.73.15-.99.41l-21.15,21.26c-.89.88-.26,2.4.99,2.4h37.14c.77,0,1.4.62,1.4,1.4v9.23c0,.77-.63,1.41-1.4,1.41h-45.1c-.77,0-1.4-.63-1.4-1.41v-34.1c0-.38.15-.73.41-1l11.16-11.21c.26-.26.61-.41.99-.41h34.76c.37,0,.73-.15.99-.42l21.15-21.25c.58-.58.51-1.44.03-1.95-.25-.27-.6-.44-1.01-.44h-67.89c-.19,0-.37.03-.53.1-.18.07-.32.17-.45.31l-23.13,23.23c-.27.27-.4.62-.4,1v70.19c0,.77.62,1.4,1.39,1.4h93c.77,0,1.39-.62,1.39-1.4v-57.34c0-.78-.62-1.41-1.39-1.41Z"></path><path class="cls-2" d="M501.77,150.31h21.15c.77,0,1.4.63,1.4,1.4v33.28c0,.78.63,1.4,1.4,1.4h45.1c.77,0,1.4-.63,1.4-1.4v-46.13c0-.37.15-.73.41-.99l21.15-21.25c.88-.88,2.38-.26,2.38.99v127.53c0,.78-.63,1.4-1.4,1.4h-21.15c-.77,0-1.4-.63-1.4-1.4v-33.28c0-.78-.63-1.4-1.4-1.4h-45.1c-.77,0-1.4.63-1.4,1.4v46.13c0,.37-.15.73-.41.99l-21.15,21.25c-.88.88-2.38.26-2.38-.99v-127.53c0-.78.63-1.4,1.4-1.4Z"></path><path class="cls-2" d="M608.13,245.15v-93.43c0-.78.63-1.4,1.4-1.4h92.99c.77,0,1.4.63,1.4,1.4v93.43c0,.78-.63,1.4-1.4,1.4h-92.99c-.77,0-1.4-.63-1.4-1.4ZM679.97,221.09v-45.31c0-.78-.63-1.4-1.4-1.4h-45.1c-.77,0-1.4.63-1.4,1.4v45.31c0,.78.63,1.4,1.4,1.4h45.1c.77,0,1.4-.63,1.4-1.4Z"></path><path class="cls-2" d="M708.69,244.15l21.15-21.25c.26-.26.62-.41.99-.41h44.35c.37,0,.73-.15.99-.41l9.18-9.22c.88-.88.26-2.4-.99-2.4h-67.07c-.77,0-1.4-.63-1.4-1.4v-34.1c0-.37.15-.73.41-.99l23.13-23.23c.26-.26.62-.41.99-.41h77.77c1.24,0,1.87,1.51.99,2.4l-21.15,21.25c-.26.26-.62.41-.99.41h-44.64c-.37,0-.73.15-.99.41l-9.18,9.22c-.88.88-.26,2.4.99,2.4h67.07c.77,0,1.4.63,1.4,1.4v34.1c0,.37-.15.73-.41.99l-23.13,23.24c-.26.26-.62.41-.99.41h-77.48c-1.24,0-1.87-1.51-.99-2.4Z"></path><path class="cls-2" d="M846.21,174.37h-31.15c-1.24,0-1.87-1.51-.99-2.4l21.15-21.25c.26-.26.62-.41.99-.41h10c.77,0,1.4-.63,1.4-1.4v-10.04c0-.37.15-.73.41-.99l21.15-21.25c.88-.88,2.38-.26,2.38.99v31.3c0,.78.63,1.4,1.4,1.4h37.14c1.24,0,1.87,1.51.99,2.4l-21.15,21.25c-.26.26-.62.41-.99.41h-15.99c-.77,0-1.4.63-1.4,1.4v82.22c0,.37-.15.73-.41.99l-21.15,21.25c-.88.88-2.38.26-2.38-.99v-103.47c0-.78-.63-1.4-1.4-1.4Z"></path></g><g><path class="cls-2" d="M314.44,187.52c0-.07-.01-.14-.03-.21-.46-2.68-2.01-5.27-4.23-6.67-.48-.32-.98-.55-1.47-.71-.21-.07-.43-.14-.63-.18-5.28-1.22-11.01,4.38-19.06,3.48-6.5-.73-11.37-5.35-15.19-10.22-1.52-1.92-2.88-3.89-4.1-5.67-.22-.32-.44-.63-.65-.96-.01-.02-.03-.03-.04-.06-5.64-8.56-7.01-15.31-9.28-24.86-.39-1.63-.81-3.36-1.28-5.18-.38-1.52-.81-3.12-1.3-4.79-4.14-14.55-7.75-27.19-15.51-37.92l-.2-.28c-1.4-1.92-2.94-3.77-4.63-5.56-2.14-2.27-18.97-19.46-44.4-19.46h-.37c-26.09.17-43.54,18.41-44.9,19.87-2.84,3.06-5.28,6.34-7.41,9.82h0c-14.58,23.78-14.33,55.74-23.98,75.42-.04.09-.09.19-.14.28-1.78,3.59-3.89,6.75-6.49,9.37-.79.8-1.64,1.61-2.58,2.39-.95.82-1.98,1.6-3.09,2.33-.22.15-.43.29-.64.42-.22.14-.44.28-.67.42-2.05,1.2-4.36,2.23-6.97,2.88-.17.04-.32.09-.48.12-1.65.4-3.16.39-4.57.18-4.79-.73-8.44-3.88-13.45-2.18-.1.03-.2.07-.31.11-.2.07-1.19.45-2.4,1.25-.01,0-.02.01-.03.02-1.65,1.07-3.71,2.88-4.79,5.63-.1.27-.21.54-.29.83-.03.09-.06.19-.08.28-.72,2.67-.47,5.78.62,8.15.63,1.4,1.55,2.53,2.73,3.17.1.06.18.09.27.13.53.24,1.04.34,1.54.37h.01c2.43.14,4.72-1.66,7.63-.21h.01c2.89,1.45,2.56,4.21,4.37,6.05.03.02.05.05.07.08.28.27.62.52,1.02.74.05.03.11.06.15.08,0,0,.01.01.03.01,1.33.68,2.63.61,3.95.26,2.8-.74,5.71-2.74,9.23-1.62.01,0,.02.01.02.01,1.78.58,3.33,1.84,4.56,3.45.02.02.02.03.03.04,1.79,2.33,2.88,5.38,2.95,8.13.03.91-.05,1.84-.23,2.74-.03.24-.08.49-.12.73-.13.58-.29,1.14-.47,1.71-.18.59-.4,1.15-.63,1.7-1.15,2.79-2.73,5.24-3.85,6.96-1.78,2.7-2.73,3.36-2.9,5.26-.31,3.34,2.07,7.28,5.17,8.87.75.39,1.55.64,2.36.71.84.07,1.67-.05,2.43-.24.12-.03.23-.06.36-.11.46-.14.9-.3,1.27-.46.18-.07.35-.16.52-.24.32-.15.56-.28.72-.37,1.72-.94,1.98-1.67,3.93-2.55.64-.29,2.19-.96,4.16-1.05,2.71-.12,4.76.97,5.79,1.53.09.05.17.1.26.16.03.01.06.03.09.04,4.61,2.68,6.62,7.62,7.82,10.66.14.36.31.8.48,1.31,0,.01.02.02.02.03.75,2.21,1.71,5.75,1.88,10.23.02.62.04,1.21.02,1.77-.05,6.47-1.83,9.37.42,13.32.19.32.5.85.95,1.42.08.12.19.23.29.35.7.81,1.69,1.62,2.99,1.96.05.02.12.04.18.05,2.43.53,4.63-.83,5.47-1.45.13-.09.22-.16.28-.2,3.22-2.55,2.77-6.18,3.59-11.12v-.03c.32-1.94.86-4.08,1.87-6.43.29-.67.77-1.77,1.39-2.97.03-.04.04-.06.05-.09,1.42-2.72,3.61-5.95,6.12-6.02,2.12-.05,4.14,2.17,5.9,5.25,3.45,5.98,5.96,15.19,6.47,17.07.42,1.52.81,3.13,1.2,4.8,2.52,10.81,4.66,24.08,8.97,31.85.01.03.01.04.03.05.16.29.33.57.49.84.89,1.45,2.26,3.31,4.24,3.84.17.06.35.1.53.12.29.05.58.05.86.03.08.02.16,0,.24,0,2.22-.25,4.12-2.04,5.13-3.07.1-.11.18-.2.26-.28,5.29-5.58,6.37-14.42,9.38-32.46.23-1.43.48-2.91.75-4.46,0,0,.84-4.95,6.29-17.3.14-.3.27-.6.41-.9.9-2.02,2.23-4.84,4.15-4.93.96-.05,2.48.57,4.55,4.49.01.01.01.02.02.04.13.24.26.49.39.76,3.41,6.93,4.14,14.33,4.73,20.6h0c.4,4.36.75,8.16,1.87,10.88.49,1.2,1.14,2.2,2.02,2.93.3.25.95.81,1.87,1.19.03.02.05.03.07.03.13.06.27.11.41.14.03.02.08.04.12.05.36.11.76.18,1.17.21h.01c.06.01.12.01.18.01h.25c2.06-.04,3.69-1.36,4.54-2.15.15-.14.28-.27.38-.36,4.34-4.27,3.22-15.73,4.31-25.41.59-5.37,1.87-10.2,5.15-12.94.15-.12.3-.24.45-.36,1.11-.81,2.99-1.82,4.91-2.09.99-.14,1.98-.07,2.86.32h.02s.03.02.05.03c2.47,1.12,2.21,3.88,5.49,6.74.01,0,.01.01.02.03.08.08.17.15.27.23.78.66,2.6,2.16,4.64,2.55.48.11.98.14,1.49.09.12-.02.23-.04.35-.06.03,0,.07,0,.09-.01,4.28-.87,6.67-7.52,7.24-9.27.04-.11.06-.19.09-.26,2.12-6.5-1.31-18.6-1.94-25.72-.04-.49-.08-1-.09-1.52-.01-.04-.01-.09-.01-.12-.11-2.37,0-4.96.36-7.49.84-6.21,3.13-12.11,7.26-13.87.05-.02.1-.03.14-.06,3.59-1.43,7.41.64,9.89-.6.01,0,.03-.02.05-.03.36-.19.69-.44.99-.79.17-.2.31-.4.4-.61.86-1.62.05-3.5,1.46-6.68.06-.14.13-.29.2-.44.32-.67,1.58-3.16,4.12-4.95.68-.49,1.32-.83,1.94-1.08,1.03-.4,1.99-.54,2.92-.62,1.88-.16,3.7-.11,5.91-1.53.03-.02.14-.08.28-.18t0-.02c.9-.64,3.59-2.84,4.43-6.25.13-.51.21-1.05.25-1.61.03-.63,0-1.26-.11-1.89ZM246.17,191.82c-1.59,6.07-7.27,6.78-11.03-1.57-2.18-4.82-2.3-15.69-8.08-13.99-5.18,1.5-2.25,31.45-9.45,33.12-9,2.09-6.69-25.84-12.22-26.82-8.23-1.45-2.95,27.48-11.83,27.62-8.2.12-6.54-29.25-16.93-24.46-1.48.67-5.59,9.05-7.5,9.85-10.63,4.47-7.07-17.12-10.63-18.92-5.55-2.8-5.15,11.91-10.64,13.81-7.43,2.54-7.27-12.2-7.68-21.52-.94-21.92.48-48.22,14.57-66.26,7.58-9.69,22.02-19.12,34.48-19.91,26.2-1.67,46.51,22.82,52.21,46.34,2.09,8.65,6.43,56.21,4.73,62.71Z"></path><path class="cls-1" d="M246.17,191.82c-1.59,6.07-7.27,6.78-11.03-1.57-2.18-4.82-2.3-15.69-8.08-13.99-5.18,1.5-2.25,31.45-9.45,33.12-9,2.09-6.69-25.84-12.22-26.82-8.23-1.45-2.95,27.48-11.83,27.62-8.2.12-6.54-29.25-16.93-24.46-1.48.67-5.59,9.05-7.5,9.85-10.63,4.47-7.07-17.12-10.63-18.92-5.55-2.8-5.15,11.91-10.64,13.81-7.43,2.54-7.27-12.2-7.68-21.52-.94-21.92.48-48.22,14.57-66.26,7.58-9.69,22.02-19.12,34.48-19.91,26.2-1.67,46.51,22.82,52.21,46.34,2.09,8.65,6.43,56.21,4.73,62.71Z"></path><path class="cls-2" d="M213.32,155.66c-20.48-2.47-19.93-45.29-3.14-46.78,23.63-2.12,37.04,50.89,3.14,46.78Z"></path><path class="cls-2" d="M173.25,155.28c-33.65,7.43-24.63-43.9-3.13-46.4,22.3-2.6,20.84,42.48,3.13,46.4Z"></path></g></svg>
""".strip()

ghost_svg_b64 = base64.b64encode(GHOST_LOGO_SVG.encode("utf-8")).decode("utf-8")

st.markdown(
    """
    <style>
    /* 1. Ghost Foundation Centered Radial Gradient */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #1C1C1C 0%, #080808 55%, #000000 100%) !important;
        color: #FFFFFF !important;
        overflow: hidden !important;
        height: 100vh !important;
    }

    [data-testid="stMain"], [data-testid="stHeader"] {
        background-color: transparent !important;
        color: #FFFFFF !important;
        overflow: hidden !important;
    }

    /* Centered Ghost Foundation Logo Watermark in Main Viewport */
    [data-testid="stMain"]::before {
        content: "";
        position: fixed;
        top: 50%;
        left: calc(50% + 140px);
        transform: translate(-50%, -50%);
        width: 1800px;
        aspect-ratio: 977.95 / 396.85;
        background-image: url("data:image/svg+xml;base64,__GHOST_SVG__");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.045;
        pointer-events: none;
        z-index: 0;
    }

    /* 2. Force sidebar to stay visible, expanded, and styled in monochrome gradient */
    [data-testid="stSidebar"] {
        display: block !important;
        transform: none !important;
        visibility: visible !important;
        background: linear-gradient(180deg, #111111 0%, #000000 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.14) !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* 3. Hide sidebar collapse/expand buttons */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    /* 4. Monochrome form controls */
    input, [data-baseweb="select"] > div {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
    }

    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background-color: #FFFFFF !important;
    }

    input[type="radio"], input[type="checkbox"] {
        accent-color: #FFFFFF !important;
    }

    /* 5. Borderless Streamlit iframe container */
    iframe {
        border: none !important;
        background: transparent !important;
        position: relative;
        z-index: 1;
    }

    /* 6. Transparent Borderless Metric Cards */
    [data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 0.75rem 0rem !important;
        position: relative;
        z-index: 1;
    }
    [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {
        color: #FFFFFF !important;
    }

    /* 7. Remove top and bottom padding from main block */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """.replace("__GHOST_SVG__", ghost_svg_b64),
    unsafe_allow_html=True
)

# ==========================================
# BIOBUZZ 2026-2027 FIELD CONSTANTS (METERS)
# Origin (0.0, 0.0) = Exact Center of Field
# ==========================================
INCH_TO_M = 0.0254
FIELD_LEN = 144.0 * INCH_TO_M             # 3.6576 m (12 ft)
FIELD_HALF = 72.0 * INCH_TO_M             # 1.8288 m (6 ft)
FIELD_HALF_MM = round(FIELD_HALF * 1000.0, 1)  # 1828.8 mm
WALL_H = 12.0 * INCH_TO_M                 # 0.3048 m (12 in)
TILE_STEP = 24.0 * INCH_TO_M              # 0.6096 m (24 in)

# Center HIVE Structure — Turned 90 deg so the PENTAGONAL HOUSE OPENING faces outward (+/-X)!
HIVE_FRAME_X = 38.95 * INCH_TO_M          # 0.9893 m base frame width along X
HIVE_FRAME_Y = 49.46 * INCH_TO_M          # 1.2563 m base frame length along Y
HIVE_PIVOT_Y = 12.75 * INCH_TO_M          # +/- 0.3239 m lateral offset of Red & Blue seesaws
HIVE_AXLE_Z = 46.50 * INCH_TO_M           # 1.1811 m central A-frame pivot axle height
HIVE_TILT_RAD = math.radians(30.0)        # 30.0 deg seesaw beam tilt angle

HIVE_OUTER_W = 24.60 * INCH_TO_M          # 0.6248 m outer width along Y
HIVE_INNER_W = 21.25 * INCH_TO_M          # 0.5398 m inner clear width along Y

HIVE_U_IN = 4.5 * INCH_TO_M               # 0.1143 m inner back wall along seesaw beam
HIVE_U_OUT = 25.5 * INCH_TO_M             # 0.6477 m outer pentagonal opening along seesaw beam
HIVE_W_EAVE = 14.0 * INCH_TO_M            # 0.3556 m eave height above beam
HIVE_W_TOP = 22.0 * INCH_TO_M             # 0.5588 m roof peak height above beam

# Exact Raised ("Up") Pentagonal Entrance Plane Coordinates derived from HIVE_U_OUT & HIVE_TILT_RAD
HIVE_OPEN_LOW_X = HIVE_U_OUT * math.cos(HIVE_TILT_RAD)
HIVE_OPEN_LOW_Z = HIVE_AXLE_Z + HIVE_U_OUT * math.sin(HIVE_TILT_RAD)
HIVE_OPEN_HIGH_X = HIVE_U_OUT * math.cos(HIVE_TILT_RAD) - HIVE_W_TOP * math.sin(HIVE_TILT_RAD)
HIVE_OPEN_HIGH_Z = HIVE_AXLE_Z + HIVE_U_OUT * math.sin(HIVE_TILT_RAD) + HIVE_W_TOP * math.cos(HIVE_TILT_RAD)

# Perimeter FLOWERS (Manual Section 11.4.3 - Tile seams W6, F4, Y1, A2)
# Open-top horizontal hoop (11.1" OD, 9.5" ID, 2.5" rim depth) on a slim perimeter support post at 32.5" rim height
FLOWER_Z = 32.5 * INCH_TO_M               # 0.8255 m top rim height
FLOWER_OUTER_R = (11.1 * INCH_TO_M) / 2.0 # 0.1410 m outer radius
FLOWER_INNER_R = (9.5 * INCH_TO_M) / 2.0  # 0.1207 m inner clear opening radius
FLOWER_HOOP_H = 2.5 * INCH_TO_M           # 0.0635 m shallow open hoop collar depth
FLOWER_POST_R = 0.75 * INCH_TO_M          # 0.0191 m slim vertical support post radius

# LOADING / PARKING ZONES (23" x 11") & GARDENS (23" x 2") (Mirrored across X = 0 while keeping same Y sides)
LZ_DEPTH = 11.0 * INCH_TO_M               # 0.2794 m
LZ_WIDTH = 23.0 * INCH_TO_M               # 0.5842 m
GARDEN_DEPTH = 2.0 * INCH_TO_M            # 0.0508 m
GARDEN_WIDTH = 23.0 * INCH_TO_M           # 0.5842 m

# ==========================================
# 1. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.75rem;">
            <svg width="24" height="24" viewBox="55 65 265 270" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill="#FFFFFF" d="M314.44,187.52c0-.07-.01-.14-.03-.21-.46-2.68-2.01-5.27-4.23-6.67-.48-.32-.98-.55-1.47-.71-.21-.07-.43-.14-.63-.18-5.28-1.22-11.01,4.38-19.06,3.48-6.5-.73-11.37-5.35-15.19-10.22-1.52-1.92-2.88-3.89-4.1-5.67-.22-.32-.44-.63-.65-.96-.01-.02-.03-.03-.04-.06-5.64-8.56-7.01-15.31-9.28-24.86-.39-1.63-.81-3.36-1.28-5.18-.38-1.52-.81-3.12-1.3-4.79-4.14-14.55-7.75-27.19-15.51-37.92l-.2-.28c-1.4-1.92-2.94-3.77-4.63-5.56-2.14-2.27-18.97-19.46-44.4-19.46h-.37c-26.09.17-43.54,18.41-44.9,19.87-2.84,3.06-5.28,6.34-7.41,9.82h0c-14.58,23.78-14.33,55.74-23.98,75.42-.04.09-.09.19-.14.28-1.78,3.59-3.89,6.75-6.49,9.37-.79.8-1.64,1.61-2.58,2.39-.95.82-1.98,1.6-3.09,2.33-.22.15-.43.29-.64.42-.22.14-.44.28-.67.42-2.05,1.2-4.36,2.23-6.97,2.88-.17.04-.32.09-.48.12-1.65.4-3.16.39-4.57.18-4.79-.73-8.44-3.88-13.45-2.18-.1.03-.2.07-.31.11-.2.07-1.19.45-2.4,1.25-.01,0-.02.01-.03.02-1.65,1.07-3.71,2.88-4.79,5.63-.1.27-.21.54-.29.83-.03.09-.06.19-.08.28-.72,2.67-.47,5.78.62,8.15.63,1.4,1.55,2.53,2.73,3.17.1.06.18.09.27.13.53.24,1.04.34,1.54.37h.01c2.43.14,4.72-1.66,7.63-.21h.01c2.89,1.45,2.56,4.21,4.37,6.05.03.02.05.05.07.08.28.27.62.52,1.02.74.05.03.11.06.15.08,0,0,.01.01.03.01,1.33.68,2.63.61,3.95.26,2.8-.74,5.71-2.74,9.23-1.62.01,0,.02.01.02.01,1.78.58,3.33,1.84,4.56,3.45.02.02.02.03.03.04,1.79,2.33,2.88,5.38,2.95,8.13.03.91-.05,1.84-.23,2.74-.03.24-.08.49-.12.73-.13.58-.29,1.14-.47,1.71-.18.59-.4,1.15-.63,1.7-1.15,2.79-2.73,5.24-3.85,6.96-1.78,2.7-2.73,3.36-2.9,5.26-.31,3.34,2.07,7.28,5.17,8.87.75.39,1.55.64,2.36.71.84.07,1.67-.05,2.43-.24.12-.03.23-.06.36-.11.46-.14.9-.3,1.27-.46.18-.07.35-.16.52-.24.32-.15.56-.28.72-.37,1.72-.94,1.98-1.67,3.93-2.55.64-.29,2.19-.96,4.16-1.05,2.71-.12,4.76.97,5.79,1.53.09.05.17.1.26.16.03.01.06.03.09.04,4.61,2.68,6.62,7.62,7.82,10.66.14.36.31.8.48,1.31,0,.01.02.02.02.03.75,2.21,1.71,5.75,1.88,10.23.02.62.04,1.21.02,1.77-.05,6.47-1.83,9.37.42,13.32.19.32.5.85.95,1.42.08.12.19.23.29.35.7.81,1.69,1.62,2.99,1.96.05.02.12.04.18.05,2.43.53,4.63-.83,5.47-1.45.13-.09.22-.16.28-.2,3.22-2.55,2.77-6.18,3.59-11.12v-.03c.32-1.94.86-4.08,1.87-6.43.29-.67.77-1.77,1.39-2.97.03-.04.04-.06.05-.09,1.42-2.72,3.61-5.95,6.12-6.02,2.12-.05,4.14,2.17,5.9,5.25,3.45,5.98,5.96,15.19,6.47,17.07.42,1.52.81,3.13,1.2,4.8,2.52,10.81,4.66,24.08,8.97,31.85.01.03.01.04.03.05.16.29.33.57.49.84.89,1.45,2.26,3.31,4.24,3.84.17.06.35.1.53.12.29.05.58.05.86.03.08.02.16,0,.24,0,2.22-.25,4.12-2.04,5.13-3.07.1-.11.18-.2.26-.28,5.29-5.58,6.37-14.42,9.38-32.46.23-1.43.48-2.91.75-4.46,0,0,.84-4.95,6.29-17.3.14-.3.27-.6.41-.9.9-2.02,2.23-4.84,4.15-4.93.96-.05,2.48.57,4.55,4.49.01.01.01.02.02.04.13.24.26.49.39.76,3.41,6.93,4.14,14.33,4.73,20.6h0c.4,4.36.75,8.16,1.87,10.88.49,1.2,1.14,2.2,2.02,2.93.3.25.95.81,1.87,1.19.03.02.05.03.07.03.13.06.27.11.41.14.03.02.08.04.12.05.36.11.76.18,1.17.21h.01c.06.01.12.01.18.01h.25c2.06-.04,3.69-1.36,4.54-2.15.15-.14.28-.27.38-.36,4.34-4.27,3.22-15.73,4.31-25.41.59-5.37,1.87-10.2,5.15-12.94.15-.12.3-.24.45-.36,1.11-.81,2.99-1.82,4.91-2.09.99-.14,1.98-.07,2.86.32h.02s.03.02.05.03c2.47,1.12,2.21,3.88,5.49,6.74.01,0,.01.01.02.03.08.08.17.15.27.23.78.66,2.6,2.16,4.64,2.55.48.11.98.14,1.49.09.12-.02.23-.04.35-.06.03,0,.07,0,.09-.01,4.28-.87,6.67-7.52,7.24-9.27.04-.11.06-.19.09-.26,2.12-6.5-1.31-18.6-1.94-25.72-.04-.49-.08-1-.09-1.52-.01-.04-.01-.09-.01-.12-.11-2.37,0-4.96.36-7.49.84-6.21,3.13-12.11,7.26-13.87.05-.02.1-.03.14-.06,3.59-1.43,7.41.64,9.89-.6.01,0,.03-.02.05-.03.36-.19.69-.44.99-.79.17-.2.31-.4.4-.61.86-1.62.05-3.5,1.46-6.68.06-.14.13-.29.2-.44.32-.67,1.58-3.16,4.12-4.95.68-.49,1.32-.83,1.94-1.08,1.03-.4,1.99-.54,2.92-.62,1.88-.16,3.7-.11,5.91-1.53.03-.02.14-.08.28-.18t0-.02c.9-.64,3.59-2.84,4.43-6.25.13-.51.21-1.05.25-1.61.03-.63,0-1.26-.11-1.89ZM246.17,191.82c-1.59,6.07-7.27,6.78-11.03-1.57-2.18-4.82-2.3-15.69-8.08-13.99-5.18,1.5-2.25,31.45-9.45,33.12-9,2.09-6.69-25.84-12.22-26.82-8.23-1.45-2.95,27.48-11.83,27.62-8.2.12-6.54-29.25-16.93-24.46-1.48.67-5.59,9.05-7.5,9.85-10.63,4.47-7.07-17.12-10.63-18.92-5.55-2.8-5.15,11.91-10.64,13.81-7.43,2.54-7.27-12.2-7.68-21.52-.94-21.92.48-48.22,14.57-66.26,7.58-9.69,22.02-19.12,34.48-19.91,26.2-1.67,46.51,22.82,52.21,46.34,2.09,8.65,6.43,56.21,4.73,62.71Z"/>
                <path fill="#111111" d="M246.17,191.82c-1.59,6.07-7.27,6.78-11.03-1.57-2.18-4.82-2.3-15.69-8.08-13.99-5.18,1.5-2.25,31.45-9.45,33.12-9,2.09-6.69-25.84-12.22-26.82-8.23-1.45-2.95,27.48-11.83,27.62-8.2.12-6.54-29.25-16.93-24.46-1.48.67-5.59,9.05-7.5,9.85-10.63,4.47-7.07-17.12-10.63-18.92-5.55-2.8-5.15,11.91-10.64,13.81-7.43,2.54-7.27-12.2-7.68-21.52-.94-21.92.48-48.22,14.57-66.26,7.58-9.69,22.02-19.12,34.48-19.91,26.2-1.67,46.51,22.82,52.21,46.34,2.09,8.65,6.43,56.21,4.73,62.71Z"/>
                <path fill="#FFFFFF" d="M213.32,155.66c-20.48-2.47-19.93-45.29-3.14-46.78,23.63-2.12,37.04,50.89,3.14,46.78Z"/>
                <path fill="#FFFFFF" d="M173.25,155.28c-33.65,7.43-24.63-43.9-3.13-46.4,22.3-2.6,20.84,42.48,3.13,46.4Z"/>
            </svg>
            <span style="font-size: 1.35rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.01em;">
                Trajectory Settings
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    view_mode = st.radio(
        "Projection Mode",
        options=["2D View", "3D View"],
        index=1,
        horizontal=True
    )
    is_3d = view_mode == "3D View"

    with st.expander("Field", expanded=False):
        competition_mode = st.radio(
            "Competition",
            options=["FTC", "FRC"],
            index=0,
            horizontal=True
        )

        show_ftc_field = (competition_mode == "FTC")

        if competition_mode == "FTC":
            ftc_game = st.selectbox(
                "FTC Game",
                options=["None", "BIOBUZZ"],
                index=1
            )
            show_biobuzz_elements = (ftc_game == "BIOBUZZ")
        else:
            frc_game = st.selectbox(
                "FRC Game",
                options=["NONE"],
                index=0
            )
            show_biobuzz_elements = False

        if show_biobuzz_elements:
            # Gamepiece Selector (Pollen or Nectar — BIOBUZZ season specific)
            gamepiece = st.radio(
                "Gamepiece",
                options=["Pollen", "Nectar"],
                index=0,
                horizontal=True
            )

            if gamepiece == "Pollen":
                ball_diameter_inch, ball_mass_g = 2.8, 25
            else:
                ball_diameter_inch, ball_mass_g = 3.6, 41

            st.caption(f'Diameter: {ball_diameter_inch}" | Mass: {ball_mass_g} g')

            st.header("Target HIVE Seesaw")
            target_alliance = st.radio(
                "Alliance HIVE Seesaw",
                options=["Red HIVE (Y = -0.32m)", "Blue HIVE (Y = +0.32m)"],
                index=0,
                horizontal=True
            )
            raised_side = st.radio(
                "Raised ('Up') Cell Side",
                options=["Left (-X) Up", "Right (+X) Up"],
                index=0,
                horizontal=True
            )

            is_red_hive = "Red" in target_alliance
            is_left_up = "Left" in raised_side
            side_sign_x = -1.0 if is_left_up else 1.0
            side_sign_y = -1.0 if is_red_hive else 1.0

            def_gx1 = round(side_sign_x * HIVE_OPEN_LOW_X * 1000)
            def_gz1 = round(HIVE_OPEN_LOW_Z * 1000)
            def_gx2 = round(side_sign_x * HIVE_OPEN_HIGH_X * 1000)
            def_gz2 = round(HIVE_OPEN_HIGH_Z * 1000)
            def_gy = round(side_sign_y * HIVE_PIVOT_Y * 1000)
            def_gw = round(HIVE_INNER_W * 1000)

            target_start_x_mm, target_start_z_mm = def_gx1, def_gz1
            target_end_x_mm, target_end_z_mm = def_gx2, def_gz2
            target_center_y_mm = def_gy
            target_width_mm = def_gw
        else:
            # No BIOBUZZ gamepieces (Pollen/Nectar) when FTC -> None or FRC is selected
            st.caption("No game-specific pieces active for this selection.")
            ball_diameter_inch = st.number_input('Custom Ball Diameter [inch]', 1.0, 15.0, 5.0, 0.25)
            ball_mass_g = st.number_input('Custom Ball Mass [g]', 10.0, 1000.0, 150.0, 5.0)

            is_red_hive = True
            is_left_up = True
            side_sign_x = -1.0
            raised_side = "Custom Target"

            st.header("Custom Target Opening")
            target_start_x_mm = st.number_input('Target Bottom X [mm]', -5000.0, 5000.0, 0.0, 10.0)
            target_start_z_mm = st.number_input('Target Bottom Z [mm]', 100.0, 4000.0, 1200.0, 10.0)
            target_end_x_mm = st.number_input('Target Top X [mm]', -5000.0, 5000.0, 0.0, 10.0)
            target_end_z_mm = st.number_input('Target Top Z [mm]', 200.0, 4500.0, 1800.0, 10.0)
            target_center_y_mm = st.number_input('Target Center Y [mm]', -4000.0, 4000.0, 0.0, 10.0, disabled=not is_3d)
            target_width_mm = st.number_input('Target Width Y [mm]', 100.0, 3000.0, 600.0, 10.0, disabled=not is_3d)

    with st.expander("Launch Parameters", expanded=False):
        shooter_type = st.radio("Shooter Mechanism Type", options=["Single Flywheel", "Dual flywheel"], index=0)
        efficiency_loss = st.slider('Efficiency Loss [%]', 0.0, 50.0, 10.0, 0.5)
        pitch_deg = st.slider('Pitch Angle [deg]', 1.0, 90.0, 62.0, 0.5)
        wheel_Radius_inch = st.slider('Wheel Radius [inch]', 0.5, 6.0, 3.0, 0.1)

    with st.expander("Robot Dimensions & Shooter", expanded=False):
        robot_length_mm = st.number_input('Robot Length (Front–Back) [mm]', 100.0, 1500.0, 457.0, 5.0)
        robot_width_mm = st.number_input('Robot Width (Left–Right) [mm]', 100.0, 1500.0, 457.0, 5.0)
        height_mm = st.number_input('Launch Height Z [mm]', 0.0, 2000.0, 365.0, 5.0)

        half_len_mm = robot_length_mm / 2.0
        half_wid_mm = robot_width_mm / 2.0
        shooter_off_x_mm = st.number_input(
            'Shooter Offset X on Robot [mm]',
            -half_len_mm, half_len_mm, 0.0, 5.0
        )
        shooter_off_y_mm = st.number_input(
            'Shooter Offset Y on Robot [mm]',
            -half_wid_mm, half_wid_mm, 0.0, 5.0,
            disabled=not is_3d
        )

    # Enforce strict field perimeter containment for the entire robot footprint
    max_center_x_mm = max(0.0, FIELD_HALF_MM - half_len_mm)
    max_center_y_mm = max(0.0, FIELD_HALF_MM - half_wid_mm)

    with st.expander("Robot Location", expanded=False):
        st.header("Robot Center (Field Center = 0,0)")
        st.caption("Tip: Hold **Shift + Drag** in the plot to move the Robot.")
        robot_x_mm = st.number_input(
            'Robot X [mm]',
            -max_center_x_mm, max_center_x_mm,
            max(-max_center_x_mm, min(max_center_x_mm, -1200.0)),
            10.0
        )
        robot_y_mm = st.number_input(
            'Robot Lateral Y [mm]',
            -max_center_y_mm, max_center_y_mm,
            max(-max_center_y_mm, min(max_center_y_mm, -324.0)),
            10.0,
            disabled=not is_3d
        )

    with st.expander("Aerodynamics & Spin", expanded=False):
        use_drag = st.checkbox("Enable Air Resistance (Drag)", value=True)
        use_magnus = st.checkbox("Enable Spin Effect (Magnus)", value=True)
        spin_type = st.selectbox("Primary Spin Direction", ["Backspin", "Topspin"], disabled=not use_magnus)
        sidespin_deg = st.slider(
            "Spin Axis Roll / Sidespin [deg]",
            -45.0, 45.0, 0.0, 1.0,
            disabled=(not use_magnus or view_mode != "3D View")
        )


# ==========================================
# 2. UNIFIED 2D / 3D PHYSICS CALCULATIONS
# ==========================================
active_robot_y_mm = robot_y_mm if is_3d else 0.0
active_shooter_off_y_mm = shooter_off_y_mm if is_3d else 0.0
active_sidespin_deg = sidespin_deg if is_3d else 0.0
active_goal_center_y_mm = target_center_y_mm if is_3d else 0.0

robot_length_m = float(robot_length_mm) / 1000.0
robot_width_m = float(robot_width_mm) / 1000.0
half_robot_len_m = robot_length_m / 2.0
half_robot_wid_m = robot_width_m / 2.0

# Clamp robot center to field walls accounting for full robot dimensions
min_robot_x_m = -FIELD_HALF + half_robot_len_m
max_robot_x_m = FIELD_HALF - half_robot_len_m
min_robot_y_m = -FIELD_HALF + half_robot_wid_m
max_robot_y_m = FIELD_HALF - half_robot_wid_m

robot_x_m = max(min_robot_x_m, min(max_robot_x_m, float(robot_x_mm) / 1000.0))
robot_y_m = max(min_robot_y_m, min(max_robot_y_m, float(active_robot_y_mm) / 1000.0))
height_m = float(height_mm) / 1000.0

shooter_off_x_m = float(shooter_off_x_mm) / 1000.0
shooter_off_y_m = float(active_shooter_off_y_mm) / 1000.0

goal_x1 = target_start_x_mm / 1000.0
goal_z1 = target_start_z_mm / 1000.0
goal_x2 = target_end_x_mm / 1000.0
goal_z2 = target_end_z_mm / 1000.0
goal_y_center = active_goal_center_y_mm / 1000.0
goal_half_w = (target_width_mm / 1000.0) / 2.0
goal_y_min = goal_y_center - goal_half_w
goal_y_max = goal_y_center + goal_half_w

# World position of the shooter mounted on the robot chassis
goal_x_center = (goal_x1 + goal_x2) / 2.0
if is_3d:
    launcher_x_m = robot_x_m + shooter_off_x_m
    launcher_y_m = robot_y_m + shooter_off_y_m
    dx_goal = goal_x_center - launcher_x_m
    dy_goal = goal_y_center - launcher_y_m
    active_yaw_deg = math.degrees(math.atan2(dy_goal, dx_goal))
else:
    facing_2d = 1.0 if (goal_x_center - robot_x_m) >= 0.0 else -1.0
    launcher_x_m = robot_x_m + facing_2d * shooter_off_x_m
    launcher_y_m = 0.0
    dx_goal = goal_x_center - launcher_x_m
    active_yaw_deg = 0.0 if dx_goal >= 0.0 else 180.0

wheel_Radius_meter = wheel_Radius_inch * 0.0254
ball_mass_kg = float(ball_mass_g) / 1000.0
ball_radius_m = (ball_diameter_inch * 0.0254) / 2.0

spin_efficiency = 0.70
efficiency_multiplier = (100.0 - efficiency_loss) / 100.0
gravity = 9.81


def get_launch_params(rpm):
    wheel_surface_speed = rpm * (2 * math.pi / 60.0) * wheel_Radius_meter

    if shooter_type == "Single Flywheel":
        base_velocity_ms = wheel_surface_speed * 0.5
        raw_spin = rpm * (wheel_Radius_inch / ball_diameter_inch) * spin_efficiency
        spin_dir = 1.0 if spin_type == "Backspin" else -1.0
        spin_rpm = raw_spin * spin_dir
    else:
        base_velocity_ms = wheel_surface_speed
        spin_rpm = 0.0

    velocity_ms = base_velocity_ms * efficiency_multiplier
    return velocity_ms, spin_rpm


def check_goal_intersection(p1, p2):
    """Checks if the ball (with physical radius ball_radius_m) passes cleanly through the
    target entrance without hitting the bottom lip, side walls, or top rim."""
    (x1, y1, z1), (x2, y2, z2) = p1, p2

    # 1. Check if the ball's outer skin collides with the bottom floor lip or top roof peak
    for rx, rz in ((goal_x1, goal_z1), (goal_x2, goal_z2)):
        dx, dz = x2 - x1, z2 - z1
        seg_len_sq = dx * dx + dz * dz
        if seg_len_sq > 1e-12:
            proj = max(0.0, min(1.0, ((rx - x1) * dx + (rz - z1) * dz) / seg_len_sq))
            cx, cz = x1 + proj * dx, z1 + proj * dz
        else:
            cx, cz = x1, z1

        dist_xz = math.hypot(rx - cx, rz - cz)
        if dist_xz < ball_radius_m:
            iy_rim = y1 + (proj if seg_len_sq > 1e-12 else 0.0) * (y2 - y1)
            if not is_3d or (goal_y_min - ball_radius_m <= iy_rim <= goal_y_max + ball_radius_m):
                return "RIM_HIT", (cx, iy_rim, cz)

    # 2. Check crossing of the entrance plane
    goal_dx = goal_x2 - goal_x1
    goal_dz = goal_z2 - goal_z1
    goal_len = math.hypot(goal_dx, goal_dz)

    if goal_len <= 2.0 * ball_radius_m:
        return False, None
    if is_3d and (goal_y_max - goal_y_min) <= 2.0 * ball_radius_m:
        return False, None

    if show_biobuzz_elements:
        out_nx = side_sign_x * math.cos(HIVE_TILT_RAD)
        out_nz = math.sin(HIVE_TILT_RAD)
        if (x2 - x1) * out_nx + (z2 - z1) * out_nz >= 0.0:
            return False, None

    denom = (x1 - x2) * (goal_z1 - goal_z2) - (z1 - z2) * (goal_x1 - goal_x2)
    if abs(denom) < 1e-9:
        return False, None

    t = ((x1 - goal_x1) * (goal_z1 - goal_z2) - (z1 - goal_z1) * (goal_x1 - goal_x2)) / denom
    u = ((x1 - goal_x1) * (z1 - z2) - (z1 - goal_z1) * (x1 - x2)) / denom

    if 0.0 <= t <= 1.0:
        iy = y1 + t * (y2 - y1)
        if not is_3d:
            u_margin = ball_radius_m / goal_len
            if u_margin <= u <= 1.0 - u_margin:
                return True, (x1 + t * (x2 - x1), iy, z1 + t * (z2 - z1))
        else:
            lat_offset = abs(iy - goal_y_center)
            if lat_offset <= (goal_half_w - ball_radius_m):
                if show_biobuzz_elements:
                    w_hit = u * HIVE_W_TOP
                    roof_slope = (HIVE_W_TOP - HIVE_W_EAVE) / goal_half_w
                    roof_margin = ball_radius_m * math.hypot(1.0, roof_slope)
                    max_w_allowed = HIVE_W_TOP - roof_slope * lat_offset - roof_margin
                    if ball_radius_m <= w_hit <= max_w_allowed:
                        return True, (x1 + t * (x2 - x1), iy, z1 + t * (z2 - z1))
                else:
                    u_margin = ball_radius_m / goal_len
                    if u_margin <= u <= 1.0 - u_margin:
                        return True, (x1 + t * (x2 - x1), iy, z1 + t * (z2 - z1))

    return False, None


def check_hive_interior_collision(p1, p2):
    """After passing the entrance, checks when the ball's outer skin (ball_radius_m)
    hits the sloped bottom floor (w = 0), back wall (u = HIVE_U_IN), side walls, or roof."""
    if not show_biobuzz_elements:
        return False, None

    (x1, y1, z1), (x2, y2, z2) = p1, p2

    def world_to_local_uw(x, z):
        rx = side_sign_x * x
        dz = z - HIVE_AXLE_Z
        u = rx * math.cos(HIVE_TILT_RAD) + dz * math.sin(HIVE_TILT_RAD)
        w = -rx * math.sin(HIVE_TILT_RAD) + dz * math.cos(HIVE_TILT_RAD)
        return u, w

    u1, w1 = world_to_local_uw(x1, z1)
    u2, w2 = world_to_local_uw(x2, z2)

    if w1 > ball_radius_m and w2 <= ball_radius_m:
        frac = (w1 - ball_radius_m) / (w1 - w2)
        return True, (x1 + frac * (x2 - x1), y1 + frac * (y2 - y1), z1 + frac * (z2 - z1))

    back_limit = HIVE_U_IN + ball_radius_m
    if u1 > back_limit and u2 <= back_limit:
        frac = (u1 - back_limit) / (u1 - u2)
        return True, (x1 + frac * (x2 - x1), y1 + frac * (y2 - y1), z1 + frac * (z2 - z1))

    if is_3d:
        lat1 = abs(y1 - goal_y_center)
        lat2 = abs(y2 - goal_y_center)
        side_limit = goal_half_w - ball_radius_m
        if lat1 < side_limit and lat2 >= side_limit:
            frac = (side_limit - lat1) / (lat2 - lat1)
            return True, (x1 + frac * (x2 - x1), y1 + frac * (y2 - y1), z1 + frac * (z2 - z1))

        roof_slope = (HIVE_W_TOP - HIVE_W_EAVE) / goal_half_w
        roof_margin = ball_radius_m * math.hypot(1.0, roof_slope)
        max_w2 = HIVE_W_TOP - roof_slope * lat2 - roof_margin
        if w2 >= max_w2:
            return True, (x2, y2, z2)
    else:
        if w2 >= HIVE_W_TOP - ball_radius_m:
            return True, (x2, y2, z2)

    if u2 > HIVE_U_OUT + ball_radius_m:
        return True, (x2, y2, z2)

    return False, None


def compute_trajectory(u, pitch_deg, yaw_deg, start_pos, g=9.81, drag=True, magnus=True, spin_rpm=0.0, roll_deg=0.0):
    pitch = math.radians(pitch_deg)
    yaw = math.radians(yaw_deg)

    v_horiz = u * math.cos(pitch)
    vx = v_horiz * math.cos(yaw)
    vy = v_horiz * math.sin(yaw)
    vz = u * math.sin(pitch)

    cd, rho = 0.47, 1.225
    area = math.pi * (ball_radius_m ** 2)
    k_drag = (0.5 * rho * cd * area / ball_mass_kg) if drag else 0.0

    omega_mag = spin_rpm * (2.0 * math.pi / 60.0)
    abs_omega = abs(omega_mag)
    spin_sign = -1.0 if omega_mag > 0 else (1.0 if omega_mag < 0 else 0.0)

    roll = math.radians(roll_deg)
    lx, ly, lz = -math.sin(yaw), math.cos(yaw), 0.0
    ux = -math.sin(pitch) * math.cos(yaw)
    uy = -math.sin(pitch) * math.sin(yaw)
    uz = math.cos(pitch)

    sx = (lx * math.cos(roll) + ux * math.sin(roll)) * spin_sign
    sy = (ly * math.cos(roll) + uy * math.sin(roll)) * spin_sign
    sz = (lz * math.cos(roll) + uz * math.sin(roll)) * spin_sign

    dt = 0.002
    x, y, z = start_pos
    x_arr, y_arr, z_arr = [x], [y], [z]
    hit_target, impact_point = False, None
    entered_hive = False

    while z >= 0 and len(x_arr) < 3000:
        v = math.sqrt(vx * vx + vy * vy + vz * vz)
        if v < 1e-4:
            break

        ax_drag = -k_drag * v * vx
        ay_drag = -k_drag * v * vy
        az_drag = -k_drag * v * vz

        ax_mag, ay_mag, az_mag = 0.0, 0.0, 0.0
        if magnus and abs_omega > 1e-3:
            spin_ratio = (abs_omega * ball_radius_m) / v
            cl = min(0.5, spin_ratio)
            k_magnus = 0.5 * rho * cl * area / ball_mass_kg

            cx = sy * vz - sz * vy
            cy = sz * vx - sx * vz
            cz = sx * vy - sy * vx

            ax_mag = k_magnus * v * cx
            ay_mag = k_magnus * v * cy
            az_mag = k_magnus * v * cz

        ax = ax_drag + ax_mag
        ay = ay_drag + ay_mag
        az = -g + az_drag + az_mag

        vx += ax * dt
        vy += ay * dt
        vz += az * dt

        nx, ny, nz = x + vx * dt, y + vy * dt, z + vz * dt

        if not entered_hive:
            status, pt = check_goal_intersection((x, y, z), (nx, ny, nz))
            if status is True:
                hit_target = True
                impact_point = pt
                entered_hive = True
            elif status == "RIM_HIT":
                x_arr.append(pt[0])
                y_arr.append(pt[1])
                z_arr.append(pt[2])
                hit_target, impact_point = False, None
                break
        else:
            hit_floor, floor_pt = check_hive_interior_collision((x, y, z), (nx, ny, nz))
            if hit_floor:
                x_arr.append(floor_pt[0])
                y_arr.append(floor_pt[1])
                z_arr.append(floor_pt[2])
                break

        x, y, z = nx, ny, nz
        x_arr.append(x)
        y_arr.append(y)
        z_arr.append(z)

    return np.array(x_arr), np.array(y_arr), np.array(z_arr), hit_target, impact_point


# Sweep RPMs from 500 to 8000 in steps of 25; stop after 3 consecutive misses post-hit
scoring_trajectories = []
consecutive_misses = 0

for rpm in range(500, 8001, 25):
    vel_ms, s_rpm = get_launch_params(rpm)
    x_arr, y_arr, z_arr, hit_target, impact_point = compute_trajectory(
        vel_ms, pitch_deg, active_yaw_deg, (launcher_x_m, launcher_y_m, height_m),
        gravity, use_drag, use_magnus, s_rpm, active_sidespin_deg
    )
    if hit_target:
        scoring_trajectories.append((rpm, vel_ms, x_arr, y_arr, z_arr, impact_point))
        consecutive_misses = 0
    elif scoring_trajectories:
        consecutive_misses += 1
        if consecutive_misses >= 3:
            break

# ==========================================
# 3. BUILD 2D OR 3D PLOTLY GRAPH + JS ANIMATOR
# ==========================================
st.subheader("Shot Calculator Trajectory")

fig_traj = go.Figure()
anim_points = []


def add_cylinder_mesh_3d(fig, cx, cy, z_bottom, z_top, radius, color, opacity=0.85, name="Cylinder"):
    """Adds a closed vertical 3D cylinder mesh between z_bottom and z_top."""
    n_seg = 24
    theta = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False)
    xs_ring = cx + radius * np.cos(theta)
    ys_ring = cy + radius * np.sin(theta)

    vx = np.concatenate([xs_ring, xs_ring, [cx, cx]]).tolist()
    vy = np.concatenate([ys_ring, ys_ring, [cy, cy]]).tolist()
    vz = np.concatenate([
        np.full(n_seg, z_bottom),
        np.full(n_seg, z_top),
        [z_bottom, z_top]
    ]).tolist()

    i_idx, j_idx, k_idx = [], [], []
    idx_bot_c = 2 * n_seg
    idx_top_c = 2 * n_seg + 1

    for s in range(n_seg):
        s_next = (s + 1) % n_seg
        b0, b1 = s, s_next
        t0, t1 = n_seg + s, n_seg + s_next

        i_idx.extend([b0, b1])
        j_idx.extend([b1, t1])
        k_idx.extend([t0, t0])

        i_idx.extend([idx_bot_c, idx_top_c])
        j_idx.extend([b1, t0])
        k_idx.extend([b0, t1])

    fig.add_trace(go.Mesh3d(
        x=vx,
        y=vy,
        z=vz,
        i=i_idx,
        j=j_idx,
        k=k_idx,
        color=color,
        opacity=opacity,
        flatshading=False,
        lighting=dict(ambient=0.75, diffuse=0.85, specular=0.25),
        name=name,
        showlegend=False,
        hoverinfo="skip"
    ))


def add_hollow_hoop_mesh_3d(fig, cx, cy, z_bottom, z_top, r_inner, r_outer, color, opacity=0.88, name="FLOWER Hoop"):
    """Adds an open-top hollow cylindrical hoop (ring wall + top/bottom rims) matching the BIOBUZZ FLOWER basket."""
    n_seg = 32
    theta = np.linspace(0.0, 2.0 * np.pi, n_seg, endpoint=False)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)

    vx = np.concatenate([
        cx + r_outer * cos_t,
        cx + r_outer * cos_t,
        cx + r_inner * cos_t,
        cx + r_inner * cos_t
    ]).tolist()
    vy = np.concatenate([
        cy + r_outer * sin_t,
        cy + r_outer * sin_t,
        cy + r_inner * sin_t,
        cy + r_inner * sin_t
    ]).tolist()
    vz = np.concatenate([
        np.full(n_seg, z_bottom),
        np.full(n_seg, z_top),
        np.full(n_seg, z_bottom),
        np.full(n_seg, z_top)
    ]).tolist()

    i_idx, j_idx, k_idx = [], [], []
    for s in range(n_seg):
        sn = (s + 1) % n_seg
        ob0, ob1 = s, sn
        ot0, ot1 = n_seg + s, n_seg + sn
        ib0, ib1 = 2 * n_seg + s, 2 * n_seg + sn
        it0, it1 = 3 * n_seg + s, 3 * n_seg + sn

        i_idx.extend([ob0, ob1])
        j_idx.extend([ob1, ot1])
        k_idx.extend([ot0, ot0])

        i_idx.extend([ib0, ib1])
        j_idx.extend([it0, ib0])
        k_idx.extend([it1, it1])

        i_idx.extend([ot0, ot1])
        j_idx.extend([ot1, it1])
        k_idx.extend([it0, it0])

        i_idx.extend([ob0, ob1])
        j_idx.extend([ib0, ob0])
        k_idx.extend([ib1, ib1])

    fig.add_trace(go.Mesh3d(
        x=vx,
        y=vy,
        z=vz,
        i=i_idx,
        j=j_idx,
        k=k_idx,
        color=color,
        opacity=opacity,
        flatshading=False,
        lighting=dict(ambient=0.8, diffuse=0.85, specular=0.3),
        name=name,
        showlegend=False,
        hoverinfo="skip"
    ))


def get_rounded_rect_xy(rx, ry, half_len, half_wid, corner_r, n_arc=6):
    """Returns perimeter (x, y) points for a rectangle with rounded corners."""
    r = max(0.0, min(corner_r, half_len * 0.45, half_wid * 0.45))
    if r <= 1e-5:
        return [
            (rx - half_len, ry - half_wid),
            (rx + half_len, ry - half_wid),
            (rx + half_len, ry + half_wid),
            (rx - half_len, ry + half_wid),
        ]

    # Corner centers and start/end angles (CCW)
    arcs = [
        (rx + half_len - r, ry - half_wid + r, -0.5 * math.pi, 0.0),
        (rx + half_len - r, ry + half_wid - r, 0.0, 0.5 * math.pi),
        (rx - half_len + r, ry + half_wid - r, 0.5 * math.pi, math.pi),
        (rx - half_len + r, ry - half_wid + r, math.pi, 1.5 * math.pi),
    ]
    pts = []
    for cx, cy, a0, a1 in arcs:
        for a in np.linspace(a0, a1, n_arc):
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def add_rounded_box_mesh_3d(fig, rx, ry, half_len, half_wid, z_min, z_max, corner_r=0.03, color="#FFFFFF", opacity=0.93, name="Box", showlegend=False):
    """Adds a solid 3D extruded prism with slightly rounded vertical corners."""
    ring = get_rounded_rect_xy(rx, ry, half_len, half_wid, corner_r, n_arc=6)
    n = len(ring)

    vx = [p[0] for p in ring] + [p[0] for p in ring] + [rx, rx]
    vy = [p[1] for p in ring] + [p[1] for p in ring] + [ry, ry]
    vz = [z_min] * n + [z_max] * n + [z_min, z_max]

    idx_bot_c = 2 * n
    idx_top_c = 2 * n + 1
    i_idx, j_idx, k_idx = [], [], []

    for s in range(n):
        sn = (s + 1) % n
        b0, b1 = s, sn
        t0, t1 = n + s, n + sn

        # Side quad
        i_idx.extend([b0, b1])
        j_idx.extend([b1, t1])
        k_idx.extend([t0, t0])

        # Bottom & top caps
        i_idx.extend([idx_bot_c, idx_top_c])
        j_idx.extend([b1, t0])
        k_idx.extend([b0, t1])

    fig.add_trace(go.Mesh3d(
        x=vx,
        y=vy,
        z=vz,
        i=i_idx,
        j=j_idx,
        k=k_idx,
        color=color,
        opacity=opacity,
        flatshading=False,
        lighting=dict(ambient=0.85, diffuse=0.85, specular=0.2),
        name=name,
        showlegend=showlegend,
        hoverinfo="skip"
    ))
    return ring


def add_robot_model_3d(fig, rx, ry, lx_world, ly_world, lz, half_len, half_wid, yaw_deg, pitch_deg):
    """Adds a white 3D FTC robot chassis (opacity=0.93) with rounded corners, cylindrical turret, and dotted light-grey launch angle line."""
    z_floor = 0.005
    z_bump = 0.12
    z_deck = 0.18
    robot_opacity = 0.93
    corner_r = min(0.035, half_len * 0.22, half_wid * 0.22)
    yaw_rad = math.radians(yaw_deg)
    pitch_rad = math.radians(pitch_deg)
    cos_y, sin_y = math.cos(yaw_rad), math.sin(yaw_rad)

    robot_label = f"Robot ({int(round(half_len * 2000))}×{int(round(half_wid * 2000))} mm)"

    # White chassis body with rounded corners
    ring = add_rounded_box_mesh_3d(
        fig,
        rx, ry, half_len, half_wid,
        z_floor, z_bump,
        corner_r=corner_r,
        color="#FFFFFF",
        opacity=robot_opacity,
        name=robot_label,
        showlegend=False
    )

    # Cylindrical turret housing
    turret_r = min(0.085, half_len * 0.45, half_wid * 0.45)
    turret_z_top = max(z_deck, lz - 0.02)
    add_cylinder_mesh_3d(
        fig,
        lx_world, ly_world,
        z_bump, turret_z_top,
        turret_r,
        color="#FFFFFF",
        opacity=robot_opacity,
        name=robot_label
    )

    # Subtle rounded perimeter outline + turret top ring for crisp edge definition
    closed_ring = ring + [ring[0]]
    px, py, pz = [], [], []
    for z_ring in (z_floor, z_bump):
        px.extend([c[0] for c in closed_ring] + [None])
        py.extend([c[1] for c in closed_ring] + [None])
        pz.extend([z_ring] * len(closed_ring) + [None])

    t_theta = np.linspace(0.0, 2.0 * np.pi, 25)
    px.extend((lx_world + turret_r * np.cos(t_theta)).tolist() + [None])
    py.extend((ly_world + turret_r * np.sin(t_theta)).tolist() + [None])
    pz.extend(np.full_like(t_theta, turret_z_top).tolist() + [None])

    fig.add_trace(go.Scatter3d(
        x=px,
        y=py,
        z=pz,
        mode="lines",
        name=robot_label,
        legendgroup="robot_solid_3d",
        showlegend=False,
        line=dict(color="rgba(24, 24, 27, 0.7)", width=2),
        hoverinfo="skip"
    ))

    # Vertical shooter mast from cylindrical turret to launch point
    fig.add_trace(go.Scatter3d(
        x=[lx_world, lx_world],
        y=[ly_world, ly_world],
        z=[turret_z_top, lz],
        mode="lines",
        name=robot_label,
        legendgroup="robot_solid_3d",
        showlegend=True,
        line=dict(color="rgba(255, 255, 255, 0.93)", width=5),
        hoverinfo="skip"
    ))

    # Dotted light-grey launch angle line
    barrel_len = 0.34
    bx_tip = lx_world + barrel_len * math.cos(pitch_rad) * cos_y
    by_tip = ly_world + barrel_len * math.cos(pitch_rad) * sin_y
    bz_tip = lz + barrel_len * math.sin(pitch_rad)

    fig.add_trace(go.Scatter3d(
        x=[lx_world, bx_tip],
        y=[ly_world, by_tip],
        z=[lz, bz_tip],
        mode="lines",
        name=f"{robot_label} Launch Angle",
        legendgroup="robot_solid_3d",
        showlegend=False,
        line=dict(color="#9CA3AF", width=3.5, dash="dot"),
        hoverinfo="skip"
    ))


def add_robot_model_2d(fig, rx, lx_world, lz, half_len, yaw_deg, pitch_deg):
    """Adds a white 2D side-profile robot chassis (opacity=0.93) with rounded top corners, cylindrical turret profile, and a dotted light-grey launch angle line."""
    facing = 1.0 if math.cos(math.radians(yaw_deg)) >= 0 else -1.0
    pitch_rad = math.radians(pitch_deg)

    barrel_len = 0.34
    bx_tip = lx_world + facing * barrel_len * math.cos(pitch_rad)
    bz_tip = lz + barrel_len * math.sin(pitch_rad)
    robot_label = f"Robot ({int(round(half_len * 2000))} mm L)"

    # White chassis with slightly rounded upper corners
    chassis_h = 0.13
    r_c = min(0.025, half_len * 0.2, chassis_h * 0.35)
    tr_ang = np.linspace(0.0, 0.5 * math.pi, 6)
    tl_ang = np.linspace(0.5 * math.pi, math.pi, 6)

    cx_pts = (
        [rx - half_len, rx + half_len]
        + (rx + half_len - r_c + r_c * np.cos(tr_ang)).tolist()
        + (rx - half_len + r_c + r_c * np.cos(tl_ang)).tolist()
        + [rx - half_len]
    )
    cz_pts = (
        [0.0, 0.0]
        + (chassis_h - r_c + r_c * np.sin(tr_ang)).tolist()
        + (chassis_h - r_c + r_c * np.sin(tl_ang)).tolist()
        + [0.0]
    )

    fig.add_trace(go.Scatter(
        x=cx_pts,
        y=cz_pts,
        mode="lines",
        fill="toself",
        fillcolor="rgba(255, 255, 255, 0.93)",
        name=robot_label,
        legendgroup="robot_solid_2d",
        showlegend=True,
        line=dict(color="rgba(255, 255, 255, 0.95)", width=2),
        hoverinfo="skip"
    ))

    # Cylindrical turret side profile + vertical mast
    turret_r = min(0.075, half_len * 0.4)
    turret_top = max(0.18, lz - 0.02)
    fig.add_trace(go.Scatter(
        x=[lx_world - turret_r, lx_world + turret_r, lx_world + turret_r, lx_world - turret_r, lx_world - turret_r],
        y=[chassis_h, chassis_h, turret_top, turret_top, chassis_h],
        mode="lines",
        fill="toself",
        fillcolor="rgba(255, 255, 255, 0.93)",
        name=robot_label,
        legendgroup="robot_solid_2d",
        showlegend=False,
        line=dict(color="rgba(255, 255, 255, 0.95)", width=1.5),
        hoverinfo="skip"
    ))

    # Dotted light-grey launch angle line
    fig.add_trace(go.Scatter(
        x=[lx_world, bx_tip],
        y=[lz, bz_tip],
        mode="lines",
        name=f"{robot_label} Launch Angle",
        legendgroup="robot_solid_2d",
        showlegend=False,
        line=dict(color="#9CA3AF", width=3, dash="dot"),
        hoverinfo="skip"
    ))


def add_biobuzz_field_elements(fig, red_selected, left_up):
    """Adds 2026-2027 BIOBUZZ game elements (all hidden from legend for a clean HUD)."""
    bx = HIVE_FRAME_X / 2.0
    by = HIVE_FRAME_Y / 2.0

    frame_x = [
        -bx, bx, bx, -bx, -bx, None,
        -bx, 0.0, bx, None,
        -bx, 0.0, bx, None,
        0.0, 0.0
    ]
    frame_y = [
        -by, -by, by, by, -by, None,
        -by, -by, -by, None,
        by, by, by, None,
        -by, by
    ]
    frame_z = [
        0.004, 0.004, 0.004, 0.004, 0.004, None,
        0.004, HIVE_AXLE_Z, 0.004, None,
        0.004, HIVE_AXLE_Z, 0.004, None,
        HIVE_AXLE_Z, HIVE_AXLE_Z
    ]
    fig.add_trace(go.Scatter3d(
        x=frame_x,
        y=frame_y,
        z=frame_z,
        mode="lines",
        name="HIVE A-Frame",
        showlegend=False,
        line=dict(color="rgba(255, 255, 255, 0.55)", width=4),
        hoverinfo="skip"
    ))

    # Red & Blue seesaws tilt in opposite directions (Red up on one side, Blue up on the opposite side)
    red_left_up = left_up if red_selected else (not left_up)
    blue_left_up = (not left_up) if red_selected else left_up

    seesaws = [
        (-1.0, "Red HIVE", "#EF4444", red_selected, red_left_up),
        (1.0, "Blue HIVE", "#3B82F6", not red_selected, blue_left_up)
    ]

    hw = HIVE_OUTER_W / 2.0
    hw_in = HIVE_INNER_W / 2.0

    def beam_to_world(u_local, y_val, w_local, cell_side, is_up):
        alpha = HIVE_TILT_RAD if is_up else -HIVE_TILT_RAD
        r_x = u_local * math.cos(alpha) - w_local * math.sin(alpha)
        z_w = HIVE_AXLE_Z + u_local * math.sin(alpha) + w_local * math.cos(alpha)
        return cell_side * r_x, y_val, z_w

    for y_sign, base_label, color_hex, is_alliance_target, seesaw_left_up in seesaws:
        yc = y_sign * HIVE_PIVOT_Y
        rx, ry, rz = [], [], []

        pent_yw = [
            (yc - hw, 0.0),
            (yc + hw, 0.0),
            (yc + hw, HIVE_W_EAVE),
            (yc, HIVE_W_TOP),
            (yc - hw, HIVE_W_EAVE),
            (yc - hw, 0.0),
        ]

        for cell_side in (-1.0, 1.0):
            is_up = (cell_side < 0 and seesaw_left_up) or (cell_side > 0 and not seesaw_left_up)

            p_piv = (0.0, yc, HIVE_AXLE_Z)
            p_arm_end = beam_to_world(HIVE_U_OUT, yc, 0.0, cell_side, is_up)
            rx.extend([p_piv[0], p_arm_end[0], None])
            ry.extend([p_piv[1], p_arm_end[1], None])
            rz.extend([p_piv[2], p_arm_end[2], None])

            rear_pent = [beam_to_world(HIVE_U_IN, y_v, w_v, cell_side, is_up) for (y_v, w_v) in pent_yw]
            front_pent = [beam_to_world(HIVE_U_OUT, y_v, w_v, cell_side, is_up) for (y_v, w_v) in pent_yw]

            for pent_loop in (rear_pent, front_pent):
                rx.extend([p[0] for p in pent_loop] + [None])
                ry.extend([p[1] for p in pent_loop] + [None])
                rz.extend([p[2] for p in pent_loop] + [None])

            for idx_v in range(5):
                rp = rear_pent[idx_v]
                fp = front_pent[idx_v]
                rx.extend([rp[0], fp[0], None])
                ry.extend([rp[1], fp[1], None])
                rz.extend([rp[2], fp[2], None])

            if is_up:
                in_pent_yw = [
                    (yc - hw_in, 0.0),
                    (yc + hw_in, 0.0),
                    (yc + hw_in, HIVE_W_EAVE),
                    (yc, HIVE_W_TOP),
                    (yc - hw_in, HIVE_W_EAVE),
                ]
                mouth_pts = [beam_to_world(HIVE_U_OUT, y_v, w_v, cell_side, True) for (y_v, w_v) in in_pent_yw]
                fig.add_trace(go.Mesh3d(
                    x=[p[0] for p in mouth_pts],
                    y=[p[1] for p in mouth_pts],
                    z=[p[2] for p in mouth_pts],
                    i=[0, 0, 0],
                    j=[1, 2, 3],
                    k=[2, 3, 4],
                    color=color_hex,
                    opacity=0.28 if is_alliance_target else 0.14,
                    name=f"{base_label} Pentagonal Entrance",
                    showlegend=False,
                    hoverinfo="skip"
                ))

        label = f"{base_label} Seesaw (Target)" if is_alliance_target else f"{base_label} Seesaw"
        fig.add_trace(go.Scatter3d(
            x=rx,
            y=ry,
            z=rz,
            mode="lines",
            name=label,
            showlegend=False,
            line=dict(color=color_hex, width=5 if is_alliance_target else 3.5),
            hovertemplate=f"{label}: (%{{x:.2f}}, %{{y:.2f}}, %{{z:.2f}} m)<extra></extra>"
        ))

    # 4 Perimeter FLOWERS (Manual Section 11.4.3): Completely green (#22C55E)
    flower_green = "#22C55E"
    flower_theta = np.linspace(0, 2 * np.pi, 36)
    flowers_spec = [
        (-TILE_STEP, FIELD_HALF - FLOWER_OUTER_R, -TILE_STEP, FIELD_HALF - FLOWER_POST_R, FLOWER_Z),
        (FIELD_HALF - FLOWER_OUTER_R, TILE_STEP, FIELD_HALF - FLOWER_POST_R, TILE_STEP, FLOWER_Z),
        (TILE_STEP, -FIELD_HALF + FLOWER_OUTER_R, TILE_STEP, -FIELD_HALF + FLOWER_POST_R, FLOWER_Z),
        (-FIELD_HALF + FLOWER_OUTER_R, -TILE_STEP, -FIELD_HALF + FLOWER_POST_R, -TILE_STEP, FLOWER_Z),
    ]

    fl_x, fl_y, fl_z = [], [], []
    hoop_bottom_z = FLOWER_Z - FLOWER_HOOP_H
    for cx, cy, px, py, cz in flowers_spec:
        add_cylinder_mesh_3d(
            fig, px, py, 0.0, cz, FLOWER_POST_R,
            color=flower_green, opacity=0.90, name="FLOWER Support Mast"
        )
        add_hollow_hoop_mesh_3d(
            fig, cx, cy, hoop_bottom_z, cz, FLOWER_INNER_R, FLOWER_OUTER_R,
            color=flower_green, opacity=0.90, name="FLOWER Hoop"
        )

        out_x = cx + FLOWER_OUTER_R * np.cos(flower_theta)
        out_y = cy + FLOWER_OUTER_R * np.sin(flower_theta)
        in_x = cx + FLOWER_INNER_R * np.cos(flower_theta)
        in_y = cy + FLOWER_INNER_R * np.sin(flower_theta)

        fl_x.extend(out_x.tolist() + [None] + in_x.tolist() + [None])
        fl_y.extend(out_y.tolist() + [None] + in_y.tolist() + [None])
        fl_z.extend(np.full_like(flower_theta, cz).tolist() + [None] + np.full_like(flower_theta, cz).tolist() + [None])

    fig.add_trace(go.Scatter3d(
        x=fl_x,
        y=fl_y,
        z=fl_z,
        mode="lines",
        name='4 FLOWERS (32.5" H)',
        showlegend=False,
        line=dict(color=flower_green, width=3),
        hovertemplate="FLOWER Rim (32.5\" H): (%{x:.2f}, %{y:.2f}, %{z:.2f} m)<extra></extra>"
    ))

    # Red Parking / Robot Pre-load Zone (along -Y wall, X in [-TILE_STEP - LZ_WIDTH, -TILE_STEP])
    red_lz_x_right = -TILE_STEP
    red_lz_x_left = red_lz_x_right - LZ_WIDTH
    fig.add_trace(go.Scatter3d(
        x=[red_lz_x_left, red_lz_x_right, red_lz_x_right, red_lz_x_left, red_lz_x_left],
        y=[-FIELD_HALF, -FIELD_HALF, -FIELD_HALF + LZ_DEPTH, -FIELD_HALF + LZ_DEPTH, -FIELD_HALF],
        z=[0.003] * 5,
        mode="lines",
        name="Red Loading / Parking Zone",
        showlegend=False,
        line=dict(color="#EF4444", width=3.5),
        hoverinfo="skip"
    ))

    # Blue Parking / Robot Pre-load Zone (along +Y wall, X in [TILE_STEP, TILE_STEP + LZ_WIDTH])
    blue_lz_x_left = TILE_STEP
    blue_lz_x_right = blue_lz_x_left + LZ_WIDTH
    fig.add_trace(go.Scatter3d(
        x=[blue_lz_x_left, blue_lz_x_right, blue_lz_x_right, blue_lz_x_left, blue_lz_x_left],
        y=[FIELD_HALF - LZ_DEPTH, FIELD_HALF - LZ_DEPTH, FIELD_HALF, FIELD_HALF, FIELD_HALF - LZ_DEPTH],
        z=[0.003] * 5,
        mode="lines",
        name="Blue Loading / Parking Zone",
        showlegend=False,
        line=dict(color="#3B82F6", width=3.5),
        hoverinfo="skip"
    ))

    # Red GARDEN (along +X wall at bottom-right corner +X = +FIELD_HALF, -Y = -FIELD_HALF)
    fig.add_trace(go.Scatter3d(
        x=[FIELD_HALF - GARDEN_DEPTH, FIELD_HALF, FIELD_HALF, FIELD_HALF - GARDEN_DEPTH, FIELD_HALF - GARDEN_DEPTH],
        y=[-FIELD_HALF, -FIELD_HALF, -FIELD_HALF + GARDEN_WIDTH, -FIELD_HALF + GARDEN_WIDTH, -FIELD_HALF],
        z=[0.003] * 5,
        mode="lines",
        name="Red GARDEN",
        showlegend=False,
        line=dict(color="#EF4444", width=3.5, dash="dot"),
        hoverinfo="skip"
    ))

    # Blue GARDEN (along -X wall at top-left corner -X = -FIELD_HALF, +Y = +FIELD_HALF)
    fig.add_trace(go.Scatter3d(
        x=[-FIELD_HALF, -FIELD_HALF + GARDEN_DEPTH, -FIELD_HALF + GARDEN_DEPTH, -FIELD_HALF, -FIELD_HALF],
        y=[FIELD_HALF - GARDEN_WIDTH, FIELD_HALF - GARDEN_WIDTH, FIELD_HALF, FIELD_HALF, FIELD_HALF - GARDEN_WIDTH],
        z=[0.003] * 5,
        mode="lines",
        name="Blue GARDEN",
        showlegend=False,
        line=dict(color="#3B82F6", width=3.5, dash="dot"),
        hoverinfo="skip"
    ))


def add_biobuzz_field_elements_2d(fig, red_selected, left_up):
    """Adds the 2D X-Z side-profile geometry of the BIOBUZZ HIVE A-frame and active seesaw cell in grey."""
    bx = HIVE_FRAME_X / 2.0
    hive_color = "#8E8E93"
    hive_fill = "rgba(142, 142, 147, 0.14)"
    hive_label = "Red HIVE" if red_selected else "Blue HIVE"

    fig.add_trace(go.Scatter(
        x=[-bx, 0.0, bx, -bx],
        y=[0.0, HIVE_AXLE_Z, 0.0, 0.0],
        mode="lines",
        name="HIVE A-Frame",
        showlegend=False,
        line=dict(color="rgba(255, 255, 255, 0.40)", width=3),
        hoverinfo="skip"
    ))

    def beam_to_xz(u_local, w_local, cell_side, is_up):
        alpha = HIVE_TILT_RAD if is_up else -HIVE_TILT_RAD
        r_x = u_local * math.cos(alpha) - w_local * math.sin(alpha)
        z_w = HIVE_AXLE_Z + u_local * math.sin(alpha) + w_local * math.cos(alpha)
        return cell_side * r_x, z_w

    cell_side = -1.0 if left_up else 1.0
    p_piv = (0.0, HIVE_AXLE_Z)
    p_floor_in = beam_to_xz(HIVE_U_IN, 0.0, cell_side, True)
    p_floor_out = beam_to_xz(HIVE_U_OUT, 0.0, cell_side, True)
    p_eave_out = beam_to_xz(HIVE_U_OUT, HIVE_W_EAVE, cell_side, True)
    p_roof_out = beam_to_xz(HIVE_U_OUT, HIVE_W_TOP, cell_side, True)
    p_roof_in = beam_to_xz(HIVE_U_IN, HIVE_W_TOP, cell_side, True)
    p_eave_in = beam_to_xz(HIVE_U_IN, HIVE_W_EAVE, cell_side, True)

    fig.add_trace(go.Scatter(
        x=[p_piv[0], p_floor_out[0]],
        y=[p_piv[1], p_floor_out[1]],
        mode="lines",
        name=f"{hive_label} Seesaw",
        legendgroup="hive_2d_body",
        showlegend=False,
        line=dict(color=hive_color, width=4),
        hoverinfo="skip"
    ))

    wall_pts = [p_floor_out, p_floor_in, p_roof_in, p_roof_out]
    fig.add_trace(go.Scatter(
        x=[p[0] for p in wall_pts],
        y=[p[1] for p in wall_pts],
        mode="lines",
        fill="toself",
        fillcolor=hive_fill,
        name=f"{hive_label} Cell",
        legendgroup="hive_2d_body",
        showlegend=False,
        line=dict(color=hive_color, width=3.5),
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[p_eave_in[0], p_eave_out[0]],
        y=[p_eave_in[1], p_eave_out[1]],
        mode="lines",
        legendgroup="hive_2d_body",
        showlegend=False,
        line=dict(color=hive_color, width=1.5, dash="dot"),
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=[0.0],
        y=[HIVE_AXLE_Z],
        mode="markers",
        name="HIVE Pivot Axle",
        showlegend=False,
        marker=dict(size=8, color="#FFFFFF", line=dict(color="#000000", width=1.5)),
        hovertemplate=f"HIVE Pivot Axle: (0.00 m, {HIVE_AXLE_Z:.2f} m)<extra></extra>"
    ))


if is_3d:
    # ---------- 3D VIEW RENDERING ----------
    u_sph = np.linspace(0, 2 * np.pi, 16)
    v_sph = np.linspace(0, np.pi, 12)
    uu, vv = np.meshgrid(u_sph, v_sph)
    unit_x = (np.cos(uu) * np.sin(vv)).ravel()
    unit_y = (np.sin(uu) * np.sin(vv)).ravel()
    unit_z = np.cos(vv).ravel()

    rows, cols = uu.shape
    tri_i, tri_j, tri_k = [], [], []
    for r in range(rows - 1):
        for c in range(cols - 1):
            p0 = r * cols + c
            p1 = p0 + 1
            p2 = (r + 1) * cols + c
            p3 = p2 + 1
            tri_i.extend([p0, p1])
            tri_j.extend([p2, p2])
            tri_k.extend([p1, p3])

    def make_3d_ball(cx, cy, cz, r):
        return (
            (cx + r * unit_x).tolist(),
            (cy + r * unit_y).tolist(),
            (cz + r * unit_z).tolist(),
        )

    if scoring_trajectories:
        center_u = 0.42
        target_cx = goal_x1 + center_u * (goal_x2 - goal_x1)
        target_cy = goal_y_center
        target_cz = goal_z1 + center_u * (goal_z2 - goal_z1)
        mid_idx = min(
            range(len(scoring_trajectories)),
            key=lambda i: math.dist(scoring_trajectories[i][5], (target_cx, target_cy, target_cz))
        )
        mid_rpm, mid_vel, mid_x, mid_y, mid_z, _ = scoring_trajectories[mid_idx]

        bx0, by0, bz0 = make_3d_ball(mid_x[0], mid_y[0], mid_z[0], ball_radius_m)

        # Trace 0: Physically-scaled Yellow 3D Sphere (must stay at index 0 for animation)
        fig_traj.add_trace(go.Mesh3d(
            x=bx0,
            y=by0,
            z=bz0,
            i=tri_i,
            j=tri_j,
            k=tri_k,
            color='#FACC15',
            opacity=1.0,
            flatshading=False,
            lighting=dict(ambient=0.7, diffuse=0.8, specular=0.3),
            name=f'Ball ({ball_diameter_inch:.1f}")',
            hoverinfo='skip'
        ))

        step_indices = np.linspace(0, len(mid_x) - 1, min(65, len(mid_x)), dtype=int)
        for idx_pt in step_indices:
            bx, by, bz = make_3d_ball(mid_x[idx_pt], mid_y[idx_pt], mid_z[idx_pt], ball_radius_m)
            anim_points.append({"x": bx, "y": by, "z": bz})

        grey_legend_shown = False
        for idx, (rpm, vel_ms, x_arr, y_arr, z_arr, impact_point) in enumerate(scoring_trajectories):
            if idx == mid_idx:
                continue

            fig_traj.add_trace(go.Scatter3d(
                x=x_arr,
                y=y_arr,
                z=z_arr,
                mode='lines',
                name='Other Scoring Paths',
                legendgroup='other_scoring_paths',
                showlegend=not grey_legend_shown,
                line=dict(color='#383838', width=1.5),
                hovertemplate=(
                    f"<b>{rpm} RPM</b> ({vel_ms:.2f} m/s)<br>"
                    "X: %{x:.2f} m | Y: %{y:.2f} m | Z: %{z:.2f} m<extra></extra>"
                )
            ))
            grey_legend_shown = True

        fig_traj.add_trace(go.Scatter3d(
            x=mid_x,
            y=mid_y,
            z=mid_z,
            mode='lines',
            name=f'Middle Scoring Path ({mid_rpm} RPM)',
            line=dict(color='#FFFFFF', width=6),
            hovertemplate=(
                f"<b>Middle: {mid_rpm} RPM</b> ({mid_vel:.2f} m/s)<br>"
                "X: %{x:.2f} m | Y: %{y:.2f} m | Z: %{z:.2f} m<extra></extra>"
            )
        ))

    # White 3D FTC Robot Chassis (opacity=0.93) + Cylindrical Turret + Dotted Light-Grey Launch Angle Line
    add_robot_model_3d(
        fig_traj, robot_x_m, robot_y_m, launcher_x_m, launcher_y_m, height_m,
        half_robot_len_m, half_robot_wid_m, active_yaw_deg, pitch_deg
    )

    fig_traj.add_trace(go.Scatter3d(
        x=[launcher_x_m],
        y=[launcher_y_m],
        z=[height_m],
        mode='markers',
        name='Launcher',
        marker=dict(size=7, color='#FFFFFF', symbol='circle-open', line=dict(width=3)),
        hovertemplate="Launcher (Shift+Drag to move Robot): (%{x:.2f}, %{y:.2f}, %{z:.2f} m)<extra></extra>"
    ))

    # 12ft x 12ft (3.6576m x 3.6576m) FTC Field Centered at (0.0, 0.0)
    if show_ftc_field:
        fig_traj.add_trace(go.Mesh3d(
            x=[-FIELD_HALF, FIELD_HALF, FIELD_HALF, -FIELD_HALF],
            y=[-FIELD_HALF, -FIELD_HALF, FIELD_HALF, FIELD_HALF],
            z=[0.0, 0.0, 0.0, 0.0],
            i=[0, 0],
            j=[1, 2],
            k=[2, 3],
            color="#0D0D0D",
            opacity=0.5,
            name="FTC Field Floor",
            showlegend=False,
            hoverinfo="skip"
        ))

        grid_x, grid_y, grid_z = [], [], []
        for k_tile in range(7):
            pos = -FIELD_HALF + k_tile * TILE_STEP
            grid_x.extend([pos, pos, None])
            grid_y.extend([-FIELD_HALF, FIELD_HALF, None])
            grid_z.extend([0.001, 0.001, None])

            grid_x.extend([-FIELD_HALF, FIELD_HALF, None])
            grid_y.extend([pos, pos, None])
            grid_z.extend([0.001, 0.001, None])

        fig_traj.add_trace(go.Scatter3d(
            x=grid_x,
            y=grid_y,
            z=grid_z,
            mode="lines",
            name='FTC Tile Grid (24")',
            showlegend=False,
            line=dict(color="rgba(255, 255, 255, 0.14)", width=1.5),
            hoverinfo="skip"
        ))

        fig_traj.add_trace(go.Scatter3d(
            x=[0.0, 0.0],
            y=[-FIELD_HALF, FIELD_HALF],
            z=[0.002, 0.002],
            mode="lines",
            name="Center Line (X = 0.0)",
            showlegend=False,
            line=dict(color="rgba(255, 255, 255, 0.35)", width=3, dash="dash"),
            hoverinfo="skip"
        ))

        fig_traj.add_trace(go.Scatter3d(
            x=[0.0],
            y=[0.0],
            z=[0.004],
            mode="markers",
            name="Field Origin (0.0, 0.0)",
            showlegend=False,
            marker=dict(size=4, color="#FFFFFF", symbol="cross"),
            hovertemplate="Field Center: (0.00, 0.00, 0.00 m)<extra></extra>"
        ))

        wx = [
            -FIELD_HALF, FIELD_HALF, FIELD_HALF, -FIELD_HALF, -FIELD_HALF, None,
            -FIELD_HALF, FIELD_HALF, FIELD_HALF, -FIELD_HALF, -FIELD_HALF, None,
            -FIELD_HALF, -FIELD_HALF, None, FIELD_HALF, FIELD_HALF, None,
            FIELD_HALF, FIELD_HALF, None, -FIELD_HALF, -FIELD_HALF
        ]
        wy = [
            -FIELD_HALF, -FIELD_HALF, FIELD_HALF, FIELD_HALF, -FIELD_HALF, None,
            -FIELD_HALF, -FIELD_HALF, FIELD_HALF, FIELD_HALF, -FIELD_HALF, None,
            -FIELD_HALF, -FIELD_HALF, None, -FIELD_HALF, -FIELD_HALF, None,
            FIELD_HALF, FIELD_HALF, None, FIELD_HALF, FIELD_HALF
        ]
        wz = [
            0.0, 0.0, 0.0, 0.0, 0.0, None,
            WALL_H, WALL_H, WALL_H, WALL_H, WALL_H, None,
            0.0, WALL_H, None, 0.0, WALL_H, None,
            0.0, WALL_H, None, 0.0, WALL_H
        ]

        fig_traj.add_trace(go.Scatter3d(
            x=wx,
            y=wy,
            z=wz,
            mode="lines",
            name="FTC Perimeter Walls",
            showlegend=False,
            line=dict(color="rgba(255, 255, 255, 0.32)", width=2.5),
            hoverinfo="skip"
        ))

        if show_biobuzz_elements:
            add_biobuzz_field_elements(fig_traj, is_red_hive, is_left_up)

    if scoring_trajectories:
        max_traj_x = max(float(np.max(np.abs(item[2]))) for item in scoring_trajectories)
        max_traj_y = max(float(np.max(np.abs(item[3]))) for item in scoring_trajectories)
        max_traj_z = max(float(np.max(item[4])) for item in scoring_trajectories)
    else:
        max_traj_x, max_traj_y, max_traj_z = 0.0, 0.0, 0.0

    field_xy_bound = 1.85 if show_ftc_field else 1.5
    x_bound = max(field_xy_bound, abs(goal_x1) + 0.4, abs(goal_x2) + 0.4, abs(robot_x_m) + half_robot_len_m + 0.2, max_traj_x + 0.3)
    y_bound = max(field_xy_bound, abs(goal_y_center) + goal_half_w + 0.4, abs(robot_y_m) + half_robot_wid_m + 0.2, max_traj_y + 0.3)
    max_z_range = max(2.2, goal_z2 + 0.5, height_m + 0.5, max_traj_z + 0.3)

    axis_style = dict(
        backgroundcolor="rgba(0,0,0,0)",
        gridcolor="#1E1E1E",
        linecolor="#262626",
        zerolinecolor="#3A3A3A",
        tickcolor="#333333",
        spikecolor="#333333",
        color="#777777"
    )

    fig_traj.update_layout(
        template="plotly_dark",
        uirevision="ghost_view",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        hoverlabel=dict(bgcolor="#0A0A0A", bordercolor="#FFFFFF", font=dict(color="#FFFFFF")),
        scene=dict(
            uirevision="ghost_view",
            bgcolor="rgba(0,0,0,0)",
            aspectmode="data",
            xaxis=dict(title="Field X (m) [0 = Center]", range=[-x_bound, x_bound], **axis_style),
            yaxis=dict(title="Field Y (m) [0 = Center]", range=[-y_bound, y_bound], **axis_style),
            zaxis=dict(title="Height Z (m)", range=[0, max_z_range], **axis_style),
            camera=dict(eye=dict(x=-1.15, y=-1.65, z=0.95))
        ),
        margin=dict(l=0, r=0, t=20, b=0),
        height=560
    )

else:
    # ---------- 2D VIEW RENDERING ----------
    theta_circle = np.linspace(0, 2 * np.pi, 32)

    def make_2d_ball(cx, cz, r):
        return (cx + r * np.cos(theta_circle)).tolist(), (cz + r * np.sin(theta_circle)).tolist()

    if scoring_trajectories:
        target_cx = 0.5 * (goal_x1 + goal_x2)
        target_cz = 0.5 * (goal_z1 + goal_z2)
        mid_idx = min(
            range(len(scoring_trajectories)),
            key=lambda i: math.hypot(scoring_trajectories[i][5][0] - target_cx, scoring_trajectories[i][5][2] - target_cz)
        )
        mid_rpm, mid_vel, mid_x, _, mid_z, _ = scoring_trajectories[mid_idx]

        bx0, bz0 = make_2d_ball(mid_x[0], mid_z[0], ball_radius_m)

        # Trace 0: Physically-scaled Yellow 2D Circle
        fig_traj.add_trace(go.Scatter(
            x=bx0,
            y=bz0,
            mode='lines',
            fill='toself',
            fillcolor='#FACC15',
            line=dict(color='#000000', width=1.5),
            name=f'Ball ({ball_diameter_inch:.1f}")',
            hoverinfo='skip'
        ))

        step_indices = np.linspace(0, len(mid_x) - 1, min(65, len(mid_x)), dtype=int)
        for idx_pt in step_indices:
            bx, bz = make_2d_ball(mid_x[idx_pt], mid_z[idx_pt], ball_radius_m)
            anim_points.append({"x": bx, "y": bz})

        grey_legend_shown = False
        for idx, (rpm, vel_ms, x_arr, y_arr, z_arr, impact_point) in enumerate(scoring_trajectories):
            if idx == mid_idx:
                continue

            fig_traj.add_trace(go.Scatter(
                x=x_arr,
                y=z_arr,
                mode='lines',
                name='Other Scoring Paths',
                legendgroup='other_scoring_paths',
                showlegend=not grey_legend_shown,
                line=dict(color='rgba(255, 255, 255, 0.22)', width=1.2),
                hovertemplate=(
                    f"<b>{rpm} RPM</b> ({vel_ms:.2f} m/s)<br>"
                    "Field X: %{x:.2f} m<br>"
                    "Height Z: %{y:.2f} m<extra></extra>"
                )
            ))
            grey_legend_shown = True

        fig_traj.add_trace(go.Scatter(
            x=mid_x,
            y=mid_z,
            mode='lines',
            name=f'Middle Scoring Path ({mid_rpm} RPM)',
            line=dict(color='#FFFFFF', width=3.5),
            hovertemplate=(
                f"<b>Middle: {mid_rpm} RPM</b> ({mid_vel:.2f} m/s)<br>"
                "Field X: %{x:.2f} m<br>"
                "Height Z: %{y:.2f} m<extra></extra>"
            )
        ))

    if show_ftc_field and show_biobuzz_elements:
        add_biobuzz_field_elements_2d(fig_traj, is_red_hive, is_left_up)

    fig_traj.add_trace(go.Scatter(
        x=[goal_x1, goal_x2],
        y=[goal_z1, goal_z2],
        mode='lines+markers',
        name=f"{'Red' if is_red_hive else 'Blue'} Entrance ({raised_side})",
        showlegend=False,
        line=dict(color='#FFFFFF', width=2.5, dash='dash'),
        marker=dict(size=7, color='#8E8E93', line=dict(color='#FFFFFF', width=1.5)),
        hovertemplate="Target Entrance: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
    ))

    # White 2D Robot Side Profile (opacity=0.93) + Cylindrical Turret + Dotted Light-Grey Launch Angle Line
    add_robot_model_2d(
        fig_traj, robot_x_m, launcher_x_m, height_m,
        half_robot_len_m, active_yaw_deg, pitch_deg
    )

    fig_traj.add_trace(go.Scatter(
        x=[launcher_x_m],
        y=[height_m],
        mode='markers',
        name='Launcher',
        marker=dict(size=10, color='#FFFFFF', symbol='circle-open', line=dict(width=3)),
        hovertemplate="Launcher (Shift+Drag to move Robot in X): (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
    ))

    if show_ftc_field:
        fig_traj.add_vline(
            x=0.0,
            line_width=2,
            line_dash="dash",
            line_color="rgba(255, 255, 255, 0.35)",
            annotation_text="Center (0.0)",
            annotation_position="top"
        )
        fig_traj.add_trace(go.Scatter(
            x=[-FIELD_HALF, -FIELD_HALF, None, FIELD_HALF, FIELD_HALF],
            y=[0.0, WALL_H, None, 0.0, WALL_H],
            mode='lines',
            name='Perimeter Walls',
            showlegend=False,
            line=dict(color='rgba(255, 255, 255, 0.45)', width=3),
            hoverinfo='skip'
        ))

    x_axis_cfg = dict(
        title="Field X (m) [0.0 = Center]",
        fixedrange=True,
        color="#FFFFFF",
        gridcolor="rgba(255, 255, 255, 0.10)",
        showgrid=True,
        zerolinecolor="rgba(255, 255, 255, 0.35)",
        dtick=0.5,
        minor=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.03)", dtick="0.3")
    )
    if show_ftc_field:
        x_axis_cfg["range"] = [-1.95, 1.95]

    fig_traj.update_layout(
        template="plotly_dark",
        uirevision="ghost_view",
        dragmode=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        hoverlabel=dict(bgcolor="#0A0A0A", bordercolor="#FFFFFF", font=dict(color="#FFFFFF")),
        xaxis=x_axis_cfg,
        yaxis=dict(
            title="Height Z (m)",
            fixedrange=True,
            color="#FFFFFF",
            gridcolor="rgba(255, 255, 255, 0.10)",
            showgrid=True,
            zerolinecolor="rgba(255, 255, 255, 0.25)",
            rangemode="tozero",
            scaleanchor="x",
            scaleratio=1,
            dtick=0.5,
            minor=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.03)", dtick="0.3")
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=560
    )

# Render interactive Plotly chart with Shift+Drag Robot positioning & smooth client-side animation
fig_json = fig_traj.to_json()
frames_json = json.dumps(anim_points)
is_3d_js = "true" if is_3d else "false"
has_frames_js = "true" if len(anim_points) > 0 else "false"
scroll_zoom_js = "true" if is_3d else "false"

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  html, body {{
    margin: 0;
    padding: 0;
    background: transparent;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}
  #wrapper {{
    position: relative;
    width: 100%;
    height: 560px;
  }}
  #chart {{
    width: 100%;
    height: 100%;
  }}
  #playBtn {{
    position: absolute;
    top: 10px;
    left: 14px;
    z-index: 20;
    background: #111111;
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.35);
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  }}
  #playBtn:hover {{
    background: #FFFFFF;
    color: #000000;
    border-color: #FFFFFF;
  }}
  #dragHint {{
    position: absolute;
    bottom: 10px;
    left: 14px;
    z-index: 20;
    background: rgba(17, 17, 17, 0.85);
    color: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    pointer-events: none;
  }}
</style>
</head>
<body>
<div id="wrapper">
  {"<button id='playBtn'>&#9654;&nbsp; Play Shot</button>" if len(anim_points) > 0 else ""}
  <div id='dragHint'>Hold <b>Shift + Drag</b> to move Robot {"in X-Y" if is_3d else "in X"}</div>
  <div id="chart"></div>
</div>
<script>
  const fig = {fig_json};
  const frames = {frames_json};
  const is3D = {is_3d_js};
  const hasFrames = {has_frames_js};
  const launchZ = {height_m};
  const initRobotX = {robot_x_m};
  const initRobotY = {robot_y_m};
  const initLauncherX = {launcher_x_m};
  const initLauncherY = {launcher_y_m};
  const minRobotX = {min_robot_x_m};
  const maxRobotX = {max_robot_x_m};
  const minRobotY = {min_robot_y_m};
  const maxRobotY = {max_robot_y_m};
  const gd = document.getElementById('chart');

  function clampRobotX(val) {{
    return Math.max(minRobotX, Math.min(maxRobotX, val));
  }}

  function clampRobotY(val) {{
    return Math.max(minRobotY, Math.min(maxRobotY, val));
  }}

  function syncStreamlitNumberInput(labelText, newValue) {{
    try {{
      const doc = window.parent.document;

      const expanders = Array.from(doc.querySelectorAll('[data-testid="stSidebar"] [data-testid="stExpander"]'));
      for (const exp of expanders) {{
        if (exp.textContent && exp.textContent.includes('Robot Location')) {{
          const details = exp.querySelector('details');
          const summary = exp.querySelector('summary');
          if (details && !details.open && summary) {{
            summary.click();
          }}
        }}
      }}

      setTimeout(() => {{
        const inputs = Array.from(doc.querySelectorAll('[data-testid="stSidebar"] input[type="number"]'));
        for (const inp of inputs) {{
          const container = inp.closest('[data-testid="stNumberInput"]');
          if (container && container.textContent && container.textContent.includes(labelText)) {{
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            inp.focus();
            nativeSetter.call(inp, String(newValue));
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            inp.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
            inp.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
            inp.blur();
            break;
          }}
        }}
      }}, 30);
    }} catch (err) {{
      console.warn('Sidebar sync skipped:', err);
    }}
  }}

  function map2DPixelToX(clientX) {{
    const fullLayout = gd._fullLayout;
    if (!fullLayout || !fullLayout.xaxis || !fullLayout._size) return null;

    const rect = gd.getBoundingClientRect();
    const px = (clientX - rect.left) - fullLayout._size.l;
    const worldX = fullLayout.xaxis.p2d(px);
    if (!Number.isFinite(worldX)) return null;

    return {{
      x: worldX,
      y: null
    }};
  }}

  function projectWorldToScreen(wx, wy, wz) {{
    const sceneLayout = gd._fullLayout && gd._fullLayout.scene;
    if (!sceneLayout) return null;

    const xRange = sceneLayout.xaxis.range;
    const yRange = sceneLayout.yaxis.range;
    const zRange = sceneLayout.zaxis.range;
    const spanX = xRange[1] - xRange[0];
    const spanY = yRange[1] - yRange[0];
    const spanZ = zRange[1] - zRange[0];
    const midX = 0.5 * (xRange[0] + xRange[1]);
    const midY = 0.5 * (yRange[0] + yRange[1]);
    const midZ = 0.5 * (zRange[0] + zRange[1]);

    const ar = sceneLayout.aspectratio || {{ x: 1, y: 1, z: 1 }};
    const bx = ((wx - midX) / spanX) * ar.x;
    const by = ((wy - midY) / spanY) * ar.y;
    const bz = ((wz - midZ) / spanZ) * ar.z;

    const rect = gd.getBoundingClientRect();
    const glplot = sceneLayout._scene && sceneLayout._scene.glplot;

    let vMat = null;
    let pMat = null;
    if (glplot) {{
      const vCand = (glplot.camera && glplot.camera.view) || glplot.view;
      const pCand = (glplot.camera && glplot.camera.projection) || glplot.projection;
      vMat = (vCand && vCand.length === 16) ? vCand : (vCand && vCand.matrix && vCand.matrix.length === 16 ? vCand.matrix : null);
      pMat = (pCand && pCand.length === 16) ? pCand : (pCand && pCand.matrix && pCand.matrix.length === 16 ? pCand.matrix : null);
    }}

    const domX = sceneLayout.domain ? sceneLayout.domain.x : [0, 1];
    const domY = sceneLayout.domain ? sceneLayout.domain.y : [0, 1];
    const vpLeft = rect.left + domX[0] * rect.width;
    const vpWidth = (domX[1] - domX[0]) * rect.width;
    const vpTop = rect.top + (1.0 - domY[1]) * rect.height;
    const vpHeight = (domY[1] - domY[0]) * rect.height;

    if (vMat && pMat) {{
      const vx = vMat[0]*bx + vMat[4]*by + vMat[8]*bz + vMat[12];
      const vy = vMat[1]*bx + vMat[5]*by + vMat[9]*bz + vMat[13];
      const vz = vMat[2]*bx + vMat[6]*by + vMat[10]*bz + vMat[14];
      const vw = vMat[3]*bx + vMat[7]*by + vMat[11]*bz + vMat[15];

      const cx = pMat[0]*vx + pMat[4]*vy + pMat[8]*vz + pMat[12]*vw;
      const cy = pMat[1]*vx + pMat[5]*vy + pMat[9]*vz + pMat[13]*vw;
      const cw = pMat[3]*vx + pMat[7]*vy + pMat[11]*vz + pMat[15]*vw;

      if (Math.abs(cw) > 1e-6) {{
        const ndcX = cx / cw;
        const ndcY = cy / cw;
        return {{
          px: vpLeft + (ndcX * 0.5 + 0.5) * vpWidth,
          py: vpTop + (0.5 - ndcY * 0.5) * vpHeight
        }};
      }}
    }}

    const cam = sceneLayout.camera;
    if (!cam) return null;

    const eye = [cam.eye.x, cam.eye.y, cam.eye.z];
    const ctr = [cam.center.x, cam.center.y, cam.center.z];
    const up  = [cam.up.x, cam.up.y, cam.up.z];

    const fwd = norm3([ctr[0] - eye[0], ctr[1] - eye[1], ctr[2] - eye[2]]);
    const right = norm3(cross3(fwd, up));
    const trueUp = cross3(right, fwd);

    const rel = [bx - eye[0], by - eye[1], bz - eye[2]];
    const zCam = rel[0]*fwd[0] + rel[1]*fwd[1] + rel[2]*fwd[2];
    if (zCam <= 1e-4) return null;

    const xCam = rel[0]*right[0] + rel[1]*right[1] + rel[2]*right[2];
    const yCam = rel[0]*trueUp[0] + rel[1]*trueUp[1] + rel[2]*trueUp[2];

    const aspect = vpWidth / vpHeight;
    const tanHalfFov = Math.tan(Math.PI / 8.0);
    const ndcX = xCam / (zCam * aspect * tanHalfFov);
    const ndcY = yCam / (zCam * tanHalfFov);

    return {{
      px: vpLeft + (ndcX * 0.5 + 0.5) * vpWidth,
      py: vpTop + (0.5 - ndcY * 0.5) * vpHeight
    }};
  }}

  function buildDragMapper(x0, y0, z0) {{
    const eps = 0.05;
    const p0 = projectWorldToScreen(x0, y0, z0);
    const px = projectWorldToScreen(x0 + eps, y0, z0);
    const py = projectWorldToScreen(x0, y0 + eps, z0);
    if (!p0 || !px || !py) return null;

    const j11 = (px.px - p0.px) / eps;
    const j21 = (px.py - p0.py) / eps;
    const j12 = (py.px - p0.px) / eps;
    const j22 = (py.py - p0.py) / eps;

    const det = j11 * j22 - j12 * j21;
    if (Math.abs(det) < 1e-4) return null;

    const inv11 =  j22 / det;
    const inv12 = -j12 / det;
    const inv21 = -j21 / det;
    const inv22 =  j11 / det;

    return function mapDeltaPixels(dPx, dPy) {{
      return {{
        dx: inv11 * dPx + inv12 * dPy,
        dy: inv21 * dPx + inv22 * dPy
      }};
    }};
  }}

  function cross3(a, b) {{
    return [
      a[1]*b[2] - a[2]*b[1],
      a[2]*b[0] - a[0]*b[2],
      a[0]*b[1] - a[1]*b[0]
    ];
  }}

  function norm3(v) {{
    const len = Math.hypot(v[0], v[1], v[2]) || 1.0;
    return [v[0]/len, v[1]/len, v[2]/len];
  }}

  Plotly.newPlot(gd, fig.data, fig.layout, {{
    responsive: true,
    scrollZoom: {scroll_zoom_js},
    displayModeBar: false,
    displaylogo: false
  }}).then(() => {{
    const launcherTraceIdx = fig.data.findIndex(t => t.name === 'Launcher');

    const robotTraceIndices = [];
    const baseRobotCoords = {{}};
    fig.data.forEach((t, idx) => {{
      if (t.name && t.name.startsWith('Robot')) {{
        robotTraceIndices.push(idx);
        baseRobotCoords[idx] = {{
          x: [...gd.data[idx].x],
          y: [...gd.data[idx].y]
        }};
      }}
    }});

    const hintEl = document.getElementById('dragHint');
    let isDraggingLauncher = false;
    let currentRobotWorld = {{ x: initRobotX, y: initRobotY }};
    let lastDraggedRobotPos = null;
    let dragOriginMouse = {{ x: 0, y: 0 }};
    let dragOriginRobotWorld = {{ x: initRobotX, y: initRobotY }};
    let deltaMapper3D = null;

    function updateRobotPos(clientX, clientY) {{
      if (launcherTraceIdx === -1) return;

      let newRobotX, newRobotY = null;

      if (is3D) {{
        if (!deltaMapper3D) return;
        const dPx = clientX - dragOriginMouse.x;
        const dPy = clientY - dragOriginMouse.y;
        const delta = deltaMapper3D(dPx, dPy);
        newRobotX = clampRobotX(dragOriginRobotWorld.x + delta.dx);
        newRobotY = clampRobotY(dragOriginRobotWorld.y + delta.dy);
      }} else {{
        const hit = map2DPixelToX(clientX);
        if (!hit) return;
        newRobotX = clampRobotX(dragOriginRobotWorld.x + (hit.x - dragOriginMouse.x));
      }}

      currentRobotWorld = {{ x: newRobotX, y: is3D ? newRobotY : 0 }};
      lastDraggedRobotPos = {{ x: newRobotX, y: newRobotY }};
      const shiftX = newRobotX - initRobotX;
      const shiftY = is3D ? (newRobotY - initRobotY) : 0;

      if (is3D) {{
        Plotly.restyle(gd, {{
          x: [[initLauncherX + shiftX]],
          y: [[initLauncherY + shiftY]]
        }}, [launcherTraceIdx]);

        robotTraceIndices.forEach(idx => {{
          const shiftedX = baseRobotCoords[idx].x.map(v => v === null ? null : v + shiftX);
          const shiftedY = baseRobotCoords[idx].y.map(v => v === null ? null : v + shiftY);
          Plotly.restyle(gd, {{ x: [shiftedX], y: [shiftedY] }}, [idx]);
        }});

        if (hintEl) {{
          hintEl.innerHTML = `Robot Center: <b>X = ${{Math.round(newRobotX * 1000)}} mm</b>, <b>Y = ${{Math.round(newRobotY * 1000)}} mm</b>`;
        }}
      }} else {{
        Plotly.restyle(gd, {{ x: [[initLauncherX + shiftX]] }}, [launcherTraceIdx]);

        robotTraceIndices.forEach(idx => {{
          const shiftedX = baseRobotCoords[idx].x.map(v => v === null ? null : v + shiftX);
          Plotly.restyle(gd, {{ x: [shiftedX] }}, [idx]);
        }});

        if (hintEl) {{
          hintEl.innerHTML = `Robot Center: <b>X = ${{Math.round(newRobotX * 1000)}} mm</b>`;
        }}
      }}
    }}

    function onDragStart(e) {{
      if (e.button === 0 && e.shiftKey && launcherTraceIdx !== -1) {{
        e.stopImmediatePropagation();
        e.stopPropagation();
        e.preventDefault();
        isDraggingLauncher = true;
        gd.style.cursor = 'grabbing';

        dragOriginRobotWorld = {{ x: currentRobotWorld.x, y: currentRobotWorld.y }};
        if (is3D) {{
          dragOriginMouse = {{ x: e.clientX, y: e.clientY }};
          deltaMapper3D = buildDragMapper(dragOriginRobotWorld.x, dragOriginRobotWorld.y, launchZ);
        }} else {{
          const hit = map2DPixelToX(e.clientX);
          dragOriginMouse = {{ x: hit ? hit.x : dragOriginRobotWorld.x, y: 0 }};
        }}
      }}
    }}

    function onDragMove(e) {{
      if (!isDraggingLauncher) return;
      e.stopImmediatePropagation();
      e.stopPropagation();
      e.preventDefault();
      updateRobotPos(e.clientX, e.clientY);
    }}

    function onDragEnd(e) {{
      if (!isDraggingLauncher) return;
      e.stopImmediatePropagation();
      e.stopPropagation();
      isDraggingLauncher = false;
      gd.style.cursor = 'default';

      if (hintEl) {{
        hintEl.innerHTML = is3D
          ? 'Hold <b>Shift + Drag</b> to move Robot in X-Y'
          : 'Hold <b>Shift + Drag</b> to move Robot in X';
      }}

      if (lastDraggedRobotPos) {{
        const clampedXmm = Math.max(
          Math.ceil((minRobotX * 1000) / 10) * 10,
          Math.min(Math.floor((maxRobotX * 1000) / 10) * 10, Math.round((lastDraggedRobotPos.x * 1000) / 10) * 10)
        );
        syncStreamlitNumberInput('Robot X [mm]', clampedXmm);

        if (is3D && lastDraggedRobotPos.y !== null) {{
          const clampedYmm = Math.max(
            Math.ceil((minRobotY * 1000) / 10) * 10,
            Math.min(Math.floor((maxRobotY * 1000) / 10) * 10, Math.round((lastDraggedRobotPos.y * 1000) / 10) * 10)
          );
          setTimeout(() => syncStreamlitNumberInput('Robot Lateral Y [mm]', clampedYmm), 60);
        }}
        lastDraggedRobotPos = null;
      }}
    }}

    gd.addEventListener('mousedown', onDragStart, true);
    gd.addEventListener('pointerdown', onDragStart, true);
    window.addEventListener('mousemove', onDragMove, true);
    window.addEventListener('pointermove', onDragMove, true);
    window.addEventListener('mouseup', onDragEnd, true);
    window.addEventListener('pointerup', onDragEnd, true);
  }});

  if (hasFrames) {{
    let animId = null;
    const btn = document.getElementById('playBtn');

    btn.addEventListener('click', () => {{
      if (animId) {{
        cancelAnimationFrame(animId);
        animId = null;
      }}

      let idx = 0;
      let lastTime = 0;
      const intervalMs = 20;

      function step(timestamp) {{
        if (timestamp - lastTime >= intervalMs) {{
          lastTime = timestamp;
          const pt = frames[idx];

          if (is3D) {{
            fig.data[0].x = pt.x;
            fig.data[0].y = pt.y;
            fig.data[0].z = pt.z;
            fig.layout.datarevision = idx + 1;
            Plotly.react(gd, fig.data, fig.layout);
          }} else {{
            Plotly.restyle(gd, {{
              x: [pt.x],
              y: [pt.y]
            }}, [0]);
          }}

          idx++;
          if (idx >= frames.length) {{
            animId = null;
            return;
          }}
        }}
        animId = requestAnimationFrame(step);
      }}

      animId = requestAnimationFrame(step);
    }});
  }}
</script>
</body>
</html>
"""

components.html(html_code, height=565, scrolling=False)

# Summary Metrics for Scoring RPMs & Auto-Turret Yaw
col1, col2, col3, col4 = st.columns(4)
if scoring_trajectories:
    min_rpm = scoring_trajectories[0][0]
    max_rpm = scoring_trajectories[-1][0]
    mid_rpm, mid_vel = scoring_trajectories[mid_idx][:2]
    col1.metric("Middle Scoring RPM", f"{mid_rpm} RPM ({mid_vel:.2f} m/s)")
    col2.metric("Scoring RPM Range", f"{min_rpm} – {max_rpm} RPM")
    col3.metric("Auto Turret Yaw", f"{active_yaw_deg:.2f}°")
    col4.metric("Valid Steps Found", f"{len(scoring_trajectories)} (Δ25 RPM)")
else:
    col1.metric("Middle Scoring RPM", "None found")
    col2.metric("Scoring RPM Range", "—")
    col3.metric("Auto Turret Yaw", f"{active_yaw_deg:.2f}°")
    col4.metric("Valid Steps Found", "0")