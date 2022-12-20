from dataclasses import dataclass


@dataclass
class Date:
    year: int
    month: int

    def printDate(self):
        print(str(self.year) + "-" + str(self.month))

    def to_string(self):
        return (str(self.year) + "-" + str(self.month))

    def __gt__(self, other):
        if not isinstance(other, Date):
            return NotImplemented
        if self.year > other.year:
            return True
        if self.year == other.year:
            return self.month > other.month
        return False

    def __ge__(self,other):
        if not isinstance(other, Date):
            return NotImplemented
        if self.year > other.year:
            return True
        if self.year == other.year:
            return self.month >= other.month
        return False

    def count_month_up(self):
        self.month += 1
        if self.month > 12:
            self.month = 1
            self.year += 1
