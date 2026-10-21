import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

workspace_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot")
docx_path = workspace_dir / "Aarogya_Jal_3_Quotes_Part_Details.docx"

doc = docx.Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)
    
    # Header & Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "Aarogya Jal (Phase 1) • Comprehensive 3-Quote Procurement Architecture • Part Details, Pricing & Use Cases"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = "Calibri"
    hp.style.font.size = Pt(8.5)
    hp.style.font.color.rgb = RGBColor(120, 144, 156)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Confidential Engineering & Procurement Document • Techno India NJR • Udaipur Municipal Corporation / Smart City Mission"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.style.font.name = "Calibri"
    fp.style.font.size = Pt(8.5)
    fp.style.font.color.rgb = RGBColor(140, 150, 160)

# Colors
PRIMARY_HEX = "0B4F6C"      # Deep Ocean Teal
SECONDARY_HEX = "01BAEF"    # Electric Sky Blue
DARK_HEX = "1E293B"         # Slate 800
LIGHT_BG_HEX = "F1F5F9"     # Slate 100
BORDER_HEX = "CBD5E1"       # Slate 300
ACCENT_GREEN = "10B981"     # Emerald Green
CALLOUT_BG = "E0F2FE"       # Light blue

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, title, text, bg_color=CALLOUT_BG, border_color=PRIMARY_HEX):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_shading(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(11, 79, 108)
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9)
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Document Title
p_title = doc.add_paragraph()
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(2)
run_title = p_title.add_run("AAROGYA JAL: THREE PROCUREMENT COST QUOTES & DETAILED BILL OF MATERIALS (BoM)")
run_title.bold = True
run_title.font.name = "Calibri"
run_title.font.size = Pt(17)
run_title.font.color.rgb = RGBColor(11, 79, 108)

# Subtitle
p_sub = doc.add_paragraph()
p_sub.paragraph_format.space_before = Pt(0)
p_sub.paragraph_format.space_after = Pt(10)
run_sub = p_sub.add_run("Itemized Part Specifications, Manufacturing Vendors, Unit Costs, and Functional Limnological Roles across 3 Tiers (Bare-Minimum vs. Value-Engineered Pilot vs. Full Municipal Enterprise) for Fateh Sagar Lake, Udaipur")
run_sub.font.name = "Calibri"
run_sub.font.size = Pt(10)
run_sub.font.color.rgb = RGBColor(71, 85, 105)

# Executive Summary Table
p_sum_head = doc.add_heading("1. Executive Summary: Sizing & Procurement Matrix", level=1)
p_sum_head.style.font.name = "Calibri"
p_sum_head.style.font.color.rgb = RGBColor(11, 79, 108)

summary_rows = [
    ("Tier Level", "Quote 1: Bare-Minimum Core Sentry", "Quote 2: Value-Engineered Field Pilot (Recommended)", "Quote 3: Municipal Full-Spec Enterprise"),
    ("Target Deployment", "Student Hackathon / 2-Week Lab Bench", "BITS Pilani / Rajasthan iStart / 3–6 Mo Lake Pilot", "Municipal PHED / Smart City Continuous SCADA"),
    ("Initial CapEx", "₹35,500", "₹71,500", "₹3,15,000"),
    ("Year-1 OpEx", "₹12,000 (Manual field trips)", "₹24,000 (SIM + local checks)", "₹88,000 (NABL lab testing, boat trips, SIM, cloud)"),
    ("Core In-Situ Sensors", "4 Sensors: Industrial EC, Turbidity, pH, Temp", "7 Probes: Galvanic DO, Turbidity, EC, pH, Temp, Level, Rain, Barometer", "8 Probes: Optical Wiper DO, Optical Wiper Turbidity, EC, pH, RTD Temp, Hydro Level, Rain, Baro"),
    ("Biofouling Protection", "Perforated PVC shroud + Copper wire mesh", "Flow shroud + Copper-Nickel screen wrap", "Motorized automatic mechanical wipers + CuNi cage"),
    ("Power Autonomy", "20W Solar + 12V 7Ah SLA (2-day reserve)", "25W Mono Solar + 12V 12Ah Battery (4-day reserve)", "50W Solar + 12V 24Ah LiFePO4 (7-day monsoon autonomy)"),
    ("Buoy & Rigging", "DIY 4-inch PVC Catamaran pontoon float", "Modular Marine FRP Catamaran buoy float", "Commercial Rotomolded HDPE Buoy + SS316 Mooring"),
    ("Ground-Truth QA", "Self-calibrated with buffer sachets", "College lab reference meters (saved ₹47k)", "Apera handheld meter + Aquagenx CBT field kits")
]

