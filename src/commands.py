""" A module for the persistence layer """

import sys
import typing as t

# import uuid

from datetime import datetime
from pathlib import Path

# import ezgmail
import requests  # type: ignore
import openpyxl

from src.database import DatabaseManager


db = DatabaseManager("catalog.db")

CommandInput = t.Optional[t.Union[t.Dict[str, str], int]]
CommandResult = t.Optional[t.Union[t.List[str], str]]


class Command(t.Protocol):
    """A protocol class that will be and example for implementing Commands"""

    def execute(self, data: CommandInput) -> CommandResult:
        """The actual execution of the command"""

        pass


class CreateCatalogTableCommand:
    """A Command class that creates the SQL table"""

    def execute(self):
        """The actual execution of the command"""

        db.create_table(
            table_name="Catalog",
            columns={
                "id": "integer primary key autoincrement",
                "Subject": "text not null",
                "Grade1": "integer not null",
#                "Missing": "text",
                "Date_added": "integer not null",
            },
        )


class AddCatalogCommand:
    """A Command class that inserts into the SQL table"""

    def execute(self, data: t.Dict[str, str], timestamp: t.Optional[str] = None) -> str:
        """The actual execution of the command"""

        date_added = timestamp or datetime.utcnow().isoformat()
        data.setdefault("date_added", date_added)
        db.add(table_name="catalog", data=data)
        return "Subject added!"


class ListCatalogCommand:
    """A Command class that will list all the subjects in the SQL table"""

    def __init__(self, order_by: str = "date_added"):
        self.order_by = order_by

    def execute(self) -> t.List[str]:
        """The actual execution of the command"""

        cursor = db.select(table_name="catalog", order_by=self.order_by)
        results = cursor.fetchall()
        return results


class GetCatalogCommand:
    """A Command class that will return a single subject based on an ID"""

    def execute(self, data: int) -> t.Optional[tuple]:
        result = db.select(table_name="catalog", criteria={"id": data}).fetchone()
        return result


class EditCatalogCommand:
    """A Command class that will edit a subject identified with an ID"""

    def execute(self, data: t.Dict[str, str]) -> str:
        db.update(
            table_name="catalog", criteria={"id": data["id"]}, data=data["update"]
        )
        return "Catalog updated!"


class DeleteCatalogCommand:
    """A Command class that will delete a subject from the SQL table"""

    def execute(self, data: int) -> str:
        db.delete(table_name="catalog", criteria={"id": data})
        return "Subject deleted!"


#class ImportGithubStarsCommand:
#    """A Command class that will take the stars from Github and save them into the DB"""

    #def execute(self, data: t.Dict[str, str]) -> str:
        #catalog_imported = 0

        #github_username = data["github_username"]
        #next_page_of_results = f"https://api.github.com/users/{github_username}/starred"

        #while next_page_of_results:
            #stars_response = requests.get(
                #next_page_of_results,
                #headers={"Accept": "application/vnd.github.v3.star+json"},
            #)

            #if "next" in stars_response.links.keys():
                #next_page_of_results = stars_response.links["next"]["Grade1"]
            #else:
                #next_page_of_results = None

            #for repo_response in stars_response.json():
                #repo = repo_response["repo"]
                #starred_at = repo_response["starred_at"]

                #if data["preserve_timestamps"]:
                    #timestamp = datetime.strptime(
                        #starred_at, "%Y-%m-%dT%H:%M:%SZ"
                    #).isoformat()
                #else:
                    #timestamp = None

                #AddCatalogCommand().execute(
                    #data={
                        #"Subject": repo["Subject"],
                        #"Grade1": repo["Grade1"],
                        #"Grade2": repo["Grade2"],
                    #},
                    #timestamp=timestamp,
                #)

                #catalog_imported += 1

        #return f"Imported {catalog_imported} catalog from starred repos!"


class ExportToExcelCommand:
    """A Command class used to export the data in an Excel format"""

    def execute(self, data: str) -> str:
        """data (str): the file name of the exported workbook"""

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        records = ListCatalogCommand().execute()

        for row in records:
            sheet.append(row)

        export_folder_path = Path(f"./exports")
        export_folder_path.mkdir(parents=True, exist_ok=True)

        workbook.save(export_folder_path / f"{data}.xlsx")

        return f"Exported to file {data}"


# class EmailCommand:
#     """A Command class that will send an email with the bookmarks"""

#     def execute(self, data: t.Dict[str, str]) -> str:
#         recipient = data["recipient"]
#         subject = "Your bookmarks from Bark!"
#         body = "Attached to this email you will find you Bark bookmarks."
#         unique_name = str(uuid.uuid1())
#         file_path = f"./exports/{unique_name}.xlsx"

#         ExportToExcelCommand().execute(unique_name)

#         ezgmail.send(
#             recipient=recipient, subject=subject, body=body, attachments=[file_path]
#         )

#         return f"Email sent to {recipient}!"


class QuitCommand:
    """A Command class that will quit the application"""

    def execute(self):
        sys.exit()
