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
        width: 1800px; /* Change only this value (e.g., 900px, 1200px, or 65vw) */
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
        index=0,
        horizontal=True
    )
    is_3d = view_mode == "3D View"

    shooter_type = st.radio(
        "Shooter Mechanism Type",
        options=["Single Flywheel", "Dual flywheel"],
        index=0
    )

    efficiency_loss = st.slider('Efficiency Loss [%]', 0.0, 80.0, 10.0, 0.5)
    pitch_deg = st.slider('Pitch Angle [deg]', 1.0, 90.0, 45.0, 0.5)
    wheel_Radius_inch = st.slider('Wheel Radius [inch]', 0.5, 6.0, 3.0, 0.1)

    st.header("Launch Position")
    robot_x_mm = st.number_input('Robot X [mm]', 0.0, 3600.0, 0.0, 10.0)
    robot_y_mm = st.number_input(
        'Robot Y [mm]', -2000.0, 2000.0, 0.0, 10.0,
        disabled=not is_3d
    )
    height_mm = st.number_input('Launch Height Robot Z [mm]', 0.0, 2000.0, 365.0, 5.0)

    st.header("Aerodynamics & Spin")
    use_drag = st.checkbox("Enable Air Resistance (Drag)", value=True)
    use_magnus = st.checkbox("Enable Spin Effect (Magnus)", value=True)

    spin_type = st.selectbox(
        "Primary Spin Direction",
        options=["Backspin", "Topspin"],
        disabled=not use_magnus
    )
    sidespin_deg = st.slider(
        "Spin Axis Roll / Sidespin [deg]",
        -45.0, 45.0, 0.0, 1.0,
        disabled=(not use_magnus or not is_3d)
    )

    # Gamepiece Preset Selector
    gamepiece = st.radio(
        "Gamepiece Preset",
        options=["Custom", "Pollen", "Nectar"],
        index=0
    )

    is_locked = gamepiece != "Custom"
    if gamepiece == "Pollen":
        default_diameter, default_mass = 2.8, 25
    elif gamepiece == "Nectar":
        default_diameter, default_mass = 3.6, 41
    else:
        default_diameter, default_mass = 7.0, 200

    ball_diameter_inch = st.slider(
        "Ball Diameter [inch]",
        min_value=1.0, max_value=12.0,
        value=default_diameter, step=0.1,
        disabled=is_locked,
        key=f"dia_{gamepiece}"
    )

    ball_mass_g = st.slider(
        "Ball Mass [g]",
        min_value=10, max_value=1000,
        value=default_mass, step=1 if is_locked else 10,
        disabled=is_locked,
        key=f"mass_{gamepiece}"
    )

    st.header("Target Goal")
    target_start_x_mm = st.number_input('Goal Start X [mm]', 0, 4000, 1085, 5)
    target_start_z_mm = st.number_input('Goal Start Z (Height) [mm]', 0, 4000, 1358, 5)
    target_end_x_mm = st.number_input('Goal End X [mm]', 0, 8000, 1261, 5)
    target_end_z_mm = st.number_input('Goal End Z (Height) [mm]', 0, 8000, 1665, 5)
    target_center_y_mm = st.number_input(
        'Goal Center Y [mm]', -2000, 2000, 0, 10,
        disabled=not is_3d
    )
    target_width_mm = st.number_input(
        'Goal Opening Width Y [mm]', 100, 3000, 600, 10,
        disabled=not is_3d
    )

# ==========================================
# 2. UNIFIED 2D / 3D PHYSICS CALCULATIONS
# ==========================================
active_robot_y_mm = robot_y_mm if is_3d else 0.0
active_sidespin_deg = sidespin_deg if is_3d else 0.0
active_goal_center_y_mm = target_center_y_mm if is_3d else 0.0

robot_x_m = float(robot_x_mm) / 1000.0
robot_y_m = float(active_robot_y_mm) / 1000.0
height_m = float(height_mm) / 1000.0

goal_x1 = target_start_x_mm / 1000.0
goal_z1 = target_start_z_mm / 1000.0
goal_x2 = target_end_x_mm / 1000.0
goal_z2 = target_end_z_mm / 1000.0
goal_y_center = active_goal_center_y_mm / 1000.0
goal_half_w = (target_width_mm / 1000.0) / 2.0
goal_y_min = goal_y_center - goal_half_w
goal_y_max = goal_y_center + goal_half_w
goal_x_center = (goal_x1 + goal_x2) / 2.0
dx_goal = goal_x_center - robot_x_m
dy_goal = goal_y_center - robot_y_m

if is_3d:
    active_yaw_deg = math.degrees(math.atan2(dy_goal, dx_goal))
