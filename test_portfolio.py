import unittest

class TestPortfolioFunctions(unittest.TestCase):
    def test_sample(self):
        """Test case to verify basic functionality"""
        self.assertEqual(1 + 1, 2)
        
    def test_string_operations(self):
        """Test case for string operations"""
        test_string = "Rahul"
        self.assertEqual(test_string.upper(), "RAHUL")
        self.assertTrue(len(test_string) > 0)

if __name__ == '__main__':
    unittest.main()
