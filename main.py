from bip_utils import Bip39SeedGenerator, Bip39MnemonicValidator, Bip84, Bip84Coins, Bip44Changes, P2WPKHAddr
from mnemonic import Mnemonic

# Define your mnemonic
mnemonic_words = "apple banana cherry dog elephant frog guitar house igloo jelly kite lemon mango nest orange pear queen rabbit sun tiger umbrella violin wolf xylophone"

# Input your known public address
known_public_address = "<your address goes here>"

# Define the number of addresses to check for a match
addressesToCheckLimit = 100

# Define the length of the mnemonic
mnemonicLength = 24

# There are 2048 words in the BIP39 list that we need to try
mnemonic_obj = Mnemonic("english")
word_list = mnemonic_obj.wordlist

# Validate each word in passphrase is valid mnemonic
mnemonic_words_list = mnemonic_words.split()
for i, word in enumerate(mnemonic_words_list, 1):
    if word not in word_list:
        raise ValueError(f"Invalid word found at position {i}: '{word}'. Please check for typos.")

print("All provided words are valid.")
print(f"Known mnemonic: {mnemonic_words}")

wordsTriedCount = 0
validMnemonicsCount = 0

found = False
# Iterate through all possible positions
for position in range(mnemonicLength):
    for word in word_list:
        wordsTriedCount += 1
        if wordsTriedCount % 1000 == 0:
            print(f"Words tried: {wordsTriedCount}, Valid mnemonics: {validMnemonicsCount}")

        # Insert the candidate word at the current position
        mnemonic_candidate_list = mnemonic_words_list[:position] + [word] + mnemonic_words_list[position:]
        mnemonic_candidate = " ".join(mnemonic_candidate_list)

        # Validate the candidate mnemonic
        try:
            Bip39MnemonicValidator().Validate(mnemonic_candidate)
            validMnemonicsCount += 1
        except Exception as e:
            continue

        # Generate the seed from the candidate mnemonic
        try:
            seed_generator = Bip39SeedGenerator(mnemonic_candidate)
            seed_bytes = seed_generator.Generate()
        except Exception as e:
            print(f"Error generating seed: {e}")
            continue

        # Derive the master key and account (BIP84 for Bitcoin - Native SegWit Bech32)
        try:
            bip84_mst_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
        except Exception as e:
            print(f"Error creating BIP84 context: {e}")
            continue

        # Generate and compare SegWit (Bech32) addresses using BIP-84 path
        for i in range(addressesToCheckLimit):  # Check first 20 addresses
            bip84_acc_ctx = bip84_mst_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
            try:
                generated_address = P2WPKHAddr.EncodeKey(bip84_acc_ctx.PublicKey().RawCompressed().ToBytes(), hrp="bc")

                # Compare with the known public address
                if generated_address == known_public_address:
                    print(f"Match found! The missing word is: {word}")
                    print(f"Position of missing word: {position + 1}")
                    print(f"Full mnemonic: {mnemonic_candidate}")
                    found = True
                    break
            except Exception as e:
                print(f"Error generating address: {e}")
                continue

        if found:
            break

    if found:
        break

print(f"\nTotal words tried: {wordsTriedCount}")
print(f"Total valid mnemonics: {validMnemonicsCount}")

if not found:
    print("No matching address found. Try increasing the range or checking other address formats.")