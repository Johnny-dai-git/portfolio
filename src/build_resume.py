#!/usr/bin/env python3
"""Build Yuanjun (Johnny) Dai's resume as a PDF using pycairo + pangocairo."""

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')
from gi.repository import Pango, PangoCairo

# ── Page setup ────────────────────────────────────────────────────────────────
LETTER_W = 8.5 * 72   # 612 pt
LETTER_H = 11  * 72   # 792 pt
ML = 38; MR = 38; MT = 36; MB = 36   # margins
CW = LETTER_W - ML - MR              # content width ~536 pt

OUTPUT = "/home/johnny/Desktop/job_hunting/resume/Yuanjun_Dai_Resume.pdf"
surface = cairo.PDFSurface(OUTPUT, LETTER_W, LETTER_H)
ctx = cairo.Context(surface)

# ── Colours ───────────────────────────────────────────────────────────────────
BLACK  = (0.08, 0.08, 0.08)
DARK   = (0.15, 0.15, 0.15)
GRAY   = (0.40, 0.40, 0.40)
LGRAY  = (0.65, 0.65, 0.65)
BLUE   = (0.10, 0.30, 0.65)
RULE   = (0.20, 0.20, 0.20)

# ── Cursor ────────────────────────────────────────────────────────────────────
y = MT   # current vertical position

def set_color(c):
    ctx.set_source_rgb(*c)

def move(dy):
    global y
    y += dy

def make_layout(text, size_pt, bold=False, italic=False, color=BLACK, width=CW):
    layout = PangoCairo.create_layout(ctx)
    desc = Pango.FontDescription()
    desc.set_family("Liberation Sans")
    desc.set_size(int(size_pt * Pango.SCALE))
    desc.set_weight(Pango.Weight.BOLD if bold else Pango.Weight.NORMAL)
    desc.set_style(Pango.Style.ITALIC if italic else Pango.Style.NORMAL)
    layout.set_font_description(desc)
    layout.set_width(int(width * Pango.SCALE))
    layout.set_text(text, -1)
    return layout

def draw_text(text, x, size_pt, bold=False, italic=False, color=BLACK,
              width=CW, wrap=True, markup=False):
    """Draw text at (x, y); return height consumed."""
    layout = PangoCairo.create_layout(ctx)
    desc = Pango.FontDescription()
    desc.set_family("Liberation Sans")
    desc.set_size(int(size_pt * Pango.SCALE))
    desc.set_weight(Pango.Weight.BOLD if bold else Pango.Weight.NORMAL)
    desc.set_style(Pango.Style.ITALIC if italic else Pango.Style.NORMAL)
    layout.set_font_description(desc)
    layout.set_width(int(width * Pango.SCALE))
    layout.set_wrap(Pango.WrapMode.WORD_CHAR if wrap else Pango.WrapMode.CHAR)
    if markup:
        layout.set_markup(text, -1)
    else:
        layout.set_text(text, -1)
    set_color(color)
    ctx.move_to(x, y)
    PangoCairo.show_layout(ctx, layout)
    pw, ph = layout.get_pixel_size()
    return ph

def draw_text_at(text, x, ty, size_pt, bold=False, italic=False, color=BLACK,
                 width=CW, markup=False):
    layout = PangoCairo.create_layout(ctx)
    desc = Pango.FontDescription()
    desc.set_family("Liberation Sans")
    desc.set_size(int(size_pt * Pango.SCALE))
    desc.set_weight(Pango.Weight.BOLD if bold else Pango.Weight.NORMAL)
    desc.set_style(Pango.Style.ITALIC if italic else Pango.Style.NORMAL)
    layout.set_font_description(desc)
    layout.set_width(int(width * Pango.SCALE))
    layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    if markup:
        layout.set_markup(text, -1)
    else:
        layout.set_text(text, -1)
    set_color(color)
    ctx.move_to(x, ty)
    PangoCairo.show_layout(ctx, layout)
    pw, ph = layout.get_pixel_size()
    return ph

