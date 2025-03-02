import requests
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import math as m

# Constants
mu = 398600  # Earth's gravitational parameter (km^3/s^2)
r = 6371  # Earth's radius in km

# Function to fetch TLE data
def fetch_tle_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.split('\n')
    else:
        print("Error fetching data.")
        return []

# Function to parse TLE data from text
def parse_tle_data(tle_lines):
    satellites = {}
    i = 0
    while i < len(tle_lines) - 2:
        if tle_lines[i] and tle_lines[i + 1].startswith("1") and tle_lines[i + 2].startswith("2"):
            name = tle_lines[i].strip()
            tle1 = tle_lines[i + 1].strip()
            tle2 = tle_lines[i + 2].strip()
            satellites[name] = (tle1, tle2)
            i += 3
        else:
            i += 1
    return satellites

# Function to plot satellite orbits
def plot_satellites(tle_data):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    max_distance = r
    
    for name, (tle1, tle2) in tle_data.items():
        orb = {}
        orb["name"] = name
        orb["e"] = float("." + tle2[26:34])
        orb["a"] = (mu / ((2 * m.pi * float(tle2[52:63]) / (24 * 3600)) ** 2)) ** (1. / 3)
        orb["i"] = float(tle2[9:17]) * m.pi / 180
        orb["RAAN"] = float(tle2[17:26]) * m.pi / 180
        orb["omega"] = float(tle2[34:43]) * m.pi / 180
        orb["b"] = orb["a"] * m.sqrt(1 - orb["e"] ** 2)
        orb["c"] = orb["a"] * orb["e"]
        max_distance = max(max_distance, orb["a"] * (1 + orb["e"]))
        
        R = np.matmul(
            np.array([[m.cos(orb["RAAN"]), -m.sin(orb["RAAN"]), 0],
                      [m.sin(orb["RAAN"]), m.cos(orb["RAAN"]), 0],
                      [0, 0, 1]]),
            np.array([[1, 0, 0],
                      [0, m.cos(orb["i"]), -m.sin(orb["i"])],
                      [0, m.sin(orb["i"]), m.cos(orb["i"])]])
        )
        R = np.matmul(R, np.array([[m.cos(orb["omega"]), -m.sin(orb["omega"]), 0],
                                    [m.sin(orb["omega"]), m.cos(orb["omega"]), 0],
                                    [0, 0, 1]]))
        
        x, y, z = [], [], []
        for i in np.linspace(0, 2 * m.pi, 100):
            P = np.matmul(R, np.array([[orb["a"] * m.cos(i)],
                                        [orb["b"] * m.sin(i)],
                                        [0]])) - np.matmul(R, np.array([[orb["c"]], [0], [0]]))
            x.append(P[0])
            y.append(P[1])
            z.append(P[2])
        
        ax.plot(x, y, z, label=orb["name"])
    
    # Plot Earth
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
    ax.plot_wireframe(r * np.cos(u) * np.sin(v),
                      r * np.sin(u) * np.sin(v),
                      r * np.cos(v), color="b",
                      alpha=0.5, lw=0.5)
    
    ax.set_xlim(-max_distance * 1.1, max_distance * 1.1)
    ax.set_ylim(-max_distance * 1.1, max_distance * 1.1)
    ax.set_zlim(-max_distance * 1.1, max_distance * 1.1)
    ax.set_box_aspect([1, 1, 1])
    
    plt.title("Satellite Orbits")
    ax.set_xlabel("X-axis (km)")
    ax.set_ylabel("Y-axis (km)")
    ax.set_zlabel("Z-axis (km)")
    ax.legend()
    plt.show()

# User Menu
print("Select an option:")
print("1. Plot a single satellite orbit")
print("2. Plot a group of satellite orbits")
choice = input("Enter choice (1 or 2): ")

tle_data = {}

if choice == "1":
    satellite_name = input("Enter satellite name (e.g. SES-14, LANDSAT 9): ")
    tle_url = f"https://celestrak.org/NORAD/elements/gp.php?NAME={satellite_name}&FORMAT=tle"
    tle_lines = fetch_tle_data(tle_url)
    tle_data = parse_tle_data(tle_lines)

elif choice == "2":
    group_name = input("Enter satellite group (e.g. starlink, oneweb, tdrss): ")
    grouptle_url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group_name}&FORMAT=tle"
    tle_lines = fetch_tle_data(grouptle_url)
    tle_data = parse_tle_data(tle_lines)

if tle_data:
    plot_satellites(tle_data)
else:
    print("No valid TLE data found.")
