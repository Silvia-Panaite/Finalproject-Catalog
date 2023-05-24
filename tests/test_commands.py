from unittest import TestCase
from unittest.mock import patch, Mock

from src.commands import CreateCatalogTableCommand, AddCatalogCommand, ImportGithubStarsCommand


class CreateCatalogTableCommandTest(TestCase):
    def setUp(self):
        self.command = CreateCatalogTableCommand()

    def test_execute(self):
        with patch("src.commands.DatabaseManager.create_table") as mocked_create_table:
            self.command.execute()
            mocked_create_table.assert_called_with(
                table_name="catalog",
                columns={
                    "id": "integer primary key autoincrement",
                    "Subject": "text not null",
                    "Grade1": "integer not null",
                    "Missing": "text",
                    "Grade2": "integer not null",
                }
            )


class AddCatalogCommandTest(TestCase):
    def setUp(self):
        self.command = AddCatalogCommand()

    def test_execute(self):
        with patch("src.commands.DatabaseManager.add") as mocked_add_catalog:
            data = {
                "Subject": "mock_subject",
                "Grade1": "mock_grade1",
                "Grade2": "mock_grade2"
            }
            result = self.command.execute(data)
            mocked_add_catalog.assert_called_with(
                table_name="catalog",
                data=data
            )
            
            self.assertEqual(result, "Subject added!")


class ImportGithubStarsCommandTest(TestCase):
    def setUp(self):
        self.command = ImportGithubStarsCommand()
        self.data = {
            "github_username": "username_foo",
            "preserve_timestamps": True
        }

    def test_execute(self):
        with patch("src.commands.requests.get") as mocked_get:
            mocked_response = Mock()
            mocked_response.links = {}
            mocked_response.json.return_value = [
                {
                    "starred_at": "2000-01-01T00:00:00Z",
                    "repo": {
                        "subject": "subject_foo",
                        "grade1": "grade1_foo",
                        "grade2": "grade2_foo"
                    }
                }
            ]
            
            mocked_get.return_value = mocked_response
            
            with patch("src.commands.AddCatalogCommand.execute") as mocked_add_catalog:
                mocked_add_catalog.return_value = "Subject added!"
                
                self.command.execute(self.data)
                
                mocked_get.assert_called_with(
                    f"https://api.github.com/users/{self.data['github_username']}/starred",
                    headers = {
                        "Accept": "application/vnd.github.v3.star+json"
                    }
                )
                
                mocked_add_catalog.assert_called_with(
                    data = {
                        "Subject": "subject_foo",
                        "Grade1": "grade1_foo",
                        "Grade2": "grade2_foo"
                    },
                    timestamp="2000-01-01T00:00:00"
                )