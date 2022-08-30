#!/usr/bin/env python3

import csv
from random import randint, shuffle

def populate_students():
    students = []

    with open("students.csv", "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)

        for i in students:
            i["student number"] = int(i["student number"])

    return students


def populate_places():
    places = []

    with open("places.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            places.append(row)

    for i in places:
        i["spots"] = int(i["spots"])

    return places


def filter_prefs(master_list, preference):
    preferenced = []
    non_preferenced = []
    for i in master_list:
        if i["preference"] == preference:
            preferenced.append(i)
        else:
            non_preferenced.append(i)

    return preferenced, non_preferenced


def filter_rural_placements(master_list):
    rural_placements = []
    non_rural_placements = []

    for i in master_list:
        if i["rural"] == "true":
            rural_placements.append(i)
        else:
            non_rural_placements.append(i)

    return rural_placements, non_rural_placements


def write_to_file(final_list):
    with open("final.csv", "w") as f:
        fieldnames = ["name", "student number", "placement"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in final_list:
            writer.writerow(i)


def main():
    placed_students = []

    students = populate_students()
    places = populate_places()

    rural_stu, nonrural_stu = filter_prefs(students, "true")
    rural_plc, nonrural_plc = filter_rural_placements(places)

    # Check we have filled out the numbers properly
    num_places = 0
    for i in rural_plc:
        num_places += i["spots"]

    if num_places > len(rural_stu):
        print("Not enough rural volunteers, conscripting...")
        while len(rural_stu) < num_places:
            s = randint(0, (len(nonrural_stu) - 1))
            rural_stu.append(nonrural_stu.pop(s))
    elif num_places < len(rural_stu):
        print("Too many volunteers for rural! Culling...")
        while num_places < len(rural_stu):
            if len(rural_stu) == 0:
                break
            s = randint(0, (len(rural_stu) - 1))
            nonrural_stu.append(rural_stu.pop(s))


    # Shuffle lists
    print("Randomising places and students...")
    shuffle(rural_stu)
    shuffle(nonrural_stu)
    shuffle(rural_plc)
    shuffle(nonrural_plc)

    # Allocate rural places
    print("Allocating rural students...")
    while len(rural_plc) > 0:
        s = randint(0, (len(rural_plc) - 1))
        place = rural_plc.pop(s)
        while place["spots"] > 0:
            n = randint(0, (len(rural_stu) - 1))
            placing = rural_stu.pop(n)
            newstudent = {
                "name": placing["name"],
                "student number": placing["student number"],
                "placement": place["place"]
                }
            placed_students.append(newstudent)
            place["spots"] -= 1

    # Allocate nonrural places
    print("Allocating nonrural students...")
    while len(nonrural_plc) > 0:
        s = randint(0, (len(nonrural_plc) - 1))
        place = nonrural_plc.pop(s)
        while place["spots"] > 0:
            n = randint(0, (len(nonrural_stu) - 1))
            placing = nonrural_stu.pop(n)
            newstudent = {
                "name": placing["name"],
                "student number": placing["student number"],
                "placement": place["place"]
                }
            placed_students.append(newstudent)
            place["spots"] -= 1

    write_to_file(placed_students)


if __name__ == "__main__":
    main()
else:
    print("Do not import these methods.")
