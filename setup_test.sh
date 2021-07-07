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