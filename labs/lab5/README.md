# Розгортання в кластері

**1. Встановлення необхідних інструментів:**

* **Встановлення kubectl:** Дотримуйтесь інструкцій на офіційному сайті Kubernetes: [Install kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
* **Встановлення Minikube:** Дотримуйтесь інструкцій на офіційному сайті Minikube: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
  * Переконайтесь, що у вас встановлено гіпервізор (наприклад, VirtualBox, Hyper-V, Docker). Рекомендується використовувати драйвер Docker для кращої інтеграції.
  * Приклад встановлення на Windows з Docker Desktop:

    ```powershell
    # Встановлення за допомогою Chocolatey (якщо встановлено)
    choco install minikube
    # Або завантажити .exe з сайту та додати до PATH
    ```

* **Встановлення Docker:** Якщо ви не використовуєте Docker як драйвер для Minikube, вам все одно знадобиться Docker для побудови образу вашого додатку. [Install Docker](https://docs.docker.com/get-docker/)

**2. Запуск кластера Minikube:**

* Відкрийте термінал (PowerShell або CMD на Windows, Terminal на macOS/Linux).
* Запустіть кластер Minikube. Якщо ви використовуєте Docker Desktop, вкажіть драйвер docker:

    ```bash
    minikube start --driver=docker
    # Або без вказання драйвера, якщо ви хочете використати гіпервізор за замовчуванням
    # minikube start
    ```

* Перевірте статус кластера:

    ```bash
    minikube status
    kubectl cluster-info
    kubectl get nodes
    ```

    Ви повинні побачити, що кластер працює, і один вузол (`minikube`) має статус `Ready`.

**3. Побудова Docker образу:**

* Minikube має вбудований Docker daemon. Щоб використовувати його і не завантажувати образ у зовнішній реєстр, налаштуйте свій термінал:
  * **Linux/macOS:**

    ```bash
    eval $(minikube -p minikube docker-env)
    ```

  * **Windows PowerShell:**

    ```powershell
    & minikube -p minikube docker-env | Invoke-Expression
    ```

* Перебуваючи у кореневій папці проекту, побудуйте образ:

    ```bash
    docker build -t fastapi-app:latest .
    ```

* Перевірте, що образ створено у середовищі Minikube:

    ```bash
    docker images
    ```

    Ви повинні побачити образ `fastapi-app` з тегом `latest`.

**4. Розгортання додатку в Kubernetes:**

* Застосуйте всі маніфести:

    ```bash
    kubectl apply -f ./k8s
    ```

* Перевірте статус розгортання:

    ```bash
    kubectl get pods -w # Прапор -w для спостереження за змінами
    kubectl get deployments
    kubectl get services
    kubectl get pvc
    kubectl get secrets
    ```

    Дочекайтеся, поки всі Pod'и перейдуть у стан `Running`, а Deployments покажуть бажану кількість готових реплік (`READY` має дорівнювати `AVAILABLE`).

**5. Перевірка роботи додатку:**

* Отримайте URL для доступу до вашого FastAPI сервісу:

    ```bash
    minikube service fastapi-app-service
    ```

    Ця команда автоматично відкриє URL у вашому браузері.
* Перейдіть за отриманим URL. Ви повинні побачити повідомлення: `{"message": "Welcome to the FastAPI PostgreSQL CRUD API"}`.
* Додайте `/docs` до URL (наприклад, `http://<IP-адреса-Minikube>:<NodePort>/docs`), щоб відкрити Swagger UI.
* Використовуйте Swagger UI або інструмент типу `curl` чи Postman для тестування CRUD операцій:
  * **POST /items/**: Створіть новий елемент.
  * **GET /items/**: Отримайте список елементів.
  * **GET /items/{item_id}**: Отримайте конкретний елемент за ID.
  * **PUT /items/{item_id}**: Оновіть елемент.
  * **DELETE /items/{item_id}**: Видаліть елемент.

    Приклад з `curl` (замініть `<URL>` на отриманий від `minikube service`):

    ```bash
    # Створити елемент
    curl -X POST "<URL>/items/" -H "Content-Type: application/json" -d '{"name":"Test Item K8s","description":"Created via Kubernetes","price":99.99}'

    # Отримати всі елементи
    curl -X GET "<URL>/items/"

    # Отримати елемент з ID=1 (якщо він існує)
    curl -X GET "<URL>/items/1"
    ```

**6. Перегляд логів та налагодження (за потреби):**

* Якщо щось не працює, перевірте логи Pod'ів:

    ```bash
    # Список Pod'ів
    kubectl get pods

    # Логи FastAPI Pod'а (замініть <fastapi-pod-name> на реальне ім'я)
    kubectl logs <fastapi-pod-name>

    # Логи PostgreSQL Pod'а (замініть <postgres-pod-name> на реальне ім'я)
    kubectl logs <postgres-pod-name>
    ```

* Перевірте опис ресурсів для деталей конфігурації та подій:

    ```bash
    kubectl describe pod <pod-name>
    kubectl describe deployment <deployment-name>
    kubectl describe service <service-name>
    ```

**7. Очищення ресурсів:**

* Видаліть всі створені ресурси Kubernetes:

    ```bash
    kubectl delete -f ./k8s
    ```

* Зупиніть кластер Minikube:

    ```bash
    minikube stop
    ```

* (Опціонально) Видаліть кластер Minikube, щоб звільнити ресурси:

    ```bash
    minikube delete
    ```

* Не забудьте вимкнути перенаправлення Docker daemon Minikube (якщо використовували `eval`):
  * **Linux/macOS:**

    ```bash
    eval $(minikube docker-env -u)
    ```

  * **Windows PowerShell:**

    ```powershell
    & minikube docker-env -u | Invoke-Expression
    ```
