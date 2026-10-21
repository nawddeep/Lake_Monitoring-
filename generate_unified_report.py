import os
import subprocess
from pathlib import Path

workspace_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot")
html_path = workspace_dir / "Fateh_Sagar_Lake_Smart_Monitoring_Report.html"
pdf_path = workspace_dir / "Fateh_Sagar_Lake_Smart_Monitoring_Report.pdf"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Fateh Sagar Lake Smart Water & Health Surveillance System: Phase 1 Specification</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 8.7pt;
    line-height: 1.4;
  }

  .page-container {
    page-break-after: always;
    break-after: page;
    min-height: 98vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .page-container:last-child {
    page-break-after: avoid;
    break-after: avoid;
  }

  /* Header Cover / Hero */
  .doc-header {
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }

  .badge-row {
    display: flex;
    gap: 6px;
    margin-bottom: 6px;
  }

  .badge {
    display: inline-block;
    padding: 2px 7px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 4px;
  }

  .badge-blue { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
  .badge-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
  .badge-amber { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }

  h1.doc-title {
    font-size: 15.5pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.18;
    margin-bottom: 3px;
    letter-spacing: -0.4px;
  }

  .doc-subtitle {
    font-size: 8.8pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 8px;
  }

  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 7.5pt;
    gap: 8px;
  }

  .meta-item strong {
    display: block;
    color: #64748b;
    font-size: 6.8pt;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  .meta-item span {
    color: #0f172a;
    font-weight: 600;
  }

  /* Section Styling */
  h2.sec-heading {
    font-size: 10.5pt;
    font-weight: 750;
    color: #0f172a;
    border-left: 3.5px solid #0284c7;
    padding-left: 6px;
    margin-top: 10px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    letter-spacing: -0.2px;
  }

  h3.sub-heading {
    font-size: 9pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 8px;
    margin-bottom: 4px;
  }

  p {
    margin-bottom: 5px;
    color: #334155;
    text-align: justify;
  }

  /* Stat Cards */
  .stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin: 8px 0;
  }

  .stat-card {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 5px;
    padding: 6px 8px;
    text-align: center;
  }

  .stat-number {
    font-size: 13pt;
    font-weight: 800;
    color: #0369a1;
    line-height: 1.1;
  }

  .stat-label {
    font-size: 7pt;
    color: #475569;
    font-weight: 600;
    margin-top: 2px;
  }

  /* Callout boxes */
  .callout {
    background: #f8fafc;
    border-left: 3.5px solid #0284c7;
    border-radius: 0 5px 5px 0;
    padding: 6px 10px;
    margin: 7px 0;
    font-size: 7.9pt;
  }

  .callout.alert {
    background: #fff7ed;
    border-left-color: #f97316;
  }

  .callout.success {
    background: #f0fdf4;
    border-left-color: #22c55e;
  }

  .callout.info {
    background: #f0f9ff;
    border-left-color: #0284c7;
  }

  .callout-title {
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 7.6pt;
  }

  th, td {
    border: 1px solid #cbd5e1;
    padding: 4px 6px;
    text-align: left;
    vertical-align: middle;
  }

  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    font-size: 7.1pt;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  tr:nth-child(even) td {
    background: #f8fafc;
  }

  .highlight-row td {
    background: #e0f2fe !important;
    font-weight: 600;
    color: #0369a1;
    border-top: 1.5px solid #0284c7;
    border-bottom: 1.5px solid #0284c7;
  }

  /* Cards Grid */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin: 7px 0;
  }

  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
    margin: 7px 0;
  }

  .info-card {
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 8px;
    background: #ffffff;
    border-left: 3px solid #0284c7;
  }

  .info-card-title {
    font-weight: 700;
    font-size: 8pt;
    color: #0369a1;
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
  }

  .info-card-desc {
    font-size: 7.2pt;
    color: #475569;
    line-height: 1.3;
  }

  /* Workflow Steps */
  .step-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
    margin: 8px 0;
  }

  .step-card {
    border: 1px solid #e2e8f0;
    border-top: 2.5px solid #0284c7;
    background: #ffffff;
    border-radius: 5px;
    padding: 7px 8px;
  }

  .step-num {
    display: inline-block;
    width: 18px;
    height: 18px;
    background: #0284c7;
    color: #ffffff;
    border-radius: 50%;
    text-align: center;
    line-height: 18px;
    font-size: 7pt;
    font-weight: 700;
    margin-bottom: 4px;
  }

  .step-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
  }

  .step-desc {
    font-size: 7.2pt;
    color: #64748b;
    line-height: 1.3;
  }

  .page-footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 5px;
    font-size: 7pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
  }
