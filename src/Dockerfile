FROM python:3.8

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv 
RUN virtualenv env -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"

WORKDIR /Payment-Scheduler/src
ADD . /Payment-Scheduler/src

RUN pip install -r requirements.txt

COPY . /Payment-Scheduler/src

ENV PORT 8501

CMD streamlit run scheduler.py 

