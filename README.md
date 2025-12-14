# Anesthesia Workstation Safety Monitor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)

> A real-time medical device simulation that monitors gas delivery safety, calculates FiO₂ levels, and applies patient-specific clinical logic to prevent hypoxic mixtures during anesthesia.

---

## 📸 Interface Preview
<img width="624" height="314" alt="image" src="https://github.com/user-attachments/assets/fb099dd6-0bba-47d9-9b17-bec8efdb9f3f" />

---

## 📝 Project Overview

This project simulates the control software of a modern **Anesthesia Gas Mixer**. It serves as a decision support system that bridges the gap between mechanical flow controls and patient safety.

The application calculates the **Fraction of Inspired Oxygen (FiO₂)** in real-time based on the input of Oxygen, Nitrous Oxide, and Medical Air. It cross-references these values against **ISO 80601-2-13** safety standards and adjusts alarm thresholds based on patient demographics (Age, Weight, ASA Class).

### Key Features
* **Fresh Gas Flow Analysis:** Real-time mixing of $O_2$, $N_2O$, and Air.
* **Hypoxic Guard Logic:** Automatically flags mixtures where oxygen concentration drops below 25%.
* **Clinical Context Engine:** Adjusts safety warnings based on patient age, lung compliance, and health status (ASA).
* **Dynamic Visual Status:** Immediate Green/Orange/Red feedback loop for the operator.

---

## ⚙️ Technical Logic & Standards

This software implements logic derived from medical standards for Anesthetic Workstations.

### 1. The Hypoxic Guard (ISO 80601-2-13)
The system ensures the patient never receives a hypoxic mixture (insufficient oxygen). The FiO₂ is calculated using the weighted average of oxygen sources:

$$FiO_2 = \frac{Flow_{O2} + (Flow_{Air} \times 0.21)}{Total Flow} \times 100$$

* **CRITICAL FAIL:** If $FiO_2 < 25\%$ (Standard limit).
* **CLINICAL WARNING:** If $FiO_2 < 30\%$ for elderly patients or ASA III+ (High-risk logic).

### 2. Low Flow Anesthesia
To prevent rebreathing of CO₂ in semi-closed circuits without adequate scrubbing, the system triggers a warning if:
* $Total Flow < 0.5 \text{ L/min}$

---

## 🚀 Installation & Usage

To run this application locally, follow these steps:

### Prerequisites
* Python 3.8 or higher
* pip (Python package manager)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/anesthesia-safety-monitor.git](https://github.com/your-username/anesthesia-safety-monitor.git)
    cd anesthesia-safety-monitor
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

4.  **View in Browser:**
    The app will automatically open at `http://localhost:8501`.

---

## 📂 File Structure

```text
anesthesia-safety-monitor/
├── app.py                # Main application logic (Streamlit)
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── screenshot.png        # Application preview image
