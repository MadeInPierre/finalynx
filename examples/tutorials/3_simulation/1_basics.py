"""
Finalynx - Tutorial 3.1 - Simulate your portfolio's future
==========================================================


This tutorial shows how to simulate your portfolio's future by automagically:
- Applying the recommendations made by Finalynx to your portfolio,
- Applying the expected yearly performance of each line (specified by you),
- Reducing your portfolio's value due to inflation,
- Adding your monthly salary each month.

By default, the first three points are enabled, you can disable them by setting
the `default_events` option to `False` in the `Simulation` constructor.


See the online documentation for the list of available pre-defined envelopes:
> https://github.com/MadeInPierre/finalynx/blob/main/finalynx/portfolio/envelopes.py

Try it out by running:
> python3 examples/tutorials/12_envelopes.py

See explanations and details in the online documentation at:
> https://finalynx.readthedocs.io
"""
# noreorder
from finalynx import Assistant, Portfolio, Line
from finalynx import Simulation, Event, Salary, AddLineAmount, date

""" [SIMULATION BASICS] -------------------------------------------------------
The simulator can apply `Actions` wrapped around an `Event` instance. Events
define when to perform the action, and can define an optional `Recurrence` to
perform the action regularly (e.g. every month, at the end of each year, ...).

There are currently three supported actions for now:
- **ApplyPerformance:** Change the amounts of each `Line` depending on the
  specified `LinePerf` expected investment performance. By default, this
  action is already added in the list of events in the configuration and
  executes on each December 31st.
- **AutoBalance:** For folders and lines that use `TargetRatio` targets,
  Finalynx will automatically apply the ideal amounts for each `Line`.
  This corresponds to following the Finalynx recommendations. By default,
  this event is automatically added and executed every 3 months.
- **Salary**: Specify which `Line` in the portfolio should receive a specific
  amount each month. This class is simply a shortcut to:

  ```python
  Event(AddLineAmount(your_account, 2500), recurrence=MonthlyRecurrence(day_of_the_month, until=end_date))
  ```

By default, the simulation runs for 100 years.

To activate the simulator with the default events, add the following to your config:
"""

Assistant(Portfolio(), simulation=Simulation()).run()  # activate the simulation (with default behavior)

"""
Some other parameters can be set:
"""


livreta = Line("Livret A")  # Create a line before the portfolio to be able to reference it

portfolio = Portfolio(children=[livreta])  # Create your portfolio with the line included anywhere in it


Assistant(
    portfolio,
    buckets=[],  # Create a list with the references to your buckets (if any, none here)
    envelopes=[],  # Create a list with the references to your envelopes (if any, none here)
    # ... other options,
    simulation=Simulation(
        events=[  # Your personal config of events (salaries for now, more coming soon!)
            Salary(livreta, income=2300, expenses=1400, end_date=date(2024, 11, 30)),
            Event(AddLineAmount(livreta, 3500), planned_date=date(2024, 4, 10), name="Prime"),
            Event(AddLineAmount(livreta, 3500), planned_date=date(2025, 4, 10), name="Prime"),
            Salary(livreta, income=3000, expenses=2000, start_date=date(2025, 1, 1), name="Futur Job"),
        ],
        inflation=3.0,  # Percentage of inflation, will reduce each line's performance by this much
        end_date=date(2063, 4, 5),  # Defaults to 100 years after today
        step_years=5,  # Show a summary of the portfolio's total worth every X years in the console
        default_events=True,  # Add default events to the ones specified above, defaults to True
    ),
).run()
