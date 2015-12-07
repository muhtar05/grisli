Тестовый проект

Для реализации данного задания я использовал связку "Nginx+Tornado+Django", хотя изначально запускал Nginx+Gunicorn+Django, а Tornado как отдельный сервер. Но в итоге решил , что Django лучше запускать через Tornado и реализуется это легко с помощью WSGIContainer.

Конфигурация для Nginx находится в файле default.d , а Tornado+Django запускаются с помощью команды

python tornado_app.py

