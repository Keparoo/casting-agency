export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=True

# development, production, test
export ENV='development'

export AUTH0_CLIENT_ID=
export AUTH0_DOMAIN='websecure.us.auth0.com'
export API_AUDIENCE = 'casting-agency'

alias err98="ps -fA | grep python"

export NEW_DATABASE_URL=postgresql+psycopg2://kep:password@127.0.0.1:5432/casting
export TEST_DATABASE_URL=postgresql+psycopg2://kep:password@127.0.0.1:5432/test_casting