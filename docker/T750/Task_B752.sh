
# Меняем порт 80 -> 8080 в конфиге nginx внутри контейнера
docker exec -it nginx_test sh -c \
  "sed -ri 's/listen\s+80;/listen 8080;/; s/listen\s+\[::]:80;/listen [::]:8080;/' /etc/nginx/conf.d/default.conf && nginx -t"

# Перезапускаем контейнер
docker restart nginx_test

# Проверяем доступность по 9999 порту
curl -I http://localhost:9999

# Проверяем, что 9090 больше не работает
curl -I http://localhost:9090

# Удаляем контейнер
docker rm -f nginx_test
