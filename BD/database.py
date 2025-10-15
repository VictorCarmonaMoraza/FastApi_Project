import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre de la base de datos
sqliteName = 'movies.sqlite'

# Ruta de la base de datos
base_dir = os.path.dirname(os.path.realpath(__file__))
# Crear la base de datos si no existe
databaseUrl = f'sqlite:///{os.path.join(base_dir, sqliteName)}'

# Crear el motor de la base de datos
engine = create_engine(databaseUrl, echo=True)


# Crear la sesión
Session = sessionmaker(bind=engine)

Base = declarative_base()
