
# 安装说明

## 安装依赖包
	pip install -r requirements.txt

## 初始化数据库
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

## 启动程序
	python manage.py runserver -h 0.0.0.0

