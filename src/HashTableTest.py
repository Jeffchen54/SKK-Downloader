import unittest
from HashTable import KVPair
from HashTable import HashTable

class KVTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a hash table of size 100
        """
        self.hashT = HashTable(100)
    
    def test_hash_alg(self):
        """
        Tests hashing algorithm compared to real sfold hash results
        """
        self.assertEqual(45, self.hashT.hash("apes", self.hashT.getSize()))
        self.assertEqual(15, self.hashT.hash("31090350", self.hashT.getSize()))
        self.assertEqual(72, self.hashT.hash("30449189", self.hashT.getSize()))
        self.assertEqual(48, self.hashT.hash("0", self.hashT.getSize()))
        self.assertEqual(0, self.hashT.hash("", self.hashT.getSize()))
        self.assertEqual(32, self.hashT.hash(" ", self.hashT.getSize()))

if __name__ == '__main__':
    unittest.main()