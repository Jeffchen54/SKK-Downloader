from typing import List
from typing import TypeVar, Generic

T = TypeVar('T')
class Error(Exception):
    """Base class for other exceptions"""
    pass

class MismatchTypeException(Error):
    """Raised when a comparison is made on 2 different types"""
    pass

class KVPair (Generic[T]):
    """
    Generic KVPair structure where:
        Key is generic
        Value is int
    Upon initiailization, data becomes read-only
    """
    __key: int
    __value: T

    def __init__(self, key: int, value:T) -> None:
        self.__value = value
        self.__key = key

    def getKey(self) -> int:
        """
        Returns key
        Return: key
        """
        return self.__key

    def getValue(self) -> T:
        """
        Returns value
        Return: value
        """
        return self.__value

    def compareTo(self, other)->int:
        """
        Compares self and other key value. Ignores generic typing

        Raise: MismatchTypeException if other is not a KVPair
        Return:
            self.getKey() > other.getKey() -> 1
            self.getKey() == other.getKey() -> 0
            self.getKey() < other.getKey() -> -1

        """
        if other == None or not isinstance(other, KVPair):
            raise MismatchTypeException("other is not of type KVPair(T)")
        
        if self.__key > other.getKey():
            return 1
        if self.__key == other.getKey():
            return 0
        return -1

class HashTable:
    """
    Closed, extensible hash table database storing KVPairs of any type

    @author Jeff Chen
    @created 5/8/2022
    @Last modified 5/8/2022
    """
    __size:int
    __records:List[KVPair]
    __occupied:int

    def __init__(self, size):
        """
        Construct a hash table with initial size

        Param:
            initialSize: Initial hash table size
        """
        self.__size = size
        self.__records = list()

    def getSize(self):
        """
        Get size of hash table
        """
        return int(self.__size)

    def hash(self, s:str, m:int)->int:
        """
        Hashing algorithm using string folding. Adopted from
        OpenDSA and translated to python 

        Params
            s: string to hash
            m: size of table 
        Return: home slot of s
        """
        intLength:int = int(len(s) / 4)
        sum:int = 0

        for j in range(0, intLength):
            c = list(s[j * 4: (j * 4) + 4])
            mult = 1
            for k in range(0, len(c)):
                sum += ord(c[k]) * mult
                mult *= 256
        index = intLength * 4
        c = list(s[index:])
        mult = 1

        for k in range(0, len(c)):
            sum += ord(c[k]) * mult
            mult *= 256

        return abs(sum % m)