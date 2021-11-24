# Name: Edward Lada
# OSU Email: ladae@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: Dec. 3, 2021, 11:59pm PST
# Description: Implement a HashMap ADT without using built-in Python
# data structures.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Clear all contents of the HashMap without changing capacity.
        :return: None
        """
        for i in range(self.capacity):
            self.buckets[i] = LinkedList()
        self.size = 0

    def get(self, key: str) -> object:
        """
        Return the value associated with `key` in the map.
        Return None if `key` is not in the map.
        :param key: a string
        :return: an object or None
        """
        hashed_key = self.hash_function(key)
        index = hashed_key % self.capacity
        key_node = self.buckets[index].contains(key)
        return None if key_node is None else key_node.value

    def put(self, key: str, value: object) -> None:
        """
        Add a key/value pair to the HashMap.
        If `key` already exists in the HashMap, update its associated
        value to `value`. Else add `key`: `value` to the map.
        :param key: a string
        :param value: an object associated with `key`
        :return: None
        """
        hashed_key = self.hash_function(key)  # Compute hash of `key`
        index = hashed_key % self.capacity  # Compute index based on hashed key
        bucket_list = self.buckets[index]
        key_node = bucket_list.contains(key)
        # Check if `key` is in map
        if key_node is None:
            bucket_list.insert(key, value)
            self.size += 1
        else:  # `key` already exists, update value.
            key_node.value = value

    def remove(self, key: str) -> None:
        """
        Remove a key/value pair from the map.
        If `key` is not in the map, method does nothing.
        :param key: a string
        :return: None
        """
        hashed_key = self.hash_function(key)
        index = hashed_key % self.capacity
        is_removed = self.buckets[index].remove(key)
        if is_removed:
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Return True if the map contains 'key'. False otherwise.
        :param key: a string to search the map for.
        :return: a boolean
        """
        if self.size == 0:
            return False
        hashed_key = self.hash_function(key)
        index = hashed_key % self.capacity
        return self.buckets[index].contains(key) is not None

    def empty_buckets(self) -> int:
        """
        Return the number of empty buckets in the HashMap.
        :return: an integer
        """
        count = 0
        for i in range(self.capacity):
            if self.buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Return the current HashMap load factor.
        :return: a float
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table and re-hash
        all key/value pairs.
        If `new_capacity` < 1 the method does nothing.
        :param new_capacity: an int
        :return: None
        """
        if new_capacity > 0:
            # Create new HashMap and buckets
            temp = HashMap(new_capacity, self.hash_function)
            for i in range(new_capacity):
                temp.buckets.append(LinkedList())
            # Re-hash contents of original map into temp_buckets
            for j in range(self.capacity):
                if self.buckets[j].length() > 0:
                    for node in self.buckets[j]:
                        temp.put(node.key, node.value)
            while self.capacity > 0:  # Clear old data from self
                self.buckets.pop()
                self.capacity -= 1
            for i in range(temp.capacity):  # Add re-hashed data to self
                self.buckets.append(temp.buckets[i])
                self.capacity += 1

    def get_keys(self) -> DynamicArray:
        """
        Return a DynamicArray containing all keys stored in the map.
        :return: a DynamicArray
        """
        result = DynamicArray()
        for i in range(self.capacity):
            for node in self.buckets[i]:
                result.append(node.key)
        return result


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
