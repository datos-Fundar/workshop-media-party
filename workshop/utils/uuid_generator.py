import uuid
import random
from typing import Generator, Iterable, Any

class UuidGenerator:
    """
    Deterministic UUIDv4 generator backed by its own seeded RNG.

    For a given instance (seed), every UUID draw advances a single shared RNG.
    No matter which method you use (next(), generate(), sequence(), iterate(),
    generate_items()), if the underlying draw count is the same, you'll get the
    same next UUID.

    Example:
        gen1 = DeterministicUUID4(seed=123)
        a = gen1.next()
        b = gen1.next()

        gen2 = DeterministicUUID4(seed=123)
        s = gen2.sequence(2)
        assert [a, b] == s

        gen3 = DeterministicUUID4(seed=123)
        it = gen3.generate()
        assert next(it) == a
        assert next(it) == b
    """

    def __init__(self, seed: int | float | str | bytes | bytearray | None = None) -> None:
        self._rng = random.Random(seed)

    def _next_uuid(self) -> uuid.UUID:
        """
        Draw one UUIDv4 using this instance's RNG.

        We draw 128 random bits, then set RFC 4122 version/variant bits
        to make it a proper v4 UUID.
        """
        # 128 random bits -> 16 bytes (big-endian)
        b = bytearray(self._rng.getrandbits(128).to_bytes(16, "big"))

        # Set version to 4 (0100xxxx)
        b[6] = (b[6] & 0x0F) | 0x40
        # Set variant to RFC 4122 (10xxxxxx)
        b[8] = (b[8] & 0x3F) | 0x80

        return uuid.UUID(bytes=bytes(b))

    def next(self) -> uuid.UUID:
        """Return the next UUID in the sequence."""
        return self._next_uuid()

    def generate(self) -> Generator[uuid.UUID, None, None]:
        """
        Infinite generator of UUIDs. Consumes the same underlying RNG
        as next()/sequence()/iterate(), so state is consistent across APIs.
        """
        while True:
            yield self._next_uuid()

    def sequence(self, n: int) -> list[uuid.UUID]:
        """Return a list of the next n UUIDs."""
        if n < 0:
            raise ValueError("n must be non-negative")
        return [self._next_uuid() for _ in range(n)]

    def generate_items[T](self, xs: Iterable[T]) -> Generator[tuple[T, uuid.UUID], None, None]:
        """
        Yield (item, uuid) pairs for items in xs, preserving order and consuming
        one UUID per item from the shared RNG.
        """
        for x in xs:
            yield (x, self._next_uuid())

    def iterate[T](self, xs: Iterable[T]) -> list[tuple[T, uuid.UUID]]:
        """
        Eager version of generate_items(): returns a list of (item, uuid) pairs
        in the same order as xs.
        """
        return list(self.generate_items(xs))

    @classmethod
    def from_hash(cls, x: Any) -> 'UuidGenerator':
        return cls(seed=hash(x))