#!/usr/bin/env python3
"""Simplified wallet generation module."""

import click
from pathlib import Path
from mnemonic import Mnemonic

class SimpleCardanoWalletGenerator:
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.home_dir = Path.home() / f".CSPO_{self.ticker}"
        self.mnemo = Mnemonic("english")

    def generate_mnemonic(self) -> str:
        """Generate a 24-word recovery phrase"""
        return self.mnemo.generate(strength=256)

    def generate_wallet(self, purpose: str):
        """Generate a complete wallet (simplified version)"""
        click.echo(f"Generating {self.ticker}-{purpose} wallet (simplified version)...")
        
        # Generate mnemonic phrase
        mnemonic = self.generate_mnemonic()
        click.echo("Recovery phrase generated")
        
        # Create wallet directory
        wallet_dir = self.home_dir / purpose
        wallet_dir.mkdir(parents=True, exist_ok=True)
        
        # Save mnemonic
        mnemonic_file = wallet_dir / f"{self.ticker}-{purpose}.mnemonic.txt"
        with open(mnemonic_file, "w") as f:
            f.write(mnemonic)
        
        click.echo(f"Wallet generated in: {wallet_dir}")
        
        return {
            "ticker": self.ticker,
            "purpose": purpose,
            "wallet_dir": str(wallet_dir),
            "mnemonic": mnemonic,
        }

def generate_wallet_simple(ticker: str, purpose: str):
    """Main function to generate a wallet (simplified version)"""
    generator = SimpleCardanoWalletGenerator(ticker)
    return generator.generate_wallet(purpose)
