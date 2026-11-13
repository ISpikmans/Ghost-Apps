import math
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* 1. Force sidebar to stay visible and expanded */
    [data-testid="stSidebar"] {
        display: block !important;
        transform: none !important;
        visibility: visible !important;
    }

    /* 2. Hide the collapse arrow (<) at the top of the sidebar */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* 3. Hide the expand arrow (>) in the main top bar */
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    /* 4. Force rounded corners on Streamlit Plotly Chart */
    div[data-testid="stPlotlyChart"] {
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    div[data-testid="stPlotlyChart"] > div {
        border-radius: 16px !important;
        overflow: hidden !important;
    }

    /* 5. Lock page scroll completely */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        overflow: hidden !important;
        height: 100vh !important;
    }

    /* 6. Remove top and bottom padding from main block */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 1. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.header("Trajectory Settings")
    shooter_type = st.radio(
        "Shooter Mechanism Type",
        options=["Single Flywheel", "Dual flywheel"],
        index=0
    )

    efficiency_loss = st.slider('Efficiency Loss [%]', 0.0, 50.0, 10.0, 0.5)
    angle = st.slider('Angle [deg]', 1.0, 90.0, 45.0, 0.5)
    wheel_Radius_inch = st.slider('Wheel Radius [inch]', 0.5, 6.0, 3.0, 0.1)

    st.header("Launch Position Settings")
    robot_x_mm = st.number_input('Robot Position X [mm]', 0.0, 3600.0, 0.0, 1.0)
    height_mm = st.number_input('Launch height Y [mm]', 0.0, 2000.0, 365.0, 5.0)

    st.header("Aerodynamics & Environment")
    use_drag = st.checkbox("Enable Air Resistance (Drag)", value=True)
    use_magnus = st.checkbox("Enable Spin Effect (Magnus)", value=True)

    spin_type = st.selectbox(
        "Spin Direction",
        options=["Backspin", "Topspin"],
        disabled=not use_magnus
    )

    # Gamepiece Preset Selector
    gamepiece = st.radio(
        "Gamepiece Preset",
        options=["Custom", "Pollen", "Nectar"],
        index=0
    )

    # Determine default values and disabled state based on selected preset
    is_locked = gamepiece != "Custom"

    if gamepiece == "Pollen":
        default_diameter = 2.8
        default_mass = 25
    elif gamepiece == "Nectar":
        default_diameter = 3.6
        default_mass = 41
    else:
        default_diameter = 7.0
        default_mass = 200

    # Controls lock automatically when a preset is chosen
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

    st.header("Target Positioning")
    target_start_x_mm = st.number_input('Goal Start X [mm]', 0, 4000, 1085, 1)
    target_start_y_mm = st.number_input('Goal Start Y [mm]', 0, 4000, 1358, 1)
    target_end_x_mm = st.number_input('Goal End X [mm]', 0, 8000, 1261, 1)
    target_end_y_mm = st.number_input('Goal End Y [mm]', 0, 8000, 1665, 1)

# ==========================================
# 2. PHYSICS CALCULATIONS
# ==========================================
robot_x_m = float(robot_x_mm) / 1000.0
target_start_x = target_start_x_mm / 1000.0
target_start_y = target_start_y_mm / 1000.0
target_end_x = target_end_x_mm / 1000.0
target_end_y = target_end_y_mm / 1000.0

height_m = height_mm / 1000.0
wheel_Radius_meter = wheel_Radius_inch * 0.0254

# Conversions for drag & spin physics
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
        spin_direction_multiplier = 1.0 if spin_type == "Backspin" else -1.0
        spin_rpm = raw_spin * spin_direction_multiplier
    else:
        base_velocity_ms = wheel_surface_speed
        spin_rpm = 0.0

    velocity_ms = base_velocity_ms * efficiency_multiplier
    return velocity_ms, spin_rpm


def check_line_intersection(p1, p2, q1, q2):
    (x1, y1), (x2, y2) = p1, p2
    (x3, y3), (x4, y4) = q1, q2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(denom) < 1e-9:
        return False, None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return True, (ix, iy)

    return False, None


