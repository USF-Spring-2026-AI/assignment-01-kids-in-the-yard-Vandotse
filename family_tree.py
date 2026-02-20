import random
from collections import defaultdict

from person import Person
from person_factory import PersonFactory


class FamilyTree:
    """class that generates the family tree"""

    MAX_YEAR = 2120

    def __init__(self):
        """Initialize the family tree."""
        self._factory = PersonFactory()
        self._all_people = []
        self._person1 = None
        self._person2 = None

    @property
    def person1(self):
        """Return the first root person"""
        return self._person1

    @property
    def person2(self):
        """Return the second root person"""
        return self._person2

    def generate(self):
        """Generate family tree based on first 2 people"""
        self._factory.read_files()
        self._all_people = []

        self._person1 = Person(
            year_born=1950,
            first_name="Desmond",
            last_name="Jones",
            year_died=self._factory.compute_year_died(1950),
            is_direct_descendant=True,
        )
        self._person2 = Person(
            year_born=1950,
            first_name="Molly",
            last_name="Smith",
            year_died=self._factory.compute_year_died(1950),
            is_direct_descendant=True,
        )
        self._person1.partner = self._person2
        self._person2.partner = self._person1
        self._all_people = [self._person1, self._person2]

        # create a queue, starting with the first two people
        to_process = list(self._all_people)
        processed = set()

        while to_process:
            person = to_process.pop(0)
            if id(person) in processed:
                continue
            processed.add(id(person))
            # stop if person is older than 2120
            if person.year_born >= self.MAX_YEAR:
                continue

            # Add partner based on marriage rate
            if person.partner is None and person not in (self._person1, self._person2):
                if random.random() < self._factory.get_marriage_rate(person.year_born):
                    partner_year = person.year_born + random.randint(-10, 10)
                    # stop if partner is older than 2120
                    if partner_year > self.MAX_YEAR:
                        continue
                    # Married is not a direct descendant
                    partner = self._factory.get_person(
                        partner_year, is_direct_descendant=False
                    )
                    person.partner = partner
                    partner.partner = person
                    self._all_people.append(partner)
                    to_process.append(partner)

            # Determine number of children
            has_partner = person.partner is not None
            num_children = self._factory.get_num_children(person.year_born)

            # Only one parent has children
            if has_partner and person.partner in self._all_people:
                elder = (
                    person
                    if person.year_born <= person.partner.year_born
                    else person.partner
                )
                if person is not elder:
                    num_children = 0

            if num_children <= 0:
                continue

            elder_year = person.year_born
            if has_partner and person.partner.year_born < person.year_born:
                elder_year = person.partner.year_born
            start_year = elder_year + 25
            end_year = elder_year + 45

            if num_children == 1:
                birth_years = [random.randint(start_year, end_year)]
            else:
                step = (end_year - start_year) / (num_children - 1)
                birth_years = [
                    start_year + int(round(i * step)) for i in range(num_children)
                ]
                birth_years = [max(start_year, min(end_year, y)) for y in birth_years]
            # Child born is a direct descendant
            for birth_year in birth_years:
                if birth_year > self.MAX_YEAR:
                    continue
                child = self._factory.get_person(
                    birth_year, is_direct_descendant=True
                )
                person.add_child(child)
                if has_partner:
                    person.partner.add_child(child)
                self._all_people.append(child)
                # add every child to queue
                to_process.append(child)

    def get_total_count(self):
        """Return all people in the tree"""
        return len(self._all_people)

    def get_count_by_decade(self):
        """Separate people by decade"""
        by_decade = defaultdict(int)
        for person in self._all_people:
            by_decade[person.get_decade()] += 1
        return dict(by_decade)

    def get_duplicate_names(self):
        """check for duplicate names"""
        name_counts = defaultdict(int)
        for person in self._all_people:
            name_counts[person.full_name] += 1
        return sorted(name for name, count in name_counts.items() if count > 1)
