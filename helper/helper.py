import json


def safe_parse(raw_text: str):
    try:
        return json.loads(raw_text)
    except Exception:
        return None


def format_response(raw_text: str, fields):

    data = safe_parse(raw_text)

    if not data:
        return "⚠️ Unable to read device data."

    device = data["device"]
    battery = data["battery"]
    storage = data["storage"]

    insights = []

    output = []

    if "device" in fields:
        output.append(f"📱 Device: {device['model']} ({device['android_version']})")

    if "battery" in fields:
        output.append(f"🔋 Battery: {battery['percentage']}% - {battery['status']}")
        output.append(f"🌡 Temperature: {battery['temperature']}°C")

    if "storage" in fields:
        output.append(
            f"💾 Storage: {storage['used_gb']:.1f}/{storage['total_gb']:.1f} GB used"
        )

    # insights always
    if battery["percentage"] < 30:
        insights.append("Battery is low.")
    if battery.get("charging"):
        insights.append("Phone is charging.")

    return (
        "\n".join(output)
        + "\n\n🧠 Insights:\n- "
        + ("\n- ".join(insights) if insights else "Everything looks normal.")
    )
