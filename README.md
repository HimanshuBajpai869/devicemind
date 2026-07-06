# 📱 DeviceMind — MCP Powered Android Device Intelligence Assistant

## Overview

**DeviceMind** is a local-first AI-powered system that transforms an Android phone into a queryable intelligent device using:

- Android Debug Bridge (ADB)
- Python-based device collectors
- Model Context Protocol (MCP)
- LLM using Ollama
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

## 1. Android Collector (`collector/collector.py`)

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

## 2. MCP Server (server/server.py)

Implements a Model Context Protocol (MCP) server using FastMCP.

Exposed Tool
~~~
device_status()
~~~

Returns a full device snapshot from the collector.

## 3. MCP Client Layer (assistant/assistant.py)

Acts as the bridge between the assistant and MCP server.

### Responsibilities:

- Start MCP stdio session
- Call tools dynamically
- Return raw device telemetry
- Parse JSON safely
- Provide structured output to assistant layer

## 4. Chat Assistant (assistant/chat_assistant_v2.py)

A CLI-based conversational assistant that acts as the user interface.

## 5. Ollama based LLM Provider to Plan and Reason (llm/llm.py)

Ollama based LLM Provider to -

- Plan - To idenfity the tool which needs to be called.
- Reason - To parse the response from LLM to a more user-friendly message.

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

##### Step 1: Enable Developer Options

On your phone:

- Go to Settings → About phone
- Tap Build Number 7 times (or the equivalent on your manufacturer)
- Enter your PIN if prompted
- You should see "You are now a developer."

##### Step 2: Enable USB Debugging

Go to:

~~~
Settings
    ↓
Developer Options
    ↓
USB Debugging
~~~

Turn it ON.

##### Step 3: USB Mode

For most Android phones, File Transfer is the safest choice over USB

## Install dependencies

~~~
pip install -r requirements.txt
~~~

## Start Ollama Server

- Install Ollama based on your OS from the official documentation - https://ollama.com/
- Start Ollama Server:
~~~
ollama serve
~~~
- Pull the LLM Model - The solution right now uses qwen3:8b, but you can change model as needed.Use tinyllama for quick try out
~~~
ollama pull qwen3:8b
~~~

## Start Chat Assistant

~~~
python3 -m assistant.chat_assistant_v2
~~~

# Example Interactions

~~~
ou: How is overall health of the device?
🧠 Planning...
========== RAW LLM OUTPUT ==========
{"tool":"device_status"}
====================================
{'tool': 'device_status'}
🔧 Calling device_status
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
🤖 Reasoning...

Assistant:

The device's overall health appears to be in good condition.  

- **Battery**: At 100% charge and currently charging, with "Good" health, a temperature of 33°C, and a voltage of 4.473V. No signs of degradation or issues.  
- **Storage**: 79 GB used out of 215 GB total, leaving 135 GB available. Sufficient free space ensures optimal performance.  
- **System**: Running Android 16 with a security patch up to May 2026, indicating up-to-date software.  

No critical warnings or anomalies detected in the telemetry data.
~~~

~~~
You: how is mobile battery health?
🧠 Planning...
========== RAW LLM OUTPUT ==========
{"tool":"battery_status"}
====================================
{'tool': 'battery_status'}
🔧 Calling battery_status
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
🤖 Reasoning...

Assistant:

The mobile battery is currently at 100% capacity and is in the process of charging. Its health status is "Good," indicating no significant degradation. The temperature is 33.9°C, which is slightly elevated but within a range that typically doesn't harm the battery. The voltage reads 4.472V, which is normal for a lithium-ion battery during charging. No immediate concerns are indicated based on the provided data.
~~~

~~~
You: How is mobile storage health?
🧠 Planning...
========== RAW LLM OUTPUT ==========
{"tool":"storage_status"}
====================================
{'tool': 'storage_status'}
🔧 Calling storage_status
Processing request of type CallToolRequest
Processing request of type ListToolsRequest
🤖 Reasoning...

Assistant:

The mobile storage has **78.97 GB used** out of a total **214.98 GB**, leaving **135.50 GB available**. This indicates a healthy balance, as over half the storage remains free, which is typically sufficient for most users. However, storage health also depends on factors like app usage, system updates, and whether critical data (e.g., apps, media) are stored on internal storage versus expandable storage. If you're experiencing performance issues or low space warnings, further analysis of specific usage patterns would be helpful.
~~~

# 🚀 Roadmap

## Phase 2 — Memory Layer
- Battery trends
- Storage growth tracking
- Device history over time

## Phase 3 — Proactive Assistant
- “Storage will fill in 10 days”
- “Battery degrading faster than usual”
- “Device overheating detected”
