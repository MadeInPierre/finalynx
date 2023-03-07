# Development status
Contributions and feature ideas are warmly welcome!

**TODO** MOVE THIS LIST TO GITHUB ISSUES AND MILESTONES

- [X] **Chapter 1: Portfolio**
  - [X] Create a tree structure with `Lines` and `Folders`
  - [X] Pretty command-line printing with [`rich`](https://pypi.org/project/rich/)
  - [X] Define `Targets` with colorful rendering
  - [X] Create `Bucket` and `SharedFolder` objects to consider multiple lines as a unique position
  - [X] Fetch real-time investment amounts from Finary using [`finary_api`](https://github.com/lasconic/finary)
  - [X] Folders can be displayed as expanded, collapsed or look like a single line
- [ ] **Chapter 2: Publish to GitHub**
  - [X] Nice GitHub landing page (hopefully) just to have fun
  - [X] Demo file with comments
  - [X] Create a central Assistant class instead of a main function
  - [X] Parse options in command line
  - [X] Remove the need for the install script using syspath appends
  - [X] Auto-login using environment variables (bypass relative loads from finary_api)
  - [ ] Learn to do versioning, releases, PEP8, ...
  - [ ] Write detailed instructions to create your own config
  - [ ] Documentation? Wait to see if people are interested
- [ ] **Chapter 2: Analyzer**
  - [ ] Print a table with asset classes, types, envelopes, amounts, ...
  - [ ] Graphs of percentages for asset classes
  - [ ] Define envelope types (e.g. PEA, AV, PER, ...) and show the tax status (blocked, highly taxed, optimal)
  - [ ] TODO Statistics, others?
- [ ] **Chapter 3: Simulator**
  - [ ] Create an event-based simulation engine
  - [ ] Declare yearly (or monthly?) life objectives, events, and income
  - [ ] Display a graph of the entire portfolio evolution
  - [ ] Model the evolution of each investment (with optimistic-pessimistic probabilities), propagate uncertainties through time
  - [ ] Define a Scenario that describes portfolio operations (e.g. transfer funds, spend _x_ € on investment _y_)
  - [ ] Define investment constraints and effects (e.g. PER blocked until a set event, tax effects)
  - [ ] Simulate taxes
  - [ ] Plot the full portfolio nicely as the _tax-deducted_ evolution, classified as available/taxed/blocked
- [ ] **Chapter 4: Assistant**
  - [ ] Programmable rules to invest your salary each month
  - [ ] Rich display on terminal
  - [ ] Yearly PEA/AV/CTO vs. PER optimisation fiscale (like ramify)
  - [ ] SAT solver-based AI-like assistant that optimizes taxes and evolution to meet life goals
- [ ] **Chapter 5: Optional**
  - [ ] Create a web dashboard? Open to contributions 🙂
  - [ ] Regular backup of the portfolio tree for archive?
  - [ ] Monte Carlo simulation instead of probabilities?
  - [ ] Customizable Monte Carlo with personal beliefs (e.g. climate crisis effects)?
