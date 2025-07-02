# Incident Manager

This is a simulated incident management system, inspired by real SOC/NOC operations. It allows registering, escalating, assigning, and resolving incidents based on customizable business rules.

## 🎯 What does this system do?

- Register incidents with type, priority, and description.
- Assign incidents to valid operators.
- Automatically escalate incidents if not addressed in time.
- Mark incidents as resolved and view their history.
- Save and load incident data using `.json` files.

The entire system runs from the command line, without using a database, but applies solid principles like composition, responsibility separation, and data structures like queues, sets, and dictionaries.

## 🧱 Project structure

```
incident_manager/
├── main.py # Entry point
├── cli/ # Command-line interaction and menus
├── core/ # Business logic (dispatch, escalation, validations)
├── incident/ # Domain models and filters
├── rules/ # Customizable business rules
├── persistence/ # JSON-based data storage
├── logs/ # Action and event logs
├── README.md # This file 
└── .gitignore # Git ignore rules
```


## 🛠️ Technologies used

- Python 3.10+
- `dataclasses`, `typing`, `datetime`, `json`, `re`, `collections`
- SOLID principles (SRP, DIP, etc.)
- Decorators, generators, iterators
- Modular architecture

## 🚀 How to run

1. Open a terminal inside the project folder.
2. Run:

```bash
python3 main.py

```

## 🧪 Simulated usage example

```
> Register incident
Type: infrastructure
Priority: high
Description: authentication servers down
✔ Generated ID: 001

> View pending incidents
[001] Infrastructure | Priority: high | Status: pending

> Assign incident 001 to operator "carlos"
✔ Successfully assigned

> Resolve incident 001
✔ Marked as resolved

> View history
[001] Resolved by carlos on 2025-05-06 19:13:21
```