### ================================ Base implementation for Tutorial 7 ================= ###
### ====================== Implements Point addition and Scalar Multiplication ========== ###

from dataclasses import dataclass
from re import I
from random import randint
import hashlib
import sys
sys.path.insert(0, '../../lab2/python/Symmetric_Cipher')
import symmetric_cipher as sc

@dataclass
class PrimeGaloisField:
    prime: int

    def __contains__(self, field_value: "FieldElement") -> bool:
        return 0 <= field_value.value < self.prime


@dataclass
class FieldElement:
    value: int
    field: PrimeGaloisField

    def __repr__(self):
        return "0x" + f"{self.value:x}".zfill(64)
        
    @property
    def P(self) -> int:
        return self.field.prime
    
    def __add__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value + other.value) % self.P,
            field=self.field
        )
    
    def __sub__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value - other.value) % self.P,
            field=self.field
        )

    def __rmul__(self, scalar: int) -> "FieldValue":
        return FieldElement(
            value=(self.value * scalar) % self.P,
            field=self.field
        )

    def __mul__(self, other: "FieldElement") -> "FieldElement":
        return FieldElement(
            value=(self.value * other.value) % self.P,
            field=self.field
        )
        
    def __pow__(self, exponent: int) -> "FieldElement":
        return FieldElement(
            value=pow(self.value, exponent, self.P),
            field=self.field
        )

    def __truediv__(self, other: "FieldElement") -> "FieldElement":
        other_inv = other ** -1
        return self * other_inv


@dataclass
class EllipticCurve:
    a: int
    b: int

    field: PrimeGaloisField

    def __contains__(self, point: "ECCPoint") -> bool:
        x, y = point.x, point.y
        return y ** 2 == x ** 3 + self.a * x + self.b

    def __post_init__(self):
        # Encapsulate the int parameters in FieldElement
        self.a = FieldElement(self.a, self.field)
        self.b = FieldElement(self.b, self.field)

        # Whether the members of the curve parameters are in the field
        if self.a not in self.field or self.b not in self.field:
            raise ValueError

inf = float("inf")

# Representing an ECC Point using the curve equation y??2 = x??3 + ax + b
@dataclass
class ECCPoint:
    x: int
    y: int

    curve: EllipticCurve

    def __post_init__(self):
        if self.x is None and self.y is None:
            return
        
        # Encapsulate x and y in FieldElement
        self.x = FieldElement(self.x, self.curve.field)
        self.y = FieldElement(self.y, self.curve.field)

        # Ensure the ECCPoint satisfies the curve equation
        if self not in self.curve:
            raise ValueError

    ##  ======== Point addition P1 + P2 = P3 ============== ##
    def __add__(self, other):
        if self == I:                       # I + P2 = P2
            return other

        if other == I:
            return self                     # P1 + I = P1

        if self.x == other.x and self.y == (-1 * other.y):
            return I                        # P + (-P) = I

        if self.x != other.x:
            x1, x2 = self.x, other.x
            y1, y2 = self.y, other.y

            out = (y2 - y1) / (x2 - x1)
            x3 = out ** 2 - x1 - x2
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

        if self == other and self.y == inf:
            return I

        if self == other:
            x1, y1, a = self.x, self.y, self.curve.a

            out = (3 * x1 ** 2 + a) / (2 * y1)
            x3 = out ** 2 - 2 * x1
            y3 = out * (x1 - x3) - y1

            return self.__class__(
                x = x3.value,
                y = y3.value,
                curve = curve256k1
            )

    ##  ======== Scalar Multiplication x * P1 = P1 ============== ##
    def __rmul__(self, scalar: int) -> "ECCPoint":
        inPoint = self
        outPoint = I

        while scalar:
            if scalar & 1:
                outPoint = outPoint + inPoint
            inPoint = inPoint + inPoint
            scalar >>= 1
        return outPoint

def generate_hash(plaintext):
    h = hashlib.new('sha256')
    h.update(plaintext.encode('utf-8'))
    return int(h.hexdigest(), base=16)

