FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
# Note: The port 8501 is the default for Streamlit applications.
# The command starts the Streamlit app and binds it to all network interfaces.
