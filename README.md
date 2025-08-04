# Real-Time Stock Price Streaming Pipeline

This project demonstrates a real-time data pipeline that streams stock price data from the Finnhub API into Snowflake using open-source tools and Python. It simulates real-world data engineering use cases like micro-batch ingestion, real-time processing, and warehouse integration.

## Project Overview

- Python Kafka Producer to fetch stock prices using the Finnhub API
- Kafka topic to stream the stock price data
- Spark Structured Streaming to process the data and write to CSV
- Manual upload of CSVs to a Snowflake internal stage
- SQL scripts to create target tables and load data using `COPY INTO`

## Tech Stack

| Layer             | Tool/Service             | Purpose                                  |
|------------------|--------------------------|------------------------------------------|
| Data Source       | Finnhub API              | Real-time stock price feed               |
| Ingestion         | Python + Kafka Producer  | Stream data into Kafka                   |
| Streaming Engine  | Apache Spark             | Real-time processing of Kafka stream     |
| Temporary Storage | CSV Files                | Sink for micro-batch streaming           |
| Data Warehouse    | Snowflake                | Queryable destination for final data     |

## Steps Performed

### 1. Finnhub API Key Setup
- Registered for a free API key from finnhub.io to access stock price data.

### 2. Kafka Installation and Setup
- Downloaded Kafka 2.12-3.4.1 and started both Zookeeper and Kafka servers.
- Kafka topic `stock_prices` created to serve as the messaging layer.

### 3. Kafka Producer (Python)
- Wrote a Kafka producer script using `kafka-python` that fetches stock price data in real time.
- Sends JSON-formatted messages to the `stock_prices` topic every second.

### 4. Spark Streaming Job
- Wrote a Spark Structured Streaming job to read messages from Kafka.
- Parsed the incoming JSON and wrote micro-batch CSV files to the `output/stock_prices` directory.

### 5. Snowflake Integration
- Created a target table and internal stage in Snowflake using provided SQL scripts.
- Uploaded CSVs manually through the Snowflake Web UI for simulation.
- Executed `COPY INTO` statements to load data into the Snowflake table.

## Folder Structure
```text
real-time-stock-streaming/
├── kafka_producer/
│ └── stock_price_producer.py
├── spark_streaming/
│ └── stock_stream_processor.py
├── sql/
│ ├── create_table.sql
│ ├── create_stage.sql
│ └── copy_into.sql
├── output/
│ └── stock_prices/ # Spark output (not committed)
├── jars/ # Spark-Kafka JARs (not committed)
├── .gitignore
└── README.md
```

## How to Run This Project

### Prerequisites

- Python 3.9+
- Apache Kafka 2.12-3.4.1
- Apache Spark 3.4.1
- Snowflake account
- Required JARs: Kafka-Spark integration connectors

### Steps

1. **Start Kafka and Zookeeper**

```bash
# Terminal 1
bin/windows/zookeeper-server-start.bat config/zookeeper.properties

# Terminal 2
bin/windows/kafka-server-start.bat config/server.properties
```
2. ****Create Kafka Topic****
```bash
bin/windows/kafka-topics.bat --create --topic stock_prices --bootstrap-server localhost:9092
```
3. **Run the Kafka Producer**
```bash
python kafka_producer/stock_price_producer.py
```
4. **Run the Spark Streaming Job**
```bash
spark-submit --jars "file:///path/to/spark-sql-kafka-*.jar,file:///path/to/kafka-clients-*.jar" spark_streaming/stock_stream_processor.py
```
5. **Upload CSVs to Snowflake Stage**
- Go to Snowflake Web UI → Databases → Stage
- Upload files from the output/stock_prices/ folder

6.**Run SQL Scripts**
```sql
-- Create table
CREATE OR REPLACE TABLE STOCK_PRICES (...);

-- Create internal stage
CREATE OR REPLACE STAGE stock_stage;

-- Load from stage to table
COPY INTO STOCK_PRICES FROM @stock_stage FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1);
```
**.gitignore**
```text
jars/
output/
*.log
*.csv
*.pyc
__pycache__/
kafka_producer/kafka_2.12-3.4.1/
```
<img width="1258" height="722" alt="Screenshot 2025-08-03 233535" src="https://github.com/user-attachments/assets/4ff1670a-2c5e-477c-a3fc-4c55f0786a9d" />
<img width="1083" height="643" alt="Screenshot 2025-08-03 233512" src="https://github.com/user-attachments/assets/5a7eefa6-9730-45ff-9b75-817035364f97" />
<img width="1063" height="638" alt="Screenshot 2025-08-03 233432" src="https://github.com/user-attachments/assets/64302ff5-3209-447a-b155-6cc2134fbae9" />
<img width="1049" height="645" alt="Screenshot 2025-08-03 233351" src="https://github.com/user-attachments/assets/d651ea28-6ce9-4046-8ccb-86d54b30e981" />
