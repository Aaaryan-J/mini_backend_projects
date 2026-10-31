# Expense Tracker

A simple command-line expense tracker built with Python.

This is my implementation of the [Expense Tracker project](https://roadmap.sh/projects/expense-tracker) from roadmap.sh. I am building it as backend practice while learning how to work with command-line arguments, JSON data, file handling, and basic data processing in Python.

## Features

- Add an expense with a description and amount
- List saved expenses
- Show the total amount spent
- Show expenses for a specific month
- Delete an expense using its ID
- Save expenses locally in a JSON file

## Requirements

- Python 3

The program uses Python's standard library, so no additional packages are required.

## Usage

Run the program from the `cli_expense_tracker` directory:

```powershell
python main.py --help
```

### Add an expense

```powershell
python main.py add --description "Lunch" --amount 20
```

### List expenses

```powershell
python main.py list
```

### Show the total

```powershell
python main.py summary
```

### Show the total for a month

Use a month number from `1` to `12`:

```powershell
python main.py summary --month 8
```

### Delete an expense

Use the ID shown by the list command:

```powershell
python main.py delete --id 2
```

## Example

```text
$ python main.py add --description "Lunch" --amount 20
Expense added successfully (ID: 1)

$ python main.py add --description "Dinner" --amount 10
Expense added successfully (ID: 2)

$ python main.py list
ID  Date        Description  Amount
1   2026-10-31  Lunch        $20
2   2026-10-31  Dinner       $10

$ python main.py summary
Total expenses: $30

$ python main.py delete --id 2
Expense deleted successfully

$ python main.py summary
Total expenses: $20
```

## Data storage

Expenses are stored in `expenses.json` in the same directory as the program. The file is created when the first expense is added.

This project is intentionally kept small. The main goal is to practise building a usable backend-style command-line program before moving on to larger applications and databases.
