## Encryption/decryption script
A script to simulate the generation of keys and encryption/decryption a number by them.

## Usage
This script requires python 3. version.
To run it, type:
```bash
python main.py
```
### Menu commands and their purposes
Select 1st prime
:	User chooses first prime number being a part of private key
Select 2nd prime
:	User chooses second prime number being a part of private key
elect parameter `e`
:	User chooses the value for a part of public key usually denoted by `e`
Encrypt number
:	User types the value he wants to encrypt
Decrypt number
:	User types the value he wants to decrypt
Brute force guess
:	Simulating the brute force attack to find the value before encryption (this simulation can take noticeably long time)
Show public values
:	It gives the values for public key
Show private values
:	It gives the values for public key

## TODOs:
- Implement elliptic-curve cryptography (ECC) class and methods.


## Important notice
THIS SCRIPT IS DESIGNED FOR LEARNING ON E.G. COURSES ONLY
AND IT IS ILL-ADVISED TO USE IT FOR PRIVATE OR BUSINESS PURPOSES.
THE LENGTH OF KEYS IS SMALL (LIKE 16 bit) AND CAN BE HACKED EASILY WHAT CAN BE SEEN BY RUNNING E.G.:
```python
crypto.brute_force_hack(encrypted_value)
```

