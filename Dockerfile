#�����������python:3.7
FROM python:3.7

ENV PYTHONIOENCODING=utf-8

#工作目录
WORKDIR  ./Arabidopsis.tf.pred

#复制文件到容器
ADD . .

#安装nginx
RUN sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update
# RUN apt-get install -y nginx 

#安装python依赖
RUN pip install setuptools
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com


# #setup nginx
# RUN rm /etc/nginx/sites-enabled/default
# COPY nginx_flask.conf /etc/nginx/sites-available/
# RUN ln -s /etc/nginx/sites-available/nginx_flask.conf /etc/nginx/sites-enabled/
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf


#EXPOSE 9810 
#容器启动时运行shell脚本，启动gunicorn和nginx
# RUN chmod +x ./run.sh
CMD [ "python", "./app.py" ] 




