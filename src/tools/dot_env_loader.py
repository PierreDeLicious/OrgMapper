import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
lkd_user = os.environ.get('LINKEDIN_USER')
lkd_pwd = os.environ.get('LINKEDIN_PWD')
