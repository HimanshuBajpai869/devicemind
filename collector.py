from adb_client import ADBClient

STATUS = {
    "1": "Unknown",
    "2": "Charging",
    "3": "Discharging",
    "4": "Not Charging",
    "5": "Full",
}

HEALTH = {
    "1": "Unknown",
    "2": "Good",
    "3": "Overheat",
    "4": "Dead",
    "5": "Over Voltage",
    "6": "Failure",
}


class AndroidCollector:

    def __init__(self):
        self.adb = ADBClient()

    def get_battery(self):

        output = self.adb.dumpsys("battery")

        battery = {}

        for line in output.splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            battery[key.strip()] = value.strip()

        return {
            "percentage": int(battery["level"]),
            "status": STATUS.get(battery["status"]),
            "health": HEALTH.get(battery["health"]),
            "temperature": int(battery["temperature"]) / 10,
            "voltage": int(battery["voltage"]) / 1000,
        }

    def get_device_info(self):
        return {
            "manufacturer": self.adb.getprop("ro.product.manufacturer"),
            "model": self.adb.getprop("ro.product.model"),
            "android_version": self.adb.getprop("ro.build.version.release"),
            "security_patch": self.adb.getprop("ro.build.version.security_patch"),
        }

    def get_storage(self):
        output = self.adb.shell("df /storage/emulated/0")

        lines = output.splitlines()
        if len(lines) < 2:
            return None

        parts = lines[1].split()

        def to_gb(value):
            if value.endswith("G"):
                return float(value.replace("G", ""))
            if value.endswith("M"):
                return float(value.replace("M", "")) / 1024
            if value.isdigit():
                # assume KB
                return float(value) / (1024 * 1024)
            return 0.0

        return {
            "total_gb": to_gb(parts[1]),
            "used_gb": to_gb(parts[2]),
            "available_gb": to_gb(parts[3]),
        }

    def get_status(self):
        return {
            "device": self.get_device_info(),
            "battery": self.get_battery(),
            "storage": self.get_storage(),
        }
