"""
Main CLI module for Cardano SPO CLI
"""

import os
import sys
from pathlib import Path
from typing import Optional
import click
from colorama import init, Fore, Style
import json

from .tools.download import download_cardano_tools, verify_tools
from .tools.wallet import generate_wallet_real
from .tools.wallet_simple import generate_wallet_simple
from .tools.export import export_wallet_files, list_wallet_files
from .version import get_version_info

# Initialize colorama for color support
init()


def print_banner():
    """Display CLI banner"""
    version_info = get_version_info()
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}Cardano SPO CLI{Fore.CYAN}                           ║
║              Professional Stake Pool Operator Tool                    ║
║                    Version {version_info['version']}                                    ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    click.echo(banner)


def print_security_warning():
    """Display security warning"""
    warning = f"""
{Fore.RED}SECURITY WARNING{Style.RESET_ALL}

This CLI generates sensitive private keys for your Cardano wallet.
Make sure to:

{Fore.YELLOW}• Run this CLI in a secure environment
• Store the recovery phrase in a safe place
• Never share your private keys
• Create encrypted backups of generated files{Style.RESET_ALL}

{Fore.CYAN}Continue only if you understand these risks.{Style.RESET_ALL}
"""
    click.echo(warning)


def print_next_steps(ticker: str, purpose: str, wallet_dir: Path):
    """Display next steps"""
    steps = f"""
{Fore.GREEN}Wallet generated successfully!{Style.RESET_ALL}

{Fore.CYAN}Next steps:{Style.RESET_ALL}

1. {Fore.YELLOW}Import the wallet{Style.RESET_ALL}
   • Open a compatible Cardano wallet
   • Import using the 24-word recovery phrase
   • Configure in single-address mode

2. {Fore.YELLOW}Transfer funds{Style.RESET_ALL}
   • Send ADA to the address: {Fore.CYAN}{wallet_dir}/{ticker}-{purpose}.base_addr{Style.RESET_ALL}
   • Test first with a small amount (1 ADA)

3. {Fore.YELLOW}Send files to your stake pool operator{Style.RESET_ALL}
   • {ticker}-{purpose}.base_addr
   • {ticker}-{purpose}.reward_addr  
   • {ticker}-{purpose}.staking_skey
   • {ticker}-{purpose}.staking_vkey

4. {Fore.YELLOW}Maintain balance{Style.RESET_ALL}
   • Always keep balance above declared pledge level
   • Monitor pool performance

{Fore.RED}IMPORTANT:{Style.RESET_ALL}
• Store recovery phrase securely
• Never share private keys
• Create encrypted backups

{Fore.BLUE}Support: See documentation for assistance{Style.RESET_ALL}
"""
    click.echo(steps)


@click.group()
def cli():
    """
    Cardano SPO CLI - Professional Stake Pool Operator Tool

    Generate secure Cardano wallets for stake pool operations.
    Creates 24-word recovery phrases, addresses, and keys for pledge/rewards wallets.

    Files stored in: ~/.CSPO_{TICKER_NAME}/{purpose}/
    Security: Local storage with secure permissions.

    Examples:
        cspocli generate --ticker MYPOOL --purpose pledge
        cspocli generate -t MYPOOL -p rewards --simple
        cspocli version
    """
    pass


