import os
import subprocess
import base64
from pathlib import Path

workspace_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot")
html_path = workspace_dir / "Aarogya_Jal_Research_Report.html"
pdf_path = workspace_dir / "Aarogya_Jal_Research_Report.pdf"

# Function to convert image to base64 data URI
def to_b64(filename):
    p = workspace_dir / filename
    if not p.exists():
        return ""
    mime = "image/png" if filename.endswith(".png") else "image/jpeg"
    with open(p, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{data}"

b64_ketos = to_b64("ketos_hardware_software.png")
b64_aquagenx = to_b64("aquagenx_cbt.jpg")
b64_omnivis = to_b64("omnivis_device.jpg")
b64_cluix = to_b64("cluix_device.jpg")
b64_ysi_exo = to_b64("ysi_exo_hardware.jpg")
b64_ysi_hydro = to_b64("ysi_hydrosphere_software.jpg")
b64_scan = to_b64("scan_spectrolyser.jpg")
b64_kando = to_b64("kando_hardware.jpg")
b64_aqvify = to_b64("aqvify_site_image.jpg")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AarogyaJal: AI-Powered Smart Water Health Surveillance & Early Warning System</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 8.7pt;
    line-height: 1.4;
  }}

  .page-container {{
    page-break-after: always;
    break-after: page;
    min-height: 98vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .page-container:last-child {{
    page-break-after: avoid;
    break-after: avoid;
  }}

  /* Header Cover / Hero */
  .doc-header {{
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 8px;
    margin-bottom: 10px;
  }}

  .badge-row {{
    display: flex;
    gap: 6px;
    margin-bottom: 6px;
  }}

  .badge {{
    display: inline-block;
    padding: 2px 7px;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 4px;
  }}

  .badge-blue {{ background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }}
  .badge-green {{ background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }}
  .badge-purple {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #e9d5ff; }}

  h1.doc-title {{
    font-size: 16pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    margin-bottom: 3px;
    letter-spacing: -0.4px;
  }}

  .doc-subtitle {{
    font-size: 9pt;
    color: #475569;
    font-weight: 500;
    margin-bottom: 8px;
  }}

  .meta-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 7.5pt;
    gap: 8px;
  }}

  .meta-item strong {{
    display: block;
    color: #64748b;
    font-size: 6.8pt;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}

  .meta-item span {{
    color: #0f172a;
    font-weight: 600;
  }}

  /* Section Styling */
  h2.sec-heading {{
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
  }}

  h3.sub-heading {{
    font-size: 9pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 8px;
    margin-bottom: 4px;
  }}

  p {{
    margin-bottom: 5px;
    color: #334155;
    text-align: justify;
  }}

  /* Stat Cards */
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin: 8px 0;
  }}

  .stat-card {{
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 5px;
    padding: 6px 8px;
    text-align: center;
  }}

  .stat-number {{
    font-size: 13.5pt;
    font-weight: 800;
    color: #0369a1;
    line-height: 1.1;
  }}

  .stat-label {{
    font-size: 7pt;
    color: #475569;
    font-weight: 600;
    margin-top: 2px;
  }}

  /* Callout boxes */
  .callout {{
    background: #f8fafc;
    border-left: 3.5px solid #0284c7;
    border-radius: 0 5px 5px 0;
    padding: 6px 10px;
    margin: 7px 0;
    font-size: 8pt;
  }}

  .callout.alert {{
    background: #fff7ed;
    border-left-color: #f97316;
  }}

  .callout.success {{
    background: #f0fdf4;
    border-left-color: #22c55e;
  }}

  .callout.info {{
    background: #f0f9ff;
    border-left-color: #0284c7;
  }}

  .callout-title {{
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 6px 0;
    font-size: 7.7pt;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 4px 6px;
    text-align: left;
    vertical-align: middle;
  }}

  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    font-size: 7.2pt;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  .highlight-row td {{
    background: #e0f2fe !important;
    font-weight: 600;
    color: #0369a1;
    border-top: 1.5px solid #0284c7;
    border-bottom: 1.5px solid #0284c7;
  }}

  /* Workflow Steps */
  .step-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
    margin: 8px 0;
  }}

  .step-card {{
    border: 1px solid #e2e8f0;
    border-top: 2.5px solid #0284c7;
    background: #ffffff;
    border-radius: 5px;
    padding: 7px 8px;
  }}

  .step-num {{
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
  }}

  .step-title {{
    font-size: 8.2pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
  }}

  .step-desc {{
    font-size: 7.2pt;
    color: #64748b;
    line-height: 1.3;
  }}

  /* Pilot location grid */
  .location-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
    margin: 7px 0;
  }}

  .location-card {{
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 6px 8px;
    background: #ffffff;
    border-left: 3px solid #0284c7;
  }}

  .location-title {{
    font-weight: 700;
    font-size: 8pt;
    color: #0369a1;
    display: flex;
    justify-content: space-between;
    margin-bottom: 2px;
  }}

  .location-detail {{
    font-size: 7.3pt;
    color: #475569;
    line-height: 1.28;
  }}

  /* Comparison trade-off cards */
  .tradeoff-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 7px;
    margin: 7px 0;
  }}

  .tradeoff-card {{
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    padding: 7px 8px;
    background: #f8fafc;
  }}

  .tradeoff-title {{
    font-weight: 750;
    font-size: 8pt;
    color: #0f172a;
    margin-bottom: 3px;
    display: flex;
    justify-content: space-between;
  }}

  .tradeoff-desc {{
    font-size: 7.2pt;
    color: #475569;
    line-height: 1.3;
  }}

  /* Gallery Styling (Pages 6 & 7) */
  .gallery-grid-3 {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 9px;
    margin: 8px 0;
  }}

  .gallery-grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin: 8px 0;
  }}

  .gallery-card {{
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    background: #ffffff;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }}

  .gallery-img-box {{
    height: 130px;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 4px;
    border-bottom: 1px solid #e2e8f0;
  }}

  .gallery-img-box img {{
    max-height: 100%;
    max-width: 100%;
    object-fit: contain;
  }}

  .gallery-content {{
    padding: 6px 8px;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .gallery-head {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 3px;
  }}

  .gallery-title {{
    font-weight: 750;
    font-size: 8pt;
    color: #0f172a;
  }}

  .gallery-tag {{
    font-size: 6.5pt;
    font-weight: 700;
    padding: 1px 5px;
    border-radius: 3px;
    background: #f1f5f9;
    color: #475569;
    border: 1px solid #cbd5e1;
    white-space: nowrap;
  }}

  .gallery-caption {{
    font-size: 7.1pt;
    color: #475569;
    line-height: 1.25;
  }}

  .gallery-verdict {{
    margin-top: 4px;
    font-size: 7pt;
    font-weight: 600;
    color: #0369a1;
    background: #f0f9ff;
    padding: 3px 5px;
    border-radius: 3px;
  }}

  /* Tech badges */
  .tech-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin: 4px 0 6px 0;
  }}

  .pill {{
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 6.8pt;
    font-weight: 600;
    color: #334155;
  }}

  .page-footer {{
    border-top: 1px solid #e2e8f0;
    padding-top: 5px;
    font-size: 7pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
  }}

  .check-tag {{ color: #16a34a; font-weight: 700; }}
  .cross-tag {{ color: #dc2626; font-weight: 600; }}
  .partial-tag {{ color: #d97706; font-weight: 600; }}
</style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="page-container">
    <div>
      <div class="doc-header">
        <div class="badge-row">
          <span class="badge badge-blue">Official Research Dossier</span>
          <span class="badge badge-green">Project Reboot 2.0</span>
          <span class="badge badge-purple">AI & IoT Public Health Architecture</span>
        </div>
        <h1 class="doc-title">AarogyaJal: AI-Powered Smart Water Health Surveillance & Early Warning System</h1>
        <div class="doc-subtitle">A Proactive, Multi-Sensor Epidemiological Platform for Rural & Tribal Water Security</div>
        
        <div class="meta-grid">
          <div class="meta-item">
            <strong>Principal Investigator</strong>
            <span>Manan Ramani</span>
          </div>
          <div class="meta-item">
            <strong>Domain Focus</strong>
            <span>IoT, Edge AI & Syndromic Surveillance</span>
          </div>
          <div class="meta-item">
            <strong>Deployment Target</strong>
            <span>Northeastern Region (NER) & Rural India</span>
          </div>
          <div class="meta-item">
            <strong>Hardware Architecture</strong>
            <span>ESP32 / Multi-Sensor Edge Node</span>
          </div>
        </div>
      </div>

      <div class="stat-grid">
        <div class="stat-card">
          <div class="stat-number">38+ Million</div>
          <div class="stat-label">Annual Water-Borne Cases (India)</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">~200,000</div>
          <div class="stat-label">Preventable Annual Deaths</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">&lt; ₹5,500</div>
          <div class="stat-label">Autonomous Sensor Node Cost</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">24/7 + SMS</div>
          <div class="stat-label">Offline & Intermittent Resilient</div>
        </div>
      </div>

      <div class="callout alert" style="background: #fffbeb; border-left-color: #d97706; margin: 6px 0;">
        <div class="callout-title" style="color: #b45309; font-size: 7.8pt;">⚠️ EXECUTIVE CONTEXT & REBOOT 2.0 MANDATE</div>
        <div style="font-size: 7.2pt; color: #78350f; line-height: 1.3;">
          <strong>Historical Baseline Notice:</strong> The technical specifications, component pricing, and competitor evaluations in this dossier reflect our foundational research conducted approximately <strong>1 year ago</strong>. As part of the active <strong>AarogyaJal Reboot 2.0</strong> roadmap, our immediate next deliverables are: 
          <strong>(1) Sensor Refresh:</strong> Benchmarking next-generation digital probes and solid-state sensors with enhanced drift stability; 
          <strong>(2) Cost Remodeling:</strong> Updating the hardware Bill of Materials (BOM) against current 2026 supplier pricing and bulk fabrication volume curves; and 
          <strong>(3) Market Re-Audit:</strong> Conducting a fresh competitive intelligence sweep for newly emerged private startups and Jal Jeevan Mission government initiatives.
        </div>
      </div>

      <h2 class="sec-heading">1. Executive Summary & Problem Landscape</h2>
      <p>
        Water-borne diseases—predominantly diarrhea, cholera, typhoid, and hepatitis A—present a severe, recurring mortality burden across rural and tribal belts in India, most acutely throughout the Northeastern Region (NER). Fragile riverine topography, unsealed community borewells, open drainage runoff, and severe monsoon inundations regularly trigger microbial and chemical infiltration into primary drinking water sources.
      </p>
      <p>
        Currently, public health management functions in a <strong>reactive posture</strong>: disease outbreaks are identified only after rural Primary Health Centres (PHCs) experience an influx of acutely ill patients. Due to mountainous terrain and isolated transit corridors, medical and chlorination responses arrive days or weeks late, allowing localized water contamination to multiply into community-wide epidemics.
      </p>

      <div class="callout alert">
        <div class="callout-title">The Critical Surveillance Bottleneck</div>
        Conventional microbiological lab testing requires physical sample carriage and 24–72 hours of culturing. AarogyaJal replaces this lagging model with an <strong>integrated early warning paradigm</strong> combining continuous physical-chemical telemetry (pH, Turbidity, TDS, Temp, Level, DO, Volatile Gases), rapid weekly field test strips (E. coli / Coliforms), and community syndromic reporting via ASHA health workers.
      </div>

      <h2 class="sec-heading">2. Multi-Vector Disease, Pathogen & Sensor Indicator Matrix</h2>
      <p>
        AarogyaJal establishes direct correlations between epidemic pathogens and measurable physical/chemical proxies that can be reliably tracked using low-cost sensor nodes:
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 14%;">Disease Target</th>
            <th style="width: 25%;">Primary Pathogen & Vector</th>
            <th style="width: 33%;">Key Water Contamination Proxies</th>
            <th style="width: 28%;">Sensor & Detection Modality</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Diarrhea</strong></td>
            <td><em>Escherichia coli</em>, Rotavirus, Cryptosporidium</td>
            <td>Turbidity surges, pH shifts, fecal sediment intrusion</td>
            <td>Optical Turbidity Sensor, Analog pH Module, <em>E. coli</em> Test Strips</td>
          </tr>
          <tr>
            <td><strong>Cholera</strong></td>
            <td><em>Vibrio cholerae</em> (fecal-oral pathway)</td>
            <td>Coliform proliferation, organic decay, dissolved oxygen depletion</td>
            <td>Dissolved Oxygen (DO) Sensor, Turbidity Sensor, Rapid Coliform Strips</td>
          </tr>
          <tr>
            <td><strong>Typhoid</strong></td>
            <td><em>Salmonella typhi</em> (sewage intrusion)</td>
            <td>Conductivity surges, elevated Total Dissolved Solids, fecal traces</td>
            <td>TDS / Electrical Conductivity (EC) Probe, Rapid Field Strips</td>
          </tr>
          <tr>
            <td><strong>Hepatitis A</strong></td>
            <td>Hepatitis A virus (HAV)</td>
            <td>Fecal contamination proxies, sewage backflow, abnormal pH</td>
            <td>pH Sensor, Turbidity Module, Coliform Biosensor Strips</td>
          </tr>
          <tr>
            <td><strong>Septic / Stagnant</strong></td>
            <td>Anaerobic bacterial bloom, rotting matter</td>
            <td>Severe DO drop, thermal spikes, toxic gas liberation (H₂S, NH₃)</td>
            <td>DO Sensor, Temp (DS18B20), MQ-136 (H₂S), MQ-137 (Ammonia)</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Section 1 & 2</span>
      <span>Page 1 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">3. Multi-Tier Sensing Pipeline & Sensor Modality Trade-Off Analysis</h2>
      <p>
        Deploying continuous water surveillance across rugged, low-resource terrain requires an explicit engineering compromise between measurement accuracy, capital cost, and maintenance tolerance.
      </p>

      <div class="step-grid">
        <div class="step-card">
          <div class="step-num">1</div>
          <div class="step-title">Continuous IoT</div>
          <div class="step-desc">24/7 continuous telemetry of pH, Level, TDS, Temp, Turbidity, DO, and headspace gases.</div>
        </div>
        <div class="step-card">
          <div class="step-num">2</div>
          <div class="step-title">ASHA Telemetry</div>
          <div class="step-desc">ASHA health workers log weekly coliform test strips and cluster symptoms via mobile app/SMS.</div>
        </div>
        <div class="step-card">
          <div class="step-num">3</div>
          <div class="step-title">AI Outbreak Engine</div>
          <div class="step-desc">Ensemble ML cross-correlates parameter drift with syndromic logs and monsoon flooding data.</div>
        </div>
        <div class="step-card">
          <div class="step-num">4</div>
          <div class="step-title">Rapid Response</div>
          <div class="step-desc">Automated SMS advisories dispatch to PHCs, district officers, and village water committees.</div>
        </div>
      </div>

      <h3 class="sub-heading">3.1 Sensor Modality Trade-Offs: Servicing Tolerance vs. Budget</h3>
      <p>
        The central architectural dilemma in environmental monitoring is: <em>How much manual servicing can this deployment tolerate vs. budget?</em> In rural Northeastern India, where nodes are hours away from district centers, automated unattended reliability is paramount.
      </p>

      <div class="tradeoff-grid">
        <div class="tradeoff-card">
          <div class="tradeoff-title">
            <span>ISE (Ion-Selective)</span>
            <span style="color:#d97706; font-size:7pt;">Drift-Prone</span>
          </div>
          <div class="tradeoff-desc">
            <strong>Pros:</strong> Cheap and simple for specific ions (Nitrate/Fluoride).<br>
            <strong>Cons:</strong> Severe calibration drift; highly sensitive to ionic interference. Requires recurring calibration against known chemical standards, making unattended rural operation fragile.
          </div>
        </div>

        <div class="tradeoff-card">
          <div class="tradeoff-title">
            <span>Wet-Chemical Analyzers</span>
            <span style="color:#dc2626; font-size:7pt;">Reagent-Heavy</span>
          </div>
          <div class="tradeoff-desc">
            <strong>Pros:</strong> Gold-standard lab accuracy in the field.<br>
            <strong>Cons:</strong> Consumes liquid reagents. Requires a trained field technician for periodic refills and pump maintenance. Fails the "install-and-forget" requirement in remote tribal terrain.
          </div>
        </div>

        <div class="tradeoff-card">
          <div class="tradeoff-title">
            <span>Optical / UV Absorption</span>
            <span style="color:#64748b; font-size:7pt;">High CapEx</span>
          </div>
          <div class="tradeoff-desc">
            <strong>Pros:</strong> Drift-free, highly accurate, low ongoing maintenance.<br>
            <strong>Cons:</strong> Prohibitively expensive per unit (₹40,000–₹1,50,000+ per probe). Cannot scale across thousands of rural panchayats with limited public health budgets.
          </div>
        </div>
      </div>

      <div class="callout info">
        <div class="callout-title">AarogyaJal's Winning Design Decision: Solid-State Core + Surrogate AI Modeling</div>
        Instead of fragile wet-chemical reagents or cost-prohibitive UV probes, AarogyaJal deploys robust, solid-state sensors (**pH, Water Level, TDS, Temperature, Turbidity, DO**) paired with periodic weekly manual paper test strips. This eliminates recurring technician reagent costs while retaining maximum field durability.
      </div>

      <h3 class="sub-heading">3.2 Real-Time Surrogates: BOD & Algal Bloom (Chlorophyll-a)</h3>
      <ul style="margin-left: 16px; font-size: 7.7pt; color: #334155; line-height: 1.5;">
        <li><strong>Biochemical Oxygen Demand (BOD):</strong> BOD cannot be sensed directly in real-time because standard BOD₅ requires a 5-day biological incubation period. AarogyaJal circumvents this by computing an <em>Inferred Organic Load Surrogate</em>: combining real-time <strong>Dissolved Oxygen (DO) depletion rates</strong>, <strong>turbidity spikes</strong>, and <strong>water temperature</strong> into an ML-derived proxy for sudden organic/septic contamination.</li>
        <li><strong>Chlorophyll-a (Algal Bloom Proxy):</strong> Measured via fluorescence sensors. Evaluated as an optional Phase-2 add-on for open surface reservoirs and community harvesting ponds, but excluded from base drinking water nodes to preserve sub-₹5,500 unit economics.</li>
        <li><strong>The Fundamental Four Continuous Baseline:</strong> <strong>pH</strong> (chemical stability), <strong>Water Level</strong> (tank volume/sudden drainage), <strong>TDS/Conductivity</strong> (salinity/dissolved ionic intrusion), and <strong>Temperature</strong> (thermal correction & bacterial kinetic modeling).</li>
      </ul>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Section 3</span>
      <span>Page 2 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 3 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">4. IoT Hardware Bill of Materials (BOM) & Unit Economics</h2>
      <p>
        The AarogyaJal hardware stack is engineered around widely accessible, commercially available industrial and hobby-grade components sourced directly from Indian supply chains, achieving unprecedented unit economics:
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 24%;">Component</th>
            <th style="width: 18%;">Price Range (INR)</th>
            <th style="width: 22%;">Supplier References</th>
            <th style="width: 36%;">Technical Specification & Function</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>pH Sensor Kit</strong></td>
            <td>₹800 – ₹1,500</td>
            <td>QBM India / Graylogix</td>
            <td>Analog glass probe + signal conditioning board (0–14 pH, ±0.1 accuracy).</td>
          </tr>
          <tr>
            <td><strong>Turbidity Sensor Module</strong></td>
            <td>₹500 – ₹600</td>
            <td>Robu.in / HatchnHack</td>
            <td>Optical infrared phototransistor measuring light scatter (0–3000 NTU).</td>
          </tr>
          <tr>
            <td><strong>TDS / Conductivity Sensor</strong></td>
            <td>₹250 – ₹450</td>
            <td>Robu / QuartzComponents</td>
            <td>Dual-pin AC excitation probe preventing electrode polarization (0–1000 ppm).</td>
          </tr>
          <tr>
            <td><strong>Water Temperature Sensor</strong></td>
            <td>₹120 – ₹220</td>
            <td>Quartz / Robu</td>
            <td>DS18B20 digital stainless steel waterproof probe (-55°C to +125°C).</td>
          </tr>
          <tr>
            <td><strong>Water Level Sensor</strong></td>
            <td>₹80 – ₹200</td>
            <td>HatchnHack / Quartz</td>
            <td>JSN-SR04T waterproof ultrasonic probe for reservoir tank volume monitoring.</td>
          </tr>
          <tr>
            <td><strong>Dissolved Oxygen (DO) Probe</strong></td>
            <td>₹1,000 – ₹2,500</td>
            <td>Robu / Importers</td>
            <td>Galvanic/polarographic DO probe detecting organic decay and stagnation.</td>
          </tr>
          <tr>
            <td><strong>Gas & Odour Sensor Suite</strong></td>
            <td>₹100 – ₹300</td>
            <td>Quartz / Robu</td>
            <td>MQ-136 (H₂S), MQ-137 (Ammonia) to detect anaerobic organic decomposition.</td>
          </tr>
          <tr>
            <td><strong>ESP32 / NodeMCU MCU</strong></td>
            <td>₹220 – ₹350</td>
            <td>QuartzComponents / Robu</td>
            <td>Dual-core 240MHz, Wi-Fi 802.11 b/g/n + BLE, deep sleep power cycling (&lt;15µA).</td>
          </tr>
          <tr>
            <td><strong>Power Subsystem (Battery)</strong></td>
            <td>₹400 – ₹1,500</td>
            <td>Local / Li-ion Cells</td>
            <td>3.7V 18650 Li-ion / Li-Po rechargeable pack with BMS protection circuit.</td>
          </tr>
          <tr>
            <td><strong>Solar Harvesting Panel</strong></td>
            <td>₹600 – ₹2,500</td>
            <td>Solar Retailers / Robu</td>
            <td>5W–10W monocrystalline solar panel + TP4056 / MPPT step-down solar charger.</td>
          </tr>
          <tr>
            <td><strong>Weatherproof Enclosure</strong></td>
            <td>₹350 – ₹700</td>
            <td>IP66 Junction Boxes</td>
            <td>UV-resistant ABS enclosure with IP68 cable glands and mounting bracket.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>TOTAL COMPLETE NODE</strong></td>
            <td><strong>₹4,420 – ₹9,320</strong></td>
            <td><strong>~$53 – $110 USD</strong></td>
            <td><strong>96%+ cost reduction vs. commercial stations (₹1.5 Lakh – ₹5 Lakh)</strong></td>
          </tr>
        </tbody>
      </table>

      <div class="callout success">
        <div class="callout-title">Mass Deployability & Fiscal Sustainability</div>
        At an average node cost of <strong>₹5,500 (~$65 USD)</strong>, an entire district water surveillance network spanning 50 critical points of interest (handpumps, storage tanks, and riverbanks) can be outfitted for under <strong>₹2.75 Lakh</strong>—less than the acquisition cost of a single municipal-grade SCADA monitoring station.
      </div>

      <h3 class="sub-heading">4.1 Edge Energy Budget, Harvesting & Anti-Fouling Architecture</h3>
      <ul style="margin-left: 16px; font-size: 7.6pt; color: #334155; line-height: 1.48;">
        <li><strong>Low-Power Duty Cycle:</strong> ESP32 firmware executes a 55-second deep sleep cycle (&lt;15 µA quiescent draw) followed by a 5-second burst sensing, analog-to-digital averaging, and MQTT transmission phase. Average operational consumption is constrained to ~20 mA at 3.3V.</li>
        <li><strong>Monsoon Solar Power Budget:</strong> A compact 5W–10W monocrystalline solar panel produces 18–25 Wh daily under normal diffuse sunlight. The edge node consumes approximately 0.48 Wh per 24-hour operating period, providing a ~40&times; safety multiplier to sustain autonomous operation through 14 consecutive days of heavy overcast monsoonal rains.</li>
        <li><strong>Anti-Fouling & Electrode Longevity:</strong> Alternating current (AC) excitation pulses across TDS/conductivity probes eliminate galvanic polarization, prevent electrode oxidation, and inhibit biological biofilm fouling in stagnant well environments.</li>
      </ul>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Section 4</span>
      <span>Page 3 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 4 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">5. Target Pilot Deployments: Northeastern Region (NER)</h2>
      <p>
        Due to extreme rainfall, seasonal floods, and fragmented healthcare networks, five high-risk pilot sites in the NER have been earmarked to validate sensor performance and predictive outbreak modeling under harsh operating conditions:
      </p>

      <div class="location-grid">
        <div class="location-card">
          <div class="location-title">
            <span>1. Majuli, Assam</span>
            <span>River Island Aquifer</span>
          </div>
          <div class="location-detail"><strong>Installation Point:</strong> Exit manifold of community handpump near Brahmaputra riverbank.</div>
          <div class="location-detail"><strong>Risk Vector:</strong> Monsoonal river swells cause subsurface silt infiltration and cross-contamination of shallow drinking aquifers.</div>
        </div>

        <div class="location-card">
          <div class="location-title">
            <span>2. Churachandpur, Manipur</span>
            <span>Centralized Reservoir</span>
          </div>
          <div class="location-detail"><strong>Installation Point:</strong> Village-level gravity-fed overhead storage reservoir.</div>
          <div class="location-detail"><strong>Risk Vector:</strong> Centralized distribution point; a single pathogen infiltration instantly contaminates the entire settlement.</div>
        </div>

        <div class="location-card">
          <div class="location-title">
            <span>3. Tura, Meghalaya</span>
            <span>Traditional Open Well</span>
          </div>
          <div class="location-detail"><strong>Installation Point:</strong> Community dug well located in Rongram Block.</div>
          <div class="location-detail"><strong>Risk Vector:</strong> Heavy precipitation causes rapid agricultural and surface runoff into the well, spiking turbidity and fecal coliforms.</div>
        </div>

        <div class="location-card">
          <div class="location-title">
            <span>4. Aizawl, Mizoram</span>
            <span>Drainage Discharge</span>
          </div>
          <div class="location-detail"><strong>Installation Point:</strong> Drain exit point discharging into a community harvesting pond.</div>
          <div class="location-detail"><strong>Risk Vector:</strong> Untreated hillside sewage overflow mixes directly with primary community bathing and utility water.</div>
        </div>
      </div>

      <div class="location-card" style="margin-bottom: 8px;">
        <div class="location-title">
          <span>5. Pasighat, Arunachal Pradesh</span>
          <span>Borewell Riverbank Infiltration</span>
        </div>
        <div class="location-detail"><strong>Installation Point:</strong> Community borewell discharge outlet adjacent to the Siang riverbank.</div>
        <div class="location-detail"><strong>Risk Vector:</strong> Frequent flash floods cause backflow and seepage of river silt and untreated surface waste into borewell intake pipes.</div>
      </div>

      <h2 class="sec-heading">6. Comprehensive Industry & Competitive Benchmark</h2>
      <p>
        AarogyaJal combines the advantages of continuous IoT monitoring, microbiological field testing, and AI-driven syndromic fusion while maintaining accessibility for rural budgets:
      </p>

      <table>
        <thead>
          <tr>
            <th style="width: 16%;">Company / Solution</th>
            <th style="width: 12%;">Real-Time IoT</th>
            <th style="width: 14%;">Pathogen Testing</th>
            <th style="width: 14%;">AI / Predictive</th>
            <th style="width: 12%;">Dashboard & Alerts</th>
            <th style="width: 12%;">Rural / Low-Cost</th>
            <th style="width: 20%;">Comparative Takeaway</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>KETOS (US)</strong></td>
            <td><span class="check-tag">&#10004;</span> Autonomous</td>
            <td><span class="partial-tag">&#9679;</span> Auto-analyzer</td>
            <td><span class="check-tag">&#10004;</span> Predictive</td>
            <td><span class="check-tag">&#10004;</span> Cloud</td>
            <td><span class="cross-tag">&#10008;</span> Industrial only</td>
            <td>High-end automated analyzer; excessive cost for rural deployment.</td>
          </tr>
          <tr>
            <td><strong>Aquagenx</strong></td>
            <td><span class="cross-tag">&#10008;</span> Manual kits</td>
            <td><span class="check-tag">&#10004;</span> Coliform/E. coli</td>
            <td><span class="cross-tag">&#10008;</span> None</td>
            <td><span class="partial-tag">&#9679;</span> Manual logs</td>
            <td><span class="check-tag">&#10004;</span> Field-focused</td>
            <td>Gold standard microbiological kits, but no continuous telemetry.</td>
          </tr>
          <tr>
            <td><strong>OmniVis</strong></td>
            <td><span class="partial-tag">&#9679;</span> Smartphone dock</td>
            <td><span class="check-tag">&#10004;</span> Cholera bio-test</td>
            <td><span class="cross-tag">&#10008;</span> Research phase</td>
            <td><span class="partial-tag">&#9679;</span> Mobile app</td>
            <td><span class="check-tag">&#10004;</span> Clinical scope</td>
            <td>Rapid handheld cholera test, but requires manual operator sampling.</td>
          </tr>
          <tr>
            <td><strong>IntuThings (India)</strong></td>
            <td><span class="check-tag">&#10004;</span> IoT modules</td>
            <td><span class="cross-tag">&#10008;</span> No pathogens</td>
            <td><span class="partial-tag">&#9679;</span> Telemetry stats</td>
            <td><span class="check-tag">&#10004;</span> Web portal</td>
            <td><span class="partial-tag">&#9679;</span> Municipal focus</td>
            <td>Indian IoT integrator focused on urban piped water networks.</td>
          </tr>
          <tr>
            <td><strong>CLUIX (India)</strong></td>
            <td><span class="check-tag">&#10004;</span> Portable reader</td>
            <td><span class="partial-tag">&#9679;</span> Optical proxies</td>
            <td><span class="cross-tag">&#10008;</span> Limited</td>
            <td><span class="check-tag">&#10004;</span> App + Device</td>
            <td><span class="partial-tag">&#9679;</span> Semi-portable</td>
            <td>Portable digital water analyzer measuring 12+ physical parameters.</td>
          </tr>
          <tr>
            <td><strong>Hach / Xylem</strong></td>
            <td><span class="check-tag">&#10004;</span> Industrial probes</td>
            <td><span class="partial-tag">&#9679;</span> Lab methods</td>
            <td><span class="partial-tag">&#9679;</span> SCADA analytics</td>
            <td><span class="check-tag">&#10004;</span> Enterprise UI</td>
            <td><span class="cross-tag">&#10008;</span> High CapEx</td>
            <td>Global benchmarks costing ₹15 Lakh – ₹50 Lakh per station.</td>
          </tr>
          <tr>
            <td><strong>s::can / Kando</strong></td>
            <td><span class="check-tag">&#10004;</span> Spectrometry / IoT</td>
            <td><span class="partial-tag">&#9679;</span> Optical proxies</td>
            <td><span class="check-tag">&#10004;</span> Event detection</td>
            <td><span class="check-tag">&#10004;</span> Real-time</td>
            <td><span class="cross-tag">&#10008;</span> Utility only</td>
            <td>Advanced optical spectrometry probes for municipal wastewater grids.</td>
          </tr>
          <tr>
            <td><strong>AquaSense (India)</strong></td>
            <td><span class="check-tag">&#10004;</span> Surface / Ground</td>
            <td><span class="cross-tag">&#10008;</span> No direct tests</td>
            <td><span class="partial-tag">&#9679;</span> Anomaly alerts</td>
            <td><span class="check-tag">&#10004;</span> Web dashboard</td>
            <td><span class="partial-tag">&#9679;</span> Commercial</td>
            <td>Indian sensor solutions for environmental groundwater tracking.</td>
          </tr>
          <tr>
            <td><strong>Aqvify</strong></td>
            <td><span class="check-tag">&#10004;</span> Level / TDS</td>
            <td><span class="cross-tag">&#10008;</span> None</td>
            <td><span class="cross-tag">&#10008;</span> Trend graphs</td>
            <td><span class="check-tag">&#10004;</span> Mobile App</td>
            <td><span class="check-tag">&#10004;</span> Well-level focus</td>
            <td>Excellent telemetry for well depth, but lacks public health analytics.</td>
          </tr>
          <tr class="highlight-row">
            <td><strong>AarogyaJal (Reboot)</strong></td>
            <td><strong><span class="check-tag">&#10004;</span> Continuous Array</strong></td>
            <td><strong><span class="check-tag">&#10004;</span> Integrated Strips</strong></td>
            <td><strong><span class="check-tag">&#10004;</span> XGBoost / RF</strong></td>
            <td><strong><span class="check-tag">&#10004;</span> SMS + GIS Web</strong></td>
            <td><strong><span class="check-tag">&#10004;</span> Offline / &lt;₹5.5k</strong></td>
            <td><strong>Only hybrid model uniting low-cost IoT, ASHA syndromic logs, and predictive outbreak AI for rural geographies.</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Section 5 & 6</span>
      <span>Page 4 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 5 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">7. Technical Architecture & Technology Stack</h2>
      <p>
        The AarogyaJal Reboot 2.0 system leverages a decoupled, offline-resilient microservice pattern built for high fault-tolerance across low-bandwidth environments:
      </p>

      <div class="callout success">
        <div class="callout-title">Unified Technology Ecosystem</div>
        <div class="tech-pills">
          <span class="pill">ESP32 / NodeMCU</span>
          <span class="pill">MQTT (Mosquitto / EMQX)</span>
          <span class="pill">FastAPI (Python)</span>
          <span class="pill">Node.js / Express</span>
          <span class="pill">PostgreSQL + PostGIS</span>
          <span class="pill">TimescaleDB</span>
          <span class="pill">MongoDB</span>
          <span class="pill">Redis Caching</span>
          <span class="pill">Next.js & React</span>
          <span class="pill">Tailwind CSS</span>
          <span class="pill">Flutter (Mobile App)</span>
          <span class="pill">Scikit-learn</span>
          <span class="pill">XGBoost</span>
          <span class="pill">Gemini LLM (Advisory)</span>
          <span class="pill">SMS Gateway / Twilio</span>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th style="width: 22%;">System Layer</th>
            <th style="width: 38%;">Core Technologies</th>
            <th style="width: 40%;">Functional Responsibility</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Hardware & Edge</strong></td>
            <td>ESP32 / NodeMCU, FreeRTOS, Arduino C++, Deep Sleep</td>
            <td>Analog sampling, digital filtering, power management, burst MQTT telemetry.</td>
          </tr>
          <tr>
            <td><strong>Ingestion & Queuing</strong></td>
            <td>MQTT Broker (EMQX / Mosquitto), WebSockets, REST Gateways</td>
            <td>High-throughput telemetry ingestion, buffering dropped packets during outages.</td>
          </tr>
          <tr>
            <td><strong>Core Backend API</strong></td>
            <td>FastAPI / NestJS, PostgreSQL + PostGIS, TimescaleDB, Redis</td>
            <td>Time-series logging, spatial GIS queries, role-based access (PHC, ASHA, VWSC).</td>
          </tr>
          <tr>
            <td><strong>AI / ML Analytics</strong></td>
            <td>Python, XGBoost, Random Forest, Scikit-learn, Gemini API</td>
            <td>Water Quality Index (WQI) scoring, anomaly detection, automated advisory alerts.</td>
          </tr>
          <tr>
            <td><strong>Web Dashboard & GIS</strong></td>
            <td>Next.js, React, Tailwind CSS, Leaflet / Mapbox GL</td>
            <td>Geospatial contamination heatmaps, telemetry graphs, alert dispatch console.</td>
          </tr>
          <tr>
            <td><strong>Mobile Field Client</strong></td>
            <td>Flutter, SQLite (Offline-first), Background Sync</td>
            <td>ASHA symptom logging, test strip camera capture, offline SMS fallback.</td>
          </tr>
        </tbody>
      </table>

      <h2 class="sec-heading">8. Outbreak Prediction Engine & Risk Index Formulation</h2>
      <p>
        The prediction engine computes a dynamic <strong>Outbreak Risk Index (ORI)</strong> by fusing physical telemetry deviations, microbiological validations, and localized syndromic health reports:
      </p>

      <div class="callout">
        <div class="callout-title">Algorithmic Formulation: Outbreak Risk Index (ORI)</div>
        <p style="font-family: monospace; font-size: 7.6pt; color: #0f172a; margin-bottom: 4px;">
          ORI = w₁ &middot; &Delta;WQI(t) + w₂ &middot; Biol(t) + w₃ &middot; &Sigma; SymptomCluster(t, r) + w₄ &middot; SeasonRainFactor(t)
        </p>
        <span style="font-size: 7.2pt; color: #475569;">
          Where &Delta;WQI tracks rate of parameter deviation (pH, Turbidity, DO, TDS); Biol represents positive <em>E. coli</em> strip detection; SymptomCluster aggregates ASHA diarrheal and febrile complaint surges within radius <em>r</em>; and SeasonRainFactor scales risk during peak monsoon flooding. If ORI exceeds 0.75, automated emergency alerts are dispatched.
        </span>
      </div>

      <h2 class="sec-heading">9. Reboot 2.0 Strategic Execution Roadmap</h2>
      <div class="step-grid">
        <div class="step-card">
          <div class="step-num">P1</div>
          <div class="step-title">Hardware & Edge</div>
          <div class="step-desc">Refactor ESP32 firmware with burst MQTT, solar battery power management, and local calibration tables.</div>
        </div>
        <div class="step-card">
          <div class="step-num">P2</div>
          <div class="step-title">Cloud Backend</div>
          <div class="step-desc">Implement FastAPI backend with TimescaleDB time-series storage and ASHA symptom intake APIs.</div>
        </div>
        <div class="step-card">
          <div class="step-num">P3</div>
          <div class="step-title">AI & Dashboard</div>
          <div class="step-desc">Train XGBoost anomaly models, integrate WQI calculator, and build Next.js GIS surveillance console.</div>
        </div>
        <div class="step-card">
          <div class="step-num">P4</div>
          <div class="step-title">Field Deployment</div>
          <div class="step-desc">Pilot 5 nodes across Assam & Meghalaya, onboard ASHA workers, and benchmark prediction accuracy.</div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Prepared by Manan Ramani &bull; Confidential & Proprietary</span>
      <span>Page 5 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 6 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">10. Visual Benchmark Gallery: Existing Market Hardware & Sensors</h2>
      <p>
        Visual inspection of commercial competitors across industrial kiosks, multiparameter probes, and handheld analyzers confirms the structural gap in rural accessibility:
      </p>

      <div class="gallery-grid-3">
        <!-- 1. KETOS SHIELD -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_ketos}" alt="KETOS SHIELD Hardware">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">KETOS SHIELD (US)</span>
                <span class="gallery-tag">Autonomous Kiosk</span>
              </div>
              <div class="gallery-caption">Industrial-grade automated testing cabinet. Features automated robotic fluid handling, self-calibration, and multi-metal testing.</div>
            </div>
            <div class="gallery-verdict">Limitation: Prohibitive CapEx; requires subscription SaaS & industrial housing.</div>
          </div>
        </div>

        <!-- 2. YSI EXO1 Sonde -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_ysi_exo}" alt="YSI EXO Multiparameter Sonde">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">YSI EXO1 Sonde (Xylem)</span>
                <span class="gallery-tag">Multi-Probe Sonde</span>
              </div>
              <div class="gallery-caption">High-precision oceanographic & riverine sonde featuring 4 smart sensor ports, antifouling wiper, and titanium housing.</div>
            </div>
            <div class="gallery-verdict">Limitation: Unit cost ₹8L–₹25L; designed for marine research, not village wells.</div>
          </div>
        </div>

        <!-- 3. s::can spectro::lyser -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_scan}" alt="s::can spectrolyser Probe">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">s::can spectro::lyser</span>
                <span class="gallery-tag">UV-Vis Spectrometer</span>
              </div>
              <div class="gallery-caption">Submersible optical spectrometer measuring TOC, COD, BOD proxies, and nitrate absorption spectrum without reagents.</div>
            </div>
            <div class="gallery-verdict">Limitation: Costs ₹15L–₹35L; high optical maintenance & compressed air cleaning.</div>
          </div>
        </div>

        <!-- 4. OmniVis Cholera Device -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_omnivis}" alt="OmniVis Cholera Detector">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">OmniVis Cholera Device</span>
                <span class="gallery-tag">Mobile Diagnostic</span>
              </div>
              <div class="gallery-caption">Purdue-developed smartphone hardware attachment using RT-LAMP isothermal amplification & particle diffusometry for cholera.</div>
            </div>
            <div class="gallery-verdict">Limitation: Dedicated single-pathogen tool; requires manual sample extraction.</div>
          </div>
        </div>

        <!-- 5. CLUIX C022 Handheld -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_cluix}" alt="CLUIX C022 Digital Water Analyzer">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">CLUIX C022 (India)</span>
                <span class="gallery-tag">Handheld Analyzer</span>
              </div>
              <div class="gallery-caption">Indian IoT handheld digital analyzer measuring 12+ physical parameters with cloud sync and Jal Jeevan Mission integration.</div>
            </div>
            <div class="gallery-verdict">Limitation: Operator-dependent grab testing; no continuous 24/7 telemetry.</div>
          </div>
        </div>

        <!-- 6. Kando kLog V3.0 -->
        <div class="gallery-card">
          <div class="gallery-img-box">
            <img src="{b64_kando}" alt="Kando Wastewater Unit">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">Kando kLog V3.0</span>
                <span class="gallery-tag">Sewer Manhole IoT</span>
              </div>
              <div class="gallery-caption">Ruggedized underground controller for sewer trunk lines, detecting toxic municipal discharges and pathogen spikes via AI.</div>
            </div>
            <div class="gallery-verdict">Limitation: Tailored strictly for municipal wastewater grids, not rural drinking aquifers.</div>
          </div>
        </div>
      </div>

      <div class="callout success">
        <div class="callout-title">The AarogyaJal Hardware Differentiation</div>
        Existing market hardware falls into two extremes: <strong>hyper-expensive municipal SCADA instruments</strong> (₹8L–₹35L like YSI and s::can) or <strong>intermittent manual testing devices</strong> (CLUIX, OmniVis). AarogyaJal creates a new category: an <strong>autonomous 24/7 continuous multi-probe array at under ₹5,500</strong> with integrated solar harvesting.
      </div>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Section 10: Hardware Benchmark</span>
      <span>Page 6 of 7</span>
    </div>
  </div>

  <!-- ==================== PAGE 7 ==================== -->
  <div class="page-container">
    <div>
      <h2 class="sec-heading" style="margin-top: 0;">11. Visual Benchmark Gallery: Software Platforms & Field Applications</h2>
      <p>
        Examining competitor software architectures underscores the critical necessity of combining real-time environmental telemetry with bottom-up syndromic health reports:
      </p>

      <div class="gallery-grid-2">
        <!-- 1. KETOS Dashboard -->
        <div class="gallery-card">
          <div class="gallery-img-box" style="height: 155px;">
            <img src="{b64_ketos}" alt="KETOS Software Platform">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">KETOS Wave / Cloud Analytics</span>
                <span class="gallery-tag">Enterprise SaaS</span>
              </div>
              <div class="gallery-caption">Enterprise cloud portal displaying real-time parameter tracking, automated compliance alerts, and multi-tenant telemetry dashboards.</div>
            </div>
            <div class="gallery-verdict">Takeaway: High UI polish, but completely lacks grassroots syndromic (ASHA) health reporting.</div>
          </div>
        </div>

        <!-- 2. YSI HydroSphere -->
        <div class="gallery-card">
          <div class="gallery-img-box" style="height: 155px;">
            <img src="{b64_ysi_hydro}" alt="YSI HydroSphere Software">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">YSI HydroSphere Platform</span>
                <span class="gallery-tag">GIS River Network</span>
              </div>
              <div class="gallery-caption">Geospatial cloud platform mapping water sensors across river basins with automated thresholds, historical curves, and public portal view.</div>
            </div>
            <div class="gallery-verdict">Takeaway: Excellent geospatial visualization; serves as benchmark for AarogyaJal's GIS map.</div>
          </div>
        </div>

        <!-- 3. Aqvify Mobile App -->
        <div class="gallery-card">
          <div class="gallery-img-box" style="height: 155px;">
            <img src="{b64_aqvify}" alt="Aqvify Well Monitor & App">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">Aqvify Well Telemetry & Mobile App</span>
                <span class="gallery-tag">Consumer IoT</span>
              </div>
              <div class="gallery-caption">Submersible pressure transducer paired with a mobile app displaying live water column height, 24h consumption graphs, and low-level alerts.</div>
            </div>
            <div class="gallery-verdict">Takeaway: Validates the usability of mobile-first telemetry; lacks epidemiological disease predictive intelligence.</div>
          </div>
        </div>

        <!-- 4. Aquagenx CBT Field Test Protocol -->
        <div class="gallery-card">
          <div class="gallery-img-box" style="height: 155px;">
            <img src="{b64_aquagenx}" alt="Aquagenx CBT Report">
          </div>
          <div class="gallery-content">
            <div>
              <div class="gallery-head">
                <span class="gallery-title">Aquagenx CBT Field Test Kit</span>
                <span class="gallery-tag">Microbiological Field Protocol</span>
              </div>
              <div class="gallery-caption">WHO/UNICEF JMP validated compartment bag test quantifying <em>E. coli</em> and coliforms via MPN color change without electricity or laboratories.</div>
            </div>
            <div class="gallery-verdict">Takeaway: Standardizes the exact biological spot-check protocol adopted for AarogyaJal's ASHA validation loop.</div>
          </div>
        </div>
      </div>

      <div class="callout alert">
        <div class="callout-title">The AarogyaJal Synthesis & Architectural Monopoly</div>
        No single competitor bridges all three operational pillars: <strong>(1) Sub-₹5,500 continuous physical IoT telemetry</strong>, <strong>(2) Rapid microbiological test-strip ground-truthing</strong>, and <strong>(3) Grassroots syndromic outbreak prediction via ASHA frontline workers</strong>. AarogyaJal solves the rural water crisis by creating an interconnected epidemiological early-warning shield engineered precisely for India's most underserved regions.
      </div>
    </div>

    <div class="page-footer">
      <span>AarogyaJal Reboot Research Dossier &bull; Prepared by Manan Ramani &bull; Confidential & Proprietary</span>
      <span>Page 7 of 7</span>
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
    print(f"SUCCESS: Master PDF generated at: {pdf_path} ({file_size_kb:.2f} KB)")
else:
    print("ERROR: PDF was not generated.")
