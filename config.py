import os

os.environ['API_URL'] = 'https://rickandmortyapi.com/api'
os.environ['PAGE_SIZE'] = '20'

os.environ['SECRET_KEY'] = 'wubba-lubba-dub-dub'
os.environ['TOKEN_EXPIRATION'] = '3600'

os.environ['CACHE_SIZE'] = '1000'
os.environ['CACHE_TTL'] = '86400'

os.environ['TEST_USER_HASHED_PASSWORD'] = "$2b$12$uCLsfsY5mynQ0586b2.3seTvP8BVKRruVD0EyAHBfcZzJX/Y54Why"
os.environ['TEST_USER_BEARER_TOKEN'] = ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzExMzIxOTQ4fQ'
                                 '.57uddM8bRxPkOM_sh7IidIT4ICWYyw1XFsn3glGlLNg')