def compute_trajectory(u, angle_deg, h0, start_x=0.0, g=9.81, drag=True, magnus=True, spin_rpm=0.0):
    theta = math.radians(angle_deg)
    vx, vy = u * math.cos(theta), u * math.sin(theta)

    cd, rho = 0.47, 1.225
    area = math.pi * (ball_radius_m ** 2)
    k_drag = (0.5 * rho * cd * area / ball_mass_kg) if drag else 0.0

    omega = spin_rpm * (2 * math.pi / 60.0)
    spin_sign = 1.0 if omega > 0 else (-1.0 if omega < 0 else 0.0)
    abs_omega = abs(omega)

    dt = 0.002
    x_arr, y_arr = [start_x], [h0]
    x, y = start_x, h0
    hit_target, impact_point = False, None
    goal_p1, goal_p2 = (target_start_x, target_start_y), (target_end_x, target_end_y)

    while y >= 0 and len(x_arr) < 3000:
        v = math.hypot(vx, vy)
        if v < 1e-4:
            break

        ax_drag = -k_drag * v * vx
        ay_drag = -k_drag * v * vy

        ax_mag, ay_mag = 0.0, 0.0
        if magnus and abs_omega > 1e-3:
            spin_ratio = (abs_omega * ball_radius_m) / v
            cl = min(0.5, spin_ratio)
            k_magnus = 0.5 * rho * cl * area / ball_mass_kg

            ax_mag = -k_magnus * v * vy * spin_sign
            ay_mag = k_magnus * v * vx * spin_sign

        ax = ax_drag + ax_mag
        ay = -g + ay_drag + ay_mag

        vx += ax * dt
        vy += ay * dt
        next_x, next_y = x + vx * dt, y + vy * dt

        intersects, pt = check_line_intersection((x, y), (next_x, next_y), goal_p1, goal_p2)
        if intersects:
            x_arr.append(pt[0])
            y_arr.append(pt[1])
            hit_target, impact_point = True, pt
            break

        x, y = next_x, next_y
        x_arr.append(x)
        y_arr.append(y)

    return np.array(x_arr), np.array(y_arr), hit_target, impact_point


# Sweep RPMs from 500 to 8000 in steps of 25; stop after 3 consecutive misses post-hit
scoring_trajectories = []
consecutive_misses = 0

for rpm in range(500, 8001, 25):
    vel_ms, s_rpm = get_launch_params(rpm)
    x_arr, y_arr, hit_target, impact_point = compute_trajectory(
        vel_ms, angle, height_m, robot_x_m, gravity, use_drag, use_magnus, s_rpm
    )
    if hit_target:
        scoring_trajectories.append((rpm, vel_ms, x_arr, y_arr, impact_point))
        consecutive_misses = 0
    elif scoring_trajectories:
        consecutive_misses += 1
        if consecutive_misses >= 3:
            break

# ==========================================
# 3. BUILD PLOTLY GRAPH & RENDER UI
# ==========================================
st.subheader("Shot Calculator Trajectory")

fig_traj = go.Figure()

