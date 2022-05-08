import unittest
from HashTable import KVPair
from HashTable import MismatchTypeException

class KVTestCase(unittest.TestCase):
    def setUp(self):
        """
        Intentionally left empty
        """
    def test_getKey(self):
        """
        Tests getKey()
        """
        pair = KVPair[str](5, "Happee")
        self.assertEqual(5, pair.getKey())
    
    def test_getValue(self):
        """
        Tests getValue()
        """
        pair = KVPair[str](5, "Happee")
        self.assertEqual("Happee", pair.getValue())

    def test_compareTo(self):
        pair =KVPair[str](5, "Happee") 
        pair2 = KVPair[int](5, 5)
        pairLow = KVPair[str](0, "low")
        pairHigh = KVPair[str](10, "high")
        pairEqual = KVPair[str](5, "equal")
        null = None
        non = "str"

        # Comparison testing
        self.assertEqual(0, pair.compareTo(pair))
        self.assertEqual(0, pair.compareTo(pair2))
        self.assertEqual(1, pair.compareTo(pairLow))
        self.assertEqual(-1, pair.compareTo(pairHigh))
        self.assertEqual(0, pair.compareTo(pairEqual))

        # Exception testing
        self.assertRaises(MismatchTypeException, pair.compareTo, null)
        self.assertRaises(MismatchTypeException, pair.compareTo, non)


if __name__ == '__main__':
    unittest.main()