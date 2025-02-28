FROM python:3.11

WORKDIR /translatepdf

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY app /translatepdf/app
COPY data /translatepdf/data
COPY logs /translatepdf/logs

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение с помощью Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]