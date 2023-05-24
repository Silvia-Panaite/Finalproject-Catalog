""" A module for the presentation layer """

import os
import typing as t

from src.commands import Command


class Option:
    def __init__(
        self, name: str, command: Command, prep_call: t.Optional[t.Callable] = None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        result = self.command.execute(data) if data else self.command.execute()
        if isinstance(result, list):
            for line in result:
                print(line)
        else:
            print(result)

    def __str__(self):
        return self.name


def print_options(options: t.Dict[str, Option]) -> None:
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")
    print()


def option_choice_is_valid(choice: str, options: t.Dict[str, Option]) -> bool:
    result = choice in options or choice.upper() in options
    return result


def get_option_choice(options: t.Dict[str, Option]) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_user_input(label: str, required: bool = True) -> t.Optional[str]:
    value = input(f"{label}: ") or None
    while required and not value:
        value = input(f"{label}: ") or None
    return value


def get_new_catalog_data() -> t.Dict[str, t.Optional[str]]:
    result = {
        "Subject": get_user_input("Subject"),
        "Grade1": get_user_input("Grade1"),
        "Date_added": get_user_input("Date_added", required=False),
    }

    return result


def get_catalog_id() -> int:
    result = int(get_user_input("Enter a subject ID"))  # type: ignore
    return result


def get_update_catalog_data() -> t.Dict[str, t.Union[int, t.Dict[str, str]]]:
    subject_id = int(get_user_input("Enter a subject ID to edit"))
    field = get_user_input("Choose a value to edit (subject, grade1, date_added)")
    new_value = get_user_input(f"Enter a new value for {field}")
    return {"id": subject_id, "update": {field: new_value}}


#def get_github_import_options() -> t.Dict[str, t.Union[str, bool]]:
#       github_username = get_user_input("Please input the Github username")
#       preserve_timestamps = get_user_input("Preserve timestamps? [Y/n]")

#   if preserve_timestamps in ["Y", "y", ""]:
#        preserve_timestamps = True
#    else:
#        preserve_timestamps = False

#    return {
#       "github_username": github_username,
#       "preserve_timestamps": preserve_timestamps,
#    }


def get_file_name() -> str:
    file_name = get_user_input(
        "Please type in the name of the Excel file where you want to save"
    )
    return file_name


# def get_email() -> t.Dict[str, str]:
#     recipient = get_user_input("Enter an email")
#     return {"recipient": recipient}


def clear_screen():
    clear_command = "cls" if os.name == "nt" else "clear"
    os.system(clear_command)
