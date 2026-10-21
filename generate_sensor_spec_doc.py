import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

workspace_dir = Path(r"c:\Users\rkheu\Downloads\Aarogya jal reboot")
docx_path = workspace_dir / "Aarogya_Jal_Sensor_Specifications_and_BoM.docx"

doc = docx.Document()

# Page Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)
    
    # Header & Footer
    header = section.header
    hp = header.paragraphs[0]
    hp.text = "Aarogya Jal (Phase 1) • Multi-Tier Technical Specifications & 3-Quote Cost Distribution • Fateh Sagar Lake"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hp.style.font.name = "Calibri"
    hp.style.font.size = Pt(8.5)
    hp.style.font.color.rgb = RGBColor(120, 144, 156)
    
    footer = section.footer
    fp = footer.paragraphs[0]
    fp.text = "Confidential & Engineering Report • Techno India NJR • Udaipur Municipal Corporation / Smart City Mission"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fp.style.font.name = "Calibri"
    fp.style.font.size = Pt(8.5)
    fp.style.font.color.rgb = RGBColor(140, 150, 160)

# Color Constants
PRIMARY_HEX = "0B4F6C"      # Deep Ocean Teal
SECONDARY_HEX = "01BAEF"    # Electric Sky Blue
DARK_HEX = "1E293B"         # Slate 800
LIGHT_BG_HEX = "F1F5F9"     # Slate 100
BORDER_HEX = "CBD5E1"       # Slate 300
ACCENT_GREEN = "10B981"     # Emerald
ACCENT_RED = "EF4444"       # Amber/Red
CALLOUT_BG = "E0F2FE"       # Light blue callout
ALERT_BG = "FEF3C7"         # Light amber alert

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
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
    p.paragraph_format.space_after = Pt(3)
    run_t = p.add_run(f"📌 {title}\n")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor(11, 79, 108)
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Document Title
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(12)
title_p.paragraph_format.space_after = Pt(2)
run_title = title_p.add_run("AAROGYA JAL (PHASE 1): MULTI-TIER SENSOR SPECIFICATIONS & 3-QUOTE FINANCIAL ARCHITECTURE")
run_title.bold = True
run_title.font.name = "Calibri"
run_title.font.size = Pt(19)
run_title.font.color.rgb = RGBColor(11, 79, 108)

# Subtitle
sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(14)
run_sub = sub_p.add_run("Engineering Specifications, Limnological Pathogen-Proxy Physics, and Comprehensive 3-Tier Budget Options (Bare-Minimum vs. Value-Engineered Pilot vs. Full Municipal Enterprise) for Fateh Sagar Lake, Udaipur")
run_sub.font.name = "Calibri"
run_sub.font.size = Pt(10.5)
run_sub.font.color.rgb = RGBColor(71, 85, 105)

