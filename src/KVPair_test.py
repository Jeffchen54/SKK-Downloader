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
        pair = KVPair[int,str](5, "Happee")
        self.assertEqual(5, pair.getKey())
    
    def test_getValue(self):
        """
        Tests getValue()
        """
        pair = KVPair[int,str](5, "Happee")
        self.assertEqual("Happee", pair.getValue())

    def test_compareTo(self):
        """
        Tests compareTo()
        """
        pair =KVPair[int, str](5, "Happee") 
        pair2 = KVPair[int, int](5, 5)
        pairLow = KVPair[int, str](0, "low")
        pairHigh = KVPair[int, str](10, "high")
        pairEqual = KVPair[int, str](5, "equal")
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

    def test_toString(self):
        """
        tests str(KVPair)
        """
        pair =KVPair[int, str](5, "Happee") 
        pair2 = KVPair[int, int](5, 5)
        self.assertEqual("{key:5, value:Happee, Tomb:F}", str(pair))
        self.assertEqual("{key:5, value:5, Tomb:F}", str(pair2))
        pair.setTombstone()
        self.assertEqual("{key:5, value:Happee, Tomb:T}", str(pair))
        pair.disableTombstone()
        self.assertEqual("{key:5, value:Happee, Tomb:F}", str(pair))
        
    def test_tombstone(self):
        """
        Tests all related tombstone functions
        -> init(), isTombstone(), setTombstone(), disableTombstone()
        """
        pair =KVPair[int, str](5, "Happee") 
        self.assertFalse(pair.isTombstone())
        pair.setTombstone()
        self.assertTrue(pair.isTombstone())
        pair.disableTombstone()
        self.assertFalse(pair.isTombstone())


if __name__ == '__main__':
    unittest.main()