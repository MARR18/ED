import unittest
from external_sorting import RecursiveMergeSort, DirectMergeSort, BalancedMergeSort


class TestMergeSort(unittest.TestCase):
    def test_recursive_asc(self):
        data = [3, 1, 4, 1, 5, 9, 2]
        sorter = RecursiveMergeSort()
        self.assertEqual(sorter.sort(data), sorted(data))

    def test_recursive_desc(self):
        data = [3, 1, 4, 1, 5, 9, 2]
        sorter = RecursiveMergeSort(reverse=True)
        self.assertEqual(sorter.sort(data), sorted(data, reverse=True))

    def test_direct_asc(self):
        data = [3, 1, 4, 1, 5, 9, 2]
        sorter = DirectMergeSort()
        self.assertEqual(sorter.sort(data), sorted(data))

    def test_direct_key(self):
        data = ["apple", "banana", "kiwi", "berry"]
        sorter = DirectMergeSort(key=lambda x: len(x))
        self.assertEqual(sorter.sort(data), ["kiwi", "apple", "berry", "banana"])

    def test_balanced_asc_list(self):
        data = [5, 2, 8, 1, 9, 3]
        sorter = BalancedMergeSort(chunk_size=2)
        self.assertEqual(sorter.sort(data), sorted(data))

    def test_balanced_desc_list(self):
        data = [5, 2, 8, 1, 9, 3]
        sorter = BalancedMergeSort(chunk_size=2, reverse=True)
        self.assertEqual(sorter.sort(data), sorted(data, reverse=True))


if __name__ == "__main__":
    unittest.main()