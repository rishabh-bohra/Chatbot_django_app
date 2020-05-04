FROM centos
RUN yum install python36 -y
RUN yum install git -y
#RUN yum install epel-release -y
#RUN yum repolist
#RUN yum install python-pip -y
RUN git clone https://github.com/rishabh-bohra/chatbot_django_app.git
#RUN easy_install-3.6 pip 
RUN python3 ./chatbot_django_app/get-pip.py
RUN pip3 install -r ./chatbot_django_app/chat_app/requirements.txt
RUN pip3 install bs4
EXPOSE 8000
CMD python3 ./chatbot_django_app/chat_app/manage.py runserver 0.0.0.0:8000