def text_width(text, size_pt, bold=False):
    layout = PangoCairo.create_layout(ctx)
    desc = Pango.FontDescription()
    desc.set_family("Liberation Sans")
    desc.set_size(int(size_pt * Pango.SCALE))
    desc.set_weight(Pango.Weight.BOLD if bold else Pango.Weight.NORMAL)
    layout.set_font_description(desc)
    layout.set_text(text, -1)
    pw, ph = layout.get_pixel_size()
    return pw

def hrule(lw=0.5, color=RULE):
    set_color(color)
    ctx.set_line_width(lw)
    ctx.move_to(ML, y)
    ctx.line_to(ML + CW, y)
    ctx.stroke()

def section_header(title):
    global y
    move(7)
    hrule(0.4, RULE)
    move(4)
    draw_text(title.upper(), ML, 9.5, bold=True, color=BLACK)
    move(13)

def job_entry(title, company, date, url=None):
    global y
    # Title (bold) and date on same line
    date_w = text_width(date, 8.5)
    draw_text(title, ML, 9.5, bold=True, color=BLACK, width=CW - date_w - 4)
    draw_text_at(date, ML + CW - date_w, y, 8.5, color=GRAY)
    move(12)
    if url:
        draw_text(company + "  |  " + url, ML, 8.5, italic=False, color=GRAY)
    else:
        draw_text(company, ML, 8.5, color=GRAY)
    move(11)

def bullet(text, indent=8, size=8.5):
    global y
    bx = ML + indent
    # Draw bullet dot
    set_color(DARK)
    ctx.arc(bx - 5, y + 4.5, 1.3, 0, 2 * 3.14159)
    ctx.fill()
    # Draw text
    wrap_w = CW - indent - 2
    h = draw_text(text, bx, size, color=DARK, width=wrap_w)
    move(h + 2.5)

def sub_bullet(text, indent=18, size=8.2):
    global y
    bx = ML + indent
    set_color(GRAY)
    ctx.arc(bx - 5, y + 4.2, 1.0, 0, 2 * 3.14159)
    ctx.fill()
    wrap_w = CW - indent - 2
    h = draw_text(text, bx, size, color=DARK, width=wrap_w)
    move(h + 2)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
# Name
h = draw_text("YUANJUN (JOHNNY) DAI", ML, 22, bold=True, color=BLACK)
move(h + 3)

# Contact line
contact = "216-269-2394   \u2022   yxd429@case.edu   \u2022   github.com/Johnny-dai-git   \u2022   johnny-dai-git.github.io/portfolio   \u2022   Cleveland, OH"
h = draw_text(contact, ML, 8.8, color=GRAY)
move(h + 2)

# Thin rule under header
hrule(0.6, LGRAY)
move(6)

# ── SUMMARY ───────────────────────────────────────────────────────────────────
section_header("Summary")
summary = (
    "AI Infrastructure Engineer and PhD Candidate at Case Western Reserve University, specializing in "
    "distributed ML systems, eBPF-based observability, and large-scale LLM deployment. "
    "Published 8 research papers (7 first-author) at IEEE, ACM, and Springer venues. "
    "5+ years of industry experience at Cisco and Broadcom in high-performance networking "
    "and systems optimization."
)
h = draw_text(summary, ML, 8.8, color=DARK, width=CW)
move(h + 4)

# ── EDUCATION ─────────────────────────────────────────────────────────────────
section_header("Education")

date_w = text_width("08/2019 – Present", 8.5)
draw_text("Ph.D. Candidate in Computer Science (AI Infrastructure)", ML, 9.5, bold=True, color=BLACK, width=CW - date_w - 4)
draw_text_at("08/2019 – Present", ML + CW - date_w, y, 8.5, color=GRAY)
move(12)
draw_text("Case Western Reserve University", ML, 8.5, color=GRAY)
move(13)

draw_text("M.S. in ECE (Computer Microarchitecture)", ML, 9.5, bold=True, color=BLACK)
move(12)
draw_text("University of Pittsburgh", ML, 8.5, color=GRAY)
move(6)

# ── RESEARCH EXPERIENCE ───────────────────────────────────────────────────────
section_header("Research & Systems Engineering Experience")

