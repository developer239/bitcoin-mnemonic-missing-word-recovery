### Disclaimer

I wrote this script to help my friend recover his lost Bitcoin. I do not endorse or promote the use of cryptocurrencies in any way.

# Bitcoin Mnemonic Missing Word Recovery

This project helps recover a missing word from a 24-word (12-word) Bitcoin mnemonic phrase. It can find the missing word regardless of its position in the mnemonic.

## Prerequisites

- Python 3.7 or higher
- Conda (for environment management)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/developer239/bitcoin-mnemonic-missing-word-recovery.git
   cd bitcoin-mnemonic-missing-word-recovery
   ```

2. Create and activate the Conda environment:
   ```
   conda env create -f environment.yml
   conda activate bitcoin-mnemonic-missing-word-recovery
   ```

## Usage

1. Open the `main.py` file in a text editor.

2. Replace the `mnemonic_words` variable with your 23 known words. Make sure to separate them with spaces:
   ```python
   mnemonic_words = "your 23 words go here separated by spaces"
   ```

3. Replace `<your address goes here>` with your actual Bitcoin address:
   ```python
   known_public_address = "your_actual_bitcoin_address"
   ```

4. Save the file and run the script:
   ```
   python main.py
   ```

5. The script will attempt to find the missing word by trying all possible words in all positions. This process may take a while.

6. If a match is found, the script will display the missing word, its position, and the complete mnemonic.

```bash
Match found! The missing word is: <your missing word>
Position of missing word: <position of missing word>
Full mnemonic: <full mnemonic>
```

## Notes

- This script checks the first 100 addresses derived from each potential mnemonic. If your address is beyond the first 100, you may need to increase this number in the script.
- The script uses the BIP84 derivation path for Native SegWit (Bech32) addresses. If your wallet uses a different derivation path, you may need to modify the script accordingly.
- Always exercise caution when dealing with mnemonic phrases and private keys. Run this script on a secure, offline computer if possible.
