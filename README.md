# 📱 DeviceMind — MCP Powered Android Device Intelligence Assistant

## Overview

**DeviceMind** is a local-first AI-powered system that transforms an Android phone into a queryable intelligent device using:

- Android Debug Bridge (ADB)
- Python-based device collectors
- Model Context Protocol (MCP)
- A conversational assistant layer with tool routing and reasoning

DeviceMind demonstrates a new paradigm:

~~~
Turning physical devices into AI-accessible intelligence systems via MCP.
~~~

It bridges:

- Hardware (Android device)
- System access (ADB)
- Protocol layer (MCP)
- Reasoning layer (assistant logic)
- Natural language interface

It enables natural language queries like:

- “How is my phone doing?”
- “What is my battery status?”
- “Is my storage getting full?”
- “Should I worry about my device health?”

And returns structured, real-time insights directly from the physical device.

---

# 🧠 Core Idea

Traditional device monitoring systems are:
- Static dashboards
- Manual inspection tools
- Fragmented system APIs

**DeviceMind inverts this model:**

> Your device becomes a tool-accessible intelligence source for an AI assistant.

Instead of checking logs or dashboards, you simply ask questions in natural language.

---

# ⚙️ System Architecture

~~~
User (Natural Language)
↓
Chat Assistant (Intent Router + Formatter)
↓
MCP Client (stdio)
↓
MCP Server (FastMCP)
↓
AndroidCollector (Python Layer)
↓
ADB (Android Debug Bridge)
↓
Physical Android Device
~~~


---

# 🧩 Components

## 1. Android Collector (`collector.py`)

Responsible for extracting structured telemetry from the Android device via ADB.

### Extracted Signals:
- Battery status
- Charging state
- Temperature
- Voltage
- Storage usage
- Device metadata

### Example Output:

```json
{
  "device": {
    "manufacturer": "motorola",
    "model": "motorola edge 50 neo",
    "android_version": "16",
    "security_patch": "2026-05-01"
  },
  "battery": {
    "percentage": 65,
    "status": "Charging",
    "temperature": 35.0
  },
  "storage": {
    "used_gb": 79.7,
    "total_gb": 215.0
  }
}
```

## 2. MCP Server (server.py)

Implements a Model Context Protocol (MCP) server using FastMCP.

Exposed Tool
~~~
device_status()
~~~

Returns a full device snapshot from the collector.

## 3. MCP Client Layer (assistant.py)

Acts as the bridge between the assistant and MCP server.

### Responsibilities:

- Start MCP stdio session
- Call tools dynamically
- Return raw device telemetry
- Parse JSON safely
- Provide structured output to assistant layer

## 4. Chat Assistant (chat_assistant.py)

A CLI-based conversational assistant that acts as the user interface.

### Responsibilities:

#### 1. Intent Routing (Rule-based)

Maps user queries to MCP tools:

- Query	Tool
- battery	device_status
- storage	device_status
- device / health	device_status

#### 2. Query-aware Field Extraction

Extracts only relevant fields:

- battery → battery section only
- storage → storage section only
- device → device metadata
- general → full snapshot

#### 3. Natural Language Formatting

Transforms raw JSON into structured human-readable output with insights.

## 5. CLI Assistant (run_assistant.py)

A simple runtime script that:

- Calls MCP tool
- Formats response
- Prints device intelligence report


# 💡 Key Features
✅ Real Android Telemetry
Live device data via ADB.

✅ MCP-based Tool Architecture
Device exposed as structured tools using MCP.

✅ Natural Language Interface
Ask questions instead of inspecting logs.

✅ Query-aware Responses
Output adapts based on user intent.

✅ Fully Local-first System
No cloud dependency — runs entirely via USB + local machine.

# 🚀 Usage

## Connect device to your laptop

- Enable Developer 
## Install dependencies

~~~
pip install -r requirements.txt
~~~

## Start Chat Assistant

~~~
python3 chat_assistant.py
~~~

# Example Interactions

## Battery Query

~~~
You: How is my battery?

Response:

🔋 Battery: 62% - Discharging
🌡 Temperature: 33.0°C

🧠 Insights:
- Everything looks normal.
~~~

## Storage Query

~~~
You: How is storage?

Response:

💾 Storage: 79.7/215.0 GB used

🧠 Insights:
- Everything looks normal.
~~~

## Full Device Query

~~~
You: How is my device doing?

Response:

📱 Device: motorola edge 50 neo (16)

🔋 Battery: 65%
🌡 Temperature: 35°C
💾 Storage: 79.7/215.0 GB used
~~~


# 🚀 Roadmap

## Phase 2 — MCP Tool Expansion

Split into:

- battery_status()
- storage_status()
- device_info()


## Phase 3 — LLM-Based Agent Routing

Replace rule engine with LLM-based tool selection.

## Phase 4 — Memory Layer
- Battery trends
- Storage growth tracking
- Device history over time

## Phase 5 — Proactive Assistant
- “Storage will fill in 10 days”
- “Battery degrading faster than usual”
- “Device overheating detected”
