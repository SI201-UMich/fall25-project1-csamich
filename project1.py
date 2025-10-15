# SI 201 Project 1
# Your name: Corey Armstrong
# Your student id: 72387457
# Your email: coreyarm@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.  
# I used chatGPT to help debug and suggest the general structure of the code.

import csv
import os
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
    Calculates the average bill length of each species.
    Example output:
    {'Adelie': 38.5, 'Gentoo': 47.2, 'Chinstrap': 48.8}
    """
    species_set = set(p["species"] for p in penguins)
    averages = {}
    for s in species_set:
        bills = get_species_bills(penguins, s)
        if bills:
            averages[s] = sum(bills) / len(bills)
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

def run_tests():
    print("\nRunning tests...")

    sample_penguins = [
        {"species": "Adelie", "island": "Torgersen", "bill_length_mm": 40.0},
        {"species": "Adelie", "island": "Torgersen", "bill_length_mm": 38.0},
        {"species": "Gentoo", "island": "Biscoe", "bill_length_mm": 47.0},
        {"species": "Chinstrap", "island": "Dream", "bill_length_mm": 48.0},
    ]

    # ----------------- get_island_species -----------------
    assert get_island_species(sample_penguins, "Torgersen") == {"Adelie": 2}, "General Case 1 failed"
    assert get_island_species(sample_penguins, "Biscoe") == {"Gentoo": 1}, "General Case 2 failed"
    assert get_island_species([], "Torgersen") == {}, "Edge Case 1 failed (empty list)"
    assert get_island_species(sample_penguins, "Nonexistent") == {}, "Edge Case 2 failed (unknown island)"

    # ----------------- islands_proportions -----------------
    props = islands_proportions(sample_penguins)
    assert round(props["Torgersen"]["Adelie"], 2) == 1.00, "General Case 1 failed"
    assert round(props["Biscoe"]["Gentoo"], 2) == 1.00, "General Case 2 failed"
    assert islands_proportions([]) == {}, "Edge Case 1 failed (empty)"
    # If an island exists but has no penguins (impossible in this test), it should still give empty dict
    empty_penguins = [{"species": "Adelie", "island": "Torgersen", "bill_length_mm": 40.0}]
    assert "Dream" not in islands_proportions(empty_penguins), "Edge Case 2 failed"

    # ----------------- get_species_bills -----------------
    assert get_species_bills(sample_penguins, "Adelie") == [40.0, 38.0], "General Case 1 failed"
    assert get_species_bills(sample_penguins, "Gentoo") == [47.0], "General Case 2 failed"
    assert get_species_bills(sample_penguins, "Nonexistent") == [], "Edge Case 1 failed"
    bad_data = sample_penguins + [{"species": "Adelie", "island": "Torgersen", "bill_length_mm": None}]
    assert get_species_bills(bad_data, "Adelie") == [40.0, 38.0], "Edge Case 2 failed (None value)"

    # ----------------- average_bill_length -----------------
    avg = average_bill_length(sample_penguins)
    assert round(avg["Adelie"], 2) == 39.00, "General Case 1 failed"
    assert round(avg["Gentoo"], 2) == 47.00, "General Case 2 failed"
    assert average_bill_length([]) == {}, "Edge Case 1 failed (empty)"
    assert average_bill_length([{"species": "Adelie", "island": "Torgersen", "bill_length_mm": None}])["Adelie"] == 0, "Edge Case 2 failed (None value)"

    # ----------------- generate_report -----------------
    # Just ensure it runs without error and creates a file
    test_props = {"Torgersen": {"Adelie": 1.0}}
    test_avgs = {"Adelie": 39.0}
    generate_report(test_props, test_avgs, filename="test_penguin_report.txt")
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, "test_penguin_report.txt")
    assert os.path.exists(full_path), "Report file not created"

    print("All tests passed!")

def main():
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