if scoring_trajectories:
    mid_idx = len(scoring_trajectories) // 2
    grey_legend_shown = False

    # 1. Draw all non-middle scoring trajectories in thin greyish lines
    for idx, (rpm, vel_ms, x_arr, y_arr, impact_point) in enumerate(scoring_trajectories):
        if idx == mid_idx:
            continue

        fig_traj.add_trace(go.Scatter(
            x=x_arr,
            y=y_arr,
            mode='lines',
            name='Other Scoring Paths',
            legendgroup='other_scoring_paths',
            showlegend=not grey_legend_shown,
            line=dict(color='rgba(156, 163, 175, 0.35)', width=1.2),
            hovertemplate=(
                f"<b>{rpm} RPM</b> ({vel_ms:.2f} m/s)<br>"
                "Distance: %{x:.2f} m<br>"
                "Height: %{y:.2f} m<extra></extra>"
            )
        ))
        grey_legend_shown = True

    # 2. Draw the middle scoring trajectory in green on top
    mid_rpm, mid_vel, mid_x, mid_y, mid_impact = scoring_trajectories[mid_idx]
    fig_traj.add_trace(go.Scatter(
        x=mid_x,
        y=mid_y,
        mode='lines',
        name=f'Middle Scoring Path ({mid_rpm} RPM)',
        line=dict(color='#10B981', width=3),
        hovertemplate=(
            f"<b>Middle: {mid_rpm} RPM</b> ({mid_vel:.2f} m/s)<br>"
            "Distance: %{x:.2f} m<br>"
            "Height: %{y:.2f} m<extra></extra>"
        )
    ))

    # 3. Draw greyish impact dots for the outer scoring shots
    other_impacts = [item for idx, item in enumerate(scoring_trajectories) if idx != mid_idx]
    if other_impacts:
        fig_traj.add_trace(go.Scatter(
            x=[item[4][0] for item in other_impacts],
            y=[item[4][1] for item in other_impacts],
            mode='markers',
            name='Other Impacts',
            marker=dict(size=5, color='rgba(156, 163, 175, 0.55)', symbol='circle'),
            customdata=[item[0] for item in other_impacts],
            hovertemplate="<b>%{customdata} RPM</b><br>HIT Point: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
        ))

# Target Goal Line
fig_traj.add_trace(go.Scatter(
    x=[target_start_x, target_end_x],
    y=[target_start_y, target_end_y],
    mode='lines+markers',
    name='Target Goal',
    line=dict(color='#9CA3AF', width=6),
    marker=dict(size=8, color='#9CA3AF'),
    hovertemplate="Goal Point: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
))

# Launcher Node
fig_traj.add_trace(go.Scatter(
    x=[robot_x_m],
    y=[height_m],
    mode='markers',
    name='Launcher',
    marker=dict(size=10, color='#377DFF', symbol='circle-open', line=dict(width=3)),
    hovertemplate="Launcher Location: (%{x:.2f} m, %{y:.2f} m)<extra></extra>"
))

fig_traj.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1D2A3A",
    plot_bgcolor="#1D2A3A",
    xaxis=dict(
        title="Distance (m)",
        gridcolor="rgba(255, 255, 255, 0.08)",
        showgrid=True,
        zerolinecolor="rgba(255, 255, 255, 0.15)",
        rangemode="tozero",
        dtick=0.5,
        minor=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.02)",
            dtick="0.3"
        )
    ),
    yaxis=dict(
        title="Height (m)",
        gridcolor="rgba(255, 255, 255, 0.08)",
        showgrid=True,
        zerolinecolor="rgba(255, 255, 255, 0.15)",
        rangemode="tozero",
        scaleanchor="x",
        scaleratio=1,
        dtick=0.5,
        minor=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.02)",
            dtick="0.3"
        )
    ),
    margin=dict(l=20, r=20, t=30, b=20),
    height=600
)

st.markdown(
    """
    <style>
    div[data-testid="stPlotlyChart"] {
        border-radius: 75px !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stPlotlyChart"] > div {
        border-radius: 16px !important;
        overflow: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.plotly_chart(fig_traj, use_container_width=True)

# Summary Metrics for Scoring RPMs
col1, col2, col3 = st.columns(3)
if scoring_trajectories:
    min_rpm = scoring_trajectories[0][0]
    max_rpm = scoring_trajectories[-1][0]
    mid_rpm, mid_vel = scoring_trajectories[len(scoring_trajectories) // 2][:2]
    col1.metric("Middle Scoring RPM", f"{mid_rpm} RPM ({mid_vel:.2f} m/s)")
    col2.metric("Scoring RPM Range", f"{min_rpm} – {max_rpm} RPM")
    col3.metric("Valid Steps Found", f"{len(scoring_trajectories)} (Δ25 RPM)")
else:
    col1.metric("Middle Scoring RPM", "None found")
    col2.metric("Scoring RPM Range", "—")
    col3.metric("Valid Steps Found", "0")