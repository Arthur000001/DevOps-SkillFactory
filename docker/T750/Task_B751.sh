
# Запуск контейнера nginx с именем nginx_test
# -d                → запуск в фоне (detached mode)
# --name nginx_test → имя контейнера
# -p 9090:80        → проброс: порт 9090 на хосте → порт 80 в контейнере
# -p 9999:8080      → проброс: порт 9999 на хосте → порт 8080 в контейнере
# --mount           → примонтировать volume
#   type=volume     → тип: volume (управляемое Docker хранилище)
#   src=nginx_logs  → имя тома (создастся автоматически, если его ещё нет)
#   dst=/var/log/nginx → путь внутри контейнера (каталог с логами nginx)
# nginx             → образ, на основе которого создаётся контейнер

docker run -d --name nginx_test \
  -p 9090:80 \
  -p 9999:8080 \
  --mount type=volume,src=nginx_logs,dst=/var/log/nginx \
  nginx
