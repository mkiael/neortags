from unittest import TestCase
from unittest.mock import patch

from rtags_client import RtagsClient


class TestRtagsClient(TestCase):

    @patch('subprocess.check_output')
    def test_find_references(self, mock_check_output):

        mock_check_output.return_value = b"test1\ntest2\ntest3\n"

        client = RtagsClient()

        result = client.find_references(4)

        assert mock_check_output.called
        assert result[0] == "test1"
        assert result[1] == "test2"
        assert result[2] == "test3"
