import sys
import random
import os


def random_fact():
    source_path = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.abspath(".")
    file_path = os.path.join(source_path, "FACT.txt")
    with open(file_path, encoding="utf-8") as file:
        facts = file.readlines()
    return random.choice(facts).strip()
