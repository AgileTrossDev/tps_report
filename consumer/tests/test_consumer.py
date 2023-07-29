import unittest
import asyncio
import pytest
import signal
import time

from unittest.mock import patch, Mock, MagicMock

from ..main import ConsumerDbClient
from influxdb_client import InfluxDBClient


class TestConsumerDbClient(unittest.TestCase):

    def setUp(self):
        # Create a new instance of the ConsumerDbClient before each test
        self.client = ConsumerDbClient()

    def tearDown(self):
        # Clean up any resources after each test (if needed)
        pass

    def test_connect(self):
        # Test the connect method
        self.client.connect('http://localhost:8086', 'my-admin-token')
        self.assertIsNotNone(self.client.client)
        self.assertIsNotNone(self.client.write_api)
        assert self.client.active is True

    def test_handle_interrupt(self):
        # Test the handle_interrupt method
        # Since this method prints to the console, we can't directly check the output
        # Instead, we can mock the sys.stdout object and check if the correct
        # message is printed
        with patch("builtins.print") as mock_print:
            client = ConsumerDbClient()
            assert client.active is True

            # Simulate a KeyboardInterrupt by sending signal.SIGINT
            # client.handle_interrupt(signal.SIGINT, None)
            # with patch("sys.exit") as mock_exit:
            client.handle_interrupt(signal.SIGINT, None)

            assert client.active is False
            # Get the last call to the mock print function, and make surer it
            # says it was Interrupted
            last_call = mock_print.call_args_list[-1]
            args, kwargs = last_call
            assert args[0] == "Interrupt received. Stopping the loop."

    def test_process_msg(self):
        # Test the process_msg method

        # Create a mock write_api instance
        mock_write_api = MagicMock()

        # Create a sample data to be processed
        sample_data = {
            "payload": {
                "data": {
                    "temperature": 25.0
                }
            }
        }

        client = ConsumerDbClient()
        client.write_api = mock_write_api

        client.process_msg(sample_data)

        # Assert that the write method of the mock write_api was called with
        # the correct arguments
        mock_write_api.write.assert_called_once_with(
            bucket=client.bucket,
            org=client.org,
            record=[{
                "measurement": "temperature",
                "tags": {"device": "1"},
                "fields": {"value": sample_data["payload"]["data"]["temperature"]},
            }]
        )


@pytest.mark.asyncio
async def test_capture_data(mocker):

    # Create a mock websocket for the test
    class MockWebSocket:

        def __init__(self) -> None:
            self.send_counter = 0
            self.recv_counter = 0

        async def send(self, data):
            self.send_counter += 1
            pass

        async def recv(self):
            self.recv_counter += 1
            time.sleep(0.1)
            return '{"payload": {"data": {"temperature": 25.0}}}'

    # Create a mock for websockets.connect
    mock_websockets_connect = mocker.patch('websockets.connect')

    # Patch this now because it is called in the constructor
    mock_connect_function = mocker.patch.object(
        ConsumerDbClient, 'connect', return_value="Patched Result")

    # Create an instance of ConsumerDbClient, while using mocked connect
    # function
    client = ConsumerDbClient()
    assert client.active is True
    assert client.write_api is None
    assert client.client is None

    # Mock and Patch Stuff
    client.write_api = MagicMock()       # Create a mock write_api instance
    client.client = MagicMock()       # Create a mock InfluxDB client
    mock_process_function = mocker.patch.object(client, 'process_msg')

    # Santity check
    assert isinstance(client.write_api, MagicMock)
    assert isinstance(client.client, MagicMock)

    # Set the return value of mock_websockets_connect to the mock WebSocket
    # connection
    mock_websockets_connect.return_value.__aenter__.return_value = MockWebSocket()

    # await client.capture_data()
    capture_task = asyncio.create_task(client.capture_data())

    # Let the task run for a short time
    await asyncio.sleep(0.5)

    # Deactive
    await client.shutdown()

    # client.active = False
    # client.handle_interrupt(signal.SIGINT, None)
    assert client.active is False

    # Wait for capture_data to finish
    await capture_task

    # Check if Data was written to the database
    assert mock_process_function.call_count > 0
