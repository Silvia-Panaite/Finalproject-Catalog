from unittest import TestCase
from unittest.mock import patch, MagicMock

import src.mathematics as m

class MathematicsTestCase(TestCase):
    def test_add_result(self):
        expected = 3
        result = m.add(1, 2)
        self.assertEqual(result, expected)

    def test_do_a_double_and_addition(self):
        with patch("src.mathematics.add") as mock_add:
            m.do_a_double_and_addition(1, 2)
            mock_add.assert_called_with(2, 4)
