import click
import os
import shutil
import filecmp
import requests

from PIL import Image

from RLTDatabase import RLTDatabase

def findCountryCode(countries, country):
    return list(countries.keys())[list(countries.values()).index(country)]

@click.command()
@click.option("--dest", help="Directory to contain driver anthems", required=True)
@click.option("--src", help="Directory containing source anthems", required=True)
@click.pass_context
def makeAnthems(ctx, dest, src):
    database = ctx.obj["DATABASE"]
    debug = ctx.obj["DEBUG"]

    print(f"Database: '{database}', src: '{src}', dest: '{dest}'")

    countries = requests.get("https://flagcdn.com/en/codes.json").json()

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
                print(f"'{driver['Name']}' - '{sourceFile}' doesn't exist")

            destFile = os.path.join(dest, driver['Name'] + ".png")
            if not os.path.isfile(destFile):
                country = nationality['Name']
                if country=="United States Of America":
                    country="United States"

                print(f"Downloading flag for '{country}' to '{destFile}'")

                url = f"https://flagcdn.com/h240/{findCountryCode(countries, country)}.png"

                srcImage = Image.open(requests.get(url, stream=True).raw)

                destImage = Image.new("RGB", size=[srcImage.width+20, srcImage.height+20], color="white")
                destImage.paste(srcImage, (10,10,srcImage.width+10,srcImage.height+10))
                destImage.save(destFile, "PNG")
                print(f"'{destFile}' - {destImage.width} x {destImage.height}")
        else:
            print(f"Couldn't find nationality for '{driver['Name']}'")
