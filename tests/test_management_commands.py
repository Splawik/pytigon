"""Tests for pytigon management commands - add_arguments methods."""

import argparse

import pytest


class TestCompileTemplatesAddArguments:
    def test_add_arguments(self):
        from pytigon.schserw.schsys.management.commands.compiletemplates import Command

        cmd = Command()
        parser = argparse.ArgumentParser()
        cmd.add_arguments(parser)
        args = parser.parse_args(["--file", "test.ihtml"])
        assert args.file == "test.ihtml"


class TestEncryptAddArguments:
    def test_add_arguments(self):
        from pytigon.schserw.schsys.management.commands.encrypt import Command

        cmd = Command()
        parser = argparse.ArgumentParser()
        cmd.add_arguments(parser)
        args = parser.parse_args(["input.txt"])
        assert args.input == "input.txt"
        assert args.decrypt is False

    def test_add_arguments_decrypt(self):
        from pytigon.schserw.schsys.management.commands.encrypt import Command

        cmd = Command()
        parser = argparse.ArgumentParser()
        cmd.add_arguments(parser)
        args = parser.parse_args(["input.txt", "--decrypt", "--base64"])
        assert args.decrypt is True
        assert args.base64 is True