@cli.command()
@click.option(
    "--ticker",
    "-t",
    required=True,
    help="Pool ticker symbol (e.g., MYPOOL, ADA, CARDANO)",
)
@click.option(
    "--purpose",
    "-p",
    required=True,
    type=click.Choice(["pledge", "rewards"]),
    help="Wallet purpose: pledge or rewards",
)
@click.option(
    "--network",
    "-n",
    default="mainnet",
    type=click.Choice(["mainnet", "testnet", "preview", "preprod"]),
    help="Cardano network (default: mainnet)",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force regeneration of existing wallet",
)
@click.option("--no-banner", is_flag=True, help="Skip welcome banner")
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Quiet mode - JSON output only",
)
@click.option(
    "--simple",
    "-s",
    is_flag=True,
    help="Use simplified mode (no external tools)",
)
def generate(
    ticker: str,
    purpose: str,
    network: str,
    force: bool,
    no_banner: bool,
    quiet: bool,
    simple: bool,
):
    """
    Generate a secure Cardano wallet for stake pool operations

    Creates wallet files for pledge or rewards purposes:
    • base_addr - Address for pledge funds
    • reward_addr - Address for staking rewards
    • staking_skey - Private staking key (SENSITIVE)
    • staking_vkey - Public staking key
    • mnemonic.txt - 24-word recovery phrase (SENSITIVE)

    Storage: ~/.CSPO_{TICKER}/{PURPOSE}/
    Security: BIP39 recovery phrase, secure permissions (600)

    Examples:
        cspocli generate --ticker MYPOOL --purpose pledge
        cspocli generate -t ADA -p rewards --simple
        cspocli generate --ticker CARDANO --purpose pledge --quiet
    """

    if not quiet and not no_banner:
        print_banner()

    if not quiet:
        print_security_warning()

        # Ask for confirmation
        if not click.confirm("Do you want to continue?", default=True):
            click.echo(f"{Fore.RED}Operation cancelled{Style.RESET_ALL}")
            sys.exit(0)

    try:
        # Check if wallet already exists
        home_dir = Path.home() / f".CSPO_{ticker.upper()}"
        wallet_dir = home_dir / purpose

        if wallet_dir.exists() and not force:
            if not quiet:
                click.echo(
                    f"{Fore.YELLOW}Wallet {ticker}-{purpose} already exists{Style.RESET_ALL}"
                )
                if not click.confirm("Do you want to regenerate it?", default=False):
                    click.echo(f"{Fore.RED}Operation cancelled{Style.RESET_ALL}")
                    sys.exit(0)

        # Generate wallet
        if not quiet:
            click.echo(
                f"{Fore.CYAN}Generating {ticker}-{purpose} wallet...{Style.RESET_ALL}"
            )

        if simple:
            # Use simplified version
            wallet_data = generate_wallet_simple(ticker, purpose, network)
        else:
            # Use real Cardano tools by default
            try:
                wallet_data = generate_wallet_real(ticker, purpose, network)
            except click.ClickException as e:
                if "Real Cardano tools not available" in str(e):
                    click.echo(
                        f"{Fore.YELLOW}Real tools not available. Switching to simplified mode...{Style.RESET_ALL}"
                    )
                    wallet_data = generate_wallet_simple(ticker, purpose, network)
                else:
                    raise e

        # Display wallet information
        if not quiet:
            click.echo(
                f"\n{Fore.GREEN}Files generated in: {wallet_dir}{Style.RESET_ALL}"
            )

            # List generated files
            files = list(wallet_dir.glob(f"{ticker}-{purpose}.*"))
            for file in files:
                if file.name.endswith(".mnemonic.txt") or file.name.endswith(
                    ".staking_skey"
                ):
                    click.echo(f"  {Fore.RED}{file.name} (SENSITIVE){Style.RESET_ALL}")
                else:
                    click.echo(f"  {Fore.CYAN}{file.name}{Style.RESET_ALL}")

            # Display addresses
            click.echo(f"\n{Fore.CYAN}Generated addresses:{Style.RESET_ALL}")
            click.echo(f"  Base Address: {wallet_data['base_addr']}")
            click.echo(f"  Reward Address: {wallet_data['reward_addr']}")

            # Display next steps
            print_next_steps(ticker, purpose, wallet_dir)

        # Return information in quiet mode
        if quiet:
            result = {
                "ticker": ticker,
                "purpose": purpose,
                "wallet_dir": str(wallet_dir),
                "base_addr": wallet_data["base_addr"],
                "reward_addr": wallet_data["reward_addr"],
                "files": [str(f) for f in wallet_dir.glob(f"{ticker}-{purpose}.*")],
            }
            click.echo(json.dumps(result, indent=2))

    except click.ClickException as e:
        click.echo(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
@click.option(
    "--ticker",
    "-t",
    required=True,
    help="Pool ticker symbol (e.g., MYPOOL, ADA, CARDANO)",
)
@click.option(
    "--purpose",
    "-p",
    required=True,
    type=click.Choice(["pledge", "rewards"]),
    help="Wallet purpose: pledge or rewards",
)
@click.option(
    "--password",
    required=True,
    help="Password for encrypted export",
)
def export(ticker: str, purpose: str, password: str):
    """
    Export wallet files in encrypted ZIP format

    Creates an encrypted ZIP file containing essential wallet files:
    • base_addr - Address for pledge funds
    • reward_addr - Address for staking rewards
    • staking_skey - Private staking key (SENSITIVE)
    • staking_vkey - Public staking key

    The export is encrypted and can be safely uploaded.

    Examples:
        cspocli export --ticker MYPOOL --purpose pledge --password mypassword
        cspocli export -t ADA -p rewards --password securepass123
    """
    try:
        export_file = export_wallet_files(ticker, purpose, password)
        click.echo(f"{Fore.GREEN}Export completed successfully!{Style.RESET_ALL}")
        click.echo(f"Export file: {export_file}")
    except click.ClickException as e:
        click.echo(f"{Fore.RED}Export failed: {e}{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
def version():
    """
    Display version and build information

    Shows version, commit hash, and build status.
    Useful for troubleshooting and support requests.

    Examples:
        cspocli version
    """
    version_info = get_version_info()

    click.echo(f"Cardano SPO CLI v{version_info['full_version']}")

    if version_info["commit_hash"]:
        click.echo(f"Commit: {version_info['commit_hash']}")

    if version_info["is_dirty"]:
        click.echo(
            f"{Fore.YELLOW}Working tree has uncommitted changes{Style.RESET_ALL}"
        )


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()
