# TODO replace this script with more secure and portable 12factor app config
mkdir -p data
mkdir -p data/result_photos

export FLASK_APP=pbhoo/pbhoo.py
export FLASK_DEBUG=1
flask run
