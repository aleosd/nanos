import logging
from unittest.mock import MagicMock, patch

import pytest
from hamcrest import assert_that, equal_to, is_

from nanos import logging as nanos_logging


def test__logger_mixin_logger_property():
    # Create a class that uses the mixin
    class TestClass(nanos_logging.LoggerMixin):
        pass

    # Instantiate the class
    instance = TestClass()

    # Check that the logger name is correct
    assert_that(instance.logger.name, equal_to(f"{TestClass.__module__}.{TestClass.__name__}"))
    # Check that the logger is cached
    assert_that(instance.logger, is_(instance.logger))


class TestSetLevelForLogger:
    def test__with_single_logger(self):
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            # Test with a single logger name
            nanos_logging.set_level_for_logger("test.logger", logging.INFO)

            # Verify the logger was retrieved with the correct name
            mock_get_logger.assert_called_once_with("test.logger")
            # Verify the level was set correctly
            mock_logger.setLevel.assert_called_once_with(logging.INFO)

    @pytest.mark.parametrize(
        "logger_names",
        [
            ("test.logger1", "test.logger2"),
            ["test.logger1", "test.logger2"],
        ],
    )
    def test__with_multiple_loggers(self, logger_names):
        with patch("logging.getLogger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            # Test with a list of logger names
            nanos_logging.set_level_for_logger(logger_names, logging.DEBUG)

            # Verify the loggers were retrieved with the correct names
            assert_that(mock_get_logger.call_count, equal_to(2))
            mock_get_logger.assert_any_call("test.logger1")
            mock_get_logger.assert_any_call("test.logger2")

            # Verify the level was set correctly for both loggers
            assert_that(mock_logger.setLevel.call_count, equal_to(2))
            mock_logger.setLevel.assert_called_with(logging.DEBUG)

    def test__raises_type_error_for_invalid_logger_names_type(self):
        # Test with an invalid type for logger_names
        with pytest.raises(TypeError):
            nanos_logging.set_level_for_logger(123)  # type: ignore


class TestGetSimpleLogger:
    def test__defaults(self):
        with (
            patch("logging.getLogger") as mock_get_logger,
            patch("logging.StreamHandler") as mock_stream_handler,
            patch("logging.Formatter") as mock_formatter,
        ):
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_handler = MagicMock()
            mock_stream_handler.return_value = mock_handler
            mock_format = MagicMock()
            mock_formatter.return_value = mock_format

            # Test with default parameters
            result = nanos_logging.get_simple_logger()

            # Verify logger was created and configured correctly
            assert_that(result, equal_to(mock_logger))
            assert_that(mock_logger.name, equal_to("root"))
            mock_logger.setLevel.assert_called_once_with(logging.DEBUG)

            # Verify console handler was added
            mock_stream_handler.assert_called_once()
            mock_handler.setLevel.assert_called_once_with(logging.DEBUG)
            mock_handler.setFormatter.assert_called_once_with(mock_format)
            mock_logger.addHandler.assert_called_once_with(mock_handler)

    def test__with_file(self):
        with (
            patch("logging.getLogger") as mock_get_logger,
            patch("logging.StreamHandler") as mock_stream_handler,
            patch("logging.FileHandler") as mock_file_handler,
            patch("logging.Formatter") as mock_formatter,
        ):
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_console_handler = MagicMock()
            mock_stream_handler.return_value = mock_console_handler
            mock_file = MagicMock()
            mock_file_handler.return_value = mock_file
            mock_format = MagicMock()
            mock_formatter.return_value = mock_format

            # Test with file handler
            result = nanos_logging.get_simple_logger(
                name="test", log_file="test.log", log_level=logging.ERROR
            )

            # Verify logger was created and configured correctly
            assert_that(result, equal_to(mock_logger))
            assert_that(mock_logger.name, equal_to("test"))
            mock_logger.setLevel.assert_called_once_with(logging.ERROR)

            # Verify file handler was created correctly
            mock_file_handler.assert_called_once_with("test.log", mode="a")
            mock_file.setFormatter.assert_called_once_with(mock_format)

            # Verify both handlers were added
            assert_that(mock_logger.addHandler.call_count, equal_to(2))
