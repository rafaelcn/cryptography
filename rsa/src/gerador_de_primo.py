import random

lista_de_primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67, 
                     71, 73, 79, 83, 89, 97, 101, 103, 
                     107, 109, 113, 127, 131, 137, 139, 
                     149, 151, 157, 163, 167, 173, 179, 
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(numero):
  return random.randrange(2**(numero - 1) + 1, 2 ** numero - 1)

def getLowLevelPrime(numero): 
  '''Generate a prime candidate divisible
    by first primes'''
  while True:
    pc = nBitRandom(numero)
    for divisor in lista_de_primos:
      if pc % divisor == 0 and divisor**2 <= pc:
        break
      else: return pc

def teste_de_primalidade_de_miller_rabin(mrc):
  '''Run 20 iterations of Rabin Miller Primality test'''
  maxDivisionByTwo = 0
  ec = mrc - 1
  while ec %  2 == 0:
    ec >>= 1
    maxDivisionByTwo += 1
    assert(2**maxDivisionByTwo * ec == mrc - 1)
    
    def trialComposite(round_tester):
      if pow(round_tester, ec, mrc) == 1:
        return False
      for i in range(maxDivisionByTwo):
        if (pow(round_tester, 2**i * ec, mrc) == mrc - 1):
          return False
      return True
    
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
      round_tester = random.randrange(2, mrc)
      if trialComposite(round_tester):
        return False
    return True

def tamanho_de_bits(numero):
  while True:
    prime_candidate = getLowLevelPrime(numero)
    if not teste_de_primalidade_de_miller_rabin(prime_candidate):
      continue
    else: 
      return prime_candidate
    