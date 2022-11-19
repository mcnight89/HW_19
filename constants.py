from config import Config

PWD_HASH_SALT = b'secret here'
PWD_HASH_ITERATIONS = 100_000
JWT_SECRET = Config().SECRET_HERE
JWT_ALGORITHM = 'HS256'