from src import commands as c
from src import presentation as p


def loop():
    options = {
        "A": p.Option(
            name="Add a subject",
            command=c.AddCatalogCommand(),
            prep_call=p.get_new_catalog_data,
        ),
        "S": p.Option(
            name="Get catalog by ID",
            command=c.GetCatalogCommand(),
            prep_call=p.get_catalog_id,
        ),
        "B": p.Option(name="List subjects by date", command=c.ListCatalogCommand()),
        "T": p.Option(
            name="List catalog by subject",
            command=c.ListCatalogCommand(order_by="subject"),
        ),
        "E": p.Option(
            name="Edit a subject",
            command=c.EditCatalogCommand(),
            prep_call=p.get_update_catalog_data,
        ),
        #"G": p.Option(
        #    name="Import Github stars",
        #    command=c.ImportGithubStarsCommand(),
        #    prep_call=p.get_github_import_options,
        #),
        "D": p.Option(
            name="Delete a subject",
            command=c.DeleteCatalogCommand(),
            prep_call=p.get_catalog_id,
        ),
        "X": p.Option(
            name="Export to Excel",
            command=c.ExportToExcelCommand(),
            prep_call=p.get_file_name,
        ),
        # "M": p.Option(
        #     name="Email the bookmarks", command=c.EmailCommand(), prep_call=p.get_email
        # ),
        "Q": p.Option(name="Quit", command=c.QuitCommand()),
    }

    p.clear_screen()
    p.print_options(options)
    chosen_option = p.get_option_choice(options)
    p.clear_screen()
    chosen_option.choose()

    _ = input("Press ENTER to return to menu")


if __name__ == "__main__":
    c.CreateCatalogTableCommand().execute()
    while True:
        loop()
