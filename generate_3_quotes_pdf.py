import subprocess
from pathlib import Path

workspace_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot")
html_path = workspace_dir / "Aarogya_Jal_3_Quotes_Part_Details.html"
pdf_path = workspace_dir / "Aarogya_Jal_3_Quotes_Part_Details.pdf"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aarogya Jal - 3 Quotes Part Details & BoM</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 12mm 10mm 12mm;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 8.2pt;
    line-height: 1.35;
  }
  .page {
    page-break-after: always;
    min-height: 98vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  .page:last-child { page-break-after: avoid; margin-bottom: 0; }
  .header {
    border-bottom: 2px solid #0b4f6c;
    padding-bottom: 6px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .title-area h1 {
    font-size: 14pt;
    color: #0b4f6c;
    font-weight: 800;
  }
  .title-area p {
    font-size: 8pt;
    color: #64748b;
  }
  .meta-tag {
    font-size: 7.5pt;
    background: #e0f2fe;
    color: #0369a1;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 600;
  }
  h2 {
    font-size: 10pt;
    color: #0b4f6c;
    margin: 8px 0 4px 0;
    border-left: 3.5px solid #01baef;
    padding-left: 6px;
    font-weight: 700;
  }
  p.desc {
    font-size: 7.8pt;
    color: #475569;
    margin-bottom: 6px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 8px;
    font-size: 7.5pt;
  }
  th {
    background: #0b4f6c;
    color: #ffffff;
    text-align: left;
    padding: 5px 6px;
    font-weight: 700;
  }
  td {
    padding: 4px 6px;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }
  tr:nth-child(even) td { background: #f8fafc; }
  .part-name { font-weight: 700; color: #0f172a; }
  .vendor { color: #334155; }
  .price { font-weight: 700; color: #0b4f6c; text-align: right; white-space: nowrap; }
  .tot-row td {
    background: #e0f2fe !important;
    font-weight: 800;
    color: #0b4f6c;
    border-top: 1.5px solid #0284c7;
    border-bottom: 1.5px solid #0284c7;
    font-size: 8pt;
  }
  .callout {
    background: #f0fdf4;
    border-left: 3px solid #10b981;
    padding: 6px 10px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 7.5pt;
  }
  .callout-amber {
    background: #fef3c7;
    border-left: 3px solid #f59e0b;
    padding: 6px 10px;
    margin: 6px 0;
    border-radius: 0 4px 4px 0;
    font-size: 7.5pt;
  }
  .footer {
    border-top: 1px solid #cbd5e1;
    padding-top: 4px;
    font-size: 7pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
  }
</style>
</head>
<body>

<!-- PAGE 1: EXEC SUMMARY & QUOTE 1 -->
<div class="page">
  <div>
    <div class="header">
      <div class="title-area">
        <h1>AAROGYA JAL: 3 PROCUREMENT QUOTES & DETAILED PART BoM</h1>
        <p>Comprehensive Specifications: Part Name, Company/Model, Price & Limnological Use</p>
      </div>
      <div class="meta-tag">Fateh Sagar Lake • Phase 1</div>
    </div>

    <h2>1. Executive 3-Tier Budget Comparison Matrix</h2>
    <table>
      <thead>
        <tr>
          <th>Tier Level</th>
          <th>Initial CapEx</th>
          <th>Scope & Included Sensors</th>
          <th>Power & Mooring Rigging</th>
          <th>Target Deployment</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="part-name">Quote 1: Bare-Minimum Core Sentry</td>
          <td class="price">₹35,500</td>
          <td>4 Sensors: Industrial EC + Optical Turbidity + pH + Dual Temperature</td>
          <td>20W Solar + 12V 7Ah SLA + DIY 4" PVC Catamaran Float</td>
          <td>Hackathon / 2-Wk Lab Demo</td>
        </tr>
        <tr style="background:#f0fdfa;">
          <td class="part-name" style="color:#0f766e;">Quote 2: Value-Engineered Pilot (★ Recommended)</td>
          <td class="price" style="color:#0f766e;">₹71,500</td>
          <td>7 Probes: Galvanic DO + Turbidity + EC + pH + Temp + Level + Rain + Baro</td>
          <td>25W Mono Solar + 12V 12Ah Battery + Marine FRP Buoy</td>
          <td>BITS Pitch / Rajasthan iStart / 6-Mo Pilot</td>
        </tr>
        <tr>
          <td class="part-name">Quote 3: Municipal Enterprise Station</td>
          <td class="price">₹3,15,000</td>
          <td>8 Probes: Optical Wiper DO + Optical Wiper Turbidity + Toroidal EC + pH + RTD Temp + Hydrostatic Level + Rain + Baro + Handheld QA Kit</td>
          <td>50W Solar + 12V 24Ah LiFePO4 (7-Day Monsoon) + SS316 Buoy</td>
          <td>Municipal PHED / Smart City Continuous SCADA</td>
        </tr>
      </tbody>
    </table>

    <h2>2. Quote 1: The Bare-Minimum 4-Sensor Sentry (₹35,500 CapEx)</h2>
    <p class="desc">Designed for student grants and bench validation. Focuses on the core physical-chemical markers (EC + Turbidity + pH + Temp) responsible for 85% of sewage detection capability. Requires bi-weekly manual probe cleaning.</p>

    <table>
      <thead>
        <tr>
          <th>Part / Component Name</th>
          <th>Manufacturer / Candidate Model</th>
          <th>Unit Price</th>
          <th>Operational Limnological Use & Purpose</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="part-name">Industrial 4-Electrode EC / Salinity Sensor</td>
          <td class="vendor">Rika Sensors / Renke (RK500-08 Graphite Modbus)</td>
          <td class="price">₹6,500</td>
          <td>Measures ionic concentration; proxy for raw sewage ingress (Na+, K+, Cl- from urine) and industrial effluent.</td>
        </tr>
        <tr>
          <td class="part-name">Near-IR 860nm Optical Turbidity Sensor</td>
          <td class="vendor">OEM Industrial / DF-Robot Modbus (Static Optics)</td>
          <td class="price">₹9,500</td>
          <td>Nephelometric 90° scatter measurement of suspended solids & silt; flags sewage sludge intrusion without reagents.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial Flat-Glass Isolated pH Sensor</td>
          <td class="vendor">Renke OEM / Sensorex Double-Junction Glass Probe</td>
          <td class="price">₹5,000</td>
          <td>Measures hydrogen-ion activity; flags chemical dumping, septic acidification, and basic algal blooms.</td>
        </tr>
        <tr>
          <td class="part-name">Waterproof SS316 Temperature Probe</td>
          <td class="vendor">Dallas / Maxim Integrated (DS18B20 Encapsulated Pair)</td>
          <td class="price">₹600</td>
          <td>Water temperature monitoring; drives Nernst temperature compensation algorithms for pH and EC.</td>
        </tr>
        <tr>
          <td class="part-name">ESP32 Microcontroller + Isolated RS-485 Hub</td>
          <td class="vendor">Espressif (ESP32-WROOM-32U) + Mornsun B0505S Isolator</td>
          <td class="price">₹1,500</td>
          <td>Master edge board; polls Modbus RS-485 sensors, executes compensation algorithms, and packages telemetry.</td>
        </tr>
        <tr>
          <td class="part-name">SIMCom A7672S 4G LTE-Cat1 Cellular IoT Module</td>
          <td class="vendor">SIMCom Wireless Solutions (A7672S Breakout + 3dBi Ant)</td>
          <td class="price">₹2,200</td>
          <td>Streams telemetry over 4G directly to cloud MySQL database server and emergency alert channels.</td>
        </tr>
        <tr>
          <td class="part-name">20W Solar Panel + 10A PWM Charge Controller</td>
          <td class="vendor">Loom Solar / Luminous 20W Poly + OEM 10A Controller</td>
          <td class="price">₹2,200</td>
          <td>Harvests solar power during daylight to recharge battery and power station autonomously.</td>
        </tr>
        <tr>
          <td class="part-name">12V 7Ah Sealed Lead-Acid (SLA) Battery</td>
          <td class="vendor">Exide Industries (Exide Powersafe Plus 12V 7Ah)</td>
          <td class="price">₹1,500</td>
          <td>Stores electrical energy for nocturnal operations and overcast days (2 to 3 days autonomy).</td>
        </tr>
        <tr>
          <td class="part-name">IP65 Weatherproof ABS Enclosure + Glands</td>
          <td class="vendor">Hensel / Sinox IP65 ABS Enclosure (250x180x100 mm)</td>
          <td class="price">₹1,200</td>
          <td>Protects edge controller, modem, and battery from rain, humidity, dust, and water spray.</td>
        </tr>
        <tr>
          <td class="part-name">DIY 4-Inch PVC Catamaran Pontoon Float & Anchor</td>
          <td class="vendor">Supreme / Astral Heavy PVC Pipe + Galvanized Chain</td>
          <td class="price">₹3,500</td>
          <td>Provides buoyant floating platform in open lake water and anchors station at fixed GPS coordinate.</td>
        </tr>
        <tr>
          <td class="part-name">Perforated Sensor Shroud + Copper Mesh Wrap</td>
          <td class="vendor">Custom Fabricated PVC Shroud + Copper Alloy Mesh</td>
          <td class="price">₹800</td>
          <td>Protective cage shielding submerged probes from debris and biofouling via passive copper ion release.</td>
        </tr>
        <tr>
          <td class="part-name">NIST Traceable Calibration Buffer Pack</td>
          <td class="vendor">Thermo Fisher Scientific / Hanna Instruments Packets</td>
          <td class="price">₹1,000</td>
          <td>Routine calibration standard chemicals (pH 4.01, 7.00, 10.01 & 1413 µS/cm EC) to ensure zero drift.</td>
        </tr>
        <tr class="tot-row">
          <td>TOTAL QUOTE 1 INITIAL CapEx</td>
          <td>Complete Turnkey 4-Sensor Sentry</td>
          <td class="price">₹35,500</td>
          <td>85% sewage ingress detection coverage; bi-weekly manual wipe required.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="footer">
    <span>Aarogya Jal (Phase 1) • Procurement Specification • Techno India NJR</span>
    <span>Page 1 of 3</span>
  </div>
</div>

<!-- PAGE 2: QUOTE 2 -->
<div class="page">
  <div>
    <div class="header">
      <div class="title-area">
        <h1>QUOTE 2: VALUE-ENGINEERED FIELD PILOT (₹71,500 CapEx)</h1>
        <p>Recommended Sweet Spot: BITS Pilani Pitch, Rajasthan iStart, 3 to 6-Month Lake Validation</p>
      </div>
      <div class="meta-tag">★ Recommended Pilot</div>
    </div>

    <div class="callout">
      <b>Institutional Cost Synergy:</b> Saves ~₹47,000 in upfront CapEx by leveraging university engineering lab benchtop reference meters and incubators for routine ground-truth calibrations.
    </div>

    <table>
      <thead>
        <tr>
          <th>Part / Component Name</th>
          <th>Manufacturer / Candidate Model</th>
          <th>Unit Price</th>
          <th>Operational Limnological Use & Purpose</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="part-name">Galvanic Dissolved Oxygen (DO) Probe + Transmitter</td>
          <td class="vendor">DFRobot Industrial / OEM Galvanic DO Transducer</td>
          <td class="price">₹14,000</td>
          <td>Continuous dissolved oxygen (mg/L and % saturation) monitoring; vital for detecting bacterial decomposition of raw sewage (hypoxia &lt;4 mg/L) and toxic algal blooms.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial Optical Turbidity Sensor (860nm Near-IR)</td>
          <td class="vendor">Rika Sensors / Renke OEM Optical Modbus Turbidity</td>
          <td class="price">₹9,500</td>
          <td>Measures water clarity and suspended particulate matter without reagent; near-IR eliminates sunlight error.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial 4-Electrode EC / Salinity Probe</td>
          <td class="vendor">Rika Sensors (RK500-08 Graphite RS-485 Modbus)</td>
          <td class="price">₹6,500</td>
          <td>Wide-range electrical conductivity measurement; detects dissolved urine salts, sewage ingress, and runoff.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial Flat-Glass Isolated pH Sensor</td>
          <td class="vendor">Renke OEM / Sensorex S8000 Industrial Series</td>
          <td class="price">₹5,000</td>
          <td>Continuous acidity/alkalinity measurement; flags industrial effluent, chemical dumping, and algal bloom spikes.</td>
        </tr>
        <tr>
          <td class="part-name">Dual-Depth Water Temp Profiler (0.5m & 3.0m)</td>
          <td class="vendor">Maxim Integrated / Dallas (DS18B20 SS316 Pair)</td>
          <td class="price">₹600</td>
          <td>Detects lake thermal inversion / destratification (toxic anoxic hypolimnion turnover) and probe compensations.</td>
        </tr>
        <tr>
          <td class="part-name">Waterproof Ultrasonic / Hydrostatic Level Sensor</td>
          <td class="vendor">JSN-SR04T-2.0 / OEM Submersible Pressure Transducer</td>
          <td class="price">₹2,500</td>
          <td>Measures distance to water surface and lake elevation relative to datum; tracks reservoir storage depletion.</td>
        </tr>
        <tr>
          <td class="part-name">Tipping Bucket Rain Gauge + Barometer</td>
          <td class="vendor">Misol WH-SP-RG (0.2mm) + Bosch BMP280 Barometer</td>
          <td class="price">₹2,800</td>
          <td>Measures rainfall rate and atmospheric pressure; essential for barometric DO calibration and first-flush storm runoff.</td>
        </tr>
        <tr>
          <td class="part-name">ESP32-S3 Industrial Controller + RTC + SD</td>
          <td class="vendor">Espressif (ESP32-S3-DevKitC-1) + ADM2483 + DS3231 RTC</td>
          <td class="price">₹2,800</td>
          <td>Master controller; hardware UART Modbus polling, local non-volatile SD telemetry backup, and cryptographic signing.</td>
        </tr>
        <tr>
          <td class="part-name">SIMCom A7672S 4G LTE-Cat1 Cellular IoT Module</td>
          <td class="vendor">SIMCom Wireless Solutions (A7672S + 5dBi Antenna)</td>
          <td class="price">₹2,400</td>
          <td>Real-time cellular link streaming sensor readings directly to cloud MySQL database every 1–2 minutes.</td>
        </tr>
        <tr>
          <td class="part-name">Power Board, TVS Protection & Isolated DC-DC</td>
          <td class="vendor">Mornsun / Texas Instruments (B0505S, LM2596S, TVS)</td>
          <td class="price">₹1,500</td>
          <td>Protects sensitive microelectronics against inductive voltage spikes, solar transients, and ground loops.</td>
        </tr>
        <tr>
          <td class="part-name">25W Monocrystalline High-Efficiency Solar Panel</td>
          <td class="vendor">Loom Solar / Waaree Energies 25W Mono PERC</td>
          <td class="price">₹2,200</td>
          <td>High-efficiency power generation even under low-light diffuse monsoon conditions to maintain battery charge.</td>
        </tr>
        <tr>
          <td class="part-name">12V 12Ah Deep-Cycle Battery Pack with BMS</td>
          <td class="vendor">Topband / Exide Deep-Cycle SLA or LiFePO4 Pack</td>
          <td class="price">₹4,500</td>
          <td>Provides continuous 3 to 5-day power autonomy through heavy cloud cover and nocturnal telemetry polling.</td>
        </tr>
        <tr>
          <td class="part-name">10A MPPT / Smart Solar Charge Controller</td>
          <td class="vendor">EPsolar / EPEver LandStar 10A Controller</td>
          <td class="price">₹1,500</td>
          <td>Optimizes solar power harvesting and safeguards battery from overcharging and deep discharge degradation.</td>
        </tr>
        <tr>
          <td class="part-name">IP66 Weatherproof Polycarbonate Station Enclosure</td>
          <td class="vendor">Hensel / Fibox NEMA 4X Polycarbonate Box</td>
          <td class="price">₹2,500</td>
          <td>Hermetically seals master board, battery, and modems against intense UV radiation, water ingress, and corrosion.</td>
        </tr>
        <tr>
          <td class="part-name">Modular PVC/FRP Pontoon Catamaran Buoy Float</td>
          <td class="vendor">Custom Modular Marine FRP Pontoon + Anchor Rigging</td>
          <td class="price">₹5,500</td>
          <td>Stable hydrodynamic floating platform designed for wind-whipped lake conditions with anti-capsizing ballast.</td>
        </tr>
        <tr>
          <td class="part-name">Flow Shroud with Copper-Nickel Anti-Fouling Screen</td>
          <td class="vendor">Custom SS304/PVC Flow Shroud + CuNi Mesh Wrap</td>
          <td class="price">₹2,200</td>
          <td>Channelizes uniform water laminar flow past sensor tips while inhibiting algae adhesion and biofouling.</td>
        </tr>
        <tr>
          <td class="part-name">Submersible Shielded Polyurethane (PUR) Cables</td>
          <td class="vendor">Lapp Group / Helukabel Submersible PUR Multicore</td>
          <td class="price">₹2,500</td>
          <td>Heavy-duty waterproof cabling connecting submerged probes to the surface deck without water wicking.</td>
        </tr>
        <tr>
          <td class="part-name">Certified Calibration Standard Buffer Pack</td>
          <td class="vendor">Hanna Instruments / Thermo Fisher Standard Set</td>
          <td class="price">₹3,000</td>
          <td>Chemical standards for two-point calibrations (pH 4/7/10, EC 1413 µS/cm, Sodium Sulfite DO zero).</td>
        </tr>
        <tr>
          <td class="part-name">College Institutional Lab Synergies</td>
          <td class="vendor">Techno NJR / MLSU Environmental Engineering Lab</td>
          <td class="price">₹0</td>
          <td>Provides certified bench reference meters & bacterial verification without buying ₹47,000+ benchtop tools.</td>
        </tr>
        <tr class="tot-row">
          <td>TOTAL QUOTE 2 INITIAL CapEx</td>
          <td>Turnkey Field Pilot Station (7 Probes)</td>
          <td class="price">₹71,500</td>
          <td>Adds Dissolved Oxygen & Water Level; comprehensive bacterial proxy coverage.</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="footer">
    <span>Aarogya Jal (Phase 1) • Procurement Specification • Techno India NJR</span>
    <span>Page 2 of 3</span>
  </div>
</div>

<!-- PAGE 3: QUOTE 3 -->
<div class="page">
  <div>
    <div class="header">
      <div class="title-area">
        <h1>QUOTE 3: MUNICIPAL ENTERPRISE STATION (₹3,15,000 CapEx)</h1>
        <p>Smart City Tender & Municipal SCADA Grade • Autonomous Motorized Wipers • Zero Manual Cleaning</p>
      </div>
      <div class="meta-tag">Enterprise / SCADA</div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Part / Component Name</th>
          <th>Manufacturer / Candidate Model</th>
          <th>Unit Price</th>
          <th>Operational Limnological Use & Purpose</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="part-name">Optical Luminescent DO with Motorized Wiper</td>
          <td class="vendor">Yosemitech (Y504-A Luminescent Optical DO)</td>
          <td class="price">₹48,000</td>
          <td>Luminescent optical quenching with automatic mechanical brush wiper; zero oxygen consumption, zero refills.</td>
        </tr>
        <tr>
          <td class="part-name">Optical Turbidity with Motorized Wiper</td>
          <td class="vendor">Yosemitech (Y510-A Infrared Optical Turbidity)</td>
          <td class="price">₹44,000</td>
          <td>Self-cleaning nephelometric probe with automatic wiper; unhindered by dense algae or heavy silt.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial 4-Electrode Toroidal Conductivity Sensor</td>
          <td class="vendor">Rika Sensors (RK500-08 Industrial Modbus / Sensorex)</td>
          <td class="price">₹22,000</td>
          <td>Toroidal conductivity; immune to polarization resistance; captures sewage contamination across wide range.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial Preamplified Double-Junction Glass pH</td>
          <td class="vendor">Sensorex (S8000 Series / Renke Heavy-Duty Glass)</td>
          <td class="price">₹18,500</td>
          <td>Sealed gel-filled double junction; resists sulfide poisoning and chemical degradation in wastewater.</td>
        </tr>
        <tr>
          <td class="part-name">Dual PT1000 Class-A RTD Water Temp Sensors</td>
          <td class="vendor">TE Connectivity / Sensata PT1000 Class A SS316</td>
          <td class="price">₹3,500</td>
          <td>0.05°C precision thermal profiling at surface & thermocline; detects overturn and drives compensation.</td>
        </tr>
        <tr>
          <td class="part-name">Multi-Channel Galvanic Isolation Hub & Board</td>
          <td class="vendor">Custom Industrial PCB with ADI ADM2483 Isolators</td>
          <td class="price">₹20,000</td>
          <td>2.5kV galvanic isolation per channel, eliminating inter-probe ground loop cross-talk in conductive water.</td>
        </tr>
        <tr>
          <td class="part-name">Submersible Hydrostatic Level Transducer (0–5m)</td>
          <td class="vendor">Rika Sensors (RK500-01 Submersible Level Sensor)</td>
          <td class="price">₹14,000</td>
          <td>Vented gauge piezoresistive transducer with Kevlar atmospheric tube; millimeter-level elevation accuracy.</td>
        </tr>
        <tr>
          <td class="part-name">Tipping Bucket Precision Rain Gauge (0.2mm)</td>
          <td class="vendor">Misol (WH-SP-RG Aerodynamic Tipping Bucket)</td>
          <td class="price">₹5,500</td>
          <td>Quantifies rain intensity; detects stormwater runoff events flushing urban contaminants into the lake.</td>
        </tr>
        <tr>
          <td class="part-name">Barometric Pressure Sensor in Radiation Shield</td>
          <td class="vendor">Bosch Sensortec (BMP280 / BME280 Precision)</td>
          <td class="price">₹1,800</td>
          <td>Local atmospheric barometric pressure for dynamic barometric correction of Dissolved Oxygen equations.</td>
        </tr>
        <tr>
          <td class="part-name">ESP32-S3 Industrial Controller Unit (IP67)</td>
          <td class="vendor">Espressif Systems (ESP32-S3 Industrial Carrier)</td>
          <td class="price">₹6,500</td>
          <td>Executes Modbus schedules, Wi-Fi/LTE failover, data encryption, anomaly detection, and sensor health scoring.</td>
        </tr>
        <tr>
          <td class="part-name">Quectel 4G LTE-M / NB-IoT Modem + Dome Antenna</td>
          <td class="vendor">Quectel Wireless (Quectel EC200U-CN Cat-1)</td>
          <td class="price">₹5,200</td>
          <td>Carrier-grade cellular modem with multi-operator roaming for ultra-reliable telemetry to municipal SCADA.</td>
        </tr>
        <tr>
          <td class="part-name">Industrial Power Board, TVS, RTC & MicroSD</td>
          <td class="vendor">Texas Instruments + Maxim Integrated Carrier</td>
          <td class="price">₹4,300</td>
          <td>Power sequencing, battery health telemetry, hardware watchdog, and dual micro-SD card event logs.</td>
        </tr>
        <tr>
          <td class="part-name">50W Monocrystalline Rigid Solar PV Panel + Mount</td>
          <td class="vendor">Waaree Energies / Loom Solar 50W Mono PERC</td>
          <td class="price">₹3,500</td>
          <td>Ample power generation supporting motorized wiper spikes and continuous telemetry in all seasons.</td>
        </tr>
        <tr>
          <td class="part-name">12V 24Ah LiFePO4 Battery Pack with Smart BMS</td>
          <td class="vendor">Custom Grade-A LiFePO4 Pack (3,000+ cycle life)</td>
          <td class="price">₹14,500</td>
          <td>Powers station for 7 consecutive days of zero sunshine (monsoon endurance); immune to thermal runaway.</td>
        </tr>
        <tr>
          <td class="part-name">10A MPPT Smart Charge Controller with RS-485</td>
          <td class="vendor">Victron Energy (BlueSolar 75/10) / EPEver 1210AN</td>
          <td class="price">₹4,200</td>
          <td>MPPT with 98% efficiency and real-time battery voltage/current reporting over Modbus.</td>
        </tr>
        <tr>
          <td class="part-name">Marine Tinned Copper Wiring, MC4 & Glands</td>
          <td class="vendor">Lapp Group / Amphenol Solar Marine Accessories</td>
          <td class="price">₹2,500</td>
          <td>Salt-spray and humidity corrosion-proof wiring connecting solar panel, charge controller, and edge box.</td>
        </tr>
        <tr>
          <td class="part-name">IP67 Polycarbonate Station Enclosure</td>
          <td class="vendor">Hensel (Mi-Series) / Fibox ARCA IP67 Enclosure</td>
          <td class="price">₹5,500</td>
          <td>Vandal-resistant, submersible enclosure protecting electronics, batteries, and communications modules.</td>
        </tr>
        <tr>
          <td class="part-name">Marine Anodized 6061-T6 Aluminum Mast (2m)</td>
          <td class="vendor">Custom Marine Fabricated Aluminum Mast</td>
          <td class="price">₹7,500</td>
          <td>Elevates rain gauge, solar panel, antenna, and weather sensors above water spray and wave splashing.</td>
        </tr>
        <tr>
          <td class="part-name">Perforated SS316 Sensor Cage + CuNi Mesh</td>
          <td class="vendor">Marine Fabricated SS316 Cage + 90/10 CuNi Screen</td>
          <td class="price">₹8,500</td>
          <td>Protects expensive optical sensors from waterborne debris, boat wake collisions, and macro-invertebrates.</td>
        </tr>
        <tr>
          <td class="part-name">Rotomolded HDPE Mooring Buoy System</td>
          <td class="vendor">Sealite / Resinex Marine Mooring Buoy System</td>
          <td class="price">₹16,000</td>
          <td>Heavy commercial marine buoy capable of remaining moored in open lake waters for 5+ years.</td>
        </tr>
        <tr>
          <td class="part-name">Submersible Shielded PUR Cables with Kevlar Core</td>
          <td class="vendor">Helukabel / Igus Chainflex Submersible PUR Cable</td>
          <td class="price">₹6,500</td>
          <td>Hydrolysis-resistant, abrasion-resistant cabling with Kevlar strain relief rated for long-term immersion.</td>
        </tr>
        <tr>
          <td class="part-name">Handheld Multi-Parameter Reference Meter Kit</td>
          <td class="vendor">Apera Instruments (PC60-Z Bluetooth) / HI98194</td>
          <td class="price">₹32,000</td>
          <td>Field technician ground-truth inspection tool used during visits to verify in-situ sensor calibration drift.</td>
        </tr>
        <tr>
          <td class="part-name">Certified NIST Traceable Standard Buffer Solutions</td>
          <td class="vendor">Merck Millipore / Thermo Fisher Calibration Standards</td>
          <td class="price">₹6,000</td>
          <td>High-precision certified standard buffers for on-site sensor recalibration.</td>
        </tr>
        <tr>
          <td class="part-name">Aquagenx CBT Portable Microbial Field Kits</td>
          <td class="vendor">Aquagenx Compartment Bag Test (CBT) Kit (20 tests)</td>
          <td class="price">₹15,000</td>
          <td>Portable bacterial quantification kit establishing empirical correlation between probes and coliform MPN.</td>
        </tr>
        <tr class="tot-row">
          <td>TOTAL QUOTE 3 INITIAL CapEx</td>
          <td>Municipal Enterprise SCADA Station</td>
          <td class="price">₹3,15,000</td>
          <td>Autonomous motorized wipers; zero biofouling maintenance; certified legal defensibility.</td>
        </tr>
      </tbody>
    </table>

    <div class="callout-amber">
      <b>Annual OpEx (Year 1): ₹88,000</b> — Covers fortnightly accredited lab testing (32 samples @ ₹1,500 = ₹48k), field boat visits (26 visits @ ₹1,000 = ₹26k), 4G IoT SIM (₹3.6k), and cloud ingestion server (₹10.4k).
    </div>
  </div>
  <div class="footer">
    <span>Aarogya Jal (Phase 1) • Procurement Specification • Techno India NJR</span>
    <span>Page 3 of 3</span>
  </div>
</div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated HTML: {html_path}")

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

res = subprocess.run(cmd, capture_output=True, text=True)
if pdf_path.exists():
    print(f"Generated PDF: {pdf_path} ({pdf_path.stat().st_size / 1024:.2f} KB)")
else:
    print("PDF generation failed.")
