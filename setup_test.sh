export ENV='test'

echo 'Drop tables'
python manage.py db downgrade
echo 'Create tables'
python manage.py db upgrade
echo 'Seed data'
python manage.py seed
echo 'Data seeded. Test starting'
python test_app.py