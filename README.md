# Satellite Orbit Visualization

This Python project fetches Two-Line Element (TLE) data for satellites and visualizes their orbits in a 3D space using Matplotlib. Users can either enter a specific satellite name or choose to plot an entire satellite group.

## Features
- Fetches TLE data for a single satellite from a public API.
- Fetches and plots orbits of all Starlink satellites from Celestrak.
- Dynamically adjusts the graph to fit different orbital altitudes.
- Displays an accurate representation of Earth and satellite orbits.

## Installation

### Prerequisites
Ensure you have Python installed (Python 3.7+ recommended). You also need `pip` for dependency management.

### Steps
1. Clone this repository:
   ```sh
   git clone https://github.com/syntaxerrorStephen/TLE-Sim.git
   cd TLE-Sim
   ```

2. Create a virtual environment:

   Mac:
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

   Windows:
   ```sh
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```


3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the script and follow the menu prompts:
```sh
python main.py
```

### Options:
1. **Enter a specific satellite name** - The script will fetch and plot its orbit.
2. **Plot grouped satellites** - The script will fetch all available Starlink TLE data and visualize them.

## Dependencies
This project requires the following Python libraries:
- `requests` - To fetch TLE data from APIs
- `matplotlib` - For 3D plotting
- `numpy` - For mathematical operations
- `datetime` - For time calculations

## Example Output
- A 3D plot of the satellite's orbit around Earth
- A dynamic view that adjusts to different orbital altitudes



## Acknowledgments
- [Celestrak](https://celestrak.org/) for providing TLE data
- Open-source contributors for Python libraries used in this project

---