draw_text("Research Assistant, AI Infrastructure & ML Systems", ML, 9.5, bold=True, color=BLACK)
move(12)
draw_text("Case Western Reserve University", ML, 8.5, color=GRAY)
move(12)

bullet("DYNAMIX – RL-Based Adaptive Batch Scheduling for Distributed ML  |  Paper / Code\n"
       "Designed a system-signal-driven RL scheduler (BytePS, PyTorch DDP, TensorFlow) with asynchronous "
       "event-driven control, achieving 46% end-to-end training speedup on 32+ nodes across HPC and cloud environments.")
move(1)

bullet("PRISM – Priority-Aware Transport for Distributed ML Training  |  Paper / Code\n"
       "Built a selective-reliability transport protocol differentiating critical/non-critical gradient traffic via "
       "importance-based prioritization and dual congestion control; achieved 8–21% training throughput improvement "
       "under 1% packet loss on 32 GPUs with near-zero convergence loss.")
move(1)

bullet("Training-Time Side-Channel Attacks on Distributed ML Systems  |  Paper / Code\n"
       "Instrumented MXNet BSP training to profile communication flows and power behavior via Intel RAPL telemetry; "
       "achieved >99% layer-type accuracy and <1.5% tensor-size error in model reconstruction, "
       "exposing actionable MLaaS attack surfaces.")
move(1)

bullet("Priority-Based eBPF Network Flow Telemetry for AI / DML Infrastructure  |  Paper / Code\n"
       "Built a priority-aware eBPF telemetry system for real-time in-kernel TCP/UDP monitoring with O(n) approximate "
       "Top-K flow tracking; achieved 96% Top-K accuracy, 100% priority-packet recall, and <1.1% throughput overhead at 10 Gbps.")
move(1)

bullet("High-Resolution eBPF System Resource Profiling for DML Workloads  |  Paper / Code\n"
       "Developed a per-PID eBPF profiler with in-kernel Top-K tracking, delivering 10–14x finer temporal resolution "
       "than top/htop, ~11 ms latency, and >90% Top-K fidelity on commodity Linux servers.")
move(1)

bullet("Scotch – Elastic SDN Overlay for Control-Plane Scalability  |  Paper / Code\n"
       "Designed a distributed control-plane overlay using OvS-based traffic offloading and large-flow migration; "
       "reduced controller congestion by >70% on a 34-node GENI Clos topology.")
move(1)

bullet("Enterprise-Grade LLM Production Deployment Platform on Kubernetes  |  Code\n"
       "Built a K8s microservices platform (Gateway / Router / Worker) supporting vLLM and TensorRT-LLM inference "
       "with ArgoCD GitOps, Prometheus/Grafana observability, and CI/CD automation across 50+ Kubernetes deployments.")
move(1)

bullet("Domain-Adapted LLMs for Clinical Risk Adjustment Coding  |  Paper\n"
       "Fine-tuned PubMedBERT and Qwen-7B for HCC coding from EHR notes; achieved macro-/micro-F1 of 0.775/0.742 "
       "and 0.81/0.802 on MIMIC-IV with imbalance-aware training and per-label calibration.")
move(1)

bullet("BiLSTM-Based Side-Channel Modeling for Distributed ML Analysis  |  Paper\n"
       "Designed a BiLSTM pipeline aligning CPU/memory energy traces with per-layer timestamps; "
       "reliably distinguishes Conv, FC, and activation layers during distributed ML training using ensemble learning.")
move(2)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ══════════════════════════════════════════════════════════════════════════════
surface.show_page()
y = MT

# ── INDUSTRY EXPERIENCE ───────────────────────────────────────────────────────
section_header("Industry Experience")

job_entry("Software Engineer II", "Cisco Systems, Inc.", "06/2015 – 08/2016")
bullet("Developed NPU/ASIC features for a 100 Gbps core router serving hyperscalers (Azure, AWS, Alibaba Cloud) "
       "using Broadcom BCM SDK; contributed to QoS and ECMP modules, tuned forwarding pipelines, reducing "
       "forwarding latency by ~10% under heavy load.")
move(3)