# Metadata Table
meta_tbl = doc.add_table(rows=2, cols=4)
meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    [("Project Site", "Fateh Sagar Lake, Udaipur"), ("Deployment Stage", "Phase 1 Static Buoy"), ("Target Stakeholders", "UMC, Smart City, iStart"), ("Document Version", "Rev 3.5 (Three-Tier Ready)")],
    [("Lead Engineering", "Manan Ramani & Team"), ("Quote 1 (Bare-Minimum)", "₹35,500 CapEx"), ("Quote 2 (Pilot Sweet Spot)", "₹71,500 CapEx"), ("Quote 3 (Full Municipal)", "₹3,15,000 CapEx")]
]
for r_idx, row in enumerate(meta_data):
    for c_idx, (k, v) in enumerate(row):
        cell = meta_tbl.cell(r_idx, c_idx)
        set_cell_shading(cell, "F8FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        rk = p.add_run(k + "\n")
        rk.font.name = "Calibri"
        rk.font.size = Pt(8)
        rk.font.color.rgb = RGBColor(100, 116, 139)
        rv = p.add_run(v)
        rv.bold = True
        rv.font.name = "Calibri"
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = RGBColor(15, 23, 42)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# SECTION 1: EXECUTIVE 3-TIER COMPARISON SUMMARY
h1_comp = doc.add_heading("1. Executive Financial Summary: The 3 Budget Quotes at a Glance", level=1)
h1_comp.style.font.name = "Calibri"
h1_comp.style.font.color.rgb = RGBColor(11, 79, 108)

add_callout(
    doc,
    "Strategic Budget Sizing Rationale",
    "Depending on funding availability (Student Hackathon vs. BITS/iStart Grant vs. Municipal Smart City Tender), the hardware architecture can scale across three distinct cost tiers without discarding previously developed firmware or cloud codebases.\n\n"
    "• Quote 1 (₹35,500): Focuses on the 4-sensor sewage surrogate core for immediate proof-of-concept.\n"
    "• Quote 2 (₹71,500): Recommended sweet spot for a 3-6 month field pilot, adding DO, level, rain, and power autonomy.\n"
    "• Quote 3 (₹3,15,000): Municipal enterprise standard with autonomous motorized wipers, NABL certifications, and 5-year station life."
)

# Comparison Table
comp_tbl = doc.add_table(rows=8, cols=4)
comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_comp = ["System Dimension", "Quote 1: Bare-Minimum Core", "Quote 2: Value-Engineered Pilot", "Quote 3: Municipal Full-Spec"]
for c_i, h in enumerate(headers_comp):
    c = comp_tbl.cell(0, c_i)
    set_cell_shading(c, "0B4F6C")
    set_cell_margins(c, 90, 90, 100, 100)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

comp_rows = [
    ("Total Initial CapEx", "₹35,500", "₹71,500 (Recommended)", "₹3,15,000"),
    ("Target Milestone", "Student Hackathon / Bench Demo", "BITS Pitch / iStart / 6-Mo Pilot", "Smart City RFP / Permanent Station"),
    ("Sensors Deployed", "4 Core: EC, Turbidity, pH, Temp", "7 Probes: DO, Turbidity, EC, pH, Temp, Level, Rain", "8 Probes: Wiped DO, Wiped Turbidity, EC, pH, Temp, Level, Rain, Baro"),
    ("Anti-Biofouling System", "Manual weekly wipe + Copper mesh", "Manual fortnightly wipe + Copper shroud", "Motorized Silicone Wipers (every 3h) + CuNi cage"),
    ("Telemetry & Compute", "ESP32 + 4G LTE-Cat1 Modem", "ESP32-S3 + 4G LTE + SD Log + RTC", "ESP32-S3 Industrial + Quectel 4G + Isolators"),
    ("Power Harvesting", "20W Solar Panel + 12V 7Ah SLA", "25W Mono Panel + 12V 12Ah Battery", "50W Mono Panel + 12V 24Ah LiFePO4 (7-day autonomy)"),
    ("Quality Assurance & Lab", "College bio lab petri plates", "College lab loaner meter + MacConkey", "Apera Handheld Meter + Aquagenx CBT + 26 NABL Panels")
]

for r_i, (dim, q1, q2, q3) in enumerate(comp_rows, start=1):
    for c_i, val in enumerate([dim, q1, q2, q3]):
        c = comp_tbl.cell(r_i, c_i)
        set_cell_shading(c, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
        set_cell_margins(c, 60, 60, 80, 80)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        if c_i == 0:
            r.bold = True
        elif c_i == 2:
            r.bold = True
            r.font.color.rgb = RGBColor(11, 79, 108)

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# SECTION 2: DISEASE SURVEILLANCE & PHYSICAL-CHEMICAL PROXY MODEL
h1_dis = doc.add_heading("2. Disease Surveillance Framework: The Physical-Chemical Proxy Model", level=1)
h1_dis.style.font.name = "Calibri"
h1_dis.style.font.color.rgb = RGBColor(11, 79, 108)

p_proxy = doc.add_paragraph()
p_proxy.add_run(
    "Direct, reagentless, electronic immersion probes for bacteria (E. coli, Vibrio cholerae, Salmonella typhi, Rotavirus) DO NOT EXIST globally for autonomous lake buoys due to instant membrane biofouling. "
    "Aarogya Jal monitors waterborne contamination and public health disease risk through real-time multi-parametric physical-chemical surrogates:\n"
)

dis_points = [
    ("Sewage & Enteric Pathogen Influx (E. coli, Cholera, Typhoid, Gastroenteritis, Hepatitis A):",
     " Sewage contains concentrated urine electrolytes (Na+, Cl-, K+), suspended fecal particles, and organic matter. This triggers a simultaneous Electrical Conductivity (EC) spike (+50% to +150%), Optical Turbidity spike (>25 NTU), and Dissolved Oxygen (DO) crash (<4.0 mg/L) within 15 minutes of ingress."),
    ("Cyanobacterial Toxic Algal Blooms (Microcystins & Anatoxins):",
     " Photosynthetic CO2 consumption causes midday DO supersaturation (>120% to 160%) and alkaline pH spikes (>8.8), followed by lethal nighttime hypoxia (<2.5 mg/L) and mass endotoxin release."),
    ("Seasonal Lake Inversion & Toxic Sediment Overturn:",
     " Monitored via dual-depth temperature probes (0.5m vs 3.0m). Breakdown of thermal stratification brings anoxic, foul-smelling, pathogen-rich hypolimnion sediments to the surface."),
    ("Stormwater Flash First-Flush Runoff:",
     " Tipping-bucket rain gauge combined with water level sensor logs sudden rain head, alerting municipal gates to runoff carrying street fecal sludge and heavy metals into lake bays.")
]

for d_title, d_desc in dis_points:
    dp = doc.add_paragraph(style='List Bullet')
    dp.paragraph_format.space_before = Pt(2)
    dp.paragraph_format.space_after = Pt(3)
    rt = dp.add_run(d_title)
    rt.bold = True
    rt.font.color.rgb = RGBColor(11, 79, 108)
    dp.add_run(d_desc)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# SECTION 3: QUOTE 1 — BARE-MINIMUM CORE SENTRY (₹35,500)
h1_q1 = doc.add_heading("3. Quote 1: The Bare-Minimum 4-Sensor Sentry (₹35,500)", level=1)
h1_q1.style.font.name = "Calibri"
h1_q1.style.font.color.rgb = RGBColor(11, 79, 108)

p_q1_desc = doc.add_paragraph()
p_q1_desc.add_run(
    "Designed for hackathons, early lab testing, and student grant proof-of-concept. It deploys the 4 essential surrogate sensors (EC + Turbidity + pH + Temperature) responsible for 85% of sewage detection capability, stripping all non-essential items."
)

q1_bom = [
    ("In-Situ Sensors", "Industrial 4-Electrode EC / Salinity Sensor", "Rika / OEM Graphite Modbus", "RS-485", "1", "₹6,500"),
    ("In-Situ Sensors", "Industrial Near-IR 860nm Optical Turbidity", "OEM Optical Modbus (Static)", "RS-485", "1", "₹9,500"),
    ("In-Situ Sensors", "Industrial Flat-Glass Isolated pH Sensor", "OEM Double-Junction Glass", "RS-485", "1", "₹5,000"),
    ("In-Situ Sensors", "Waterproof SS316 Temperature Probe", "DS18B20 Encapsulated", "1-Wire", "1 pair", "₹600"),
    ("Edge Compute", "ESP32 Microcontroller + MAX485 + Isolated DC-DC", "ESP32-WROOM-32U + B0505S", "GPIO/UART", "1 set", "₹1,500"),
    ("Edge Compute", "SIMCom A7672S 4G LTE-Cat1 Cellular Module", "A7672S Breakout + 3dBi Ant", "UART", "1", "₹2,200"),
    ("Solar Power", "20W Solar Panel + 10A PWM Charge Controller", "Poly/Mono 20W + PWM 10A", "DC Solar", "1 set", "₹2,200"),
    ("Solar Power", "12V 7Ah Sealed Lead-Acid Battery", "Exide Powersafe 12V 7Ah", "DC 12V", "1", "₹1,500"),
    ("Enclosure & Float", "IP65 ABS Weatherproof Junction Box + Glands", "ABS 250x180x100 mm", "IP65", "1", "₹1,200"),
    ("Enclosure & Float", "DIY 4-Inch PVC Catamaran Pontoon Float + Anchor", "Local PVC Pipe Assembly", "Buoyancy", "1 set", "₹3,500"),
    ("Anti-Fouling", "Perforated PVC Shroud with Copper Scrubber Mesh", "Local Fabricated Shroud", "Physical", "1 set", "₹800"),
    ("Calibration", "NIST Traceable pH & EC Standard Calibration Sachets", "Chemical Buffer Packets", "Chemical", "1 pack", "₹1,000")
]

q1_tbl = doc.add_table(rows=len(q1_bom)+2, cols=6)
q1_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_i, h in enumerate(["Subsystem", "Component Description", "Candidate Model", "Interface", "Qty", "Cost (₹)"]):
    cell = q1_tbl.cell(0, c_i)
    set_cell_shading(cell, "0B4F6C")
    set_cell_margins(cell, 80, 80, 80, 80)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(255, 255, 255)

for r_i, row in enumerate(q1_bom, start=1):
    for c_i, val in enumerate(row):
        cell = q1_tbl.cell(r_i, c_i)
        set_cell_shading(cell, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
        set_cell_margins(cell, 50, 50, 60, 60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        if c_i in [0, 1]:
            r.bold = True
        elif c_i == 5:
            r.bold = True
            r.font.color.rgb = RGBColor(11, 79, 108)

# Total row
tot_q1 = q1_tbl.cell(len(q1_bom)+1, 0)
tot_q1.paragraphs[0].text = "TOTAL QUOTE 1 INITIAL CapEx"
tot_q1.paragraphs[0].runs[0].bold = True
set_cell_shading(tot_q1, "E0F2FE")
for mc in range(1, 5):
    q1_tbl.cell(len(q1_bom)+1, mc).paragraphs[0].text = ""
    set_cell_shading(q1_tbl.cell(len(q1_bom)+1, mc), "E0F2FE")
tot_q1_val = q1_tbl.cell(len(q1_bom)+1, 5)
tot_q1_val.paragraphs[0].text = "₹35,500"
tot_q1_val.paragraphs[0].runs[0].bold = True
tot_q1_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(11, 79, 108)
set_cell_shading(tot_q1_val, "E0F2FE")

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# SECTION 4: QUOTE 2 — VALUE-ENGINEERED FIELD PILOT (₹71,500) — THE SWEET SPOT
h1_q2 = doc.add_heading("4. Quote 2: Value-Engineered Field Pilot (₹71,500) — Recommended Sweet Spot", level=1)
h1_q2.style.font.name = "Calibri"
h1_q2.style.font.color.rgb = RGBColor(11, 79, 108)

p_q2_desc = doc.add_paragraph()
p_q2_desc.add_run(
    "The ideal configuration for university incubation (BITS Pilani, Rajasthan iStart) and 3 to 6-month continuous field validation in Fateh Sagar Lake. "
    "It adds Dissolved Oxygen (DO), water level, tipping rain gauge, and barometer while eliminating commercial branded markups by leveraging college laboratory synergies."
)

q2_bom = [
    ("In-Situ Sensors", "Galvanic Dissolved Oxygen (DO) Probe + Modbus", "DFRobot / OEM Galvanic DO", "RS-485", "1", "₹14,000"),
    ("In-Situ Sensors", "Industrial Optical Turbidity Sensor (860nm)", "OEM Optical Modbus", "RS-485", "1", "₹9,500"),
    ("In-Situ Sensors", "Industrial 4-Electrode EC / Salinity Probe", "Rika / OEM Graphite Modbus", "RS-485", "1", "₹6,500"),
    ("In-Situ Sensors", "Industrial Flat-Glass Isolated pH Sensor", "OEM Double-Junction Glass", "RS-485", "1", "₹5,000"),
    ("In-Situ Sensors", "Dual-Depth Precision Water Temp Profiler", "Paired SS316 DS18B20", "1-Wire", "1 pair", "₹600"),
    ("Hydrology & Weather", "Waterproof Ultrasonic / Hydrostatic Level Transducer", "JSN-SR04T / WP-401B OEM", "RS-485 / Pulse", "1", "₹2,500"),
    ("Hydrology & Weather", "Tipping Bucket Rain Gauge + BMP280 Barometer", "Misol Tipping + BMP280", "Pulse / I2C", "1 set", "₹2,800"),
    ("Edge & Telemetry", "ESP32-S3 Board + Isolated RS-485 Hub + RTC + SD", "ESP32-S3 + ADM2483 + SD", "Multi-UART", "1 set", "₹2,800"),
    ("Edge & Telemetry", "SIMCom A7672S 4G LTE-Cat1 Cellular Modem + Antenna", "Quectel / SIMCom 4G Module", "UART", "1", "₹2,400"),
    ("Edge & Telemetry", "Station Power Board, Surge TVS & Isolated DC-DC", "TVS + B0505S Converters", "Internal", "1 set", "₹1,500"),
    ("Solar Power", "25W Monocrystalline Solar Panel + Aluminum Mount", "Grade-A 25W Mono", "MC4 Solar", "1", "₹2,200"),
    ("Solar Power", "12V 12Ah Deep-Cycle Battery Pack + BMS", "12V 12Ah LiFePO4 / SLA", "DC 12V", "1", "₹4,500"),
    ("Solar Power", "10A MPPT / Smart Solar Charge Controller", "Lumiao / EpEver 10A", "Solar Control", "1", "₹1,500"),
    ("Mechanical & Buoy", "IP66 Weatherproof Polycarbonate Station Box", "Fibox / Hensel IP66", "NEMA 4X", "1", "₹2,500"),
    ("Mechanical & Buoy", "Modular PVC/FRP Pontoon Float + Chain & Anchor", "Catamaran Pontoon Frame", "Buoyancy", "1 set", "₹5,500"),
    ("Mechanical & Buoy", "Perforated Sensor Shroud + Copper Mesh Wrap", "SS/PVC Cage + Copper", "Anti-Fouling", "1 set", "₹2,200"),
    ("Mechanical & Buoy", "Submersible Shielded Polyurethane Cabling (5m drops)", "PUR Shielded Multicore", "Submersible", "1 set", "₹2,500"),
    ("Validation Gear", "Certified Calibration Standards Pack (pH, EC, DO)", "NIST Buffer Solutions", "Chemical", "1 pack", "₹3,000"),
    ("Validation Gear", "College Laboratory Bridge (Reference Meter & Culture)", "Techno NJR / MLSU Lab Loan", "QA Synergy", "Loaned", "₹0")
]

q2_tbl = doc.add_table(rows=len(q2_bom)+2, cols=6)
q2_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_i, h in enumerate(["Subsystem", "Component Description", "Candidate Model", "Interface", "Qty", "Cost (₹)"]):
    cell = q2_tbl.cell(0, c_i)
    set_cell_shading(cell, "0B4F6C")
    set_cell_margins(cell, 80, 80, 80, 80)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(255, 255, 255)

for r_i, row in enumerate(q2_bom, start=1):
    for c_i, val in enumerate(row):
        cell = q2_tbl.cell(r_i, c_i)
        set_cell_shading(cell, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
        set_cell_margins(cell, 50, 50, 60, 60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        if c_i in [0, 1]:
            r.bold = True
        elif c_i == 5:
            r.bold = True
            r.font.color.rgb = RGBColor(11, 79, 108)

# Total row
tot_q2 = q2_tbl.cell(len(q2_bom)+1, 0)
tot_q2.paragraphs[0].text = "TOTAL QUOTE 2 INITIAL CapEx (Recommended Pilot)"
tot_q2.paragraphs[0].runs[0].bold = True
set_cell_shading(tot_q2, "E0F2FE")
for mc in range(1, 5):
    q2_tbl.cell(len(q2_bom)+1, mc).paragraphs[0].text = ""
    set_cell_shading(q2_tbl.cell(len(q2_bom)+1, mc), "E0F2FE")
tot_q2_val = q2_tbl.cell(len(q2_bom)+1, 5)
tot_q2_val.paragraphs[0].text = "₹71,500"
tot_q2_val.paragraphs[0].runs[0].bold = True
tot_q2_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(11, 79, 108)
set_cell_shading(tot_q2_val, "E0F2FE")

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# SECTION 5: QUOTE 3 — MUNICIPAL FULL-SPEC ENTERPRISE STATION (₹3,15,000)
h1_q3 = doc.add_heading("5. Quote 3: Municipal Full-Spec Enterprise Station (₹3,15,000)", level=1)
h1_q3.style.font.name = "Calibri"
h1_q3.style.font.color.rgb = RGBColor(11, 79, 108)

p_q3_desc = doc.add_paragraph()
p_q3_desc.add_run(
    "The complete Smart City tender and municipal concession grade specification. Deploys autonomous motorized wipers on optical DO and Turbidity, 50W solar panel with 7-day monsoon LiFePO4 battery autonomy, heavy SS316 marine mooring buoy, handheld Apera validation meter, Aquagenx CBT field kits, and certified fortnightly NABL laboratory verification."
)

q3_bom = [
    ("Category A: Water Probes", "Optical DO with motorized wiper", "Yosemitech Y504-A", "RS-485 Modbus", "1", "₹48,000"),
    ("Category A: Water Probes", "Industrial isolated pH sensor", "Sensorex S8000 / Renke", "RS-485 Modbus", "1", "₹18,500"),
    ("Category A: Water Probes", "4-Electrode EC / Salinity sensor", "Rika RK500-08", "RS-485 Modbus", "1", "₹22,000"),
    ("Category A: Water Probes", "Optical Turbidity with motorized wiper", "Yosemitech Y510-A", "RS-485 Modbus", "1", "₹44,000"),
    ("Category A: Water Probes", "Dual-depth SS316 Temp probes (0.5m & 3m)", "PT1000 Class A RTD", "Digital 1-Wire", "1 pair", "₹3,500"),
    ("Category A: Water Probes", "Galvanic Isolation Hub & Sensor Modbus Board", "ADM2483 / B0505S", "Internal Bus", "1 set", "₹20,000"),
    ("Category B: Hydro & Weather", "Submersible Hydrostatic Level Sensor (0-5m)", "Rika RK500-01", "RS-485 Modbus", "1", "₹14,000"),
    ("Category B: Hydro & Weather", "Barometric Pressure Sensor in Radiation Shield", "Bosch BMP280", "I2C / RS-485", "1", "₹1,800"),
    ("Category B: Hydro & Weather", "Tipping Bucket Rain Gauge (0.2 mm resolution)", "Misol WH-SP-RG", "Pulse Reed", "1", "₹5,500"),
    ("Category C: Edge & 4G", "ESP32-S3 Industrial Controller Unit", "ESP32-S3 Industrial", "Multi-UART", "1", "₹6,500"),
    ("Category C: Edge & 4G", "Quectel 4G LTE-M / NB-IoT Modem + 5dBi Antenna", "Quectel EC200U-CN", "UART / USB", "1", "₹5,200"),
    ("Category C: Edge & 4G", "Surge Protection, RTC DS3231, SD Backup", "Industrial TVS/RTC", "Internal", "1 set", "₹4,300"),
    ("Category D: Solar Power", "50W Monocrystalline PV Panel + Bracket", "Loom Solar / Waaree", "MC4 DC", "1", "₹3,500"),
    ("Category D: Solar Power", "12V 24Ah LiFePO4 Battery Pack + Smart BMS", "Custom LiFePO4 Pack", "DC 12V 24Ah", "1", "₹14,500"),
    ("Category D: Solar Power", "10A MPPT Solar Charge Controller with RS-485", "Victron / Lumiao 10A", "RS-485 Modbus", "1", "₹4,200"),
    ("Category D: Solar Power", "Marine Wiring, MC4 Connectors & Gland Plates", "Marine Tinned Copper", "Wiring", "1 set", "₹2,500"),
    ("Category E: Marine Mech", "IP67 Polycarbonate Station Enclosure", "Hensel / Fibox IP67", "NEMA 4X / IP67", "1", "₹5,500"),
    ("Category E: Marine Mech", "Marine Anodized Aluminum Mast & Mounts", "6061-T6 Aluminum", "Mechanical", "1", "₹7,500"),
    ("Category E: Marine Mech", "Perforated SS316 Sensor Cage + Copper Mesh", "Marine SS316 + CuNi", "Physical Shield", "1", "₹8,500"),
    ("Category E: Marine Mech", "Rotational Polyethylene Mooring Buoy + Anchor", "UV-HDPE Buoy + Chain", "Marine Mooring", "1", "₹16,000"),
    ("Category E: Marine Mech", "Submersible Shielded Polyurethane Cables (10m)", "PUR Kevlar Jacket", "Submersible", "1 set", "₹6,500"),
    ("Category F: QA/QC Gear", "Handheld Multi-Parameter Reference Meter", "Apera PC60-Z / HI98194", "Field Check", "1", "₹32,000"),
    ("Category F: QA/QC Gear", "NIST Traceable Buffer Solutions (pH, EC, DO)", "Certified Standard Buffers", "Chemical", "1 pack", "₹6,000"),
    ("Category F: QA/QC Gear", "Aquagenx CBT E. coli Portable Field Kits", "Aquagenx CBT (20 tests)", "Field Bio-assay", "1 kit", "₹15,000")
]

q3_tbl = doc.add_table(rows=len(q3_bom)+2, cols=6)
q3_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
for c_i, h in enumerate(["Subsystem", "Component Description", "Candidate Model", "Interface", "Qty", "Cost (₹)"]):
    cell = q3_tbl.cell(0, c_i)
    set_cell_shading(cell, "0B4F6C")
    set_cell_margins(cell, 80, 80, 80, 80)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(h)
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(8)
    r.font.color.rgb = RGBColor(255, 255, 255)

for r_i, row in enumerate(q3_bom, start=1):
    for c_i, val in enumerate(row):
        cell = q3_tbl.cell(r_i, c_i)
        set_cell_shading(cell, "FFFFFF" if r_i % 2 == 1 else "F8FAFC")
        set_cell_margins(cell, 50, 50, 60, 60)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(val)
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        if c_i in [0, 1]:
            r.bold = True
        elif c_i == 5:
            r.bold = True
            r.font.color.rgb = RGBColor(11, 79, 108)

# Total row
tot_q3 = q3_tbl.cell(len(q3_bom)+1, 0)
tot_q3.paragraphs[0].text = "TOTAL QUOTE 3 INITIAL CapEx (Municipal Full-Spec)"
tot_q3.paragraphs[0].runs[0].bold = True
set_cell_shading(tot_q3, "E0F2FE")
for mc in range(1, 5):
    q3_tbl.cell(len(q3_bom)+1, mc).paragraphs[0].text = ""
    set_cell_shading(q3_tbl.cell(len(q3_bom)+1, mc), "E0F2FE")
tot_q3_val = q3_tbl.cell(len(q3_bom)+1, 5)
tot_q3_val.paragraphs[0].text = "₹3,15,000"
tot_q3_val.paragraphs[0].runs[0].bold = True
tot_q3_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(11, 79, 108)
set_cell_shading(tot_q3_val, "E0F2FE")

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# SECTION 6: MODULAR UPGRADE ROADMAP
h1_up = doc.add_heading("6. Modular Upgrade Roadmap: Scaling from Quote 1 to Quote 3", level=1)
h1_up.style.font.name = "Calibri"
h1_up.style.font.color.rgb = RGBColor(11, 79, 108)

p_up = doc.add_paragraph()
p_up.add_run(
    "A key engineering advantage of Aarogya Jal is its unified Modbus RTU / RS-485 architecture. Because all three quotes share the same industrial communication bus and ESP32 telemetry codebase, funding bodies do not suffer 'sunk capital' when upgrading:\n"
)

upgrades = [
    ("Phase 1A (Student Hackathon / ₹35,500):", " Deploy Quote 1 at college jetty. Proves cloud telemetry, sewage conductivity spike alerts, and basic web dashboard."),
    ("Phase 1B (Incubator Grant / +₹36,000 incremental):", " Add Galvanic DO, ultrasonic level, and rain gauge to achieve Quote 2 capability. Conduct 3-month continuous lake monitoring."),
    ("Phase 1C (Municipal Concession / +₹2,40,000 incremental):", " Retrofit motorized wiper optical DO & Turbidity heads, upgrade to 50W LiFePO4 power system, deploy rotationally molded marine buoy, and onboard certified NABL bi-weekly testing.")
]

for u_title, u_desc in upgrades:
    up_p = doc.add_paragraph(style='List Bullet')
    up_p.paragraph_format.space_before = Pt(2)
    up_p.paragraph_format.space_after = Pt(3)
    rt = up_p.add_run(u_title)
    rt.bold = True
    rt.font.color.rgb = RGBColor(11, 79, 108)
    up_p.add_run(u_desc)

p_sign = doc.add_paragraph()
p_sign.paragraph_format.space_before = Pt(14)
r_sig1 = p_sign.add_run("Submitted by:\n")
r_sig1.font.size = Pt(9.5)
r_sig1.font.color.rgb = RGBColor(100, 116, 139)
r_sig2 = p_sign.add_run("Manan Ramani & Team Aarogya Jal\n")
r_sig2.bold = True
r_sig2.font.size = Pt(11)
r_sig2.font.color.rgb = RGBColor(11, 79, 108)
r_sig3 = p_sign.add_run("Department of Computer Science & Engineering • Techno India NJR Institute of Technology, Udaipur\nIn Collaboration with Udaipur Municipal Corporation & Smart City Mission")
r_sig3.font.size = Pt(9.5)
r_sig3.font.color.rgb = RGBColor(71, 85, 105)

# Save Document
doc.save(docx_path)
print(f"SUCCESS: Updated Master Word Document with all 3 Quotes saved at: {docx_path}")
