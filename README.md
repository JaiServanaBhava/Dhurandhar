<div align="center" {box-sizing: border-box;}>
  <img src="https://github.com/JaiServanaBhava/Dhurandhar/blob/main/Logo.png" alt="Dhurandhar Logo" width="160">
  <h1>Dhurandhar v3.0</h1>
  <p align="center">
    <b>The Ultimate Zero-Config Lab Peripheral Security & Endpoint Lock Enforcement Engine</b>
    <br />
    <i>Protect your infrastructure seamlessly. Silent. Inescapable. Professional.</i>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Engine-PnP_Hardware_Bus-black?style=for-the-badge&logo=windows" alt="PnP Engine">
    <img src="https://img.shields.io/badge/Architecture-Asynchronous_Threaded-orange?style=for-the-badge" alt="Async">
    <img src="https://img.shields.io/badge/UI-Flashing_Lockscreen-brightgreen?style=for-the-badge" alt="UI">
  </p>

  <a href="https://drive.google.com/file/d/1x6Ax7nffwZu_Nj8t9OtAtklN-2vTHaXy/view?usp=sharing">
    <img src="https://img.shields.io/badge/DOWNLOAD-DHURANDHAR_EXE-blueviolet?style=for-the-badge&logo=github&logoColor=white" alt="Download EXE">
  </a>

  <h4>
    <a href="#-key-advantages">Advantages</a> •
    <a href="#-feature-suite">Features</a> •
    <a href="#-screenshots">Screenshots</a> •
    <a href="#-installation--setup">Installation</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </h4>
</div>

---

## 🌟 Why Dhurandhar v3.0?

Traditional lab monitoring software is easily bypassed by smart students using mobile devices or fixed external storage profiles. **Dhurandhar v3.0** is custom-engineered to eliminate those security blind spots. It relies on direct kernel-level hardware notification hooks rather than fragile file-system scanners. Once an unauthorized volume or device is introduced, it isolates the machine instantly, operating with zero taskbar visibility and total persistence against system tampering.

### 💎 Key Advantages
* **Zero Setup Deployment:** Fully autonomous installation framework. Run the executable once on any system to register global, background-enforced persistence.
* **Plug-and-Play Level Detection:** Replaces basic letter scanning with full Plug-and-Play (PnP) hardware bus tracking to block devices that don't mount traditional drive letters.
* **Tamper-Proof Persistence:** The lock state is tracked continuously via localized JSON layers on disk, completely surviving forceful hard resets or system restarts.
* **Silent Execution Profile:** Runs completely headless with no console visibility, taskbar footprint, or system tray icon to hide from standard local users.
* **100% Portable Build:** Packaged cleanly as a single standalone executable file without requiring any target machine dependencies.

---

## 🛠 Feature Suite

### 📡 Hardware Bus Level Tracking
* **Mobile MTP Interception:** Successfully flags mobile phones connected via USB data lines by monitoring the Windows Portable Devices (WPD) class.
* **Fixed SSD Masking Block:** Captures high-speed external drives and partitions even if firmware registers them as fixed local disks rather than removable media.
* **Automated Drive Ejection:** Actively sends an asynchronous low-level command block to forcefully unmount and isolate the invading volume before system access occurs.

### 🔒 Inescapable UI Isolation
* **Rapid Warning System:** Launches a full-screen, topmost warning canvas that cycles high-frequency yellow and orange visual alerts to draw supervisor attention.
* **Low-Level Key Swallowing:** Installs a driver-level low-level keyboard hook to capture and discard Windows key inputs, making the Start Menu unusable.
* **Escape Route Blocking:** Complete programmatic interception of standard escape combinations, including `Alt + F4`, `Alt + Tab`, `Escape`, and `Ctrl + Esc`.

### 📁 Log Management & Self-Deploy
* **Automated Path Normalization:** Detects its launching folder and automatically installs its binary footprint safely to `C:\Dhurandhar\Dhurandhar.exe`.
* **All-Users Startup Setup:** Generates system-wide startup shortcuts automatically via silent PowerShell executions to ensure security triggers on any account login.
* **Serialized Activity Tracking:** Maintains a reliable timestamp log text file locally to trace operational milestones, intrusion events, and administrative overrides.

---

## 📸 Screenshots
*Insert your project screenshots here to showcase the system UI configuration.*

<div align="center">
  <table style="border: none;">
    <tr>
      <td><img src="https://github.com/JaiServanaBhava/Dhurandhar/blob/main/screenshots/screenshot1.png" alt="Lockscreen Block" width="250"></td>
      <td><img src="https://github.com/JaiServanaBhava/Dhurandhar/blob/main/screenshots/screenshot2.png" alt="Log Generation" width="250"></td>
    </tr>
  </table>
</div>

---

## 🚀 Installation & Setup

### 📦 Portable Setup (Fastest)
1.  **Download:** Grab the standalone `Dhurandhar.exe` assembly using the build badge at the top page layout.
2.  **Launch:** Execute the binary directly as an Administrator.
3.  **Self-Deployment:** The file automatically builds its root environment inside `C:\Dhurandhar\` and deploys its configuration to the system-wide Common Windows Startup directory.
4.  **Enforcement Status:** It runs hidden in the background. The application will activate if an unauthorized phone or USB storage option is inserted into the physical layout.
5.  **Administrative Credentials:** * The hardcoded system **Unlock Password** is `23173cm005`.
    * *Administrative Emergency Override:* Press `Ctrl + Shift + 5` to immediately release shields and terminate surveillance safely.
    * *Process Force-Termination:* Press `Ctrl + Shift + Esc` to drop an immediate terminal kill command on all engine processes.

### 💻 Developer Testing Mode
```bash
# Clone the repository structure
git clone [https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git)
cd Dhurandhar

# Package into standard standalone background form-factor
python -m PyInstaller lab_security_monitor.spec --clean --noconfirm
