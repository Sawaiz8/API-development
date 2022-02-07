from passlib.context import CryptContext

#We use passlib's function to encrypt passwords and brcypt is the hashing fucntion name
pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = "auto")

def hasher(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    #pwd_context allows us to verify the hashed and plain password wiht bcrypt
    return pwd_context.verify(plain_password, hashed_password)