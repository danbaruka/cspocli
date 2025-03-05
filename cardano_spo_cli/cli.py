#!/usr/bin/env python3
"""Cardano SPO CLI main module."""

import click
import sys
from pathlib import Path

@click.group()
def cli():
    """Cardano SPO CLI - Professional Stake Pool Operator Tool"""
    pass

@cli.command()
def version():
    """Display version information."""
    click.echo("Cardano SPO CLI v0.1.0")

if __name__ == "__main__":
    cli()
