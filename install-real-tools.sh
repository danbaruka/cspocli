#!/bin/bash

# Install Real Cardano Tools Script
# This script helps install the real Cardano tools manually

set -e

echo "🔧 Installing Real Cardano Tools..."
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    print_error "Unsupported OS: $OSTYPE"
    exit 1
fi

print_status "Detected OS: $OS"

# Create tools directory
TOOLS_DIR="$HOME/.cardano_spo_cli/tools"
mkdir -p "$TOOLS_DIR"
print_status "Tools directory: $TOOLS_DIR"

# Function to download and install tool
install_tool() {
    local tool_name=$1
    local url=$2
    local filename=$3
    
    print_status "Installing $tool_name..."
    
    # Download
    if curl -L -o "$TOOLS_DIR/$filename" "$url"; then
        print_success "Downloaded $tool_name"
    else
        print_error "Failed to download $tool_name"
        return 1
    fi
    
    # Make executable (Unix only)
    if [[ "$OS" != "windows" ]]; then
        chmod +x "$TOOLS_DIR/$filename"
        print_success "Made $tool_name executable"
    fi
    
    # Test
    if "$TOOLS_DIR/$filename" --version > /dev/null 2>&1; then
        print_success "$tool_name is working"
    else
        print_warning "$tool_name installed but version test failed"
    fi
}

# Install tools based on OS
case $OS in
    "macos")
        print_status "Installing tools for macOS..."
        
        # Note: These URLs might need updating
        # Users should check the latest releases at:
        # https://github.com/IntersectMBO/cardano-node/releases
        # https://github.com/IntersectMBO/cardano-addresses/releases
        # https://github.com/IntersectMBO/bech32/releases
        
        install_tool "cardano-cli" \
            "https://github.com/IntersectMBO/cardano-node/releases/download/10.5.1/cardano-cli-macos" \
            "cardano-cli" || print_warning "cardano-cli installation failed"
            
        install_tool "cardano-address" \
            "https://github.com/IntersectMBO/cardano-addresses/releases/download/4.0.0/cardano-address-macos" \
            "cardano-address" || print_warning "cardano-address installation failed"
            
        install_tool "bech32" \
            "https://github.com/IntersectMBO/bech32/releases/download/v1.1.2/bech32-macos" \
            "bech32" || print_warning "bech32 installation failed"
        ;;
        
    "linux")
        print_status "Installing tools for Linux..."
        
        install_tool "cardano-cli" \
            "https://github.com/IntersectMBO/cardano-node/releases/download/10.5.1/cardano-cli-linux" \
            "cardano-cli" || print_warning "cardano-cli installation failed"
            
        install_tool "cardano-address" \
            "https://github.com/IntersectMBO/cardano-addresses/releases/download/4.0.0/cardano-address-linux" \
            "cardano-address" || print_warning "cardano-address installation failed"
            
        install_tool "bech32" \
            "https://github.com/IntersectMBO/bech32/releases/download/v1.1.2/bech32-linux" \
            "bech32" || print_warning "bech32 installation failed"
        ;;
        
    "windows")
        print_status "Installing tools for Windows..."
        
        install_tool "cardano-cli" \
            "https://github.com/IntersectMBO/cardano-node/releases/download/10.5.1/cardano-cli-win64.exe" \
            "cardano-cli.exe" || print_warning "cardano-cli installation failed"
            
        install_tool "cardano-address" \
            "https://github.com/IntersectMBO/cardano-addresses/releases/download/4.0.0/cardano-address-win64.exe" \
            "cardano-address.exe" || print_warning "cardano-address installation failed"
            
        install_tool "bech32" \
            "https://github.com/IntersectMBO/bech32/releases/download/v1.1.2/bech32-win64.exe" \
            "bech32.exe" || print_warning "bech32 installation failed"
        ;;
esac

echo ""
print_status "Installation completed!"
echo ""
print_status "You can now use real tools mode:"
echo "  cspocli generate --ticker MYPOOL --purpose pledge"
echo ""
print_status "Or continue using simplified mode:"
echo "  cspocli generate --ticker MYPOOL --purpose pledge --simple"
echo ""
print_warning "Note: If some tools failed to install, the CLI will automatically"
print_warning "fall back to simplified mode when needed." 