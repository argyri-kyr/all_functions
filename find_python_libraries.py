


import site
import os
import time

paths = []

# Get all possible site-packages paths
try:
    paths.extend(site.getsitepackages())
except:
    pass

user_site = site.getusersitepackages()
if user_site:
    paths.append(user_site)

packages = []

for path in paths:
    if not path or not os.path.exists(path):
        continue

    for item in os.listdir(path):
        if item.endswith(".dist-info"):
            full_path = os.path.join(path, item)
            install_time = os.path.getctime(full_path)
            packages.append((install_time, item.replace(".dist-info", "")))

# Sort by install time (ascending)
packages.sort(key=lambda x: x[0])

print(f"{'Install Time':<22} Package")
print("-" * 60)

for t, name in packages:
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)):<22} {name}")

