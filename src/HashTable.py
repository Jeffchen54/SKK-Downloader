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
        Compares self and other key value

        Raise: MismatchTypeException if other is not the same type as self
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
    Closed, extensible hash table database storing KVPairs 

    @author Jeff Chen
    @created 5/8/2022
    @Last modified 5/8/2022
    """
    """ __capacity: int
    records:

    def __init__(self, size):
    """