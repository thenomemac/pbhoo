FROM python:latest
RUN pip install flask flask-bootstrap flask-wtf
COPY ./pbhoo /pbhoo/
RUN mkdir -p data
RUN mkdir -p data/result_photos
ENV FLASK_APP=pbhoo/pbhoo.py
ENV FLASK_DEBUG=1
CMD flask run --host=0.0.0.0
