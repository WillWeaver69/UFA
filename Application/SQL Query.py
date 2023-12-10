from sqlalchemy import create_engine

# Replace with your own connection details
username = 'root'
password = 'password'
host = 'localhost'
database = 'timeseries'

# Create a connection to the MySQL database
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}/{database}')
