from argparse import ArgumentParser, RawDescriptionHelpFormatter
import json
from datetime import date

parser = ArgumentParser(
    prog="expense-tracker",
    description="Track and manage your expenses from the command line.",
    epilog=(
        "Examples:\n"
        "  expense-tracker add --description Lunch --amount 20\n"
        "  expense-tracker list\n"
        "  expense-tracker summary --month 8\n"
        "  expense-tracker delete --id 2"
    ),
    formatter_class=RawDescriptionHelpFormatter,
)
commands = parser.add_subparsers(
    dest="command",
    required=True,
    title="commands",
    description="Choose an operation to perform",
)

add_parser = commands.add_parser(
    "add",
    help="Add a new expense",
    description="Add an expense with a description and amount.",
)
add_parser.add_argument(
    "--description",
    required=True,
    help="Description of the expense, such as 'Lunch'",
)
add_parser.add_argument(
    "--amount",
    required=True,
    type=int,
    help="Amount spent",
)

list_parser = commands.add_parser(
    "list",
    help="List all saved expenses",
    description="Display every saved expense.",
)

summary_parser = commands.add_parser(
    "summary",
    help="Show the total amount spent",
    description="Calculate the total expenses, optionally for a specific month.",
)
summary_parser.add_argument(
    "--month",
    type=int,
    choices=range(1, 13),
    metavar="MONTH",
    help="Show expenses for a month from 1 to 12",
)

delete_parser = commands.add_parser(
    "delete",
    help="Delete an expense by ID",
    description="Remove one saved expense using its ID.",
)
delete_parser.add_argument(
    "--id",
    required=True,
    type=int,
    metavar="ID",
    help="ID of the expense to delete",
)

args = parser.parse_args()

if args.command == 'add':
    try:
        with open('expenses.json', 'r', encoding='utf-8') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        expenses = []

    new_expense = {
        'id': len(expenses) + 1,
        'date': date.today().strftime('%Y-%m-%d'),
        'description': args.description,
        'amount': args.amount
    }

    expenses.append(new_expense)

    with open('expenses.json', 'w', encoding='utf-8') as file:
        json.dump(expenses, file, indent=2)

elif args.command == 'list':
    try:
        with open('expenses.json', 'r', encoding='utf-8') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        parser.error('File not found.')

    print("ID\tDate\t\tDescription\tAmount")

    for expense in expenses:
        print(f"{expense['id']}\t{expense['date']}\t{expense['description']}\t${expense['amount']}")

elif args.command == 'summary':
    try:
        with open('expenses.json', 'r', encoding='utf-8') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        parser.error('File not found.')

    total = 0
    if args.month is not None:
        expenses = [
            expense
            for expense in expenses 
            if int(expense['date'][5:7]) == args.month
        ]

    total = sum(expense['amount'] for expense in expenses)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'Decemeber']

    if args.month is not None:
        print(f"Total expenses for month {months[args.month - 1]}: ${total}")
    else:
        print(f"Total expense: ${total}")

elif args.command == 'delete':
    try:
        with open('expenses.json', 'r', encoding='utf-8') as file:
            expenses = json.load(file)
    except FileNotFoundError:
        parser.error('File not found')

    original_count = len(expenses)

    expenses = [expense for expense in expenses if expense['id'] != args.id]

    if original_count == len(expenses):
        parser.error(f"Expense with id {args.id} not found.")
    else:
        with open('expenses.json', 'w', encoding='utf-8') as file:
            json.dump(expenses, file, indent=2)
        print(f"Expense with id {args.id} deleted.")