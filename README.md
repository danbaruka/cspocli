# Cardano SPO CLI

A professional CLI tool for configuring Cardano Stake Pool Operator (SPO) wallets on Linux, macOS and Windows.

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection to download Cardano tools

### Quick Installation

#### Option 1: Using Makefile (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-repo/cardano-spo-cli.git
cd cardano-spo-cli

# Install globally (no activation needed)
make install-global
# Note: You'll be prompted for your computer password (not sudo password)

# Or install locally (requires activation)
make install
source venv/bin/activate
```

#### Option 2: Using Installation Scripts

```bash
# Clone the repository
git clone https://github.com/your-repo/cardano-spo-cli.git
cd cardano-spo-cli

# Run installation script
./install.sh  # Linux/macOS
# or
install.bat   # Windows

# Activate environment
source venv/bin/activate
```

#### Option 3: Manual Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/cardano-spo-cli.git
cd cardano-spo-cli

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the CLI
pip install -e .
```

### Installation from PyPI (when available)

```bash
pip install cardano-spo-cli
```

## 📖 Usage

### Generate a pledge wallet

```bash
cspocli generate --ticker MYPOOL --purpose pledge
```

### Generate a rewards wallet

```bash
cspocli generate --ticker MYPOOL --purpose rewards
```

### Check version

```bash
cspocli version
```

### Available options

```bash
cspocli --help
```

Main options:

- `--ticker`: Your pool ticker (ex: MYPOOL)
- `--purpose`: Wallet purpose (pledge or rewards)
- `--force`: Force regeneration of existing files
- `--simple`: Use simplified version (no external tools)
- `--quiet`: Quiet mode (JSON output)

## 🔧 Features

### Automatic generation

- ✅ Generation of 24-word recovery phrase
- ✅ Creation of required files (base_addr, reward_addr, staking_skey, staking_vkey)
- ✅ Address validation
- ✅ Multi-platform support (Linux, macOS, Windows)
- ✅ Real Cardano tools integration
- ✅ Simplified fallback mode

### Security

- 🔒 Secure key generation
- 🔒 Local storage of sensitive files
- 🔒 Integrated security instructions
- 🔒 Address validation

### Generated files

For each wallet, the CLI generates:

- `TICKER-purpose.base_addr` - Base address for pledge
- `TICKER-purpose.reward_addr` - Staking address for rewards
- `TICKER-purpose.staking_skey` - Staking private key (SENSITIVE)
- `TICKER-purpose.staking_vkey` - Staking public key
- `TICKER-purpose.mnemonic.txt` - Recovery phrase (SENSITIVE)

## 📁 Directory Structure

Wallets are stored in the user's home directory:

```
~/.CSPO_MYPOOL/
├── pledge/
│   ├── MYPOOL-pledge.base_addr
│   ├── MYPOOL-pledge.reward_addr
│   ├── MYPOOL-pledge.staking_skey
│   ├── MYPOOL-pledge.staking_vkey
│   └── MYPOOL-pledge.mnemonic.txt
└── rewards/
    ├── MYPOOL-rewards.base_addr
    ├── MYPOOL-rewards.reward_addr
    ├── MYPOOL-rewards.staking_skey
    ├── MYPOOL-rewards.staking_vkey
    └── MYPOOL-rewards.mnemonic.txt
```

## 📋 Steps after generation

1. **Import the wallet** in a compatible Cardano wallet
2. **Configure single-address mode** to ensure funds stay on the registered address
3. **Transfer ADA funds** to the base_addr address
4. **Send the files** to your stake pool operator via their secure portal

## 🔐 Security considerations

### Recovery phrase

- Store the 24-word phrase in a secure location (paper, safe)
- Never share it with anyone
- Create multiple backup copies

### Private keys

- The `staking_skey` and `payment_skey` files are sensitive
- Only share with your stake pool operator via secure connection
- Create an encrypted copy for backup

### Single-address mode

- Verify that your wallet is configured in single-address mode
- This ensures ADA funds remain on the registered address
- Funds on other addresses won't count for pledge

## 🤝 Coordination with Stake Pool Operator

1. Contact your stake pool operator for coordination
2. Discuss fixed and variable fees
3. Send generated files via their secure portal
4. Maintain wallet balance above declared level

## 🛠️ Development

### Project structure

```
cardano-spo-cli/
├── cardano_spo_cli/
│   ├── __init__.py
│   ├── cli.py
│   ├── version.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── download.py
│   │   ├── wallet.py
│   │   ├── wallet_simple.py
│   │   └── wallet_demo.py
│   └── __main__.py
├── setup.py
├── requirements.txt
└── README.md
```

### Development installation

```bash
git clone https://github.com/your-repo/cardano-spo-cli.git
cd cardano-spo-cli
pip install -e .
```

### Tests

```bash
python -m pytest tests/
```

## 🔧 Cardano Tools Integration

The CLI integrates with official Cardano tools for production use:

- **cardano-cli**: https://github.com/IntersectMBO/cardano-node
- **cardano-address**: https://github.com/IntersectMBO/cardano-addresses
- **bech32**: https://github.com/IntersectMBO/bech32

See [REAL_TOOLS.md](REAL_TOOLS.md) for detailed installation instructions.

### Modes

- **Real Tools Mode (Default)**: Uses official Cardano tools for production-ready addresses and keys
- **Simplified Mode**: Fallback option using Python-native cryptography

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For technical support:

- Email: support@cardano-spo-cli.org
- Discord: Join our Discord server

## ⚠️ Warnings

- This CLI generates sensitive private keys. Use it in a secure environment.
- Always test with small amounts before transferring significant funds.
- Rewards are paid with a two-epoch delay.
- Always maintain wallet balance above declared pledge level.
