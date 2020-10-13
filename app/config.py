import os
import dotenv


dotenv.load_dotenv()


SSO_DOMAIN = os.getenv('SSO_DOMAIN')
SSO_SERVICE_TOKEN = os.getenv('SSO_SERVICE_TOKEN')

TEST_TOKEN = os.getenv('TEST_TOKEN')

TEST_ACCOUNTS = [
    {
        "username": "zone1-user@kwg-ad2.devebs.net",
        "password": "Admintest1",
    },
    {
        "username": "zone1-simple@kwg-ad2.devebs.net",
        "password": "Admintest1",
    },
    {
        "username": "zone2-user@kwg-ad2.devebs.net",
        "password": "Admintest1",
    }
]
