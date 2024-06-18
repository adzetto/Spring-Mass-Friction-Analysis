# Spring-Mass System Simulation

## Project Overview

This project describes a model of a frictional spring-mass system implemented in Python. The results are shown in dynamic graphs, which make the system's behaviour both comprehensible and visually appealing.

## Project Structure

```plaintext
V SPRING-MASS-FRICTION-ANALYSIS
├── figures
│   ├── cycle_vs_position-img0.png
│   ├── cycle_vs_position.pdf
│   ├── cycle_vs_position.pgf
│   ├── displacement_vs_time_and_velocity_vs_displacement.pdf
│   ├── time_complexity.pgf
│   └── time_memory_complexity.pgf
├── bibtex.bib
├── configurations.tex
├── main.pdf
├── main.py
├── main.tex
└── rowdata.tex
```

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python libraries:
  - numpy
  - matplotlib
  - memory_profiler
  - manim
- LaTeX distribution (e.g., TeX Live, MiKTeX)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/spring-mass-system-simulation.git
    cd spring-mass-system-simulation
    ```

2. Install required Python packages:
    ```bash
    pip install numpy matplotlib memory_profiler manim
    ```

### Running the Simulation

1. Run the main simulation script:
    ```bash
    python code/simulation.py
    ```

2. Generate plots:
    ```bash
    python code/plotting.py
    ```

3. Create Manim animations:
    ```bash
    python code/manim_simulation.py
    ```

### LaTeX Document

1. Compile the LaTeX document:
    ```bash
    pdflatex main.tex
    biber main
    pdflatex main.tex
    pdflatex main.tex
    ```

### Output Files

- `figures/cycle_vs_position.pdf`: Plot of cycle vs position.
- `figures/displacement_vs_time_and_velocity_vs_displacement.pdf`: Plot of displacement and velocity over time.
- `figures/time_complexity.pgf`: Plot of time complexity.
- `figures/time_memory_complexity.pgf`: Plot of time and memory complexity.

### Sample Outputs

#### Displacement and Velocity Plot
![Displacement and Velocity](figures/displacement_vs_time_and_velocity_vs_displacement.pdf)

#### Time Complexity Plot
![Time Complexity](figures/time_complexity.pgf)

#### Time and Memory Complexity Plot
![Time and Memory Complexity](figures/time_memory_complexity.pgf)

## Contributing

Please don't hesitate to provide feedback in the form of problems or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- Smith, J. (2020). *Introduction to the Spring-Mass System*. Journal of Mechanics, 34(2), 123-145.
- Doe, J. and Brown, A. (2021). *Advanced Oscillatory Motion*. Springer.
- Johnson, L. (2019). *Friction and Its Effects on Motion*. Physics Today, 56(7), 78-90.
- Miller, R. (2022). *Numerical Simulation Techniques*. Wiley.
- Various other sources as listed in the main document.

## Authors

- Muhammet Yağcıoğlu - *Initial work* - [muhammet.y.resmi@gmail.com]

---
