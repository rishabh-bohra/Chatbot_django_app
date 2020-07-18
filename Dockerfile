FROM centos

ARG user=ris
ARG group=ris

RUN groupadd  ${group} \
    && useradd -g ${group} -s /bin/bash  ${user}
    
RUN yum install python36 -y
RUN yum install git -y
RUN git clone https://github.com/rishabh-bohra/chatbot_django_app.git
RUN python3 ./chatbot_django_app/get-pip.py
RUN pip3 install -r ./chatbot_django_app/chat_app/requirements.txt
RUN pip3 install bs4
EXPOSE 8000
USER ${user}
CMD python3 ./chatbot_django_app/chat_app/manage.py runserver 0.0.0.0:8000
