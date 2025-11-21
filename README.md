# RoadSide AI 🔧
**Universal Vehicle Diagnostic Agent | Google AI Agents Capstone 2025**

## 🚨 The Problem
In India, vehicle breakdowns often happen in heavy traffic (like in Kochi) or remote areas. Drivers panic. They don't know if the issue is a simple loose wire or a dangerous engine failure. Professional help is often miles away.

## 💡 The Solution
**RoadSide AI** is a Multimodal Multi-Agent System that puts an expert mechanic in your pocket.
Unlike generic chatbots, it uses a **Sequential Logic Chain** to diagnose issues step-by-step, prioritizing safety.

## 🛠️ Architecture (The "Brain")
This project uses a **Dual-Agent System** to ensure accuracy and safety:
1.  **Agent 1 (The Mechanic):** Uses **Gemini 2.0 Flash** (Vision) to analyze photos of the engine and suggest repairs.
2.  **Agent 2 (The Safety Supervisor):** A dedicated guardrail agent that reviews every piece of advice for risks (fire, heat, traffic) before the user sees it.

## ✨ Key Features
* **Vision-Powered:** Snap a photo of the engine to identify parts.
* **Sequential Logic:** The AI asks for feedback ("Did that fix it?") before moving to the next step.
* **Personality:** "Mac" the mechanic keeps the conversation calm and helpful.

## 🚀 How to Run
1.  `pip install -r requirements.txt`
2.  `streamlit run app.py`
3.  Enter your Google API Key in the sidebar.