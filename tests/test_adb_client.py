from adb.adb_client import ADBClient

adb = ADBClient()

print("Manufacturer:", adb.getprop("ro.product.manufacturer"))
print("Model:", adb.getprop("ro.product.model"))
print("Android:", adb.getprop("ro.build.version.release"))
print("Security Patch:", adb.getprop("ro.build.version.security_patch"))