# Using the secp256k1 elliptic curve equation: y??2 = x??3 + 7
# Prime of the finite field
# Necessary parameters for the cryptographic operations
P: int = (
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

field = PrimeGaloisField(prime=P)

A: int = 0
B: int = 7

curve256k1 = EllipticCurve(
    a=A,
    b=B,
    field=field
)   

I = ECCPoint(x = None, y = None, curve = curve256k1)    # where I is a point at Infinity

# Generator point of the chosen group
G = ECCPoint(
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve = curve256k1
)

# Order of the group generated by G, such that nG = I
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


## ==================== Start your implementation below this line ============================== ##
## ==================== Feel free to pull the parameters into another file if you wish ========= ##
## ==================== If you notice any bugs, kindly draw our attention to it ================ ##

# master sercret key x and public key P_pub
x = randint(0, q)
P_pub = G.__rmul__(x) 

# secret key x_i each user
x_Alice = randint(0, q)
x_Bob = randint(0, q)

# Public key P_pub_i each user
P_pub_Alice = G.__rmul__(x_Alice)
P_pub_Bob = G.__rmul__(x_Bob)

# Partial private key R_i
r_Alice = randint(0, q)
R_Alice = G.__rmul__(r_Alice)
r_Bob = randint(0, q)
R_Bob = G.__rmul__(r_Bob)

# Partial private key d_i
ID_Alice = 'ID_Alice'
ID_Bob = 'ID_Bob'
d_Alice = r_Alice + x * generate_hash(f'{ID_Alice},{R_Alice},{P_pub_Alice}')
d_Bob = r_Bob + x * generate_hash(f'{ID_Bob},{R_Bob},{P_pub_Bob}')

# Full private key SK_i
SK_Alice = (d_Alice, x_Alice)
SK_Bob = (d_Bob, x_Bob)

# Full public key PK_i
PK_Alice = (R_Alice, P_pub_Alice)
PK_Bob = (R_Bob, P_pub_Bob)

## ============ Initialize the secure communication channel
## ============ Encryption and Encapsualtion - Alice's side

l_Alice = randint(0, q)
h_Alice = randint(0, q)
U = G.__rmul__(l_Alice)
V = G.__rmul__(h_Alice)

Y = P_pub_Bob.__add__(R_Bob.__add__(P_pub.__rmul__(generate_hash(f'{ID_Bob},{R_Bob},{P_pub_Bob}'))))
T = Y.__rmul__(h_Alice)

# Session key K_AB
K_AB = generate_hash(f'{Y},{V},{T},{ID_Bob},{P_pub_Bob}')

# Encrypting with AES using session key K_AB
plaintext = 'Security Protocol'
iv, ciphertext = sc.encrypt(plaintext, bytes.fromhex(hex(K_AB)[2:]))
C_AB = ciphertext

# Encapsulating K_AB and ciphertext C_AB
H = generate_hash(f'{U},{C_AB},{T},{ID_Alice},{ID_Bob},{P_pub_Alice},{P_pub_Bob}')
W = d_Alice + l_Alice * H + x_Alice * H
phi = (U, V, W)

## =============== Decapsulation and Decryption - Bob's side

# Retrieving Y and T from Alice's side
Y_prime = G.__rmul__(d_Bob + x_Bob)
T_prime = V.__rmul__(d_Bob + x_Bob)

assert Y_prime == Y, 'Y should equal Y_prime'
print(f'Encapsulated Y: {Y}')
print(f'Decapsulated Y: {Y_prime}')

assert T_prime == T, 'T should equal T_prime'
print('=====================')
print(f'Encapsulated T: {T}')
print(f'Decapsulated T: {T_prime}')

# Retrieving session key K_AB from Alice's side
H_prime = generate_hash(f'{U},{C_AB},{T_prime},{ID_Alice},{ID_Bob},{P_pub_Alice},{P_pub_Bob}')
K_AB_prime = generate_hash(f'{Y_prime},{V},{T_prime},{ID_Bob},{P_pub_Bob}')
assert K_AB_prime == K_AB, 'K_AB should equal K_AB_prime'

# Decrypting with AES using session key K_AB_prime
decrypted_text = sc.decrypt(iv, C_AB, bytes.fromhex(hex(K_AB_prime)[2:]))
assert decrypted_text == plaintext, 'decrypted text should same as the plaintext'
print('=====================')
print(f'Plaintext: {plaintext}')
print(f'Ciphertext: {ciphertext}')
print(f'Decrypted text: {decrypted_text}')
