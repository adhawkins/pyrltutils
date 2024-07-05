import click
import os
import shutil
import filecmp

from RLTDatabase import RLTDatabase


def findNationality(nationalities, nationalityID):
    return next((item for item in nationalities if item["Id"] == nationalityID), None)


@click.command()
@click.option("--dest", help="Directory to contain driver anthems", required=True)
@click.option("--src", help="Directory containing source anthems", required=True)
@click.pass_context
def makeAnthems(ctx, dest, src):
    database = ctx.obj["DATABASE"]
    debug = ctx.obj["DEBUG"]

    print(f"Database: '{database}', src: '{src}', dest: '{dest}'")

    rltDB = RLTDatabase(database)
    nationalities = rltDB.getNationalities()
    anthems = {}

    drivers = rltDB.getDrivers()
    for driver in drivers:
        nationality = findNationality(nationalities, driver["NationId"])
        if (nationality):
            anthems[driver['Name']] = nationality['Name']
        else:
            print(f"Couldn't find nationality for '{driver['Name']}'")

    for driver, country in anthems.items():
        sourceFile = os.path.join(src, country + '.mp3')
        if os.path.isfile(sourceFile):
            destFile = os.path.join(dest, driver + ".mp3")

            if not os.path.isfile(destFile) or not filecmp.cmp(sourceFile, destFile, shallow=False):
                print(f"Copying '{sourceFile}' to '{destFile}'")
                shutil.copyfile(sourceFile, destFile)

        else:
            print(f"'{driver}' - '{sourceFile}' doesn't exist")
