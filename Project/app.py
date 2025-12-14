import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any

# =====================================================
# 1. TECHNICAL GAS SAFETY LOGIC (Machine / Calibration)
# =====================================================

def analyze_gas_mixer(
    flow_o2: float,
    flow_n2o: float,
    flow_air: float,
    agent_perc: float
) -> Dict[str, Any]:

    alerts = []
    warnings = []
    category = "SAFE"
    final_status = "PASS"

    total_flow = flow_o2 + flow_n2o + flow_air

    # CRITICAL: No flow
    if total_flow == 0:
        return {
            "status": "FAIL",
            "category": "CRITICAL",
            "metrics": {"fio2": 0, "total_flow": 0},
            "alerts": ["CRITICAL: No fresh gas flow detected."],
            "warnings": [],
            "timestamp": datetime.now().isoformat()
        }

    oxygen_volume = flow_o2 + (flow_air * 0.21)
    fio2_percent = (oxygen_volume / total_flow) * 100

    # CRITICAL: Hypoxic mixture
    if fio2_percent < 25.0:
        category = "CRITICAL"
        final_status = "FAIL"
        alerts.append(
            f"Hypoxic mixture detected: FiO₂ = {fio2_percent:.1f}% (< 25%)."
        )

    # WARNING: Low flow
    if total_flow < 0.5:
        if category != "CRITICAL":
            category = "WARNING"
        warnings.append(
            "Low fresh gas flow (< 0.5 L/min). Risk of CO₂ rebreathing."
        )

    # WARNING: High agent concentration
    if agent_perc > 8.0:
        if category != "CRITICAL":
            category = "WARNING"
        warnings.append(
            f"High anesthetic concentration ({agent_perc}%)."
        )

    return {
        "status": final_status,
        "category": category,
        "metrics": {
            "fio2": fio2_percent,
            "total_flow": total_flow
        },
        "alerts": alerts,
        "warnings": warnings,
        "timestamp": datetime.now().isoformat()
    }

# =====================================================
# 2. CLINICAL SETUP & OPERATION (Patient-Specific Logic)
# =====================================================

def clinical_adjustment(
    fio2: float,
    agent_perc: float,
    patient: Dict[str, Any]
) -> list:

    clinical_warnings = []

    # Patient-specific minimum FiO2
    recommended_fio2 = 25.0

    if patient["age"] < 1 or patient["age"] > 65:
        recommended_fio2 = 30.0

    if patient["asa"] >= 3:
        recommended_fio2 = 30.0

    if fio2 < recommended_fio2:
        clinical_warnings.append(
            f"Patient-specific FiO₂ recommendation: ≥ {recommended_fio2}%."
        )

    # Agent sensitivity
    if (patient["age"] > 65 or patient["weight"] < 50) and agent_perc > 6.0:
        clinical_warnings.append(
            "Elderly / low-weight patient may be sensitive to high anesthetic dose."
        )

    # Lung compliance
    if patient["compliance"] < 30:
        clinical_warnings.append(
            "Low lung compliance. Monitor airway pressure closely."
        )

    return clinical_warnings

# =====================================================
# 3. STREAMLIT USER INTERFACE
# =====================================================

def main():
    st.set_page_config(page_title="Anesthesia Safety Monitor", layout="wide")
    st.title("Anesthesia Workstation – Gas Safety & Clinical Monitor")

    # -------------------------------
    # Sidebar: Gas Controls
    # -------------------------------
    st.sidebar.header("Fresh Gas Flow")

    flow_o2 = st.sidebar.slider("O₂ (L/min)", 0.0, 10.0, 2.0, 0.1)
    flow_n2o = st.sidebar.slider("N₂O (L/min)", 0.0, 10.0, 2.0, 0.1)
    flow_air = st.sidebar.slider("Air (L/min)", 0.0, 10.0, 0.0, 0.1)

    st.sidebar.header("Vaporizer")
    agent = st.sidebar.slider("Sevoflurane (%)", 0.0, 10.0, 2.0, 0.1)

    # -------------------------------
    # Sidebar: Patient Clinical Setup
    # -------------------------------
    st.sidebar.markdown("---")
    st.sidebar.header("Patient Clinical Setup")

    age = st.sidebar.number_input("Age (years)", 0, 120, 30)
    weight = st.sidebar.number_input("Weight (kg)", 1, 200, 70)
    compliance = st.sidebar.slider("Lung Compliance (mL/cmH₂O)", 10, 100, 50)
    asa = st.sidebar.selectbox("ASA Class", [1, 2, 3, 4])

    patient = {
        "age": age,
        "weight": weight,
        "compliance": compliance,
        "asa": asa
    }

    # -------------------------------
    # Analysis
    # -------------------------------
    result = analyze_gas_mixer(flow_o2, flow_n2o, flow_air, agent)

    clinical_warnings = clinical_adjustment(
        fio2=result["metrics"]["fio2"],
        agent_perc=agent,
        patient=patient
    )

    result["warnings"].extend(clinical_warnings)

    # -------------------------------
    # Display Status
    # -------------------------------
    color = "green"
    if result["category"] == "WARNING":
        color = "orange"
    elif result["category"] == "CRITICAL":
        color = "red"

    st.markdown(f"""
    <div style="padding:15px;border-left:8px solid {color};
    background-color:#f9f9f9;border-radius:8px;">
    <h2 style="color:{color};margin:0;">
    SYSTEM STATUS: {result['status']} ({result['category']})
    </h2>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # Metrics
    # -------------------------------
    m1, m2, m3 = st.columns(3)
    m1.metric("FiO₂ (%)", f"{result['metrics']['fio2']:.1f}")
    m2.metric("Total Flow (L/min)", f"{result['metrics']['total_flow']:.1f}")
    m3.metric("Agent (%)", f"{agent}")

    # -------------------------------
    # Alerts & Warnings
    # -------------------------------
    st.subheader("Diagnostic Log")

    if not result["alerts"] and not result["warnings"]:
        st.success("System operating within safe clinical limits.")

    for alert in result["alerts"]:
        st.error(f"🛑 {alert}")

    for warn in result["warnings"]:
        st.warning(f"⚠ {warn}")

    # -------------------------------
    # Gas Composition Chart
    # -------------------------------
    st.subheader("Gas Composition")
    df = pd.DataFrame({
        "Gas": ["Oxygen", "Nitrous Oxide", "Air"],
        "Flow (L/min)": [flow_o2, flow_n2o, flow_air]
    })
    st.bar_chart(df, x="Gas", y="Flow (L/min)")

    # -------------------------------
    # Logic Explanation
    # -------------------------------
    with st.expander("ℹ System Logic Summary"):
        st.markdown("""
        *Technical Safety (ISO-based concepts):*
        - FiO₂ < 25% → CRITICAL
        - Total flow = 0 → CRITICAL
        - Low flow < 0.5 L/min → WARNING
        - Agent > 8% → WARNING

        *Clinical Operation:*
        - Patient age, ASA, weight, and lung compliance modify warnings
        - No effect on sensor calibration
        """)

if __name__ == "__main__":
    main()