#!/bin/sh
# Шаг 1. Запуск контейнера nginx с volume-монтом

docker run -d -p 9000:80 \
  --mount type=volume,dst=/usr/share/nginx/html/ \
  --name nginx_volume_test \
  nginx
# docker run — запуск нового контейнера.
#   -d → запуск в фоновом режиме.
#   -p 9000:80 → проброс портов: на хосте порт 9000, в контейнере порт 80.
#   --mount type=volume → монтируем volume.
#       • src не указан → Docker автоматически создаст volume с произвольным именем.
#       • dst=/usr/share/nginx/html/ → в этот каталог в контейнере (где лежит index.html nginx) будет подключён volume.
#   --name nginx_volume_test → задаём имя контейнера (чтобы потом проще находить и управлять им).
#   nginx → образ контейнера.

# Шаг 2. Проверка, что контейнер запущен
docker ps
# Покажет список работающих контейнеров. Должен быть контейнер nginx с портом 9000→80.

# Шаг 3. Определяем имя созданного volume
docker volume ls
# Эта команда показывает все volumes, созданные Docker.
# В списке будет volume без имени, связанный с контейнером nginx_volume_test.

# Шаг 4. Узнаём путь к каталогу volume
# Обычно volume хранится по пути:
#   /var/lib/docker/volumes/<имя volume>/_data/
# Там лежат файлы, которые контейнер видит в /usr/share/nginx/html.

# Шаг 5. Проверка содержимого index.html
# Переходим в каталог volume и смотрим файлы:
# (подставь имя volume вместо <имя_volume>)
cd /var/lib/docker/volumes/<имя_volume>/_data/
ls -l
cat index.html
# Здесь ты увидишь дефолтный index.html от nginx.

# Шаг 6. Изменение содержимого
echo "Hello from Docker Volume!" > index.html
# Перезаписываем index.html внутри volume.
# Теперь nginx будет отдавать новый текст.

# Шаг 7. Проверка в браузере
# Открой http://localhost:9000 → страница обновится и покажет новый текст.