</style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="page-container">
    <div>
      <div class="doc-header">
        <div class="badge-row">
          <span class="badge badge-blue">Udaipur Smart Cities & Techno India NJR Pilot</span>
          <span class="badge badge-green">Phase 1 Engineering Specification</span>
          <span class="badge badge-amber">AarogyaJal Platform Integration</span>
        </div>
        <h1 class="doc-title">Fateh Sagar Lake Smart Water & Health Surveillance System</h1>
        <div class="doc-subtitle">Integrated Sensor Selection, Hardware Architecture, Disease Detection & Telemetry Blueprint</div>
        
        <div class="meta-grid">
          <div class="meta-item">
            <strong>Lead Authors</strong>
            <span>Nawdeep & Manan Ramani</span>
          </div>
          <div class="meta-item">
            <strong>Target Site</strong>
            <span>Fateh Sagar Lake, Udaipur, Rajasthan</span>
          </div>
          <div class="meta-item">
            <strong>Affiliation</strong>
            <span>Techno India NJR / Aarogya Jal</span>
          </div>
          <div class="meta-item">
            <strong>Deployment Date</strong>
            <span>October 2026</span>
          </div>
        </div>
      </div>

      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-number">6 Probes</div>
          <div class="stat-label">Core Continuous Array</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">10 Minutes</div>
          <div class="stat-label">Telemetry Ingestion Rate</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">48 Hours</div>
          <div class="stat-label">Solar Battery Autonomy</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">4G LTE</div>
          <div class="stat-label">Encrypted TLS Ingestion</div>
        </div>
      </div>

      <h2 class="sec-heading">1. Purpose, Scope & Resolution of Deployment Parameters</h2>
      <p>
        This document integrates the <em>Phase 1 Sensor Selection Report</em> authored by Nawdeep with the complete <em>Aarogya Jal Telemetry, ML & Public Health Architecture</em>. It resolves all open scope parameters for deployment at <strong>Fateh Sagar Lake, Udaipur</strong> under the Techno India NJR / Udaipur Smart Cities framework.
      </p>

      <div class="grid-2">
        <div class="info-card">
          <div class="info-card-title">
            <span>Target Deployment Site</span>
            <span>Udaipur, RJ</span>
          </div>
          <div class="info-card-desc">
            <strong>Location:</strong> Fateh Sagar Lake (Madar canal inflow feeding mouth & Public Health Engineering Department [PHED] drinking water intake jetty).<br>
            <strong>Dual Purpose:</strong> Protection of municipal drinking water supply intake for Udaipur city + environmental lake ecology and algal bloom tracking.
          </div>
        </div>

        <div class="info-card">
          <div class="info-card-title">
            <span>Regulatory Standards Baseline</span>
            <span>CPCB & BIS</span>
          </div>
          <div class="info-card-desc">
            <strong>Lake Baseline:</strong> CPCB Designated Best Use <em>Class C</em> (Drinking water source after conventional treatment & disinfection) and <em>Class B</em> (Outdoor bathing).<br>
            <strong>Intake Manifold:</strong> Cross-referenced against <em>BIS 10500:2012</em> drinking water thresholds.
          </div>
        </div>
      </div>

      <h2 class="sec-heading">2. Phase 1 Core Sensor Suite: Lake Health & Municipal Intake Array</h2>
      <p>
        Six primary sensors cover the limnological and public health indicators of Fateh Sagar. As established in the engineering review, hobby-grade probes are excluded for pH, conductivity, and dissolved oxygen to guarantee field longevity:
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 5%;">#</th>
            <th style="width: 22%;">Sensor</th>
            <th style="width: 15%;">Reads</th>
            <th style="width: 33%;">Limnological & Municipal Significance</th>
            <th style="width: 25%;">Target Specification & Grade</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>1</strong></td>
            <td><strong>Dissolved Oxygen (DO)</strong></td>
            <td>mg/L or % saturation</td>
            <td>Single best indicator of lake health: flags organic sewage inflow, algae collapse, and oxygen starvation before municipal intake.</td>
            <td>Optical luminescent probe preferred; ±0.2 mg/L target accuracy.</td>
          </tr>
          <tr>
            <td><strong>2</strong></td>
            <td><strong>pH Sensor</strong></td>
            <td>pH units (0–14)</td>
            <td>Tracks diurnal swings driven by algal photosynthesis (daylight consumption of CO₂) vs. acidic sewage/industrial discharge.</td>
            <td>Industrial glass electrode; target ±0.05 pH (competition spec).</td>
          </tr>
          <tr>
            <td><strong>3</strong></td>
            <td><strong>Turbidity Module</strong></td>
            <td>NTU (0–3000)</td>
            <td>Measures suspended silt and runoff entering from Aravalli hills after rainfall; detects pathogen carrier vehicles.</td>
            <td>Infrared 90° nephelometric scatter; calibrated in NTU, not 0–100%.</td>
          </tr>
          <tr>
            <td><strong>4</strong></td>
            <td><strong>Conductivity & TDS</strong></td>
            <td>µS/cm, mg/L TDS</td>
            <td>Measures dissolved salts; distinguishes pure rainwater dilution from untreated domestic sewage ingress.</td>
            <td>Range to 5000 µS/cm; target ±20 mg/L TDS (ICT Grand Challenge spec).</td>
          </tr>
          <tr>
            <td><strong>5</strong></td>
            <td><strong>Water Temperature</strong></td>
            <td>°C (-55 to +125)</td>
            <td>Drives bacterial incubation kinetics; mandatory thermal compensation input for pH, DO, and conductivity probes.</td>
            <td>DS18B20 digital stainless steel probe; ±0.5°C accuracy.</td>
          </tr>
          <tr>
            <td><strong>6</strong></td>
            <td><strong>Water Level</strong></td>
            <td>cm or meters</td>
            <td>Tracks lake water balance, storm inflow surges, evaporation rates, and sluice gate discharge to Swaroop Sagar.</td>
            <td>Submerged hydrostatic pressure transducer or rigid ultrasonic mount.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Section 1 & 2</span>
      <span>Page 1 of 6</span>
    </div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">3. Detailed Sensor Physics & Operational Use Cases in Fateh Sagar</h2>
      <p>
        Each sensor addresses a specific limnological mechanism within Fateh Sagar Lake. Machine learning models require all six concurrent streams to disentangle normal diurnal biological cycles from acute contamination events:
      </p>

      <div class="info-card" style="margin-bottom: 6px;">
        <div class="info-card-title">
          <span>1. Dissolved Oxygen (DO)</span>
          <span>Optical Luminescence</span>
        </div>
        <div class="info-card-desc">
          <strong>Use Case:</strong> In Fateh Sagar, healthy lake water exhibits an oxygen curve that rises during daylight (algal photosynthesis) and drops at night (respiration). A flat or collapsing DO curve is an immediate fingerprint of high organic sewage ingress, where decomposing microbes rapidly deplete oxygen.<br>
          <strong>ML Utilization:</strong> Forecasts localized oxygen collapse 48–72 hours ahead; serves as primary input for real-time Biochemical Oxygen Demand (BOD) soft-sensor estimation.<br>
          <strong>Operational Constraints:</strong> Optical luminescent probes drift significantly less than galvanic membrane probes and do not consume oxygen during measurement. Readings must be compensated for water temperature and salinity.
        </div>
      </div>

      <div class="info-card" style="margin-bottom: 6px;">
        <div class="info-card-title">
          <span>2. pH Dynamics</span>
          <span>Industrial Glass Electrode</span>
        </div>
        <div class="info-card-desc">
          <strong>Use Case:</strong> Algal blooms in Fateh Sagar consume dissolved carbonic acid during daylight, driving pH up to 8.5–9.2. Conversely, domestic wastewater and septic inflows depress pH below 6.8.<br>
          <strong>ML Utilization:</strong> Learns the lake's seasonal diurnal baseline swing. Deviations outside the normal diurnal envelope indicate severe chemical or septic dumping.<br>
          <strong>Operational Constraints:</strong> Continuous immersion in bio-active water causes glass bulb scaling; requires automated threshold drift filtering and fortnightly buffer calibration.
        </div>
      </div>

      <div class="info-card" style="margin-bottom: 6px;">
        <div class="info-card-title">
          <span>3. Turbidity</span>
          <span>Infrared Nephelometry</span>
        </div>
        <div class="info-card-desc">
          <strong>Use Case:</strong> Silt from the Aravalli catchment and stormwater runoff washes into Fateh Sagar via the Madar feeding canal. Pathogens (E. coli, Cryptosporidium) adhere to suspended colloidal silt.<br>
          <strong>ML Utilization:</strong> Correlates rainfall volume with turbidity surge lags; feeds organic decay estimates.<br>
          <strong>Operational Constraints:</strong> Biofilm accumulation on optical windows mimics a slow artificial rise in turbidity. Addressed via software baseline drift subtraction and optical window wipers.
        </div>
      </div>

      <div class="info-card" style="margin-bottom: 6px;">
        <div class="info-card-title">
          <span>4. Conductivity & Total Dissolved Solids (TDS)</span>
          <span>AC Excitation Probe</span>
        </div>
        <div class="info-card-desc">
          <strong>Use Case:</strong> Distinguishes heavy rainwater inflows (which dilute lake conductivity) from urban sewage discharges (which cause sharp conductivity surges due to sodium, chloride, and dissolved electrolytes).<br>
          <strong>ML Utilization:</strong> Separates natural hydrological dilution from raw sewer breach events.<br>
          <strong>Operational Constraints:</strong> AC excitation pulses must be used instead of DC to prevent electrode polarization. TDS is derived as: TDS (mg/L) = k &times; EC (µS/cm), with k calibrated to Fateh Sagar water.
        </div>
      </div>

      <div class="grid-2">
        <div class="info-card">
          <div class="info-card-title">
            <span>5. Water Temperature</span>
            <span>DS18B20 Digital</span>
          </div>
          <div class="info-card-desc">
            Controls dissolved gas solubility (cold water holds more DO). Acts as the mathematical thermal compensation baseline for pH, DO, and conductivity probes. Detects deep-water thermal stratification.
          </div>
        </div>

        <div class="info-card">
          <div class="info-card-title">
            <span>6. Water Level</span>
            <span>Hydrostatic Transducer</span>
          </div>
          <div class="info-card-desc">
            Tracks lake storage volume and inflow surges. Replaces the 500 cm limit of ultrasonic sensors with a submerged 0–10m gauge pressure sensor unaffected by surface wave action or wind noise.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Section 3</span>
      <span>Page 2 of 6</span>
    </div>
  </div>

  <!-- ==================== PAGE 3 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">4. The 4-Tier Disease Detection Architecture</h2>
      <p>
        A central challenge in water health surveillance is that <strong>sensors cannot directly image or count pathogenic bacteria in real time</strong>. Aarogya Jal resolves this through an integrated four-tier surveillance engine:
      </p>

      <div class="step-grid">
        <div class="step-card">
          <div class="step-num">1</div>
          <div class="step-title">Physical Proxies</div>
          <div class="step-desc">24/7 telemetry detects the physical-chemical shocks that accompany fecal sewage intrusion: Turbidity ↑, DO ↓, Conductivity ↑.</div>
        </div>
        <div class="step-card">
          <div class="step-num">2</div>
          <div class="step-title">ML Risk Engine</div>
          <div class="step-desc">Ensemble anomaly models calculate Pathogen Ingress Probability and Outbreak Risk Index (ORI) within 10 minutes.</div>
        </div>
        <div class="step-card">
          <div class="step-num">3</div>
          <div class="step-title">Biological Ground-Truth</div>
          <div class="step-desc">Automated alert prompts on-demand rapid E. coli / Coliform enzymatic test strip (Aquagenx CBT) for direct proof.</div>
        </div>
        <div class="step-card">
          <div class="step-num">4</div>
          <div class="step-title">Municipal Alert Loop</div>
          <div class="step-desc">Alerts PHED intake engineers to increase chlorination or halt intake pumps 48–72h before clinical cases emerge.</div>
        </div>
      </div>

      <h3 class="sub-heading">Specific Disease Diagnostic Matrix</h3>
      <table>
        <thead>
          <tr>
            <th style="width: 15%;">Disease Target</th>
            <th style="width: 22%;">Primary Pathogen</th>
            <th style="width: 33%;">Real-Time In-Situ Physical Fingerprint</th>
            <th style="width: 30%;">Confirmatory Modality & Municipal Action</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Cholera</strong></td>
            <td><em>Vibrio cholerae</em></td>
            <td>Sharp DO collapse (rapid microbial aerobic respiration) + Turbidity surge + warm water (&gt;24°C).</td>
            <td>On-demand rapid coliform strip; immediate pre-chlorination dosing alert to PHED water treatment plant.</td>
          </tr>
          <tr>
            <td><strong>Diarrheal Outbreak</strong></td>
            <td><em>E. coli</em>, Rotavirus, Cryptosporidium</td>
            <td>Severe post-rain turbidity spike (&gt;15 NTU) indicating silt runoff containing livestock/human waste.</td>
            <td>Enzymatic β-glucuronidase test strip; coagulant dosage increase alert at water treatment filters.</td>
          </tr>
          <tr>
            <td><strong>Typhoid</strong></td>
            <td><em>Salmonella typhi</em></td>
            <td>Elevated conductivity surge (raw domestic sewage line breach entering Madar canal) + depressed DO.</td>
            <td>Lab sample verification; automated isolation and sluice diversion notice away from intake mouth.</td>
          </tr>
          <tr>
            <td><strong>Hepatitis A</strong></td>
            <td>Hepatitis A virus (HAV)</td>
            <td>Chronic sewage mixing indicators: elevated baseline TDS, abnormal pH drift, low baseline oxygen.</td>
            <td>Monthly viral PCR / coliform surrogate log; sanitary survey dispatched to lakefront commercial properties.</td>
          </tr>
          <tr>
            <td><strong>Algal Toxicity</strong></td>
            <td>Cyanobacteria (Microcystins)</td>
            <td>Daytime pH spikes (&gt;8.8) paired with high water temp, followed by acute nocturnal DO drops.</td>
            <td>Microscopic bloom check; activated carbon dosing recommendation to eliminate cyanotoxins.</td>
          </tr>
        </tbody>
      </table>

      <div class="callout success">
        <div class="callout-title">The Proactive 48-Hour Early-Warning Advantage</div>
        Traditional disease surveillance is <strong>reactive</strong>: authorities discover contamination only when hospitals report acute diarrheal admissions (3–5 days after exposure). In Fateh Sagar, Aarogya Jal flags fecal sewage intrusion at the lake station within <strong>10 minutes of arrival</strong>, allowing PHED treatment engineers to neutralize pathogens before contaminated water ever reaches the city tap distribution grid.
      </div>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Section 4</span>
      <span>Page 3 of 6</span>
    </div>
  </div>

  <!-- ==================== PAGE 4 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">5. Sensor Technology Trade-Offs & Real-Time Soft-Sensor Surrogates</h2>
      <p>
        The sensor selection reflects an explicit compromise between measurement precision, equipment capital expenditure, and rural/municipal maintenance feasibility:
      </p>

      <div class="grid-3">
        <div class="info-card">
          <div class="info-card-title">
            <span>ISE (Ion-Selective)</span>
            <span style="color:#d97706; font-size:6.8pt;">Drift-Prone</span>
          </div>
          <div class="info-card-desc">
            <strong>Evaluation:</strong> Inexpensive for Nitrate/Ammonium, but suffers heavy calibration drift and ionic cross-interference. Requires frequent recalibration against known chemical buffers, making unattended lake deployment unreliable.
          </div>
        </div>

        <div class="info-card">
          <div class="info-card-title">
            <span>Wet-Chemical Units</span>
            <span style="color:#dc2626; font-size:6.8pt;">Reagent-Heavy</span>
          </div>
          <div class="info-card-desc">
            <strong>Evaluation:</strong> Delivers lab-grade accuracy for Phosphate and Nitrate, but consumes liquid chemical reagents. Requires trained technicians for frequent refills and pump maintenance; fails unattended deployment criteria.
          </div>
        </div>

        <div class="info-card">
          <div class="info-card-title">
            <span>Optical / UV Probes</span>
            <span style="color:#0369a1; font-size:6.8pt;">High CapEx</span>
          </div>
          <div class="info-card-desc">
            <strong>Evaluation:</strong> Accurate and reagent-free (e.g. s::can spectro::lyser), but costs ₹15 Lakh–₹35 Lakh per probe and requires high-pressure air compressors. Infeasible for widespread municipal lake stations.
          </div>
        </div>
      </div>

      <h3 class="sub-heading">Real-Time Soft-Sensor Surrogate: Biochemical Oxygen Demand (BOD)</h3>
      <p>
        As Nawdeep's report correctly emphasized, <strong>true BOD cannot be measured by any real-time in-situ sensor</strong> because standardized BOD₅ requires a 5-day dark biological incubation period. Aarogya Jal resolves this by deploying an <strong>ML-Driven Soft Sensor</strong>:
      </p>

      <div class="callout info">
        <div class="callout-title">Algorithmic Formulation: Real-Time Estimated BOD Surrogate</div>
        <p style="font-family: monospace; font-size: 7.7pt; color: #0f172a; margin-bottom: 3px;">
          BOD_est(t) = &alpha; &middot; [&Delta;DO_deficit(t) / &Delta;t] + &beta; &middot; Turbidity(t) + &gamma; &middot; Conductivity(t) + &delta; &middot; f(Temp)
        </p>
        <span style="font-size: 7.2pt; color: #475569;">
          Where DO_deficit measures deviation from 100% saturation at ambient temperature, Turbidity reflects suspended organic loading, and Conductivity scales with sewage concentration. The soft-sensor model is trained and calibrated against monthly certified laboratory BOD₅ incubation tests.
        </span>
      </div>

      <h3 class="sub-heading">Parameters Relegated to Monthly Certified Lab Verification</h3>
      <table>
        <thead>
          <tr>
            <th style="width: 18%;">Parameter</th>
            <th style="width: 32%;">Why Excluded from In-Situ Lake Sensor</th>
            <th style="width: 25%;">Phase 1 Measurement Protocol</th>
            <th style="width: 25%;">ML Model Role</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Nitrate & Phosphate</strong></td>
            <td>ISE probes drift severely; wet-chemical analyzers require frequent reagent refills and technician servicing.</td>
            <td>Certified lab testing on monthly grab samples collected at station.</td>
            <td>Provides monthly training ground-truth to calibrate nutrient runoff models.</td>
          </tr>
          <tr>
            <td><strong>BOD₅</strong></td>
            <td>Requires 5-day laboratory incubation; physical sensor does not exist.</td>
            <td>Standard 5-day dilution incubation at certified environmental laboratory.</td>
            <td>Calibrates and validates the real-time soft-sensor BOD surrogate equation.</td>
          </tr>
          <tr>
            <td><strong>Fecal Coliforms</strong></td>
            <td>Automatic biosensors are high-cost, fragile, and research-stage only.</td>
            <td>Monthly membrane filtration / CFU plating + weekly enzymatic field strips.</td>
            <td>Ground-truth reference to train Pathogen Risk Index classifier.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Section 5</span>
      <span>Page 4 of 6</span>
    </div>
  </div>

  <!-- ==================== PAGE 5 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">6. Hardware, Firmware & Edge Upgrades: Resolving Bottlenecks</h2>
      <p>
        Nawdeep's review identified critical hardware constraints in earlier prototype designs. The engineering specification resolves each item as follows:
      </p>

      <div class="info-card" style="margin-bottom: 6px;">
        <div class="info-card-title">
          <span>Microcontroller Upgrade: Migration to ESP32</span>
          <span>Fixed Single-ADC Bug</span>
        </div>
        <div class="info-card-desc">
          <strong>The Bottleneck:</strong> The ESP8266 / NodeMCU features only one analog input (A0). Wiring both analog pH and TDS probes simultaneously causes pin contention and crosstalk.<br>
          <strong>The Solution:</strong> Upgraded to the <strong>ESP32 Dev Module</strong> (dual-core 240 MHz, multiple 12-bit ADC channels). Probes connect via an external <strong>ADS1115 16-bit I2C ADC</strong> for superior noise rejection, or via industrial <strong>RS-485 / Modbus RTU</strong> over UART.
        </div>
      </div>

      <div class="grid-2">
        <div class="info-card">
          <div class="info-card-title">
            <span>Lake Depth Measurement</span>
            <span>Pressure vs. Ultrasonic</span>
          </div>
          <div class="info-card-desc">
            The JSN-SR04T ultrasonic module reaches a maximum of 500 cm (5 m) and suffers from acoustic wave scatter off windy water surfaces. For deep lake columns (&gt;5m), an industrial <strong>submersible hydrostatic pressure transducer</strong> (0–10m range, 4–20mA output) is specified.
          </div>
        </div>

        <div class="info-card">
          <div class="info-card-title">
            <span>Air vs. Water Gas Sensors</span>
            <span>MQ-136 / MQ-137 Context</span>
          </div>
          <div class="info-card-desc">
            MQ-series sensors (H₂S, NH₃) measure gas concentrations in air, not dissolved in water. They are explicitly excluded from submerged lake stations and reserved strictly for enclosed pump-house headspaces and sealed intake wet-wells.
          </div>
        </div>
      </div>

      <h3 class="sub-heading">Power Budget, Ingestion & Full-Stack Platform Architecture</h3>
      <table>
        <thead>
          <tr>
            <th style="width: 22%;">Subsystem</th>
            <th style="width: 38%;">Component & Specification</th>
            <th style="width: 40%;">Operational Functionality</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Solar & Battery</strong></td>
            <td>12V 500mA (10W) monocrystalline panel + 3.7V 18650 Li-ion pack (10,000 mAh) + MPPT charger.</td>
            <td>Delivers <strong>48 hours continuous autonomy</strong> through extended monsoonal overcast periods. Edge deep-sleep duty cycling consumes &lt;0.5 Wh/day.</td>
          </tr>
          <tr>
            <td><strong>Connectivity</strong></td>
            <td>SIM7600 4G LTE Cat-1 module with fall-back 2G/GSM; onboard LittleFS flash ring buffer.</td>
            <td>Transmits encrypted telemetry every 10 minutes. Buffers up to 14 days of readings locally if cellular carrier drops, auto-resuming sync on reconnect.</td>
          </tr>
          <tr>
            <td><strong>Ingestion & Backend</strong></td>
            <td>MQTT over TLS (Mosquitto/EMQX) &rarr; <strong>FastAPI (Python)</strong> &rarr; <strong>TimescaleDB</strong>.</td>
            <td>High-throughput time-series ingestion; TimescaleDB hypertables optimize continuous time-bucket aggregations and geospatial lake boundary queries.</td>
          </tr>
          <tr>
            <td><strong>Surveillance UI</strong></td>
            <td><strong>Next.js / React</strong> + Tailwind CSS + Leaflet GIS Lake Map.</td>
            <td>Interactive dashboard displaying live lake parameter curves, CPCB threshold warning lines, and one-click SMS alert dispatch to PHED engineers.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Section 6</span>
      <span>Page 5 of 6</span>
    </div>
  </div>

  <!-- ==================== PAGE 6 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">7. Machine Learning Pipeline & Strict Validation Protocol</h2>
      <p>
        The ML pipeline processes 10-minute telemetry data (~52,560 readings/sensor/year). To prevent data leakage and operational failure, models adhere to strict temporal validation:
      </p>

      <div class="step-grid">
        <div class="step-card">
          <div class="step-num">1</div>
          <div class="step-title">Quality Filter</div>
          <div class="step-desc">Flags stuck values, out-of-range sensor spikes, and slow calibration drift; automatically excludes corrupt windows from training.</div>
        </div>
        <div class="step-card">
          <div class="step-num">2</div>
          <div class="step-title">Compensation</div>
          <div class="step-desc">Applies real-time non-linear thermal compensation to pH, DO, and conductivity streams using digital temperature logs.</div>
        </div>
        <div class="step-card">
          <div class="step-num">3</div>
          <div class="step-title">Soft-Sensors</div>
          <div class="step-desc">Estimates real-time BOD and nutrient proxies, dynamically adjusted against monthly certified laboratory incubation ground truth.</div>
        </div>
        <div class="step-card">
          <div class="step-num">4</div>
          <div class="step-title">Time Forecasting</div>
          <div class="step-desc">Gradient boosted trees (XGBoost) forecast 48h dissolved oxygen collapse and algal bloom risk based on rain and weather APIs.</div>
        </div>
      </div>

      <div class="callout alert">
        <div class="callout-title">Validation Rule: No Random Train/Test Splits</div>
        In environmental time-series data, random k-fold splits leak future seasonal patterns into past training windows, artificially inflating model accuracy. Training and testing splits must strictly follow <strong>Temporal Forward Chaining</strong> (training on months 1–6, validating on month 7).
      </div>

      <h2 class="sec-heading">8. Maintenance Protocol, Calibration Cadence & Team Ownership</h2>
      <p>
        Sensors submerged continuously in biological lake water foul and drift. The deployment establishes an enforceable operational schedule:
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 20%;">Cadence</th>
            <th style="width: 40%;">Operational Action</th>
            <th style="width: 40%;">Assigned Accountability</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Fortnightly (14 Days)</strong></td>
            <td>Physical visit to static station: inspect immersion assembly, clean optical DO lens, wipe turbidity window, remove algal biofilm from pH bulb.</td>
            <td><strong>Field Maintenance Lead</strong> (Designated Techno India NJR / Pilot Engineer).</td>
          </tr>
          <tr>
            <td><strong>Monthly (30 Days)</strong></td>
            <td>Two-point buffer calibration (pH 4.01 & 7.00); collect 1-litre grab sample for certified laboratory analysis (BOD₅, Nitrate, Coliform).</td>
            <td><strong>Environmental Chemist / Lab Partner</strong>.</td>
          </tr>
          <tr>
            <td><strong>Automated Continuous</strong></td>
            <td>Cloud-based algorithmic checks flag flatline sensor signals, sudden noise spikes, and abnormal baseline drift in the Next.js dashboard.</td>
            <td><strong>Automated AarogyaJal Watchdog Daemon</strong>.</td>
          </tr>
        </tbody>
      </table>

      <div class="callout success">
        <div class="callout-title">Summary Synthesis: Ready for Fateh Sagar Deployment</div>
        By combining <strong>Nawdeep's rigorous 6-sensor limnological baseline and hardware reality checks</strong> with <strong>AarogyaJal's ESP32 4G telemetry, 4-tier disease detection engine, and Next.js municipal alert platform</strong>, the Phase 1 static station delivers a comprehensive, field-ready environmental and public health shield for Fateh Sagar Lake and Udaipur city.
      </div>
    </div>

    <div class="page-footer">
      <span>Fateh Sagar Lake Smart Monitoring Specification &bull; Prepared by Nawdeep & Manan Ramani &bull; Techno India NJR</span>
      <span>Page 6 of 6</span>
    </div>
  </div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML successfully generated at: {html_path}")

# Compile HTML to PDF via Headless Microsoft Edge
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    str(html_path)
]

print("Executing Edge headless PDF generation...")
result = subprocess.run(cmd, capture_output=True, text=True)

if pdf_path.exists():
    file_size_kb = pdf_path.stat().st_size / 1024
    print(f"SUCCESS: Unified PDF generated at: {pdf_path} ({file_size_kb:.2f} KB)")
else:
    print("ERROR: PDF was not generated.")
