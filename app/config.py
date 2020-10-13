import os
import dotenv


dotenv.load_dotenv()


SSO_DOMAIN = os.getenv('SSO_DOMAIN')
SSO_SERVICE_TOKEN = os.getenv('SSO_SERVICE_TOKEN')
TEST_TOKEN = os.getenv('TEST_TOKEN')