job_entry("Applied Research Engineer", "Midea Group", "09/2016 – 06/2018")
bullet("Led ML model training and deployment for a smart appliance product; designed data pipeline, applied "
       "transfer learning and ensemble techniques, and deployed scalable Docker-based services on Alibaba Cloud. "
       "Product launched at 2018 AWE Show and won the Red Dot Design Award.")
move(3)

job_entry("Technical Product Manager", "Xiaomi", "07/2018 – 01/2019")
bullet("Defined system-level architecture for an IoT-enabled smart appliance with PID-based temperature control "
       "and cloud-connected app integration, translating product constraints into deployable system designs.")
move(3)

job_entry("Software Engineer Intern", "Broadcom (Emulex)", "10/2014 – 05/2015")
bullet("Replaced polling-based data acquisition with a DMA + circular-buffer architecture in an RTOS pipeline, "
       "reducing CPU load by 30% and improving sampling rate and control-loop responsiveness.")
bullet("Ported a Linux-only management CLI for BladeEngine ASIC-based CNA hardware to Windows Server, "
       "adapting system calls, threading models, and error handling.")
move(3)

job_entry("Engineer Intern", "Tenova I2S", "01/2014 – 04/2014")
bullet("Re-architected an RTOS data acquisition pipeline using DMA and circular buffers, "
       "reducing CPU load by 42% and improving sampling rate and control-loop responsiveness.")
move(3)

# ── ADDITIONAL PROJECTS ───────────────────────────────────────────────────────
section_header("Additional Systems Engineering Experience")

draw_text("16-bit MIPS-Like Pipelined CPU Design and Implementation", ML, 9.5, bold=True, color=BLACK)
move(11)
draw_text("github.com/Johnny-dai-git/16-bit-MIPS-Like-Pipelined-CPU-Design-and-Implementation",
          ML, 8.2, color=BLUE)
move(11)
bullet("Designed end-to-end pipelined CPU from custom ISA through RTL, synthesis, and layout; 5-stage pipeline "
       "with hazard handling and branch prediction, achieving ~3x speedup over single-cycle design.")
move(4)

# ── PUBLICATIONS ──────────────────────────────────────────────────────────────
section_header("Publications")
pub_text = (
    "8 research papers (6 first-author) in distributed systems, ML systems, and AI infrastructure, "
    "published/accepted at IEEE IPDPS, IEEE CCNC, IEEE ICNC, ACM TOIT, and Springer SecureComm; "
    "2 manuscripts under review at ACM TOPS. "
    "Full list: scholar.google.com/citations?user=maCNFMAAAAJ"
)
h = draw_text(pub_text, ML, 8.8, color=DARK, width=CW)
move(h + 6)

# ── SKILLS ────────────────────────────────────────────────────────────────────
section_header("Skills")

COL1 = ML
COL2 = ML + CW * 0.38
ROW_H = 13
LABEL_W = 115

skills = [
    ("Languages",         "Python, C/C++, Java, Bash"),
    ("AI / ML",           "PyTorch (DDP/FSDP), TensorFlow, BytePS, Megatron-LM, NCCL, DeepSpeed, vLLM, TensorRT-LLM"),
    ("Infrastructure",    "Kubernetes, Docker, CI/CD, ArgoCD, Helm, Slurm, HPC, GitHub Actions"),
    ("Observability",     "eBPF, Prometheus, Grafana, DCGM Exporter, Intel RAPL, Kernel Tracing"),
    ("Cloud & Networks",  "Lambda Labs HPC, NSF FABRIC, CloudLab, SDN (OpenFlow / Ryu), P4, NPU/ASIC (Broadcom BCM SDK)"),
    ("Research Areas",    "Distributed ML Systems, ML Security, Side-Channel Analysis, RL-based Scheduling"),
]

for label, value in skills:
    ty = y
    draw_text_at(label + ":", COL1, ty, 8.8, bold=True, color=BLACK, width=LABEL_W)
    draw_text_at(value, COL1 + LABEL_W, ty, 8.8, color=DARK, width=CW - LABEL_W)
    move(ROW_H)

surface.finish()
print(f"PDF written to: {OUTPUT}")
