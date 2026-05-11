from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ── Page margins
section = doc.sections[0]
section.top_margin    = Cm(2.5)
section.bottom_margin = Cm(2.5)
section.left_margin   = Cm(3.0)
section.right_margin  = Cm(2.5)

BLUE = RGBColor(0x1F, 0x49, 0x7D)
DARK = RGBColor(0x22, 0x22, 0x22)

def add_heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sizes = {1: 16, 2: 13, 3: 11}
    for run in p.runs:
        run.font.color.rgb = BLUE
        run.font.size = Pt(sizes.get(level, 11))
    return p

def add_body(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for run in p.runs:
        run.font.size = Pt(11)
        run.font.name = "Calibri"
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph(text, style="List Bullet")
    for run in p.runs:
        run.font.size = Pt(11)
        run.font.name = "Calibri"
    return p

def spacer(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_after  = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    for run in p.runs:
        run.font.size = Pt(4)

# ── COVER BLOCK ──────────────────────────────────────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("AR-Based Worker Guidance System")
r.font.size = Pt(24); r.font.bold = True; r.font.color.rgb = BLUE; r.font.name = "Calibri"

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Omniverse-Unity Integration for Industrial Assembly Assistance")
r2.font.size = Pt(14); r2.font.italic = True; r2.font.name = "Calibri"
r2.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

spacer(doc)
p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = p3.add_run("Technical Report  |  DIREKT Research Project  |  May 2026")
r3.font.size = Pt(11); r3.font.bold = True; r3.font.name = "Calibri"; r3.font.color.rgb = BLUE

doc.add_page_break()

# ── 1. EXECUTIVE SUMMARY ─────────────────────────────────────────────────────
add_heading(doc, "1. Executive Summary", 1)
add_body(doc,
    "This report presents the design, architecture, and implementation of an Augmented Reality "
    "(AR) worker guidance system developed within the DIREKT research project. The system enables "
    "industrial assembly workers to receive real-time, step-by-step visual instructions overlaid "
    "directly onto the physical workpiece through AR smart glasses, replacing paper-based or "
    "screen-based assembly documentation with spatially anchored 3D animations."
)
spacer(doc)
add_body(doc,
    "The system integrates NVIDIA Omniverse as the authoritative source of 3D assembly animations, "
    "a Python-based server stack (FastAPI + gRPC) for asset management and session orchestration, "
    "and a Unity 6 AR client deployed on the VUZIX M4000 smart glasses. The architecture is "
    "job-agnostic: switching to a different assembly job requires only a single configuration file "
    "change, with all 3D content delivered dynamically at runtime without modifying or rebuilding "
    "the AR application."
)
spacer(doc)

# ── 2. BACKGROUND AND MOTIVATION ─────────────────────────────────────────────
add_heading(doc, "2. Background and Motivation", 1)
add_body(doc,
    "Modern industrial assembly processes increasingly demand high precision, adaptability, and "
    "minimal error rates, especially in low-volume, high-complexity production environments. "
    "Traditional guidance approaches such as printed work instructions, PDF documents displayed on "
    "tablets, or static 2D diagrams require workers to shift attention between the instruction "
    "medium and the physical assembly, increasing cognitive load and the probability of assembly "
    "errors."
)
spacer(doc)
add_body(doc,
    "Augmented Reality technology provides a promising pathway to address these limitations by "
    "projecting context-aware, spatially registered guidance directly into the worker's field of "
    "view. When combined with precise object tracking, AR guidance can highlight the exact "
    "component to be handled, display its correct installation orientation in three dimensions, "
    "and animate the assembly motion, all anchored to the real physical object in front of the "
    "worker."
)
spacer(doc)
add_body(doc,
    "The DIREKT project targets the integration of professional-grade 3D simulation tools "
    "(NVIDIA Omniverse) with AR wearable devices, creating an end-to-end pipeline that moves from "
    "digitally authored assembly animations to live AR guidance on the factory floor without "
    "requiring manual content re-authoring for each new deployment or each new assembly job."
)
spacer(doc)

# ── 3. PROJECT GOALS AND OBJECTIVES ──────────────────────────────────────────
add_heading(doc, "3. Project Goals and Objectives", 1)
add_body(doc,
    "The primary goal of this project is to deliver a working, reproducible end-to-end AR guidance "
    "pipeline that can be demonstrated on real industrial assembly tasks and extended to new jobs "
    "with minimal engineering effort. The specific objectives are:"
)
spacer(doc)

add_heading(doc, "3.1  Omniverse-to-AR Content Pipeline", 2)
add_body(doc,
    "Establish an automated export pipeline that extracts per-step GLB animation packages directly "
    "from Omniverse USD stage files hosted on a Nucleus server, with content-addressed versioning "
    "(SHA-256) to guarantee cache consistency and reproducibility across deployments."
)
spacer(doc)

add_heading(doc, "3.2  Dynamic Runtime Asset Delivery", 2)
add_body(doc,
    "Deliver all assembly-specific content (3D models, Vuforia tracking databases, step manifests) "
    "to the AR device at runtime over the local network. The Unity application ships with zero "
    "embedded assembly data, ensuring that the APK itself never needs to be rebuilt when a new "
    "job or updated assets are deployed to the server."
)
spacer(doc)

add_heading(doc, "3.3  Accurate Spatial Anchoring via Vuforia", 2)
add_body(doc,
    "Anchor 3D assembly animations to the physical workpiece using Vuforia Model Target and Image "
    "Target tracking, so that animated guidance overlays remain spatially registered to the real "
    "object as the worker moves freely around the workspace."
)
spacer(doc)

add_heading(doc, "3.4  Step-Sequenced Guidance Workflow", 2)
add_body(doc,
    "Implement a deterministic, server-driven step progression model in which the worker confirms "
    "completion of each assembly step before the next animation is loaded and presented. The "
    "session must survive network interruptions through automatic reconnect logic without losing "
    "step state."
)
spacer(doc)

add_heading(doc, "3.5  Job-Agnostic Architecture", 2)
add_body(doc,
    "Design the full system so that adding a new assembly job requires only a JSON configuration "
    "file describing the USD source path, Nucleus location, and list of parts, with no code "
    "changes required in the server, the Unity client, or the export pipeline."
)
spacer(doc)

# ── 4. SYSTEM OVERVIEW ────────────────────────────────────────────────────────
add_heading(doc, "4. System Overview", 1)
add_body(doc,
    "The system consists of four integrated layers, each with a clearly defined responsibility:"
)
spacer(doc)

add_heading(doc, "4.1  Authoring Layer  —  NVIDIA Omniverse / Nucleus", 2)
add_body(doc,
    "Assembly animations are authored in NVIDIA Omniverse as Universal Scene Description (USD) "
    "stage files stored on a Nucleus server. Each assembly job corresponds to a USD stage "
    "containing per-part animation layers. Omniverse's physics and animation capabilities allow "
    "engineers to define precise, physically accurate assembly motions that are then exported "
    "automatically as runtime-ready GLB files."
)
spacer(doc)

add_heading(doc, "4.2  Export and Packaging Layer  —  Python Export Pipeline", 2)
add_body(doc,
    "A Python-based export pipeline (tools/packaging/) opens each part's USD stage in Omniverse "
    "Kit via the scripting API, extracts the relevant animation layers, and exports them as "
    "self-contained GLB files. Files are named using SHA-256 content hashing to guarantee "
    "immutable versioning. The pipeline is driven by per-job JSON configuration files, making "
    "it straightforward to add new assembly jobs without modifying any pipeline code."
)
spacer(doc)

add_heading(doc, "4.3  Server Layer  —  FastAPI + gRPC (Python)", 2)
add_body(doc,
    "The server-kit provides two complementary interfaces running on the same host machine:"
)
add_bullet(doc,
    "FastAPI HTTP REST (port 8080): exposes endpoints for job manifests, asset metadata, "
    "Vuforia target file delivery, and the export job trigger API."
)
add_bullet(doc,
    "gRPC services (port 50051): the GuidanceSessionService provides a bidirectional streaming "
    "channel for session management (connect, heartbeat, step-activate, step-complete), while "
    "the AssetTransferService streams GLB models and Vuforia target files in chunks directly "
    "to the AR device."
)
spacer(doc)
add_body(doc,
    "All assembly assets reside in the server's shared asset store and are referenced by "
    "content-addressed version strings, ensuring that the AR device never re-downloads an "
    "asset it already has in its local cache."
)
spacer(doc)

add_heading(doc, "4.4  AR Client Layer  —  Unity 6 on VUZIX M4000", 2)
add_body(doc,
    "The Unity 6 client application runs on the VUZIX M4000 Android-based AR smart glasses. "
    "At session start, the client connects to the gRPC server, receives the active step "
    "activation event, downloads the required GLB model and Vuforia target database if not "
    "already locally cached, activates Vuforia tracking, and presents the 3D assembly animation "
    "anchored to the physical workpiece. The animation is rendered with a holographic visual "
    "style (translucent cyan, fresnel rim glow, animated scan lines) to clearly distinguish "
    "AR guidance from the real environment. The worker confirms step completion via an on-screen "
    "button, which advances the server-side step state and triggers the next activation."
)
spacer(doc)

# ── 5. KEY TECHNICAL CHALLENGES ───────────────────────────────────────────────
add_heading(doc, "5. Key Technical Challenges and Solutions", 1)
add_body(doc,
    "The development of this system involved solving several non-trivial technical challenges "
    "across the full stack:"
)
spacer(doc)

challenges = [
    (
        "Omniverse Stage Synchronization.",
        "Opening large USD stages with nested references in Omniverse Kit is asynchronous. "
        "A naive export call issued immediately after stage open returns a stage-busy error. "
        "This was resolved by implementing a polling loop that checks the Kit stage state "
        "continuously until StageState.OPENED is confirmed before initiating the GLB export."
    ),
    (
        "Runtime GLB Loading on Android AR.",
        "Unity's built-in asset pipeline cannot load GLB files at runtime. The glTFast "
        "package (com.atteneder.gltfast) was integrated via UPM and accessed through "
        "reflection to maintain compatibility across glTFast versions without hard API "
        "coupling. An explicit adjustment node hierarchy was introduced so that per-job "
        "model position and orientation can be tuned from the Unity Inspector without "
        "touching any Omniverse source data."
    ),
    (
        "gRPC Transport on Android IL2CPP.",
        "Unity's Mono runtime on Android does not expose SocketsHttpHandler, which "
        "Grpc.Net.Client requires for HTTP/2. This was resolved by integrating "
        "YetAnotherHttpHandler, a Rust-based HTTP/2 implementation bridged via UniTask, "
        "as a drop-in transport for Grpc.Net.Client, enabling native gRPC over the local "
        "Wi-Fi network without any proxy infrastructure."
    ),
    (
        "Vuforia Runtime Target Loading.",
        "Vuforia's database loading API differs depending on whether the engine is already "
        "initialized or not. The VuforiaModelTargetLoader implements the official Vuforia "
        "scripting pattern: if the engine is already running it creates the tracking target "
        "immediately; otherwise it subscribes to OnVuforiaStarted and waits up to ten seconds, "
        "preventing race conditions on application startup."
    ),
    (
        "Content Versioning and Cache Consistency.",
        "To prevent stale assets from being displayed on the AR device after a job is "
        "re-exported, all GLB files and Vuforia databases are named using the first 16 "
        "characters of their SHA-256 hash. The client cache is keyed by this version string, "
        "so updated content automatically triggers a fresh download while unchanged content "
        "is served from the local cache without any network traffic."
    ),
    (
        "Animation Speed Control.",
        "Omniverse embeds animation timing directly within the exported GLB file. The Unity "
        "Animation and Animator components do not expose a global speed property at the "
        "component level; instead, speed must be applied to individual AnimationState objects "
        "inside the Animation component. A dedicated helper method traverses all Animation and "
        "Animator components in the loaded model hierarchy and applies a configurable speed "
        "multiplier, giving operators full control from the Unity Inspector without modifying "
        "Omniverse source data."
    ),
]

for title, body in challenges:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.5)
    r_title = p.add_run(title + "  ")
    r_title.font.bold = True
    r_title.font.size = Pt(11)
    r_title.font.name = "Calibri"
    r_body = p.add_run(body)
    r_body.font.size = Pt(11)
    r_body.font.name = "Calibri"
    spacer(doc)

spacer(doc)

# ── 6. IMPLEMENTATION STATUS ──────────────────────────────────────────────────
add_heading(doc, "6. Current Implementation Status", 1)
add_body(doc,
    "As of the date of this report, the following components have been fully implemented "
    "and validated:"
)
spacer(doc)

implemented = [
    "Omniverse USD export pipeline with per-job JSON configuration and SHA-256 versioning",
    "FastAPI HTTP server with manifest, asset, Vuforia target, and export-trigger endpoints",
    "gRPC session service (bidirectional streaming: connect, heartbeat, step-activate, step-complete)",
    "gRPC asset transfer service (GLB and Vuforia target chunk streaming to the AR device)",
    "Unity AR client with native gRPC transport (YetAnotherHttpHandler) and HTTP REST fallback",
    "Immutable disk-based asset cache and Vuforia target cache on the AR device",
    "glTFast runtime GLB loader with reflection-based version compatibility layer",
    "Vuforia Model Target and Image Target runtime loading from server-downloaded databases",
    "Holographic visual style shader (translucent cyan, fresnel rim glow, scan-line animation)",
    "Fixture overlay with slice-plane reveal animation on first target acquisition",
    "Configurable model position offset and animation speed multiplier from the Unity Inspector",
    "Per-job JSON configuration files for the export pipeline (Demonstrator and PU Segment Assembly)",
    "Pose smoothing (Lerp / Slerp) and tracking hint angle computation in TargetManager",
    "Session state machine with automatic reconnect loop and step progression in AppBootstrap",
    "Architecture, server-setup, Unity client, and Omniverse integration documentation",
]

for item in implemented:
    add_bullet(doc, item)

spacer(doc)

# ── 7. REPORT STRUCTURE ───────────────────────────────────────────────────────
add_heading(doc, "7. Structure of This Report", 1)
add_body(doc,
    "The remainder of this report is organised as follows:"
)
spacer(doc)

report_sections = [
    ("Section 8  –  Detailed Architecture",
     "Component-level descriptions, data flow diagrams, and interface contracts."),
    ("Section 9  –  Export Pipeline",
     "Omniverse USD-to-GLB export workflow, job configuration schema, and versioning strategy."),
    ("Section 10  –  Server-Kit",
     "FastAPI and gRPC service design, REST endpoints, environment configuration, and deployment."),
    ("Section 11  –  Unity AR Client",
     "Session lifecycle, asset resolution, model loading, Vuforia integration, and visual effects."),
    ("Section 12  –  Validation and Testing",
     "Validation matrix, pilot workflow checklists, and device performance budget."),
    ("Section 13  –  Future Work",
     "Planned extensions, open engineering items, and recommended next steps."),
    ("Section 14  –  Conclusion",
     "Summary of achievements and significance of the project within the DIREKT context."),
]

for sec_title, sec_desc in report_sections:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(0.5)
    r_t = p.add_run(sec_title + ":  ")
    r_t.font.bold = True
    r_t.font.size = Pt(11)
    r_t.font.name = "Calibri"
    r_d = p.add_run(sec_desc)
    r_d.font.size = Pt(11)
    r_d.font.name = "Calibri"

# ── SAVE ──────────────────────────────────────────────────────────────────────
out = r"D:\DIREKT\Worker guidance\Omniverse-UnityAR-WorkerGuidance\docs\DIREKT_AR_WorkerGuidance_TechnicalReport_Introduction.docx"
doc.save(out)
print("Saved:", out)
