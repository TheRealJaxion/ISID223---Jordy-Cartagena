import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://usuario:contraseña@host/base_datos')

df_books = pd.read_sql("SELECT * FROM libros", engine)
df_accounts = pd.read_sql("SELECT * FROM personas", engine)
df_loans  = pd.read_sql("SELECT * FROM prestamos", engine)
