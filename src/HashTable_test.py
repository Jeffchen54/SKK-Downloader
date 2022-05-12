import unittest
from HashTable import KVPair
from HashTable import HashTable


class KVTestCase(unittest.TestCase):
    def setUp(self):
        """
        Creates a hash table of size 100
        """
        self.hashT = HashTable(100)

    def test_construct(self):
        self.hashT = HashTable(2)
        self.assertEqual(2, self.hashT.hashtable_getSize())

    def test_hash_alg(self):
        """
        Tests hashing algorithm compared to real sfold hash results
        """
        self.assertEqual(45, self.hashT.hash(
            "apes", self.hashT.hashtable_getSize()))
        self.assertEqual(15, self.hashT.hash(
            "31090350", self.hashT.hashtable_getSize()))
        self.assertEqual(72, self.hashT.hash(
            "30449189", self.hashT.hashtable_getSize()))
        self.assertEqual(48, self.hashT.hash(
            "0", self.hashT.hashtable_getSize()))
        self.assertEqual(0, self.hashT.hash(
            "", self.hashT.hashtable_getSize()))
        self.assertEqual(32, self.hashT.hash(
            " ", self.hashT.hashtable_getSize()))

    def test_add(self):
        """
        Tests add()
        """
        # Add one entry
        self.hashT.hashtable_add(KVPair[int, str](12345, "aaa"))
        self.assertEqual(100, self.hashT.hashtable_getSize())
        self.assertEqual(1, self.hashT.hashtable_getOccupied())

        # Add duplicate entry
        self.hashT.hashtable_add(KVPair[int, str](12345, "a"))
        self.assertEqual(100, self.hashT.hashtable_getSize())
        self.assertEqual(1, self.hashT.hashtable_getOccupied())

        # Add 50 more entries
        for i in range(0, 50):
            self.hashT.hashtable_add(KVPair[int, str](i, str(i)))

        self.assertEqual(200, self.hashT.hashtable_getSize())
        self.assertEqual(51, self.hashT.hashtable_getOccupied())
        pass

    def test_delete(self):
        """
        Tests delete()
        """
        # Delete non-existant
        self.assertFalse(self.hashT.hashtable_delete(KVPair[int, str](12345, "Does not exist")))

        # Add and delete entry
        self.hashT.hashtable_add(KVPair[int, str](12345, "Does exists"))
        self.assertTrue(self.hashT.hashtable_delete(KVPair[int, str](12345, "Does exist")))
        self.assertEqual(100, self.hashT.hashtable_getSize())
        self.assertEqual(0, self.hashT.hashtable_getOccupied())

        # Delete entry again
        self.assertFalse(self.hashT.hashtable_delete(KVPair[int, str](12345, "Does exist")))
        self.assertEqual(100, self.hashT.hashtable_getSize())
        self.assertEqual(0, self.hashT.hashtable_getOccupied())

    def test_exists(self):
        """
        Tests exists() infinite loop detector
        exists is tested alongside delete() and add()
        """
        # Empty exists()
        self.assertEqual(-1, self.hashT.hashtable_exist(KVPair[int, str](47124367, "aaaa")))

        # 8 is a known size that bricks quadratic probe
        self.hashT = HashTable(8)

        self.hashT.hashtable_add(KVPair[int, str](97, "a"))
        self.hashT.hashtable_add(KVPair[int, str](4324, "aa"))
        self.hashT.hashtable_add(KVPair[int, str](43214, "aaa"))
        #self.hashT.hashtable_add(KVPair[str](47124367, "aaaa"))
        self.assertEqual(-1, self.hashT.hashtable_exist(KVPair[int, str](47124367, "aaaa")))
        self.assertEqual(16, self.hashT.hashtable_getSize())
        self.assertEqual(3, self.hashT.hashtable_getOccupied())
        

    def test_getters(self):
        """
        Tests getters
        -> getSize() getOccupied()
        """
        pass

        self.assertEqual(100, self.hashT.hashtable_getSize())
        self.assertEqual(0, self.hashT.hashtable_getOccupied())


if __name__ == '__main__':
    unittest.main()