else:
    active_yaw_deg = 0.0

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
    """Checks if segment p1->p2 crosses the goal opening (2D plane or 3D bounded opening)."""
    (x1, y1, z1), (x2, y2, z2) = p1, p2

    denom = (x1 - x2) * (goal_z1 - goal_z2) - (z1 - z2) * (goal_x1 - goal_x2)
    if abs(denom) < 1e-9:
        return False, None

    t = ((x1 - goal_x1) * (goal_z1 - goal_z2) - (z1 - goal_z1) * (goal_x1 - goal_x2)) / denom
    u = ((x1 - goal_x1) * (z1 - z2) - (z1 - goal_z1) * (x1 - x2)) / denom

    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        iy = y1 + t * (y2 - y1)
        if not is_3d or (goal_y_min <= iy <= goal_y_max):
            ix = x1 + t * (x2 - x1)
            iz = z1 + t * (z2 - z1)
            return True, (ix, iy, iz)

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
    spin_sign = 1.0 if omega_mag > 0 else (-1.0 if omega_mag < 0 else 0.0)

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

        intersects, pt = check_goal_intersection((x, y, z), (nx, ny, nz))
        if intersects:
            x_arr.append(pt[0])
            y_arr.append(pt[1])
            z_arr.append(pt[2])
            hit_target, impact_point = True, pt
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
        vel_ms, pitch_deg, active_yaw_deg, (robot_x_m, robot_y_m, height_m),
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
st.subheader(f"Shot Calculator Trajectory ({view_mode})")

