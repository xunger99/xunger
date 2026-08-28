#!/usr/bin/env python3
from pathlib import Path
import json
import re
import shutil
import sys
import zipfile
import html

ROOT = Path.cwd()
def nav_html() -> str:
    return """<header class="site-header">
    <a class="brand" href="index.html">
      <span class="logo">AI</span>
      <span>
        <strong>AI-Enabled Control Engineering</strong>
        <small>PKU GLOBEX Summer Program</small>
      </span>
    </a>
    <nav class="nav-links">
      <a href="index.html">Home</a>
      <a href="schedule.html">Schedule</a>
      <a href="lectures.html">Slides</a>
      <a href="code.html">RIP Code</a>
      <a href="ros2-platform.html">ROS2 Platform</a>
      <a href="tasks.html">Lab Tasks</a>
      <a href="resources.html">Resources</a>
      <a href="staff.html">Staff</a>
    </nav>
  </header>"""


def page_html() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ROS2 RIP Platform · AI-Enabled Control Engineering</title>
  <link rel="stylesheet" href="assets/css/styles.css">
  <script src="assets/js/course-data.js" defer></script>
  <script src="assets/js/main.js" defer></script>
</head>
<body>
  {nav_html()}

  <main class="container page ros2-page">
    <section class="ros2-hero">
      <span class="kicker">Optional Exploration</span>
      <h1>ROS2-Based Rotary Inverted Pendulum Platform</h1>
      <p class="lead">
        This page is provided for interested students who want to explore how a physical rotary inverted
        pendulum can be organized as a ROS2 system. It is not required for the core course assessment,
        but it offers a practical route from embedded control to distributed robotic software.
      </p>
      <div class="notice">
        <strong>Code access.</strong>
        Download the ROS2 package here or receive it through the course group.
      </div>
      <div class="downloads">
        <a class="download-btn" href="downloads/code/RIP_ROS2_Optional_Platform_Code.zip" download>Download ROS2 Code</a>
        <a class="download-btn ghost" href="downloads/code/RIP_Complete_Course_Code.zip" download>Download All RIP Code</a>
        <a class="download-btn ghost" href="#quick-start">Quick Start</a>
      </div>
    </section>

    <section class="ros2-grid">
      <article class="ros2-card">
        <h2>Why ROS2?</h2>
        <p>
          In the basic RIP experiments, the STM32 board performs real-time sensing and low-level control.
          ROS2 adds a higher-level software layer on the PC: serial communication, state publishing,
          command management, visualization, and experiment logging can be separated into independent nodes.
        </p>
      </article>

      <article class="ros2-card">
        <h2>System architecture</h2>
        <p>
          The platform follows a PC--STM32 structure. The STM32 sends sensor and controller data through
          a high-speed serial link. The PC receives these logs, converts them into ROS2 messages, manages
          commands, and displays real-time 2D/3D visual feedback.
        </p>
      </article>
    </section>

    <section class="ros2-section">
      <h2>Workspace structure</h2>
      <div class="module-list">
        <article>
          <h3>rip_interfaces</h3>
          <p>Defines <code>RipState.msg</code> and <code>RipCommand.msg</code> for state feedback and command transmission.</p>
        </article>
        <article>
          <h3>rip_serial_bridge</h3>
          <p>Reads STM32 serial logs, publishes <code>/rip/state</code>, and forwards start/stop commands to the board.</p>
        </article>
        <article>
          <h3>rip_manager</h3>
          <p>Provides a management layer for control modes, stable-control settings, and exported RL network headers.</p>
        </article>
        <article>
          <h3>rip_visualizer</h3>
          <p>Implements the ground-control interface with live angle display, PWM monitoring, plots, and 3D animation.</p>
        </article>
        <article>
          <h3>rip_bringup</h3>
          <p>Provides the launch file that starts the serial bridge, manager, and visualizer together.</p>
        </article>
      </div>
    </section>

    <section class="ros2-section">
      <h2>ROS2 data flow</h2>
      <div class="flow">
        <div>STM32 firmware<br><small>sensor logs / PWM / mode</small></div>
        <span>→</span>
        <div>rip_serial_bridge<br><small>serial to ROS2 messages</small></div>
        <span>→</span>
        <div>/rip/state<br><small>theta, alpha, velocities, PWM</small></div>
        <span>→</span>
        <div>rip_visualizer<br><small>GUI, plots, 3D view</small></div>
      </div>
      <p>
        Commands flow in the reverse direction through <code>/rip/cmd</code> or <code>/rip/raw_cmd</code>.
        The bridge converts high-level commands such as GO and STOP into serial commands sent to the STM32.
      </p>
    </section>

    <section class="ros2-section" id="quick-start">
      <h2>Quick-start tutorial</h2>
      <ol class="steps">
        <li>
          <strong>Install ROS2 and Python dependencies.</strong>
          The workspace was prepared for a ROS2 Python workflow. Students should install ROS2, <code>colcon</code>,
          <code>pyserial</code>, <code>PyQt5</code>, <code>numpy</code>, and <code>matplotlib</code> on the experiment PC.
        </li>
        <li>
          <strong>Download and extract the ROS2 code package.</strong>
          Download the <a href="downloads/code/RIP_ROS2_Optional_Platform_Code.zip" download>ROS2 ZIP package</a>
          from this website or obtain it through the course group, then open the included workspace.
          <pre><code>unzip RIP_ROS2_Optional_Platform_Code.zip
