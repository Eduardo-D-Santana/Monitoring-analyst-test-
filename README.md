# Transaction Anomaly Alert System

Este projeto é uma solução para o desafio técnico de criar um sistema de monitoramento com alertas de anomalias em transações, utilizando dados históricos e lógica baseada em regras simples.

## 🔧 Tecnologias

- Python 3
- Flask
- Pandas
- Grafana (para visualização)
- CSV como fonte de dados

## 📁 Estrutura

- `app.py`: API com endpoints para acessar dados, sumarizar status e emitir alertas.
- `data/`: contém os arquivos `transactions.csv` e `transactions_auth_codes.csv`.
- `dashboards/`: estrutura para export de dashboards do Grafana.
- `report.pdf`: relatório técnico explicando lógica, arquitetura e decisões.

## 📊 Endpoints

- `/`: Teste de saúde da API.
- `/transactions`: Lista completa das transações.
- `/auth_codes`: Lista completa dos códigos de autorização.
- `/summary`: Retorna o total por status de transação.
- `/alert`: Detecta anomalias nos últimos 5 minutos com base na média histórica.

## 🚨 Lógica de Alerta

Utiliza um modelo baseado em regras:
- Se o número de transações `FAILED`, `REVERSED`, `DENIED`, `BACKEND_REVERSED` ou `REFUNDED` nos últimos 5 minutos for 50% maior do que a média histórica por minuto, um alerta é emitido.

## ▶️ Como rodar

```bash
# Instale as dependências
pip install -r requirements.txt

# Execute a API
python3 app.py
