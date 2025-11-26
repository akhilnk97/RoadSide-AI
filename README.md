# RoadSide AI 🔧
### Universal Vehicle Diagnostic Agent
**Built for the Google AI Agents Intensive 2025 (Agents for Good Track)**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://roadside-ai.streamlit.app)

---

## 🚨 The Problem
In India, vehicle breakdowns often happen in heavy traffic (like in Kochi) or remote highway stretches. Drivers—especially non-mechanics—panic. They don't know if the issue is a simple loose wire or a dangerous engine failure. Professional help is often miles away, and existing solutions (searching Google) are too generic and often unsafe.

## 💡 The Solution
**RoadSide AI** is a Multimodal, Multi-Agent System that puts an expert mechanic in your pocket.
Unlike generic chatbots, it uses a **Sequential Logic Chain** to diagnose issues step-by-step, prioritizing safety above all else.

---

## 🎥 Demo
* **[📺 Watch the Video Demo](https://www.youtube.com/watch?v=lp1_We-0hgQ)**
* **[🚀 Try the Live App](https://roadside-ai.streamlit.app)**

---

## 🛠️ Architecture (The "Brain")
This project uses a **Dual-Agent System** to ensure accuracy and safety.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#fff'}}}%%
graph TD
    User([User / Driver]) -->|1. Photo/Text| UI[Streamlit Interface]
    UI -->|2. Input| Orchestrator{Python Logic}
    
    subgraph "The AI Agents"
        Orchestrator -->|3. Diagnose| Mech[<b>Agent 1: The Mechanic</b><br/>Gemini 2.0 Flash]
        Mech -->|4. Repair Steps| Orchestrator
        Orchestrator -->|5. Safety Check| Safe[<b>Agent 2: Safety Supervisor</b><br/>Gemini 2.0 Flash]
        Safe -->|6. Safe Advice| Orchestrator
    end
    
    Orchestrator -->|7. Display| UI -->|8. Fix| User
    
    style Mech fill:#e3f2fd,stroke:#1565c0,color:black
    style Safe fill:#ffebee,stroke:#c62828,color:black
    style UI fill:#f3e5f5,stroke:#4a148c,color:black
