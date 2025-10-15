# SI 201 Project 1
# Your name: Corey Armstrong
# Your student id: 72387457
# Your email: coreyarm@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# I used chatGPT to help debug and suggest the general structure of the code.

import csv
import os
import unittest
from collections import defaultdict

def load_penguins(csv_file):
    """
    Reads the CSV file and transforms data into a list of dictionaries.
    Each dictionary contains: species, island, bill_length_mm.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, csv_file)
    penguins = []
    with open(full_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                bill_length = float(row["bill_length_mm"])
            except (ValueError, TypeError):
                bill_length = None
            penguins.append({
                "species": row["species"],
                "island": row["island"],
                "bill_length_mm": bill_length
            })
    return penguins



def get_island_species(penguins, island):
    """
    Returns a dictionary with species counts for a given island.
    Example: {'Adelie': 10, 'Gentoo': 5, ...}
    """
    island_totals = defaultdict(int)
    for p in penguins:
        if p["island"] == island:
            island_totals[p["species"]] += 1
    return dict(island_totals)


def islands_proportions(penguins):
    """
    Calculates the proportion of each species on each island.
    Example output:
    {
      'Torgersen': {'Adelie': 0.6, 'Gentoo': 0.4},
      'Biscoe': {'Chinstrap': 0.2, 'Gentoo': 0.8}
    }
    """
    # Determine all islands
    islands = set(p["island"] for p in penguins)
    proportions = {}

    for island in islands:
        species_counts = get_island_species(penguins, island)
        total_count = sum(species_counts.values())
        if total_count > 0:
            proportions[island] = {species: count / total_count
                                   for species, count in species_counts.items()}
        else:
            proportions[island] = {}
    return proportions


def get_species_bills(penguins, species):
    """
    Returns a list of bill lengths for a given species.
    """
    bills = [p["bill_length_mm"] for p in penguins
             if p["species"] == species and p["bill_length_mm"] is not None]
    return bills


def average_bill_length(penguins):
    """
    Calculates the average bill length of each species,
    handling NA or invalid bill length values gracefully.
    """
    species_set = set(p["species"] for p in penguins)
    averages = {}

    for s in species_set:
        valid_bills = []
        for p in penguins:
            if p["species"] == s:
                val = p["bill_length_mm"]
                # Filter out None, 'NA', or other invalid values
                if isinstance(val, (int, float)):
                    valid_bills.append(val)
                else:
                    # Try to parse if it's a numeric string
                    try:
                        valid_bills.append(float(val))
                    except (ValueError, TypeError):
                        continue

        if valid_bills:
            averages[s] = sum(valid_bills) / len(valid_bills)
        else:
            averages[s] = 0

    return averages

def generate_report(proportions, average_bills, filename="penguin_report.txt"):
    """
    Writes the species proportions per island and average bill lengths per species to a file
    in the same folder as this script.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)

    with open(full_path, "w") as f:
        f.write("Penguin Report\n")
        f.write("=====================\n\n")
        f.write("Species Proportions per Island:\n")
        for island, species_data in proportions.items():
            f.write(f"\nIsland: {island}\n")
            for species, prop in species_data.items():
                f.write(f"  {species}: {prop:.2%}\n")
        
        f.write("\nAverage Bill Length per Species (mm):\n")
        for species, avg in average_bills.items():
            f.write(f"  {species}: {avg:.2f}\n")

    print(f"Report generated and saved to: {full_path}")

class TestPenguinFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # File to be cleaned up after tests
        cls.test_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "test_penguin_report.txt")

    def setUp(self):
        # General sample
        self.sample_penguins = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": 40.0},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": 38.0},
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": 47.0},
            {"species": "Chinstrap", "island": "Dream", "bill_length_mm": 48.0},
        ]

        # Sample with NA
        self.sample_with_na = [
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": "NA"},
            {"species": "Adelie", "island": "Torgersen", "bill_length_mm": None},
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": 47.0},
        ]

        # Sample with string number values
        self.sample_with_str_numbers = [
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": "48.5"},
            {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": 47.5},
        ]

    # ----------------- get_island_species -----------------
    def test_get_island_species_general(self):
        self.assertEqual(get_island_species(self.sample_penguins, "Torgersen"), {"Adelie": 2})
        self.assertEqual(get_island_species(self.sample_penguins, "Biscoe"), {"Gentoo": 1})

    def test_get_island_species_edge(self):
        self.assertEqual(get_island_species([], "Torgersen"), {})
        self.assertEqual(get_island_species(self.sample_penguins, "Nonexistent"), {})

    # ----------------- islands_proportions -----------------
    def test_islands_proportions_general(self):
        props = islands_proportions(self.sample_penguins)
        self.assertAlmostEqual(props["Torgersen"]["Adelie"], 1.0)
        self.assertAlmostEqual(props["Biscoe"]["Gentoo"], 1.0)

    def test_islands_proportions_edge(self):
        self.assertEqual(islands_proportions([]), {})
        self.assertNotIn("Dream", islands_proportions([{"species": "Adelie", "island": "Torgersen", "bill_length_mm": 40.0}]))

    # ----------------- get_species_bills -----------------
    def test_get_species_bills_general(self):
        self.assertEqual(get_species_bills(self.sample_penguins, "Adelie"), [40.0, 38.0])
        self.assertEqual(get_species_bills(self.sample_penguins, "Gentoo"), [47.0])

    def test_get_species_bills_edge(self):
        self.assertEqual(get_species_bills(self.sample_penguins, "Nonexistent"), [])
        bad_data = self.sample_penguins + [{"species": "Adelie", "island": "Torgersen", "bill_length_mm": None}]
        self.assertEqual(get_species_bills(bad_data, "Adelie"), [40.0, 38.0])

    # ----------------- average_bill_length -----------------
    def test_average_bill_length_general(self):
        avg = average_bill_length(self.sample_penguins)
        self.assertAlmostEqual(avg["Adelie"], 39.0)
        self.assertAlmostEqual(avg["Gentoo"], 47.0)

    def test_average_bill_length_edge(self):
        self.assertEqual(average_bill_length([]), {})
        avg = average_bill_length([{"species": "Adelie", "island": "Torgersen", "bill_length_mm": None}])
        self.assertEqual(avg["Adelie"], 0)

    def test_average_bill_length_with_na(self):
        avg = average_bill_length(self.sample_with_na)
        self.assertAlmostEqual(avg["Gentoo"], 47.0)
        self.assertEqual(avg["Adelie"], 0)

    def test_average_bill_length_with_string_numbers(self):
        avg = average_bill_length(self.sample_with_str_numbers)
        # (48.5 + 47.5) / 2 = 48.0
        self.assertAlmostEqual(avg["Gentoo"], 48.0)

    # ----------------- generate_report -----------------
    def test_generate_report_creates_file(self):
        test_props = {"Torgersen": {"Adelie": 1.0}}
        test_avgs = {"Adelie": 39.0}
        generate_report(test_props, test_avgs, filename="test_penguin_report.txt")
        self.assertTrue(os.path.exists(self.test_file))

    @classmethod
    def tearDownClass(cls):
        # Clean up the test file after all tests
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)


def run_tests():
    """
    Runs all unit tests for the penguin analysis functions.
    """
    unittest.main(exit=False)



def main():
    
    run_tests()
    
    # Step 1: Load data
    penguins = load_penguins("penguins.csv")

    # Step 2: Calculate proportions of species per island
    proportions = islands_proportions(penguins)

    # Step 3: Calculate average bill length per species
    average_bills = average_bill_length(penguins)

    # Step 4: Generate report
    generate_report(proportions, average_bills)


if __name__ == "__main__":
    main()
