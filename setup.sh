export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=True

# development, production, test
export ENV='development'

alias err98="ps -fA | grep python"

# These constants are only included in this file to meet 
# Rubric specs for the project. They are handled securely with dotenv and
# After successful submission these lines will be deleted.
# export AUTH0_CLIENT_ID='1KYiQV065tmQi7513VmD3Ka6TxvNpyRl'
# export AUTH0_CLIENT_SECRET='0Qiu83PpKYeGtdQrcMTv3XA9QxWm2Oc6zNni6OwfTqJL02ZvoOgfnCE5ORARvfep'
# export AUTH0_BASE_URL='https://websecure.us.auth0.com'
# export AUTH0_AUDIENCE='casting-agency'
# export AUTH0_CALLBACK_URL='http://127.0.0.1:5000/callback'

# export DATABASE_URL=postgresql+psycopg2://kep:password@127.0.0.1:5432/casting
# export TEST_DATABASE_URL=postgresql+psycopg2://kep:password@127.0.0.1:5432/test_casting