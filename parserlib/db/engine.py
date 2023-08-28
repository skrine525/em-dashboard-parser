from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from parserlib import config


# URL Базы данныз MySQL
DATABASE_URL = f"mysql+pymysql://{config.SQL_USERNAME}:{config.SQL_PASSWORD}@{config.SQL_HOST}/{config.SQL_DATABASE}"
#DATABASE_URL = "mysql+pymysql://dashboardadmin:powerpower@10.107.111.72/dashboard"

# Инициализация движка и sessiomaker-класса этого движка
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
