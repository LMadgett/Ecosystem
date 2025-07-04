# Ecosystem
A simple ecosystem simulator in Python featuring rabbits, foxes, and a food supply. The simulation models population dynamics and interactions between species over time.

## Features

- Simulates rabbits (prey), foxes (predators), and a renewable food supply.
- Adjustable parameters for birth rates, death rates, predation, and food regeneration.
- Step-by-step simulation with population tracking.
- Easily extensible for more species or environmental factors.
- Foxes turn to cannibalism if food supplies are depleted, this is less efficient.
- Tracks population of rabbits, foxes, and food supplies over time and outputs this on a graph when the simulation ends.
- Spawn foxes (left click) and rabbits (right click).

## Usage

1. Clone the repository:
    ```bash
    git clone https://github.com/LMadgett/Ecosystem.git
    cd Ecosystem
    ```

2. Run the simulation:
    ```bash
    python ecosystem.py
    ```

3. Adjust parameters in `ecosystem.py` to experiment with different scenarios.

## Example Output

```
Step 1: Rabbits=50, Foxes=10, Food=100
Step 2: Rabbits=55, Foxes=11, Food=90
...
```

## Requirements

- Python 3.x

No external dependencies required.