import subprocess


class ADBClient:
    def __init__(self, device_id: str | None = None):
        self.device_id = device_id

    def shell(self, command: str) -> str:
        cmd = ["adb"]

        if self.device_id:
            cmd.extend(["-s", self.device_id])

        cmd.extend(["shell", command])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()

    def getprop(self, prop: str) -> str:
        return self.shell(f"getprop {prop}")

    def dumpsys(self, service: str) -> str:
        return self.shell(f"dumpsys {service}")
