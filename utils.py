from typing import List, Tuple, Union

class Click:
    def __init__(self, x: int, y: int, clicks: int = 1, delay: float = 0.1):
        self.x = int(x)
        self.y = int(y)
        self.clicks = int(clicks)
        self.delay = float(delay)

    def __matmul__(self, clicks: int) -> 'Click':
        """Specifies click count using @ operator."""
        return Click(self.x, self.y, clicks, self.delay)

    def __truediv__(self, delay: Union[int, float]) -> 'Click':
        """Specifies post-click delay using / operator."""
        return Click(self.x, self.y, self.clicks, float(delay))

    def __or__(self, other: Union['Click', 'ClickSequence']) -> 'ClickSequence':
        """Chains multiple click steps together using | operator."""
        if isinstance(other, Click):
            return ClickSequence([self, other])
        elif isinstance(other, ClickSequence):
            return ClickSequence([self] + other.steps)
        raise TypeError("Chaining is only supported between Click and ClickSequence objects")

    def to_tuple(self) -> Tuple[int, int, int, float]:
        return (self.x, self.y, self.clicks, self.delay)


class ClickSequence:
    def __init__(self, steps: List[Click] = None):
        self.steps = steps or []

    def __or__(self, other: Union[Click, 'ClickSequence']) -> 'ClickSequence':
        if isinstance(other, Click):
            return ClickSequence(self.steps + [other])
        elif isinstance(other, ClickSequence):
            return ClickSequence(self.steps + other.steps)
        raise TypeError("Chaining is only supported between Click and ClickSequence objects")

    def __iter__(self):
        for step in self.steps:
            yield step.to_tuple()

    def serialize(self) -> str:
        """Serializes the click sequence to a compact string format."""
        return ";".join(f"{s.x},{s.y},{s.clicks},{s.delay}" for s in self.steps)

    @classmethod
    def deserialize(cls, serialized_data: str) -> 'ClickSequence':
        """Reconstructs ClickSequence from serialized string data."""
        if not serialized_data