fig_traj = go.Figure()
anim_points = []

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
        mid_idx = len(scoring_trajectories) // 2
        mid_rpm, mid_vel, mid_x, mid_y, mid_z, _ = scoring_trajectories[mid_idx]

        bx0, by0, bz0 = make_3d_ball(mid_x[0], mid_y[0], mid_z[0], ball_radius_m)

        # Trace 0: Physically-scaled Yellow 3D Sphere
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

        other_impacts = [item for idx, item in enumerate(scoring_trajectories) if idx != mid_idx]
        if other_impacts:
            fig_traj.add_trace(go.Scatter3d(
                x=[item[5][0] for item in other_impacts],
                y=[item[5][1] for item in other_impacts],
                z=[item[5][2] for item in other_impacts],
                mode='markers',
                name='Other Impacts',
                marker=dict(size=3, color='#4A4A4A'),
                customdata=[item[0] for item in other_impacts],
                hovertemplate="<b>%{customdata} RPM</b><br>HIT: (%{x:.2f}, %{y:.2f}, %{z:.2f} m)<extra></extra>"
            ))

    # 3D Rectangular Target Goal Opening
    gx = [goal_x1, goal_x1, goal_x2, goal_x2, goal_x1]
    gy = [goal_y_min, goal_y_max, goal_y_max, goal_y_min, goal_y_min]
    gz = [goal_z1, goal_z1, goal_z2, goal_z2, goal_z1]

    fig_traj.add_trace(go.Scatter3d(
        x=gx,
        y=gy,
        z=gz,
        mode='lines+markers',
        name='Target Goal Opening',
        line=dict(color='#555555', width=3),
        marker=dict(size=3, color='#666666'),
        hovertemplate="Goal Frame: (%{x:.2f}, %{y:.2f}, %{z:.2f} m)<extra></extra>"
    ))

    fig_traj.add_trace(go.Mesh3d(
        x=[goal_x1, goal_x1, goal_x2, goal_x2],
        y=[goal_y_min, goal_y_max, goal_y_max, goal_y_min],
        z=[goal_z1, goal_z1, goal_z2, goal_z2],
        i=[0, 0],
        j=[1, 2],
        k=[2, 3],
        color='#444444',
        opacity=0.06,
        name='Goal Plane',
        showlegend=False,
        hoverinfo='skip'
    ))

    # Launcher 3D Node
    fig_traj.add_trace(go.Scatter3d(
        x=[robot_x_m],
        y=[robot_y_m],
        z=[height_m],
        mode='markers',
        name='Launcher',
        marker=dict(size=6, color='#FFFFFF', symbol='circle-open', line=dict(width=3)),
        hovertemplate="Launcher: (%{x:.2f}, %{y:.2f}, %{z:.2f} m)<extra></extra>"
    ))

    if scoring_trajectories:
        max_traj_x = max(float(np.max(item[2])) for item in scoring_trajectories)
        max_traj_y = max(float(np.max(np.abs(item[3]))) for item in scoring_trajectories)
        max_traj_z = max(float(np.max(item[4])) for item in scoring_trajectories)
    else:
        max_traj_x, max_traj_y, max_traj_z = 0.0, 0.0, 0.0

    max_x_range = max(2.0, goal_x2 + 0.5, robot_x_m + 0.5, max_traj_x + 0.3)
    max_z_range = max(2.0, goal_z2 + 0.5, height_m + 0.5, max_traj_z + 0.3)
    y_bound = max(1.0, abs(goal_y_center) + goal_half_w + 0.4, abs(robot_y_m) + 0.4, max_traj_y + 0.3)

    axis_style = dict(
        backgroundcolor="rgba(0,0,0,0)",
        gridcolor="#1E1E1E",
        linecolor="#262626",
        zerolinecolor="#2A2A2A",
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
            xaxis=dict(title="Distance X (m)", range=[0, max_x_range], **axis_style),
            yaxis=dict(title="Lateral Y (m)", range=[-y_bound, y_bound], **axis_style),
            zaxis=dict(title="Height Z (m)", range=[0, max_z_range], **axis_style),
            camera=dict(eye=dict(x=1.35, y=-1.55, z=0.75))
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
        mid_idx = len(scoring_trajectories) // 2
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
                    "Distance: %{x:.2f} m<br>"
                    "Height: %{y:.2f} m<extra></extra>"
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
                "Distance: %{x:.2f} m<br>"
                "Height: %{y:.2f} m<extra></extra>"
            )
        ))

        other_impacts = [item for idx, item in enumerate(scoring_trajectories) if idx != mid_idx]
        if other_impacts:
            fig_traj.add_trace(go.Scatter(
                x=[item[5][0] for item in other_impacts],
                y=[item[5][2] for item in other_impacts],
                mode='markers',
                name='Other Impacts',
                marker=dict(size=5, color='rgba(255, 255, 255, 0.50)', symbol='circle'),
                customdata=[item[0] for item in other_impacts],
                hovertemplate="<b>%{customdata} RPM</b><br>HIT Point: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
            ))

    # 2D Target Goal Line
    fig_traj.add_trace(go.Scatter(
        x=[goal_x1, goal_x2],
        y=[goal_z1, goal_z2],
        mode='lines+markers',
        name='Target Goal',
        line=dict(color='#A3A3A3', width=6),
        marker=dict(size=8, color='#FFFFFF'),
        hovertemplate="Goal Point: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
    ))

    # 2D Launcher Node
    fig_traj.add_trace(go.Scatter(
        x=[robot_x_m],
        y=[height_m],
        mode='markers',
        name='Launcher',
        marker=dict(size=10, color='#FFFFFF', symbol='circle-open', line=dict(width=3)),
        hovertemplate="Launcher Location: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
    ))

    fig_traj.update_layout(
        template="plotly_dark",
        uirevision="ghost_view",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF"),
        hoverlabel=dict(bgcolor="#0A0A0A", bordercolor="#FFFFFF", font=dict(color="#FFFFFF")),
        xaxis=dict(
            title="Distance (m)",
            color="#FFFFFF",
            gridcolor="rgba(255, 255, 255, 0.10)",
            showgrid=True,
            zerolinecolor="rgba(255, 255, 255, 0.25)",
            rangemode="tozero",
            dtick=0.5,
            minor=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.03)", dtick="0.3")
        ),
        yaxis=dict(
            title="Height (m)",
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

# Render interactive Plotly chart with smooth client-side animation & camera lock
fig_json = fig_traj.to_json()
frames_json = json.dumps(anim_points)
is_3d_js = "true" if is_3d else "false"
has_frames_js = "true" if len(anim_points) > 0 else "false"

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
</style>
</head>
<body>
<div id="wrapper">
  {"<button id='playBtn'>&#9654;&nbsp; Play Shot</button>" if len(anim_points) > 0 else ""}
  <div id="chart"></div>
</div>
<script>
  const fig = {fig_json};
  const frames = {frames_json};
  const is3D = {is_3d_js};
  const hasFrames = {has_frames_js};
  const gd = document.getElementById('chart');

  Plotly.newPlot(gd, fig.data, fig.layout, {{
    responsive: true,
    displayModeBar: true,
    displaylogo: false
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

col1, col2, col3, col4 = st.columns(4)
if scoring_trajectories:
    min_rpm = scoring_trajectories[0][0]
    max_rpm = scoring_trajectories[-1][0]
    mid_rpm, mid_vel = scoring_trajectories[len(scoring_trajectories) // 2][:2]
    col1.metric("Middle Scoring RPM", f"{mid_rpm} RPM ({mid_vel:.2f} m/s)")
    col2.metric("Scoring RPM Range", f"{min_rpm} – {max_rpm} RPM")
    col3.metric("Auto Turret Yaw", f"{active_yaw_deg:.2f}°")
    col4.metric("Valid Steps Found", f"{len(scoring_trajectories)} (Δ25 RPM)")
else:
    col1.metric("Middle Scoring RPM", "None found")
    col2.metric("Scoring RPM Range", "—")
    col3.metric("Auto Turret Yaw", f"{active_yaw_deg:.2f}°")
    col4.metric("Valid Steps Found", "0")