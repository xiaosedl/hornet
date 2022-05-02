from django.test import TestCase

print(list(map(lambda i: i ** 2, [1, 2, 3])))

from pathlib import Path

t = Path(__file__).resolve().parent
print(t)