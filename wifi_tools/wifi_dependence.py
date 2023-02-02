import subprocess
import time

search_str = "ssid "
cmd = ["iw", "dev"]#,  "|", "grep", "ssid"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
wifis = []
for entry in process.stdout:
    line = entry.decode().strip()
    if line.find(search_str):
        wifis.append(line.replace(search_str, ""))
