class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://healthcare_user:12345678@127.0.0.1:5432/healthcare_db'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True