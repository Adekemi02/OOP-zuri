from token_auth import create_app
import os


app = create_app()

# config.py or your app's configuration file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_URI')


if __name__=="__main__":
    app.run(debug=False)