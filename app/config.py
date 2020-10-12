import os
import dotenv


dotenv.load_dotenv()


SSO_DOMAIN = os.getenv('SSO_DOMAIN')
SSO_SECRET = os.getenv('SSO_SECRET')
