import unittest
import uuid
from crdtcode.lww import LWWElementSet as LWWSet


class TestLWW(unittest.TestCase):
    # this function will create two LWWSet for testing purpose
    def setUp(self):
        # Create a LWWSet
        self.lwwone = LWWSet(uuid.uuid4())

        # Create another LWWSet
        self.lwwtwo = LWWSet(uuid.uuid4())

        # Add elements to lwwone
        self.lwwone.add('string_a')
        self.lwwone.add('string_b')

        # Add elements to lwwone
        self.lwwtwo.add('string_b')
        self.lwwtwo.add('string_c')
        self.lwwtwo.add('string_d')

    def test_add_element_to_lww_set(self):
        self.assertEqual([_['vertex'] for _ in self.lwwone.W], ['string_a', 'string_b'])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], [])
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.W], ['string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.R], [])

    def test_lww_set_query_only(self):
        # Check lwwone querying
        self.assertTrue(self.lwwone.query('string_a'))
        self.assertTrue(self.lwwone.query('string_b'))
        self.assertFalse(self.lwwone.query('string_c'))
        self.assertFalse(self.lwwone.query('string_d'))

        # Check lwwtwo querying
        self.assertFalse(self.lwwtwo.query('string_a'))
        self.assertTrue(self.lwwtwo.query('string_b'))
        self.assertTrue(self.lwwtwo.query('string_c'))
        self.assertTrue(self.lwwtwo.query('string_d'))

    def test_lww_set_merge_only(self):
        # Check lwwone merging
        self.lwwone.merge(self.lwwtwo)
        self.assertEqual([_['vertex'] for _ in self.lwwone.W], ['string_a', 'string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], [])

        # Check lwwtwo merging
        self.lwwtwo.merge(self.lwwone)
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.W], ['string_a', 'string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.R], [])

        # Check if they are both equal
        self.assertEqual([_['vertex'] for _ in self.lwwone.W], [_['vertex'] for _ in self.lwwtwo.W])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], [_['vertex'] for _ in self.lwwtwo.R])

    def test_lwt_set_query_and_merge(self):
        # Check lwwtwo merging
        self.lwwtwo.merge(self.lwwone)
        self.assertTrue(self.lwwtwo.query('string_a'))
        self.assertTrue(self.lwwtwo.query('string_b'))
        self.assertTrue(self.lwwtwo.query('string_c'))
        self.assertTrue(self.lwwtwo.query('string_d'))

        # Check lwwone merging
        self.lwwone.merge(self.lwwtwo)
        self.assertTrue(self.lwwone.query('string_a'))
        self.assertTrue(self.lwwone.query('string_b'))
        self.assertTrue(self.lwwone.query('string_c'))
        self.assertTrue(self.lwwone.query('string_d'))

    def test_remove_in_lww_set(self):
        # Remove elements from lwwone
        self.lwwone.remove('string_b')

        self.assertEqual([_['vertex'] for _ in self.lwwone.W], ['string_a', 'string_b'])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], ['string_b'])

        # Remove elements from lwwtwo
        self.lwwtwo.remove('string_b')
        self.lwwtwo.remove('string_c')

        self.assertEqual([_['vertex'] for _ in self.lwwtwo.W], ['string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.R], ['string_b', 'string_c'])

    def test_lww_set_query_and_removal(self):
        # Remove elements from lwwone
        self.lwwone.remove('string_b')

        # Check lwwone querying
        self.assertTrue(self.lwwone.query('string_a'))
        self.assertFalse(self.lwwone.query('string_b'))
        self.assertFalse(self.lwwone.query('string_c'))
        self.assertFalse(self.lwwone.query('string_d'))

        # Remove elements from lwwtwo
        self.lwwtwo.remove('string_b')
        self.lwwtwo.remove('string_c')

        # Check lwwtwo querying
        self.assertFalse(self.lwwtwo.query('string_a'))
        self.assertFalse(self.lwwtwo.query('string_b'))
        self.assertFalse(self.lwwtwo.query('string_c'))
        self.assertTrue(self.lwwtwo.query('string_d'))

    def test_lww_set_merger_and_removal(self):
        # Remove elements from lwwone
        self.lwwone.remove('string_b')

        # Remove elements from lwwtwo
        self.lwwtwo.remove('string_b')
        self.lwwtwo.remove('string_c')

        # Check lwwone merging
        self.lwwone.merge(self.lwwtwo)
        self.assertEqual([_['vertex'] for _ in self.lwwone.W], ['string_a', 'string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], ['string_b', 'string_c'])

        # Check lwwtwo merging
        self.lwwtwo.merge(self.lwwone)
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.W], ['string_a', 'string_b', 'string_c', 'string_d'])
        self.assertEqual([_['vertex'] for _ in self.lwwtwo.R], ['string_b', 'string_c'])

        # Check if they are both equal
        self.assertEqual([_['vertex'] for _ in self.lwwone.W], [_['vertex'] for _ in self.lwwtwo.W])
        self.assertEqual([_['vertex'] for _ in self.lwwone.R], [_['vertex'] for _ in self.lwwtwo.R])

    def test_lww_set_all(self):
        # Remove elements from lwwone
        self.lwwone.remove('string_b')

        # Remove elements from lwwtwo
        self.lwwtwo.remove('string_b')
        self.lwwtwo.remove('string_c')

        # Merge lwwtwo to lwwone
        self.lwwone.merge(self.lwwtwo)

        # Merge lwwone to lwwtwo
        self.lwwtwo.merge(self.lwwone)

        # Check lwwone querying
        self.assertTrue(self.lwwone.query('string_a'))
        self.assertFalse(self.lwwone.query('string_b'))
        self.assertFalse(self.lwwone.query('string_c'))
        self.assertTrue(self.lwwone.query('string_d'))

        # Check lwwtwo querying
        self.assertTrue(self.lwwtwo.query('string_a'))
        self.assertFalse(self.lwwtwo.query('string_b'))
        self.assertFalse(self.lwwtwo.query('string_c'))
        self.assertTrue(self.lwwtwo.query('string_d'))


if __name__ == '__main__':
    # run the test
    unittest.main()
