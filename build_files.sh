
echo " BUILD START"
python install -r requirements.txt
python manage.py collectstatic  --noinput --clear
echo " BUILD END"