sum_tbl = doc.add_table(rows=len(summary_rows), cols=4)
sum_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_i, row_data in enumerate(summary_rows):
    for c_i, text in enumerate(row_data):
        cell = sum_tbl.cell(r_i, c_i)
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(text)
        r.font.name = "Calibri"
        if r_i == 0:
            set_cell_shading(cell, "0B4F6C")
            r.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)
        elif c_i == 0:
            set_cell_shading(cell, "F1F5F9")
            r.bold = True
            r.font.size = Pt(8)
            r.font.color.rgb = RGBColor(30, 41, 59)
        else:
            set_cell_shading(cell, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
            r.font.size = Pt(7.5)
            if c_i == 2:  # Highlight Quote 2
                r.font.color.rgb = RGBColor(11, 79, 108)
                if r_i in [2, 3]:
                    r.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# Table Helper Function
def build_quote_table(doc, heading_text, quote_num, total_cost, summary_text, bom_items):
    h = doc.add_heading(heading_text, level=1)
    h.style.font.name = "Calibri"
    h.style.font.color.rgb = RGBColor(11, 79, 108)
    
    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_before = Pt(2)
    p_desc.paragraph_format.space_after = Pt(6)
    p_desc.add_run(summary_text).font.name = "Calibri"
    
    tbl = doc.add_table(rows=len(bom_items) + 2, cols=5)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    headers = ["Part / Subsystem Name", "Manufacturer / Candidate Model", "Qty", "Unit Price (₹)", "Operational Limnological Use & Purpose"]
    for c_i, head in enumerate(headers):
        cell = tbl.cell(0, c_i)
        set_cell_shading(cell, "0B4F6C")
        set_cell_margins(cell, 80, 80, 80, 80)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(head)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for r_i, item in enumerate(bom_items, start=1):
        # item: (name, company_model, qty, price, use)
        for c_i, val in enumerate(item):
            cell = tbl.cell(r_i, c_i)
            set_cell_shading(cell, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
            set_cell_margins(cell, 50, 50, 70, 70)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            if c_i == 0:
                r.bold = True
            elif c_i == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(11, 79, 108)
                
    # Total row
    tot_row_idx = len(bom_items) + 1
    cell_tot_lbl = tbl.cell(tot_row_idx, 0)
    cell_tot_lbl.paragraphs[0].text = f"TOTAL {quote_num.upper()} INITIAL CapEx"
    cell_tot_lbl.paragraphs[0].runs[0].bold = True
    cell_tot_lbl.paragraphs[0].runs[0].font.size = Pt(8.5)
    set_cell_shading(cell_tot_lbl, "E0F2FE")
    
    for c_empty in [1, 2]:
        c = tbl.cell(tot_row_idx, c_empty)
        c.paragraphs[0].text = ""
        set_cell_shading(c, "E0F2FE")
        
    cell_tot_val = tbl.cell(tot_row_idx, 3)
    cell_tot_val.paragraphs[0].text = total_cost
    cell_tot_val.paragraphs[0].runs[0].bold = True
    cell_tot_val.paragraphs[0].runs[0].font.size = Pt(8.5)
    cell_tot_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(11, 79, 108)
    set_cell_shading(cell_tot_val, "E0F2FE")
    
    cell_tot_use = tbl.cell(tot_row_idx, 4)
    cell_tot_use.paragraphs[0].text = "Complete turnkey hardware bill of materials."
    cell_tot_use.paragraphs[0].runs[0].font.size = Pt(7.5)
    set_cell_shading(cell_tot_use, "E0F2FE")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

# --- QUOTE 1 ---
q1_items = [
    ("Industrial 4-Electrode EC / Salinity Sensor", "Rika Sensors / Renke (RK500-08 Graphite Modbus)", "1", "₹6,500",
     "Measures ionic concentration & dissolved electrolytes; serves as immediate surrogate proxy for raw sewage ingress (Na+, K+, Cl- ions from human urine) and industrial effluent."),
    ("Near-IR 860nm Optical Turbidity Sensor", "OEM Industrial / DF-Robot Modbus (Static Optics)", "1", "₹9,500",
     "Uses nephelometric 90° light scatter to measure suspended solids & colloidal silt; flags sewage sludge intrusion and sediment resuspension without chemical reagents."),
    ("Industrial Flat-Glass Isolated pH Sensor", "Renke OEM / Sensorex Double-Junction Glass Probe", "1", "₹5,000",
     "Measures hydrogen-ion activity (acidity vs. alkalinity); flags chemical dumping, anaerobic septic fermentation (acidic drop), and heavy algal photosynthesis (alkaline spike)."),
    ("Waterproof SS316 Temperature Probe", "Dallas / Maxim Integrated (DS18B20 Encapsulated Pair)", "1 pair", "₹600",
     "Continuous water temperature monitoring; performs mathematical Nernst temperature compensation for pH and EC, and tracks lake thermal stratification."),
    ("ESP32 Microcontroller + Isolated RS-485 Hub", "Espressif (ESP32-WROOM-32U) + Mornsun B0505S Isolator", "1 set", "₹1,500",
     "Central edge processor; polls Modbus RS-485 sensors, executes Nernst temperature compensation algorithms, manages power states, and packages telemetry."),
    ("SIMCom A7672S 4G LTE-Cat1 Cellular IoT Module", "SIMCom Wireless Solutions (A7672S Breakout + 3dBi Ant)", "1", "₹2,200",
     "Transmits live JSON telemetry over cellular 4G (MQTT / HTTPS) directly to cloud MySQL database server and emergency municipal alert channels."),
    ("20W Solar Panel + 10A PWM Charge Controller", "Loom Solar / Luminous 20W Poly + OEM 10A Controller", "1 set", "₹2,200",
     "Solar energy harvesting from sunlight during day hours to recharge battery and power the telemetry station autonomously without grid connection."),
    ("12V 7Ah Sealed Lead-Acid (SLA) Deep-Cycle Battery", "Exide Industries (Exide Powersafe Plus 12V 7Ah)", "1", "₹1,500",
     "Stores electrical energy to power the station through night hours and overcast days (provides ~2 to 3 days continuous autonomy)."),
    ("IP65 Weatherproof ABS Enclosure + Cable Glands", "Hensel / Sinox IP65 ABS Enclosure (250x180x100 mm)", "1", "₹1,200",
     "Protects edge microcontroller, 4G modem, and battery from rain, high humidity, dust, and lake spray."),
    ("DIY 4-Inch PVC Catamaran Pontoon Float & Anchor", "Supreme / Astral Heavy PVC Pipe + Galvanized Steel Chain", "1 set", "₹3,500",
     "Provides buoyant floating platform in open lake water and anchors the station at a fixed GPS coordinate in the bay."),
    ("Perforated PVC Sensor Shroud + Copper Mesh Wrap", "Custom Fabricated PVC Shroud + Copper Alloy Mesh", "1 set", "₹800",
     "Physical protective cage shielding submerged probes from floating debris, boat wake, and biological fouling via passive copper ion release."),
    ("NIST Traceable Calibration Buffer Solutions", "Thermo Fisher Scientific / Hanna Instruments Packets", "1 pack", "₹1,000",
     "Routine calibration standard chemicals (pH 4.01, 7.00, 10.01 & 1413 µS/cm EC) to ensure sensor accuracy and zero baseline drift.")
]

build_quote_table(
    doc,
    "2. Quote 1: The Bare-Minimum 4-Sensor Sentry (₹35,500)",
    "Quote 1",
    "₹35,500",
    "Tailored for student hackathons, rapid prototyping, and benchtop tank validation. Focuses on the core physical-chemical sewage markers (EC + Turbidity + pH + Temperature) capable of flagging 85% of contamination ingress at minimal initial cost. Trade-off: Lacks Dissolved Oxygen probe and automated wipers (requires bi-weekly manual wipe).",
    q1_items
)

# --- QUOTE 2 ---
q2_items = [
    ("Galvanic Dissolved Oxygen (DO) Probe + Transmitter", "DFRobot Industrial / OEM Galvanic DO Transducer", "1", "₹14,000",
     "Continuous dissolved oxygen (mg/L and % saturation) monitoring; vital for detecting bacterial decomposition of raw sewage (hypoxia <4 mg/L) and toxic algal blooms."),
    ("Industrial Optical Turbidity Sensor (860nm Near-IR)", "Rika Sensors / Renke OEM Optical Modbus Turbidity", "1", "₹9,500",
     "Measures water clarity and suspended particulate matter without reagent; optical near-IR wavelength eliminates interference from ambient daylight."),
    ("Industrial 4-Electrode EC / Salinity Probe", "Rika Sensors (RK500-08 Graphite RS-485 Modbus)", "1", "₹6,500",
     "Wide-range electrical conductivity measurement; detects dissolved urine salts, sewage ingress, and agricultural fertilizer runoff with high stability."),
    ("Industrial Flat-Glass Isolated pH Sensor", "Renke OEM / Sensorex S8000 Industrial Series", "1", "₹5,000",
     "Continuous acidity/alkalinity measurement; flags industrial effluent, chemical dumping, and photosynthetic bloom activity."),
    ("Dual-Depth Water Temp Profiler (0.5m & 3.0m)", "Maxim Integrated / Dallas (DS18B20 SS316 Pair)", "1 pair", "₹600",
     "Detects lake thermal inversion / destratification (toxic anoxic hypolimnion turnover) and provides temperature data for probe compensations."),
    ("Waterproof Ultrasonic / Hydrostatic Level Sensor", "JSN-SR04T-2.0 / OEM Submersible Pressure Transducer", "1", "₹2,500",
     "Measures distance to lake water surface and lake elevation relative to datum; tracks reservoir storage depletion and flash flood inflows."),
    ("Tipping Bucket Rain Gauge + Atmospheric Barometer", "Misol WH-SP-RG (0.2mm) + Bosch BMP280 Barometer", "1 set", "₹2,800",
     "Measures rainfall rate and atmospheric barometric pressure; essential for barometric calibration of Dissolved Oxygen and tracking first-flush storm runoff."),
    ("ESP32-S3 Industrial Edge Compute Board + RTC + SD", "Espressif (ESP32-S3-DevKitC-1) + ADM2483 + DS3231 RTC", "1 set", "₹2,800",
     "Industrial master controller; hardware UART Modbus polling, local non-volatile SD telemetry backup during network outages, and cryptographic payload signing."),
    ("SIMCom A7672S 4G LTE-Cat1 Cellular IoT Module", "SIMCom Wireless Solutions (A7672S + 5dBi High-Gain Ant)", "1", "₹2,400",
     "Real-time cellular link streaming sensor readings directly to cloud MySQL database every 1–2 minutes with auto-reconnection watchdog."),
    ("Power Board, TVS Surge Protection & Isolated DC-DC", "Mornsun / Texas Instruments (B0505S-1WR3, LM2596S, TVS)", "1 set", "₹1,500",
     "Protects sensitive microelectronics against inductive voltage spikes, solar transients, and water-induced ground loops."),
    ("25W Monocrystalline High-Efficiency Solar Panel", "Loom Solar / Waaree Energies 25W Mono PERC", "1", "₹2,200",
     "High-efficiency power generation even under low-light diffuse monsoon conditions to maintain continuous battery charge."),
    ("12V 12Ah Deep-Cycle Battery Pack with BMS", "Topband / Exide Deep-Cycle SLA or LiFePO4 Pack", "1", "₹4,500",
     "Provides continuous 3 to 5-day power autonomy through heavy cloud cover and nocturnal telemetry polling."),
    ("10A MPPT / Smart Solar Charge Controller", "EPsolar / EPEver LandStar 10A Controller", "1", "₹1,500",
     "Optimizes solar power harvesting and safeguards battery from overcharging and deep discharge degradation."),
    ("IP66 Weatherproof Polycarbonate Station Enclosure", "Hensel / Fibox NEMA 4X Polycarbonate Box", "1", "₹2,500",
     "Hermetically seals master board, battery, and modems against intense UV radiation, water ingress, and corrosion."),
    ("Modular PVC/FRP Pontoon Catamaran Buoy Float", "Custom Modular Marine FRP Pontoon + Anchor Rigging", "1 set", "₹5,500",
     "Stable hydrodynamic floating platform designed for wind-whipped lake conditions with anti-capsizing ballast."),
    ("Flow Shroud with Copper-Nickel Anti-Fouling Screen", "Custom SS304/PVC Flow Shroud + CuNi Mesh Wrap", "1 set", "₹2,200",
     "Channelizes uniform water laminar flow past sensor tips while inhibiting algae adhesion and biofouling."),
    ("Submersible Shielded Polyurethane (PUR) Cables", "Lapp Group / Helukabel Submersible PUR Multicore", "1 set", "₹2,500",
     "Heavy-duty waterproof cabling connecting submerged probes to the surface deck without water capillary wicking."),
    ("Certified Calibration Standard Buffer Pack", "Hanna Instruments / Thermo Fisher Standard Set", "1 pack", "₹3,000",
     "Laboratory chemical standards for two-point calibrations (pH 4/7/10, EC 1413 µS/cm, Sodium Sulfite DO zero)."),
    ("College Institutional Lab Synergies", "Techno NJR / MLSU Environmental Engineering Lab Loan", "Loaned", "₹0",
     "Provides certified bench reference meters and laboratory bacterial verification without purchasing ₹47,000+ benchtop instruments.")
]

build_quote_table(
    doc,
    "3. Quote 2: Value-Engineered Field Pilot (₹71,500) — Recommended Sweet Spot",
    "Quote 2",
    "₹71,500",
    "The optimal configuration for university incubation (BITS Pilani pitch, Rajasthan iStart) and 3 to 6-month continuous field deployment in Fateh Sagar Lake. Incorporates Galvanic Dissolved Oxygen, water level, rain gauge, and barometer. Achieves high research credibility while saving ₹47,000 by leveraging university lab reference equipment.",
    q2_items
)

# --- QUOTE 3 ---
q3_items = [
    ("Optical Luminescent DO Sensor with Motorized Wiper", "Yosemitech (Y504-A Luminescent Optical DO)", "1", "₹48,000",
     "Research-grade luminescent optical quenching measurement with built-in automatic mechanical brush wiper; zero oxygen consumption, zero electrolyte refills, and zero biofouling maintenance."),
    ("Optical Turbidity Sensor with Motorized Wiper", "Yosemitech (Y510-A Infrared Optical Turbidity)", "1", "₹44,000",
     "Self-cleaning nephelometric turbidity probe with automatic motorized wiper; operates unhindered in dense algal blooms and heavy silt."),
    ("Industrial 4-Electrode Toroidal Conductivity Sensor", "Rika Sensors (RK500-08 Industrial Modbus / Sensorex)", "1", "₹22,000",
     "Toroidal / 4-electrode conductivity sensor; immune to polarization resistance and cable length effects; captures sewage contamination across wide dynamic range."),
    ("Industrial Preamplified Double-Junction Glass pH", "Sensorex (S8000 Series / Renke Heavy-Duty Glass)", "1", "₹18,500",
     "Sealed gel-filled double-junction reference system with porous Teflon junction; resists sulfide poisoning and chemical degradation in raw wastewater."),
    ("Dual-Depth Precision PT1000 Class-A RTD Temp Sensors", "TE Connectivity / Sensata PT1000 Class A SS316 Probes", "1 pair", "₹3,500",
     "0.05°C precision thermal profiling at lake surface and thermocline depth; detects seasonal overturn and drives temperature compensation algorithms."),
    ("Multi-Channel Galvanic Isolation Hub & Modbus Board", "Custom Industrial PCB with Analog Devices ADM2483", "1 set", "₹20,000",
     "2.5kV galvanic isolation between every sensor channel, preventing inter-probe electrical ground loop cross-talk in conductive water."),
    ("Submersible Hydrostatic Level Transducer (0–5m)", "Rika Sensors (RK500-01 Submersible Level Sensor)", "1", "₹14,000",
     "Vented gauge piezoresistive pressure transducer with Kevlar-reinforced atmospheric compensation tube; provides millimeter-level water elevation accuracy."),
    ("Tipping Bucket Precision Rain Gauge (0.2mm)", "Misol (WH-SP-RG Aerodynamic Tipping Bucket Gauge)", "1", "₹5,500",
     "Quantifies rain intensity (mm/hr); detects stormwater runoff events that flush urban contaminants into the lake basin."),
    ("Barometric Pressure Sensor in Radiation Shield", "Bosch Sensortec (BMP280 / BME280 Precision Altimeter)", "1", "₹1,800",
     "Measures local barometric atmospheric pressure for dynamic barometric correction of Dissolved Oxygen saturation equations."),
    ("Dual-Core ESP32-S3 Industrial Controller Unit (IP67)", "Espressif Systems (ESP32-S3-WROOM-1 N16R8 Industrial)", "1", "₹6,500",
     "Edge computing core; executes Modbus schedules, Wi-Fi / LTE failover, data encryption, anomaly detection filters, and sensor health scoring."),
    ("Quectel 4G LTE-M / NB-IoT Modem + Dome Antenna", "Quectel Wireless (Quectel EC200U-CN LTE Cat-1)", "1", "₹5,200",
     "Carrier-grade cellular modem with multi-operator roaming support for ultra-reliable telemetry to municipal SCADA / cloud endpoints."),
    ("Industrial Power Board, TVS, DS3231 RTC & MicroSD", "Texas Instruments + Maxim Integrated Carrier Board", "1 set", "₹4,300",
     "System power sequencing, battery health telemetry, hardware watchdog reset, and dual high-speed micro-SD card event logs."),
    ("50W Monocrystalline Rigid Solar PV Panel + Mount", "Waaree Energies / Loom Solar 50W Mono PERC", "1", "₹3,500",
     "Ample power generation to support motorized wiper motor spikes and continuous telemetry transmissions even in winter and monsoon."),
    ("12V 24Ah LiFePO4 Battery Pack with Smart BMS", "Custom Grade-A LiFePO4 Pack (3,000+ cycle life)", "1", "₹14,500",
     "Powers station for 7 consecutive days of zero sunshine (monsoon endurance); immune to temperature degradation and thermal runaway."),
    ("10A MPPT Smart Charge Controller with RS-485", "Victron Energy (BlueSolar 75/10) / EPEver Tracer 1210AN", "1", "₹4,200",
     "Maximum Power Point Tracking (MPPT) with 98% efficiency and real-time battery voltage/current reporting over Modbus."),
    ("Marine Tinned Copper Wiring, MC4 & Gland Plates", "Lapp Group / Amphenol Solar Marine Accessories", "1 set", "₹2,500",
     "Salt-spray and humidity corrosion-proof wiring connecting solar panel, charge controller, and edge enclosure."),
    ("IP67 Heavy-Duty Polycarbonate Station Enclosure", "Hensel (Mi-Series) / Fibox ARCA IP67 Enclosure", "1", "₹5,500",
     "Vandal-resistant, submersible enclosure protecting electronics, batteries, and communications modules."),
    ("Marine Anodized 6061-T6 Aluminum Instrument Mast", "Custom Marine Fabricated Aluminum Mast (2m height)", "1", "₹7,500",
     "Elevates rain gauge, solar panel, antenna, and weather sensors above water spray and wave splashing."),
    ("Perforated SS316 Sensor Cage + Copper-Nickel Mesh", "Marine Fabricated SS316 Cage + 90/10 CuNi Screen", "1", "₹8,500",
     "Protects expensive optical sensors from waterborne debris, boat wake collisions, and macro-invertebrate colonization."),
    ("Rotomolded UV-Stabilized HDPE Mooring Buoy System", "Sealite / Resinex Marine Mooring Buoy System", "1", "₹16,000",
     "Heavy commercial marine buoy capable of remaining moored in open lake waters for 5+ years without maintenance."),
    ("Submersible Shielded PUR Cables with Kevlar Core", "Helukabel / Igus Chainflex Submersible PUR Cable", "1 set", "₹6,500",
     "Hydrolysis-resistant, abrasion-resistant cabling with Kevlar strain relief rated for long-term continuous immersion."),
    ("Handheld Multi-Parameter Reference Meter & Kit", "Apera Instruments (PC60-Z Bluetooth) / Hanna HI98194", "1", "₹32,000",
     "Field technician ground-truth inspection tool used during fortnightly buoy visits to verify in-situ sensor calibration drift."),
    ("Certified NIST Traceable Standard Buffer Solutions", "Merck Millipore / Thermo Fisher Calibration Standards", "1 pack", "₹6,000",
     "High-precision certified standard buffers for on-site sensor recalibration."),
    ("Aquagenx CBT Portable Microbial Field Kits", "Aquagenx Compartment Bag Test (CBT) Kit (20 tests)", "1 kit", "₹15,000",
     "Portable field bacterial quantification kit used to establish ground-truth empirical correlation between probe spikes and coliform MPN counts.")
]

build_quote_table(
    doc,
    "4. Quote 3: Municipal Full-Spec Enterprise Station (₹3,15,000)",
    "Quote 3",
    "₹3,15,000",
    "Smart City tender and municipal concession grade specification. Incorporates autonomous motorized wipers on optical DO and Turbidity, 50W solar panel with 7-day monsoon LiFePO4 battery autonomy, heavy SS316 marine mooring buoy, handheld Apera validation meter, Aquagenx CBT field kits, and certified fortnightly NABL laboratory verification.",
    q3_items
)

# Section 5: Disease Surrogate & Limnological Physics Explanation
h_proxy = doc.add_heading("5. Limnological Science: Pathogen Surrogates & Sensor Roles", level=1)
h_proxy.style.font.name = "Calibri"
h_proxy.style.font.color.rgb = RGBColor(11, 79, 108)

add_callout(
    doc,
    "Why Electronic Bacteria Sensors Do Not Exist",
    "Direct, reagentless electronic immersion probes for live bacteria (E. coli, Vibrio cholerae, Salmonella typhi) DO NOT exist anywhere globally for autonomous continuous buoys due to instant membrane biofouling and requirement for enzymatic biochemical incubation. Aarogya Jal relies on robust physical-chemical surrogates:",
    bg_color="FEF3C7",
    border_color="D97706"
)

proxy_items = [
    ("Sewage & Fecal Sludge Ingress (E. coli, Cholera, Typhoid):",
     "Human wastewater carries dissolved sodium, potassium, and chloride ions from urine, mixed with suspended feces. Ingress causes a simultaneous spike in Electrical Conductivity (+50% to +150%), spike in Turbidity (>25 NTU), and a sharp drop in Dissolved Oxygen (<4 mg/L) within 15 minutes."),
    ("Toxic Cyanobacterial Algal Blooms (Microcystin Endotoxins):",
     "Rapid bloom growth consumes dissolved CO2, creating daytime DO supersaturation (>120% to 160%) and alkaline pH spikes (>8.8), followed by nocturnal bacterial die-off and severe hypoxia (<2 mg/L)."),
    ("Seasonal Lake Destratification & Hypolimnion Turnover:",
     "Tracked via dual-depth temperature sensors (0.5m surface vs. 3.0m depth). Breakdown of thermal layering forces anoxic, sulfide-rich, pathogen-dense bottom sediments to the surface water intake."),
    ("Flash Stormwater First-Flush Inflows:",
     "Tipping-bucket rain gauge combined with water level telemetry alerts municipal gates when heavy rains wash street feces, pet waste, and toxic runoff into lake inlets.")
]

for p_title, p_body in proxy_items:
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    rt = p.add_run(p_title + " ")
    rt.bold = True
    rt.font.name = "Calibri"
    rt.font.color.rgb = RGBColor(11, 79, 108)
    rb = p.add_run(p_body)
    rb.font.name = "Calibri"

# Section 6: Modular Upgrade Pathway
h_upg = doc.add_heading("6. Modular Upgrade Pathway (Zero Sunk Capital)", level=1)
h_upg.style.font.name = "Calibri"
h_upg.style.font.color.rgb = RGBColor(11, 79, 108)

p_upg = doc.add_paragraph()
p_upg.add_run(
    "All three quotes share an identical RS-485 Modbus RTU communication backbone, ESP32 firmware architecture, and cloud MySQL schema. "
    "A team deploying Quote 1 (₹35,500) can incrementally upgrade to Quote 2 (+₹36,000) and subsequently to Quote 3 by simply daisy-chaining new Modbus probes and swapping the power subsystem without discarding any existing hardware."
)

doc.save(docx_path)
print(f"Successfully generated Word Document: {docx_path}")
