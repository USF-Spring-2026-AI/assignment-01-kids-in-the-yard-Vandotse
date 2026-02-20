class Person:
    """a person in the family tree"""

    def __init__(self, year_born, first_name, last_name, year_died=None,
                 is_direct_descendant=False):
        """Initialize a Person"""
        self._year_born = year_born
        self._first_name = first_name
        self._last_name = last_name
        self._year_died = year_died
        self._is_direct_descendant = is_direct_descendant
        self._partner = None
        self._children = []

    @property
    def year_born(self):
        """Return the year the person was born."""
        return self._year_born

    @property
    def year_died(self):
        """Return the year the person died."""
        return self._year_died

    @year_died.setter
    def year_died(self, value):
        """Set the year the person died."""
        self._year_died = value

    @property
    def first_name(self):
        """Return the person's first name."""
        return self._first_name

    @property
    def last_name(self):
        """Return the person's last name."""
        return self._last_name

    @property
    def full_name(self):
        """Return the person's full name."""
        return f"{self._first_name} {self._last_name}"

    @property
    def is_direct_descendant(self):
        """Return whether person is directly descended from the first two."""
        return self._is_direct_descendant

    @property
    def partner(self):
        """Return the person's partner/spouse, or None."""
        return self._partner

    @partner.setter
    def partner(self, value):
        """Set the person's partner/spouse."""
        self._partner = value

    @property
    def children(self):
        """Return list of the person's children."""
        return self._children

    def add_child(self, child):
        """Add a child to this person."""
        self._children.append(child)

    def get_decade(self):
        """Return the decade string for the person's birth year"""
        decade_year = (self._year_born // 10) * 10
        return f"{decade_year}s"
