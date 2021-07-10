# export AUTH0_BASE_URL='https://websecure.us.auth0.com'
# export AUTH0_AUDIENCE='casting-agency'
# export AUTH0_CLIENT_ID='1KYiQV065tmQi7513VmD3Ka6TxvNpyRl'
# export AUTH0_CLIENT_SECRET='0Qiu83PpKYeGtdQrcMTv3XA9QxWm2Oc6zNni6OwfTqJL02ZvoOgfnCE5ORARvfep'
# export AUTH0_CALLBACK_URL='http://127.0.0.1:5000/callback'

export ENV='test'
export TEST_DATABASE_URL=postgresql+psycopg2://kep:password@127.0.0.1:5432/test_casting

echo 'Drop tables'
python manage.py db downgrade
echo 'Create tables'
python manage.py db upgrade
echo 'Seed data'
python manage.py seed
echo 'Data seeded. Test starting'
python test_app.py