# Yuanjun (Johnny) Dai — Portfolio

Personal portfolio and resume hub for job applications. Hosted via GitHub Pages.

## Structure

```
portfolio/
├── index.html          # Main general-purpose website
├── hub.html            # Version selector landing page
├── README.md
├── versions/
│   ├── ai-llm.html     # Version A — AI Infra / LLM
│   ├── cloud.html      # Version B — Cloud Infrastructure
│   ├── ebpf.html       # Version C — eBPF / Observability
│   ├── hardware.html   # Version D — Chip / Hardware
│   └── security.html   # Version E — ML Security
├── resumes/
│   ├── Yuanjun_Dai_Resume.pdf          # Base resume
│   ├── Yuanjun_Dai_Resume.docx         # Word version
│   ├── Yuanjun_Dai_Resume_A_AI_LLM.pdf
│   ├── Yuanjun_Dai_Resume_B_Cloud.pdf
│   ├── Yuanjun_Dai_Resume_C_eBPF.pdf
│   ├── Yuanjun_Dai_Resume_D_Hardware.pdf
│   └── Yuanjun_Dai_Resume_E_Security.pdf
└── src/
    ├── resume_improved.html    # Base resume HTML source
    ├── build_resume.py         # PDF builder (pycairo)
    └── build_resume_docx.py    # Word doc builder
```

## Resume Versions

| Version | Focus | Key Skills |
|---------|-------|------------|
| A — AI Infra / LLM | LLM serving & distributed training | vLLM, TensorRT-LLM, PyTorch DDP, K8s |
| B — Cloud Infra | Multi-cloud & HPC | Kubernetes, Slurm, CI/CD, AWS/GCP |
| C — eBPF / Observability | Kernel networking & telemetry | eBPF, Prometheus, Grafana, P4 |
| D — Chip / Hardware | Low-level systems & ASICs | NPU/ASIC, BCM SDK, P4, RTOS |
| E — ML Security | Side-channel & adversarial ML | Side-channel analysis, MLaaS, model reconstruction |

## Deployment (GitHub Pages)

1. Push this `portfolio/` folder as a GitHub repository
2. Go to **Settings → Pages → Source: Deploy from a branch → `main` / root**
3. Site will be live at `https://<username>.github.io/<repo>/hub.html`

## Contact

- Email: yxd429@case.edu
- GitHub: [github.com/Johnny-dai-git](https://github.com/Johnny-dai-git)
- Google Scholar: [scholar.google.com/citations?user=maCNFMAAAAAJ](https://scholar.google.com/citations?user=maCNFMAAAAAJ)
