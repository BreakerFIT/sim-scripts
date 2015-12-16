#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2
import shutil

ec_name = "ECorp"
ec_prefix = "ec"
ec_gauntlet_url = "https://docs.google.com/spreadsheets/d/1c5BksB7eOOZNbuzRPh21s-UArlkfMIqKP4PHU9qtzOg/export?format=tsv&id=1c5BksB7eOOZNbuzRPh21s-UArlkfMIqKP4PHU9qtzOg&gid=976537027"
ec_inventory_url = "https://docs.google.com/spreadsheets/d/1c5BksB7eOOZNbuzRPh21s-UArlkfMIqKP4PHU9qtzOg/export?format=tsv&id=1c5BksB7eOOZNbuzRPh21s-UArlkfMIqKP4PHU9qtzOg&gid=1298258913"

fs_name = "FSociety"
fs_prefix = "fs"
fs_gauntlet_url = "https://docs.google.com/spreadsheets/d/1zY77bNRRPom9fTLcgFZKmaiAZJYI_8s_LIjbyUXJ2N4/export?format=tsv&id=1zY77bNRRPom9fTLcgFZKmaiAZJYI_8s_LIjbyUXJ2N4&gid=1439836959"
fs_inventory_url = "https://docs.google.com/spreadsheets/d/1zY77bNRRPom9fTLcgFZKmaiAZJYI_8s_LIjbyUXJ2N4/export?format=tsv&id=1zY77bNRRPom9fTLcgFZKmaiAZJYI_8s_LIjbyUXJ2N4&gid=727162174"


def fetch_guild(name, prefix, gauntlet_url, inventory_url):
    gauntlet_filename = "data/" + name + "_gauntlets.txt"

    print "Downloading " + name + " gauntlets into " + gauntlet_filename


    gauntlets = urllib2.urlopen(gauntlet_url)
    gauntlet_file = open(gauntlet_filename, "w")
    for line in gauntlets:
        line = re.sub(r'[\r\n]+', '\n', line)
        gauntlet_file.write(line)

    gauntlet_file.write("\n")
    gauntlet_file.close()

    inventories = urllib2.urlopen(inventory_url)

    generic_prefix = prefix + "_"
    atk_prefix = prefix + "a_"
    def_prefix = prefix + "d_"


    print "Writing " + name + " inventories."
    for line in inventories:
        if line.startswith('//'):
            continue

        (name, inv) = line.split(": ", 1)
        inv_array = inv.split(", ")
        inv_array = [re.sub(" [x×]", " #", item) for item in inv_array]

        name_atk = name.replace(generic_prefix, atk_prefix)
        name_def = name.replace(generic_prefix, def_prefix)

        out_atk = open("data/" + name_atk + ".txt", "w")
        out_atk.write("\n".join(inv_array))
        out_atk.flush()
        out_atk.close()

        out_def = open("data/" + name_def + ".txt", "w")
        out_def.write("\n".join(inv_array))
        out_def.flush()
        out_def.close()

    inventories.close()

def merge_gauntlets(marker, guild1, guild2):
    customdecks_file = open("data/customdecks.txt", "r")
    first_time = (customdecks_file.read().find(marker) == -1)

    if first_time:
        print "Moving data/customdecks.txt to data/customdecks_extras.txt, please edit the extras file from now on to add extra decks."
        shutil.copy2("data/customdecks.txt", "data/customdecks_extras.txt")

    customdecks_file.close()

    gauntlet1_filename = "data/" + guild1 + "_gauntlets.txt"
    gauntlet2_filename = "data/" + guild2 + "_gauntlets.txt"

    customdecks_file = open("data/customdecks.txt", "w")
    extras_file = open("data/customdecks_extras.txt", "r")
    gauntlet1_file = open(gauntlet1_filename, "r")
    gauntlet2_file = open(gauntlet2_filename, "r")

    print "Merging " + guild1 + " and " + guild2 + " gauntlets into data/customdecks.txt"
    shutil.copyfileobj(extras_file, customdecks_file)
    shutil.copyfileobj(gauntlet1_file, customdecks_file)
    shutil.copyfileobj(gauntlet2_file, customdecks_file)

    customdecks_file.close()

fetch_guild(ec_name, ec_prefix, ec_gauntlet_url, ec_inventory_url)
fetch_guild(fs_name, fs_prefix, fs_gauntlet_url, fs_inventory_url)
merge_gauntlets("ECDef", ec_name, fs_name)


