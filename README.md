# OPanaTracker



## Развертывание приложения  

Установить docker  
>Если Docker не работает, включить виртуализацию  
>(панель управления - программы и компоненты - компоненты Windows - включить Hyper-V)

Из ./backend

    docker-compose up 
    docker-compose run opana_web python manage.py makemigrations   
    docker-compose run opana_web python manage.py migrate     
    docker-compose run opana_web python manage.py createsuperuser   

## Подключение к базе данных:   
**port**: 33066  
**user**: root  
**password**: root   
**Database**: mysql   

## Подключение к серверу  
<http://127.0.0.1:8000/>
