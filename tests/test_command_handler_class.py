from unittest.mock import MagicMock

import pytest

from src.command_handler_class import CommandHandler


@pytest.fixture()
def command_function_mock():
    return MagicMock()


@pytest.fixture()
def command_handler(command_function_mock):
    uvm = MagicMock()
    handler = CommandHandler(uvm)

    handler.preCommand = MagicMock()
    handler.postCommand = MagicMock()

    handler.command_map = {'test': command_function_mock}
    handler.command_set = {'test'}
    handler.uvm.currFocusView.site = 'test'

    return handler


def test_route_command_calls_map_method(command_handler, command_function_mock):
    command_handler.routeCommand('test routeCommand')

    assert command_handler.preCommand.called
    assert command_function_mock.called
    assert command_handler.postCommand.called


def test_route_command_non_existing_site_does_not_call_command(command_handler, command_function_mock):
    command_handler.uvm.currFocusView.site = 'non_existing_site'

    command_handler.routeCommand('test routeCommand')

    assert command_handler.preCommand.called
    assert not command_function_mock.called
    assert command_handler.postCommand.called


def test_route_command_existing_site_but_system_command(command_handler, command_function_mock):
    command_handler.routeCommand('view routeCommand')

    assert command_handler.preCommand.called
    assert not command_function_mock.called
    assert not command_handler.postCommand.called


def test_route_command_command_does_not_exist(command_handler, command_function_mock):
    command_handler.routeCommand('non_existing_command routeCommand')

    assert command_handler.preCommand.called
    assert not command_function_mock.called
    assert not command_handler.postCommand.called


def test_route_command_collision_avoided_site_1(command_handler, command_function_mock):
    site_1_mock = command_function_mock
    site_2_mock = MagicMock()

    command_handler.command_set = {'test', 'test'}
    command_handler.uvm.currFocusView.site = '1'
    command_handler.command_map = {
        '1': site_1_mock,
        '2': site_2_mock,
    }

    command_handler.routeCommand('test routeCommand')

    assert site_1_mock.called


def test_route_command_collision_avoided_site_2(command_handler, command_function_mock):
    site_1_mock = command_function_mock
    site_2_mock = MagicMock()

    command_handler.command_set = {'test', 'test'}
    command_handler.uvm.currFocusView.site = '2'
    command_handler.command_map = {
        '1': site_1_mock,
        '2': site_2_mock,
    }

    command_handler.routeCommand('test routeCommand')

    assert site_2_mock.called
