# 2. Technology Landscape — February 2026

## 2.1 Unreal Engine 5.5 & Pixel Streaming 2

### What Changed
UE 5.5 introduced **Pixel Streaming 2**, a rebuilt plugin using a new WebRTC abstraction layer. Both the legacy and new plugins ship together during migration, but PS2 is the forward path. Combined with Lumen (dynamic GI) and Nanite (virtualised geometry), UE5.5 delivers film-quality environments streamed to any web browser.

### Digital Twin Capabilities
- **Live IoT data ingestion** from sensors and hubs — the twin mirrors reality in real-time
- **Massive scale** — handles entire cities, not just individual buildings
- **Multi-platform deployment** — VR, AR, web, touchscreen, mobile from a single project
- **Cesium for Unreal** — geospatial tiling streams city-scale 3D Tiles with 40-60% faster load times

### Real-World Precedents
| Project | Application |
|---------|------------|
| **Renault x Publicis Sapient** | Full digital twin of Champs-Elysees showroom via Pixel Streaming — avatars, chat, multilingual |
| **EDGE Liverpool Street** | Zero-carbon office digital twin for remote and on-site sales via Pixel Streaming |
| **Ramboll (AEC)** | Massive engineering digital twins streamed via Eagle 3D, replacing local executables with web links |
| **Penn's Landing Philadelphia** | City-scale infrastructure digital twin using Cesium + UE5 |
| **VMI / Journey — Trojena (NEOM)** | Full digital twin of Trojena ski resort region built in Unreal Engine |

### Relevance to JV
VMI already builds production Unreal Engine digital twins for Saudi giga-projects. Pixel Streaming 2 means these can now be delivered as web experiences — the missing piece is intelligent interactivity (Sapient Bodhi).

---

## 2.2 3D Gaussian Splatting (3DGS)

### The "JPEG of 3D" Moment
3DGS has reached an inflection point. The technology captures photorealistic 3D scenes from photos/video and renders them in real-time. 2026 marks the year it moves from research novelty to production standard.

### Key Developments (Late 2025 — Feb 2026)

| Development | Significance |
|------------|-------------|
| **WebSplatter** (Feb 2026, arxiv) | WebGPU-based framework with wait-free hierarchical radix sort — up to 2.26x speedup across devices including mobile |
| **Visionary Platform** (Dec 2025) | WebGPU fully GPU-resident pipeline — 2.1ms/frame for 6M points, supports 4DGS temporal scenes and neural avatars |
| **glTF KHR_gaussian_splatting** (Aug 2025) | Khronos standardised 3DGS in glTF — interoperability across all 3D tools |
| **SPZ format** (Niantic, MIT license) | 90% compression (250MB PLY → 25MB SPZ) — practical web delivery |
| **MPEG Gaussian Splat Coding track** | Formal coding standards exploration — signals long-term industry commitment |
| **Safari WebGPU** (Sep 2025) | Apple ships native WebGPU on iOS 26 + macOS 26 — universal browser GPU compute |

### Industry Adoption
- **Zillow SkyTours** — first major real estate platform shipping 3DGS property tours
- **Apartments.com** — exterior 3DGS via Matterport 3D Exteriors
- **Superman (film)** — first major motion picture using dynamic Gaussian Splatting
- **OTOY OctaneRender 2026** — full path-traced Gaussian splat support
- **Meta Hyperscape** — photorealistic 3DGS scenes on Quest headsets

### Web Viewers
- **Spark** (World Labs) — current leader, named one of GitHub's most influential libraries of 2025
- **GaussianSplats3D** (Three.js) — legacy, author now recommends Spark
- **3DVista VT Pro** — added native 3DGS support for virtual tour authoring

### Relevance to JV
VMI already uses 3DGS in its pipeline. With WebGPU now universal and standardised formats (glTF, SPZ), 3DGS becomes a **fast, low-cost capture method** for existing properties and construction progress — complementing Unreal-based digital twins for off-plan visualisation. Sapient's data platform can serve and manage splat assets at enterprise scale.

---

## 2.3 WebGPU — The Universal GPU Web Standard

### Browser Support (Complete as of Late 2025)
| Browser | Platform | Status |
|---------|----------|--------|
| Chrome / Edge | Windows, macOS, ChromeOS, Android | Stable |
| Firefox | Windows, macOS | Stable (v141+) |
| Safari | macOS 26, iOS 26, iPadOS 26, visionOS | Native |

### Performance Impact
- **Babylon.js Snapshot Rendering** with WebGPU Render Bundles: ~**10x faster** than previous approaches
- **Compute shaders** in browser: physics, simulation, ML inference on GPU
- **Three.js r171** (Sep 2025): WebGPURenderer production-ready with zero-config import and WebGL 2 fallback
- Direct GPU memory management handles architectural models **exceeding 500MB**

### What This Enables
For the first time, a buyer can access a **photorealistic, interactive digital twin** of an unbuilt property directly in their browser — no app install, no high-end hardware. They can engage with an AI concierge, customise finishes in real-time, and make a purchase decision. This is technically feasible today.

---

## 2.4 Agentic AI for Real Estate

### The Shift: Chatbot → Digital Sales Agent
The industry is moving from reactive chatbots to **proactive, autonomous AI agents** that can:
- Guide buyers through 3D property tours conversationally ("Show me the master bedroom again", "What's the view from floor 12?")
- Detect sentiment and urgency in real-time
- Pre-qualify leads automatically
- Operate 24/7 in any language
- Hand off to human sales advisors at the right moment

### Proven Results
| Metric | Source |
|--------|--------|
| Inquiries jumped **3 → 22/week** (8 pre-qualified) when AI concierge added to 3D tour | AgentiveAIQ, Austin luxury listing |
| **15-20% increase** in lead-to-lease conversion | RealPage AI leasing tools |
| **70% of routine inquiries** handled by conversational AI | Industry average |
| Digital twin transactions grew **$24M → $400M+** | DAMAC Properties, Dubai |

### Sapient Bodhi as the AI Layer
Bodhi is purpose-built for this:
- **Agent orchestration** — multiple specialised agents (sales, concierge, analytics, compliance) working in concert
- **Governance built-in** — critical for regulated real estate sales in Saudi Arabia
- **Model-agnostic** — can use best-in-class LLMs as they evolve
- **Enterprise integrations** — Salesforce, SAP, CRM systems that real estate developers already use
- **Multilingual** — essential for international buyer audiences (Arabic, English, Mandarin, etc.)

---

## 2.5 Technology Convergence Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    BUYER EXPERIENCE                          │
│                                                             │
│   Browser (WebGPU) ──► Any Device, No Install               │
│        │                                                    │
│        ├── 3DGS Capture ──► Existing Properties / Progress  │
│        ├── UE5 Pixel Streaming ──► Off-Plan Digital Twins   │
│        └── AI Concierge (Bodhi) ──► Conversational Guide    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    PLATFORM LAYER                            │
│                                                             │
│   Sapient Bodhi ──► Agent Orchestration & Governance        │
│   VMI Luna ──► Interactive Maps, Analytics, CRM Integration │
│   IoT / Sensors ──► Live Data Feeds to Digital Twin         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                    DATA & INTELLIGENCE                       │
│                                                             │
│   Buyer Analytics ──► Dwell Time, Navigation, Sentiment     │
│   Sales Intelligence ──► Lead Scoring, Conversion Tracking  │
│   Property Data ──► Availability, Pricing, Customisation    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
