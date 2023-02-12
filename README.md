# Finary Assistant

Organize your portfolio in custom folders, synchronize each investment with your Finary account, and get automated 

![Employee data](/doc/screenshot.png "Result example")

## Installation
TODO Dependencies, installation, ...

## Usage 
TODO Declare portfolio, targets, ...

## Development status
- [X] **Chapter 1: Portfolio Classifier**
  - [X] Create a tree structure with `Lines` and `Folders`
  - [X] Command-line printing with [`rich`](https://pypi.org/project/rich/)
  - [X] Define `Targets` and colorful rendering
  - [X] Create `Bucket` and `SharedFolder` objects
  - [X] Finary sync with `finary_api`
- [ ] **Chapter 2: Analyzer**
  - [ ] Table with asset classes, types, envelopes, amounts, ...
  - [ ] Graphs of percentages for asset classes
  - [ ] Others?
- [ ] **Chapter 3: Simulator**
  - [ ] Create an event-based simulation engine
  - [ ] Declare yearly (or monthly?) life objectives, events, and income
  - [ ] Display a graph of the entire portfolio evolution
  - [ ] Model the evolution of each investment (with optimistic-pessimistic probabilities), propagate uncertainties through time
  - [ ] Define a `Scenario` that describes portfolio operations (e.g. transfer funds, spend _x_ € on investment _y_)
  - [ ] Define investment constraints and effects (e.g. PER blocked until a set event, tax effects)
  - [ ] Simulate taxes
  - [ ] Plot the full portfolio nicely as the _tax-deducted_ evolution, classified as available/taxed/blocked
- [ ] **Chapter 4: Assistant**
  - [ ] Programmable rules to invest your salary each month
  - [ ] Rich display on terminal
  - [ ] Yearly PEA/AV/CTO vs. PER optimisation fiscale (like ramify)
  - [ ] SAT solver-based AI-like assistant that optimizes taxes and evolution to meet life goals
- [ ] **Chapter 5: Optional**
  - [ ] Create a web interface?
  - [ ] Regular backup of the portfolio state?
  - [ ] Monte Carlo simulation instead of probabilities? Customizable Monte Carlo with personal ideas (e.g. environmental crisis effects on ETFs)?

## Donations

If you found this project useful and wish to support my work, you can buy me a coffee so I can work more on my personal projects and improve them :) Thank you!

[<img src="https://www.mathisplumail.com/wp-content/uploads/2021/04/coffee.png" width="180" />](https://www.buymeacoffee.com/MadeInPierre)