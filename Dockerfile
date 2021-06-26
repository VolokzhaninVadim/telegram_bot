FROM python
LABEL maintainer="Volokzhanin Vadim"

################# Устанавливаем часовой пояс ##############
ENV TZ=Asia/Vladivostok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update && apt-get install -y tzdata \
    && apt-get autoremove -y \ 
    && apt-get clean all 

################# Устанавливаем пакеты ###################
ADD requirements.txt requirements.txt
RUN pip install --upgrade pip \ 
     && pip install -r requirements.txt

################ Создаем папку и копируем туда настройки ####
WORKDIR .
COPY app.py /app.py

# Запускаем
CMD python app.py

