# Finary Assistant :robot:

A command-line tool to organize your investments portfolio in custom folders, synchronize it with your [Finary](https://finary.com) account, get automated monthly investment recommendations, and see your portfolio's future! :superhero: Don't have Finary yet? Sign up using my [referral link](https://finary.com/referral/f8d349c922d1e1c8f0d2)!

:warning: Use at your own risk. I'm not responsible for any issues with your account. :warning:

![Employee data](/doc/screenshot.png "Portfolio example")

## Installation

1. Install `finary_api` by following the instructions there and make sure everything works.
2. Inside `finary_api`, modify the `finary_api/constants.py` file and provide the full path to the credentials and cookies file:

```python
CREDENTIAL_FILE = "/full/path/to/credentials.json"
COOKIE_FILENAME = "/full/path/to/localCookiesMozilla.txt"
```

3. Add the following line at the end of your `.bashrc` (or `.zshrc`) file and relaunch your terminal:

```sh
export PYTHONPATH=/full/path/to/finary:$PYTHONPATH
```

4. Clone this repository anywhere:

```sh
git clone https://github.com/MadeInPierre/finary_assistant.git
```

5. Install pip dependencies:

```sh
pip install -r requirements.txt
```

6. Run the assistant:

```sh
python assistant.py
```

And you're done! Now go customize the `assistant.py` file for your own needs.

## Usage 
TODO Declare portfolio, targets, ...

## Development status
- [X] **Chapter 1: Portfolio Classifier**
  - [X] Create a tree structure with `Lines` and `Folders`
  - [X] Command-line printing with [`rich`](https://pypi.org/project/rich/)
  - [X] Define `Targets` and colorful rendering
  - [X] Create `Bucket` and `SharedFolder` objects
  - [X] Finary sync with [`finary_api`](https://github.com/lasconic/finary)
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

## Contributions and Requests
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome!

## License
This project is under the [GPLv3 License](./LICENSE) meaning anyone can use, share, extend, and contribute to this project as long as their changes are integrated to this repo or also published using GPLv3. Please contact me for any specific licensing requests.

## Donations
[<img align="right" src="https://www.mathisplumail.com/wp-content/uploads/2021/04/coffee.png" width="180" />](https://www.buymeacoffee.com/MadeInPierre)
If you found this project useful and wish to support my work, you can [buy me a coffee](https://www.buymeacoffee.com/MadeInPierre)! Coffee gives me the motivation to work on my personal projects and improve them :smile: Thank you!
