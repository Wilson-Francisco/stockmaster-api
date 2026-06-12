import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


# Carrega as configuracaoes secretas do arquivo .env
load_dotenv()