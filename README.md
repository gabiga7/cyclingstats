## Physiological bases

### Energy storage

The human body stores energy in different forms:

- **ATP (adenosine triphosphate)** : The main source of energy for muscle contractions.
- **Creatine phosphate**: Used for very short-term efforts.
- **Glycogen**: Stored in the liver and muscles and used as fuel during prolonged exercise.

### Energy pathways

- **Efforts lasting less than 10 seconds**: The body mainly uses creatine phosphate.
- **Exercises lasting between 30 seconds and 2 minutes** : Anaerobic glycolysis predominates.
- **Longer efforts**: Dependence on aerobic glycolysis and beta-oxidation.

## Cyclist Bioenergy Equation

The main formula behind this tool is based on a combination of logarithmic functions: 
**f(x) = a/ln(x) + b * ln(x) + c**

The combination of division by a logarithm and multiplication by a logarithm creates a model that can describe how a cyclist's power evolves during efforts of different durations.

N.B : This equation is based on observations of different cyclist profiles in different events. The equation is verified for a 1h effort maximum.

### Explanation of terms

1. **Term a/ln(x)** :
   
   This term could represent the body's initial dependence on rapidly available energy sources, such as ATP and creatine phosphate. When the effort is short, this term represents high initial power, but these sources are rapidly depleted.

2. **Term b*ln(x)** :

   As the initial energy sources are depleted, the body relies more heavily on glycolysis, first anaerobically, then aerobically. This term increases slowly over time, representing the increasing reliance on these more sustainable energy pathways.

3. **Term c** :

   After a prolonged period, the body relies mainly on beta-oxidation, where fat is the main source of energy. This term may indicate stabilisation at this stage, reflecting the individual's aerobic endurance.


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
