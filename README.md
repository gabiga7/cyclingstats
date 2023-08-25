# Power Analysis Tool for Cyclists

## Scientific explanation of the equations

The main formula behind this tool is based on a combination of logarithmic functions: 
f(x) = a/ln(x) + b * ln(x) + c

The combination of division by a logarithm and multiplication by a logarithm creates a model that can describe how a cyclist's power evolves during efforts of different durations.

N.B : This equation is based on observations of different cyclist profiles in different events.

## Using the scripts

### `auto.py`

This script is a live analyser that uses Bluetooth connectivity to receive and process power data in real time.

#### How to use it :

1. Ensure that your Bluetooth device is correctly configured and paired with the data source.
2. Run the script : 
python auto.py
3. Follow the on-screen instructions to start the live analysis.

### `computation.py`

This script analyses power data from `.gpx` or `.tcx` files.

#### How to use it :

1. Prepare your `.gpx` or `.tcx` file containing the power data.
2. Run the script, supplying the file as an argument:
python computation.py path_to_your_file.gpx
3. The script will process the data and provide a detailed analysis based on the formula above.

---

Remember that these interpretations are based on the constants provided and the mathematical models used. For more specific or tailored analyses, consult an expert in exercise physiology or a professional cycling coach.

By Gabriel Quint
