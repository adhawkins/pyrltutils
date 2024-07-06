import click
import os
import shutil
import filecmp

from RLTDatabase import RLTDatabase

@click.command()
@click.option("--dest", help="Directory to contain driver anthems", required=True)
@click.option("--src", help="Directory containing source anthems", required=True)
@click.pass_context
def makeAnthems(ctx, dest, src):
    database = ctx.obj["DATABASE"]
    debug = ctx.obj["DEBUG"]

    print(f"Database: '{database}', src: '{src}', dest: '{dest}'")

    rltDB = RLTDatabase(database)

    drivers = rltDB.getDrivers()
    for driver in drivers:
        nationality = driver['nationalities']
        if (nationality):
            sourceFile = os.path.join(src, nationality['Name'] + '.mp3')
            if os.path.isfile(sourceFile):
                destFile = os.path.join(dest, driver['Name'] + ".mp3")

                if not os.path.isfile(destFile) or not filecmp.cmp(sourceFile, destFile, shallow=False):
                    print(f"Copying '{sourceFile}' to '{destFile}'")
                    shutil.copyfile(sourceFile, destFile)
            else:
                print(f"'{driver}' - '{sourceFile}' doesn't exist")
        else:
            print(f"Couldn't find nationality for '{driver['Name']}'")
