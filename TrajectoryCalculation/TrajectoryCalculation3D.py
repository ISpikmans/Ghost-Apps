import json
import math
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

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
    }

    /* 6. Transparent Borderless Metric Cards */
    [data-testid="stMetric"] {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0px !important;
        padding: 0.75rem 0rem !important;
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
    """,
    unsafe_allow_html=True
)

# ==========================================
# 1. SIDEBAR CONFIGURATION
# ==========================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.75rem;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C7.58172 2 4 5.58172 4 10V20.5C4 21.15 4.75 21.52 5.27 21.13L8 19.08L10.4 20.88C10.76 21.15 11.24 21.15 11.6 20.88L12 20.58L12.4 20.88C12.76 21.15 13.24 21.15 13.6 20.88L16 19.08L18.73 21.13C19.25 21.52 20 21.15 20 20.5V10C20 5.58172 16.4183 2 12 2Z" fill="#FFFFFF"/>
                <circle cx="9.5" cy="10.5" r="1.4" fill="#000000"/>
                <circle cx="14.5" cy="10.5" r="1.4" fill="#000000"/>
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

    efficiency_loss = st.slider('Efficiency Loss [%]', 0.0, 50.0, 10.0, 0.5)
    pitch_deg = st.slider('Pitch Angle [deg]', 1.0, 90.0, 45.0, 0.5)
    yaw_deg = st.slider(
        'Turret Yaw Angle [deg]', -45.0, 45.0, 0.0, 0.5,
        disabled=not is_3d
    )
    wheel_Radius_inch = st.slider('Wheel Radius [inch]', 0.5, 6.0, 3.0, 0.1)

    st.header("Launch Position")
    robot_x_mm = st.number_input('Robot X [mm]', 0.0, 3600.0, 0.0, 10.0)
    robot_y_mm = st.number_input(
        'Robot Lateral Y [mm]', -2000.0, 2000.0, 0.0, 10.0,
        disabled=not is_3d
    )
    height_mm = st.number_input('Launch Height Z [mm]', 0.0, 2000.0, 365.0, 5.0)

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
active_yaw_deg = yaw_deg if is_3d else 0.0
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
    # Precompute unit sphere geometry for physically-scaled 3D ball
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

    max_x_range = max(2.0, goal_x2 + 0.5, robot_x_m + 0.5)
    max_z_range = max(2.0, goal_z2 + 0.5, height_m + 0.5)
    y_bound = max(1.0, abs(goal_y_center) + goal_half_w + 0.4, abs(robot_y_m) + 0.4)

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