cd RIP_ROS2_Optional_Platform_Code/ros2/rip_ros2_ws</code></pre>
        </li>
        <li>
          <strong>Build the ROS2 packages.</strong>
          <pre><code>source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash</code></pre>
        </li>
        <li>
          <strong>Connect the STM32 board.</strong>
          Check the serial device, for example <code>/dev/ttyACM0</code> or <code>/dev/ttyUSB0</code>.
          The default launch file uses <code>/dev/ttyACM0</code> and a baud rate of <code>921600</code>.
        </li>
        <li>
          <strong>Launch the platform.</strong>
          <pre><code>ros2 launch rip_bringup rip.launch.py port:=/dev/ttyACM0 baud:=921600</code></pre>
        </li>
        <li>
          <strong>Observe the state topics.</strong>
          <pre><code>ros2 topic list
ros2 topic echo /rip/state</code></pre>
        </li>
      </ol>
    </section>

    <section class="ros2-section warning-panel">
      <h2>Safety notes</h2>
      <p>
        Always keep the rotary arm clear before enabling the motor. Start with a conservative PWM limit,
        check sensor signs before closing the loop, and use the GUI STOP command immediately if the pendulum
        falls or the motor response is abnormal. This ROS2 page is intended for exploration and debugging,
        not for unsupervised operation.
      </p>
    </section>

    <section class="ros2-section">
      <h2>Suggested student exploration</h2>
      <ul class="clean">
        <li>Visualize <code>/rip/state</code> and compare ROS2 timestamps with STM32 timing logs.</li>
        <li>Modify the GUI layout to display only selected variables such as <code>alpha</code>, <code>theta</code>, and <code>pwm</code>.</li>
        <li>Record data from GO to STOP and generate publication-quality plots for controller comparison.</li>
        <li>Compare LQR, MPC, and exported RL policies under the same ROS2 logging interface.</li>
        <li>Extend the workspace for remote experiments, where the RIP hardware stays in the lab while the student monitors data from another computer.</li>
      </ul>
    </section>
  </main>

  <footer class="site-footer">
    <strong>AI-Enabled Control Engineering</strong>
    <span>GLOBEX Summer Program · College of Engineering, Peking University</span>
    <span>Instructor: Xun Huang · TAs: Zhixiang Ju, Haozhe Wang</span>
  </footer>
</body>
</html>
"""


def write_page():
    (ROOT / "ros2-platform.html").write_text(page_html(), encoding="utf-8")
    print("created: ros2-platform.html")


def update_nav_links():
    for p in ROOT.glob("*.html"):
        if p.name == "ros2-platform.html":
            continue
        s = p.read_text(encoding="utf-8")
        if "ros2-platform.html" in s:
            continue
        if '<a href="code.html">RIP Code</a>' in s:
            s = s.replace(
                '<a href="code.html">RIP Code</a>',
                '<a href="code.html">RIP Code</a>\n      <a href="ros2-platform.html">ROS2 Platform</a>',
                1
            )
            p.write_text(s, encoding="utf-8")
            print(f"updated nav: {p.name}")
        else:
            print(f"WARNING: did not find RIP Code nav link in {p.name}")


def append_css_once():
    css_path = ROOT / "assets" / "css" / "styles.css"
    marker = "ros2-platform-page"
    css = css_path.read_text(encoding="utf-8")
    if marker in css:
        print("CSS already contains ROS2 platform styles")
        return
    css += """

