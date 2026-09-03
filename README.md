# 🎙️ Nexus: Autonomous Voice Operations Console

Nexus is a low-latency, multi-agent voice operations system built for real-time infrastructure telemetry, incident management, and conversational automation. It connects dynamic Voice Activity Detection (VAD) with LangGraph state orchestration and neural speech synthesis.

---

## ⚡ Key Highlights & Architecture

* **Brain Engine:** Google Gemini Flash (Direct native API integration for fast inference).
* **State & Memory Machine:** LangGraph with dynamic routing and thread-based `MemorySaver` persistence.
* **Audio Pipeline:** 
  * **Ingestion:** Dynamic Voice Activity Detection (VAD) via `sounddevice` + `SpeechRecognition`.
  * **Playback:** Real-time neural audio streaming via `edge-tts`.
* **Telemetry & Ops:** Real-time host hardware extraction (CPU, RAM, Disk) via `psutil`.
* **Operations Dashboard:** Dark-mode Streamlit console with live latency tracking and execution trace.

```text
[ User Microphone ] 
       │ (VAD / Dynamic Silence Cutoff)
       ▼
[ Speech-to-Text ] 
       │
       ▼
[ LangGraph Brain (Gemini Flash) ] ── (Tool Routing) ──► [ System Telemetry (psutil) / Ticket Ops ]
       │
       ▼
[ Parallel Async Pipeline ]
   ├──► [ UI State & Streamlit Stream ]
   └──► [ Edge-TTS Synthesis ] ──► [ Local Audio Output ]