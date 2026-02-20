
import csv
import random
from pathlib import Path

from person import Person


class PersonFactory:
    """Reads data files and creates new Person instances using the data """

    def __init__(self):
        """Initialize all data structures. Data files are read from the current directory."""
        self._data_dir = Path(".")
        self._life_expectancy = {}
        # (decade, gender) -> [(name, cumulative_prob)]
        self._first_names = {} 
        # last names by decade and rank
        self._last_names_by_decade = {}  
        self._rank_probabilities = []
        # birth and marriage rates by decade
        self._birth_marriage_rates = {}  
        self._files_loaded = False

    def read_files(self):
        """Read all data files from the current directory."""
        self._read_life_expectancy()
        self._read_first_names()
        self._read_last_names()
        self._read_rank_probability()
        self._read_birth_marriage_rates()
        self._files_loaded = True

    def _read_life_expectancy(self):
        """Read life_expectancy.csv"""
        with open(self._data_dir / "life_expectancy.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                year = int(row["Year"])
                expectancy = float(row["Period life expectancy at birth"])
                self._life_expectancy[year] = expectancy

    def _read_first_names(self):
        """Read first_names.csv"""
        with open(self._data_dir / "first_names.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row["decade"]
                gender = row["gender"]
                name = row["name"]
                freq = float(row["frequency"])
                key = (decade, gender)
                if key not in self._first_names:
                    self._first_names[key] = []
                self._first_names[key].append((name, freq))
        # Code from ChatGPT
        for key in self._first_names:
            names = self._first_names[key]
            total = sum(p for _, p in names)
            cumul = 0
            new_list = []
            for name, prob in names:
                cumul += prob / total
                new_list.append((name, cumul))
            self._first_names[key] = new_list
        ## End of ChatGPT code

    def _read_last_names(self):
        """Read last_names.csv"""
        with open(self._data_dir / "last_names.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row["Decade"]
                rank = int(row["Rank"])
                lastname = row["LastName"]
                if decade not in self._last_names_by_decade:
                    self._last_names_by_decade[decade] = {}
                self._last_names_by_decade[decade][rank] = lastname

    def _read_rank_probability(self):
        """Read rank_to_probability.csv"""
        with open(self._data_dir / "rank_to_probability.csv", newline="") as f:
            line = f.read().strip()
            probs = [float(x) for x in line.split(",")]
            total = sum(probs)
            self._rank_probabilities = [p / total for p in probs]

    def _read_birth_marriage_rates(self):
        """Read birth_and_marriage_rates.csv."""
        with open(self._data_dir / "birth_and_marriage_rates.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                decade = row["decade"]
                self._birth_marriage_rates[decade] = {
                    "birth_rate": float(row["birth_rate"]),
                    "marriage_rate": float(row["marriage_rate"]),
                }

    def _get_decade(self, year):
        """Return decade string for a given year"""
        decade_year = (year // 10) * 10
        return f"{decade_year}s"

    def _pick_gender(self):
        """Pick gender randomly for first name selection."""
        return random.choice(["male", "female"])

    def _pick_first_name(self, year_born, gender):
        """Pick first name based on decade, gender, and frequency"""
        decade = self._get_decade(year_born)
        key = (decade, gender)
        if key not in self._first_names or not self._first_names[key]:
            return "Unknown"
        names = self._first_names[key]
        r = random.random()
        for name, cumul in names:
            if r <= cumul:
                return name
        return names[-1][0]

    def _pick_last_name_for_descendant(self):
        """Pick last name for direct descendant"""
        return random.choice(["Jones", "Smith"])

    def _pick_last_name_from_file(self, year_born):
        """Pick last name for non-descendant using rank_to_probability."""
        decade = self._get_decade(year_born)
        last_names = self._last_names_by_decade[decade]
        rank_probs = self._rank_probabilities
        rank = random.choices(
            range(1, len(rank_probs) + 1), weights=rank_probs, k=1
        )[0]
        return last_names[rank]

    def _get_life_expectancy(self, year_born):
        """Get life expectancy for birth year"""
        return self._life_expectancy[year_born]

    def compute_year_died(self, year_born):
        """Compute year died based on life expectancy"""
        if not self._files_loaded:
            self.read_files()
        expectancy = self._get_life_expectancy(year_born)
        offset = random.uniform(-10, 10)
        years_lived = expectancy + offset
        return year_born + int(round(years_lived))

    def get_person(self, year_born, is_direct_descendant=False):
        """Create a new Person"""
        if not self._files_loaded:
            self.read_files()

        gender = self._pick_gender()
        first_name = self._pick_first_name(year_born, gender)

        if is_direct_descendant:
            last_name = self._pick_last_name_for_descendant()
        else:
            last_name = self._pick_last_name_from_file(year_born)

        year_died = self.compute_year_died(year_born)

        return Person(
            year_born=year_born,
            first_name=first_name,
            last_name=last_name,
            year_died=year_died,
            is_direct_descendant=is_direct_descendant,
        )

    def get_marriage_rate(self, year_born):
        """Return marriage rate"""
        decade = self._get_decade(year_born)
        return self._birth_marriage_rates[decade]["marriage_rate"]

    def get_num_children(self, year_born):
        """Return number of children for a person based on birth rate."""
        decade = self._get_decade(year_born)
        birth_rate = self._birth_marriage_rates[decade]["birth_rate"]
        base = birth_rate + random.uniform(-1.5, 1.5)
        num = max(0, int(round(base)))
        return num