/* ===== ros2-platform-page ===== */
.ros2-page {
  max-width: 1120px;
}

.ros2-hero {
  position: relative;
  overflow: hidden;
  border-radius: 30px;
  padding: 42px;
  margin-bottom: 28px;
  color: #0f172a;
  border: 1px solid rgba(148, 163, 184, 0.30);
  background:
    radial-gradient(circle at 92% 12%, rgba(35,58,139,0.20), transparent 34%),
    linear-gradient(135deg, #ffffff 0%, #f8fafc 58%, #fff7ed 100%);
  box-shadow: 0 20px 54px rgba(15, 23, 42, 0.10);
}

.ros2-hero h1 {
  max-width: 820px;
  margin: 10px 0 14px;
  font-size: clamp(36px, 6vw, 64px);
  line-height: 0.96;
  letter-spacing: -0.055em;
  color: var(--pku-red);
}

.ros2-hero .lead {
  max-width: 820px;
  color: #475569;
  font-size: 18px;
  line-height: 1.7;
}

.download-btn.ghost {
  background: #ffffff;
  color: var(--pku-red);
  border-color: rgba(140, 21, 21, 0.35);
}

.ros2-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin: 26px 0;
}

.ros2-card,
.ros2-section {
  border: 1px solid rgba(148, 163, 184, 0.30);
  background: #ffffff;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
}

.ros2-card h2,
.ros2-section h2 {
  margin: 0 0 12px;
  color: #111827;
  letter-spacing: -0.025em;
}

.ros2-card p,
.ros2-section p,
.steps li {
  color: #475569;
  line-height: 1.68;
}

.ros2-section {
  margin: 22px 0;
}

.module-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.module-list article {
  border-radius: 18px;
  padding: 18px;
  background: #f8fafc;
  border: 1px solid rgba(226, 232, 240, 0.95);
}

.module-list h3 {
  margin: 0 0 8px;
  color: var(--pku-red);
}

.flow {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
  align-items: center;
  gap: 10px;
  margin: 18px 0;
}

.flow div {
  min-height: 84px;
  border-radius: 18px;
  background: linear-gradient(135deg, #f8fafc, #eef2ff);
  border: 1px solid rgba(148, 163, 184, 0.28);
  padding: 16px;
  font-weight: 900;
  color: #0f172a;
}

.flow small {
  display: block;
  margin-top: 6px;
  font-weight: 650;
  color: #64748b;
}

.flow span {
  color: var(--pku-red);
  font-weight: 950;
  font-size: 24px;
}

.steps {
  padding-left: 22px;
}

.steps li {
  margin: 14px 0;
}

pre {
  overflow-x: auto;
  border-radius: 16px;
  padding: 14px 16px;
  background: #0f172a;
  color: #e5e7eb;
}

code {
  border-radius: 7px;
  padding: 2px 6px;
  background: #f1f5f9;
  color: #8c1515;
  font-weight: 700;
}

pre code {
  background: transparent;
  color: inherit;
  padding: 0;
}

.warning-panel {
  border-color: rgba(217, 119, 6, 0.30);
  background: linear-gradient(135deg, #fffbeb, #ffffff);
}

@media (max-width: 900px) {
  .ros2-grid,
  .module-list {
    grid-template-columns: 1fr;
  }

  .flow {
    grid-template-columns: 1fr;
  }

  .flow span {
    text-align: center;
    transform: rotate(90deg);
  }

  .ros2-hero {
    padding: 28px;
  }
}
"""
    css_path.write_text(css, encoding="utf-8")
    print("updated: assets/css/styles.css")


def main():
    if not (ROOT / "assets" / "css" / "styles.css").exists():
        raise SystemExit("Run this script from the furuta_lab repository root, for example: cd ~/Desktop/furuta_lab")

    write_page()
    update_nav_links()
    append_css_once()

    print("\nDone. Preview:")
    print("  python3 -m http.server 8000")
    print("  http://localhost:8000/ros2-platform.html")
    print("\nThen commit:")
    print("  git add -A")
    print('  git commit -m "Add optional ROS2 RIP platform page"')
    print("  git push origin main")


if __name__ == "__main__":
    main()
