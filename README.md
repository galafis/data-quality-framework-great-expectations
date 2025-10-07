# Enterprise Data Quality Framework with Great Expectations

![Great Expectations](https://img.shields.io/badge/Great%20Expectations-FF6138?style=for-the-badge&logo=great-expectations&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Data Quality](https://img.shields.io/badge/Data_Quality-00C853?style=for-the-badge)

---

## 🇧🇷 Framework Empresarial de Qualidade de Dados com Great Expectations

Framework completo e profissional para **gestão de qualidade de dados** utilizando **Great Expectations**. Implementa validações automatizadas, profiling, documentação viva e integração com pipelines de dados modernos.

### 🎯 Objetivo

Estabelecer uma cultura de **Data Quality** em organizações, garantindo que dados sejam confiáveis, precisos e bem documentados em todos os estágios do pipeline, desde ingestão até consumo por analytics e ML.

### 🌟 Por que Great Expectations?

Great Expectations é o padrão da indústria para qualidade de dados:

| Aspecto | Sem Great Expectations | Com Great Expectations |
|---------|------------------------|------------------------|
| **Validações** | Scripts SQL ad-hoc | Expectativas declarativas |
| **Documentação** | Desatualizada ou inexistente | Gerada automaticamente |
| **Profiling** | Manual e demorado | Automatizado |
| **Alertas** | Monitoramento reativo | Proativo e configurável |
| **Colaboração** | Difícil | Data Docs compartilháveis |
| **Manutenção** | Alto esforço | Baixo esforço |

### 📊 Casos de Uso Reais

1. **E-commerce**: Validar integridade de transações e inventário
2. **Fintech**: Garantir conformidade regulatória (SOX, GDPR)
3. **Healthcare**: Validar dados de pacientes (HIPAA compliance)
4. **SaaS**: Monitorar qualidade de dados de eventos de produto
5. **Data Warehouses**: Validar dados antes de carregar em produção

### 🏗️ Arquitetura do Framework

```
┌─────────────────────────────────────────┐
│         DATA SOURCES                    │
│  - Databases, APIs, Files               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    GREAT EXPECTATIONS VALIDATION        │
│  - Expectation Suites                   │
│  - Checkpoints                          │
│  - Data Profiling                       │
└──────────────┬──────────────────────────┘
               │
               ├──────► ✅ PASS → Continue Pipeline
               │
               └──────► ❌ FAIL → Alert & Stop
                              │
                              ▼
                    ┌──────────────────┐
                    │   DATA DOCS      │
                    │  (Documentation) │
                    └──────────────────┘
```

### 📂 Estrutura do Repositório

```
data-quality-framework-great-expectations/
├── great_expectations/
│   ├── expectations/
│   │   ├── sales_data_suite.json         # Suite de vendas
│   │   ├── customer_data_suite.json      # Suite de clientes
│   │   └── product_data_suite.json       # Suite de produtos
│   ├── checkpoints/
│   │   ├── daily_validation.yml          # Validação diária
│   │   └── pre_warehouse_load.yml        # Pré-carga DW
│   ├── plugins/
│   │   └── custom_expectations/
│   │       └── expect_column_to_be_email.py
│   └── great_expectations.yml            # Configuração principal
├── notebooks/
│   ├── 01_create_expectations.ipynb      # Criar expectativas
│   ├── 02_validate_data.ipynb            # Validar dados
│   └── 03_integrate_airflow.ipynb        # Integração Airflow
├── data/
│   ├── sample_sales.csv                  # Dados de exemplo
│   └── sample_customers.csv
├── src/
│   ├── validate_data.py                  # Script de validação
│   ├── profile_data.py                   # Profiling automatizado
│   └── airflow_integration.py            # Integração com Airflow
├── tests/
│   └── test_custom_expectations.py       # Testes unitários
├── requirements.txt
└── README.md
```

### 🚀 Instalação e Configuração

#### 1. Instalar Great Expectations

```bash
# Via pip
pip install great-expectations

# Verificar instalação
great_expectations --version
```

#### 2. Inicializar Projeto

```bash
# Criar novo projeto
great_expectations init

# Estrutura criada:
# great_expectations/
#   ├── expectations/
#   ├── checkpoints/
#   ├── plugins/
#   └── great_expectations.yml
```

#### 3. Configurar Data Source

```python
import great_expectations as gx

# Criar contexto
context = gx.get_context()

# Adicionar data source (Pandas)
datasource = context.sources.add_pandas("my_datasource")

# Adicionar data asset
data_asset = datasource.add_csv_asset(
    name="sales_data",
    filepath_or_buffer="data/sales.csv"
)

# Adicionar batch definition
batch_definition = data_asset.add_batch_definition_whole_dataframe("sales_batch")
```

### 💻 Criando Expectation Suites

#### Exemplo 1: Validação de Vendas

```python
import great_expectations as gx
import pandas as pd

# Carregar contexto
context = gx.get_context()

# Criar expectation suite
suite = context.add_expectation_suite("sales_data_suite")

# Definir expectativas
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="sales_data_suite"
)

# Expectativa 1: Colunas obrigatórias
validator.expect_table_columns_to_match_ordered_list(
    column_list=[
        "order_id",
        "customer_id",
        "order_date",
        "amount",
        "status"
    ]
)

# Expectativa 2: order_id único
validator.expect_column_values_to_be_unique(
    column="order_id"
)

# Expectativa 3: amount positivo
validator.expect_column_values_to_be_between(
    column="amount",
    min_value=0,
    max_value=1000000
)

# Expectativa 4: status válido
validator.expect_column_values_to_be_in_set(
    column="status",
    value_set=["pending", "processing", "shipped", "delivered", "cancelled"]
)

# Expectativa 5: order_date não nulo
validator.expect_column_values_to_not_be_null(
    column="order_date"
)

# Expectativa 6: customer_id existe na tabela customers
validator.expect_column_values_to_match_regex(
    column="customer_id",
    regex="^CUST[0-9]{6}$"
)

# Salvar suite
validator.save_expectation_suite(discard_failed_expectations=False)
```

#### Exemplo 2: Validação de Clientes

```python
# Criar suite para clientes
suite = context.add_expectation_suite("customer_data_suite")

validator = context.get_validator(
    batch_request=customer_batch_request,
    expectation_suite_name="customer_data_suite"
)

# Email válido
validator.expect_column_values_to_match_regex(
    column="email",
    regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Idade entre 18 e 120
validator.expect_column_values_to_be_between(
    column="age",
    min_value=18,
    max_value=120
)

# País em lista válida
validator.expect_column_values_to_be_in_set(
    column="country",
    value_set=["US", "UK", "CA", "BR", "DE", "FR"]
)

# Sem duplicatas de email
validator.expect_column_values_to_be_unique(
    column="email"
)

validator.save_expectation_suite()
```

### ✅ Executando Validações com Checkpoints

```python
# Criar checkpoint
checkpoint = context.add_checkpoint(
    name="daily_sales_validation",
    validations=[
        {
            "batch_request": {
                "datasource_name": "my_datasource",
                "data_asset_name": "sales_data",
                "batch_definition_name": "sales_batch"
            },
            "expectation_suite_name": "sales_data_suite"
        }
    ]
)

# Executar checkpoint
results = checkpoint.run()

# Verificar resultados
if results["success"]:
    print("✅ Validation PASSED!")
else:
    print("❌ Validation FAILED!")
    print(results)
```

### 📊 Profiling Automatizado

```python
import great_expectations as gx

# Criar contexto
context = gx.get_context()

# Carregar dados
df = pd.read_csv("data/sales.csv")

# Criar profiler
profiler = context.sources.pandas_default.read_csv(
    "data/sales.csv"
).get_validator()

# Gerar expectativas automaticamente
profiler.expect_column_values_to_not_be_null(column="order_id")
profiler.expect_column_values_to_be_unique(column="order_id")

# Para todas as colunas numéricas
for col in df.select_dtypes(include=['number']).columns:
    profiler.expect_column_values_to_be_between(
        column=col,
        min_value=df[col].min(),
        max_value=df[col].max()
    )

# Salvar suite gerada
profiler.save_expectation_suite("auto_generated_suite")
```

### 🔗 Integração com Apache Airflow

```python
# airflow_integration.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import great_expectations as gx

def validate_data_quality(**context):
    """
    Valida qualidade de dados usando Great Expectations
    """
    # Carregar contexto
    ge_context = gx.get_context()
    
    # Executar checkpoint
    checkpoint_result = ge_context.run_checkpoint(
        checkpoint_name="daily_sales_validation"
    )
    
    # Verificar resultado
    if not checkpoint_result["success"]:
        raise ValueError("Data quality validation failed!")
    
    return "Data quality validation passed!"

# Definir DAG
with DAG(
    'data_quality_pipeline',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    # Task de validação
    validate_task = PythonOperator(
        task_id='validate_data_quality',
        python_callable=validate_data_quality
    )
    
    # Outras tasks...
    # extract_task >> transform_task >> validate_task >> load_task
```

### 📈 Expectativas Customizadas

```python
# plugins/custom_expectations/expect_column_to_be_email.py

from great_expectations.expectations.expectation import ColumnMapExpectation
import re

class ExpectColumnValuesToBeValidEmail(ColumnMapExpectation):
    """
    Expectativa customizada para validar emails
    """
    
    map_metric = "column_values.match_regex"
    success_keys = ("regex",)
    
    default_kwarg_values = {
        "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "mostly": 1.0
    }
    
    library_metadata = {
        "maturity": "production",
        "tags": ["email", "validation"],
        "contributors": ["@galafis"]
    }

# Usar expectativa customizada
validator.expect_column_values_to_be_valid_email(
    column="email"
)
```

### 📊 Métricas de Qualidade de Dados

| Métrica | Descrição | Expectativa GX |
|---------|-----------|----------------|
| **Completude** | % de valores não nulos | `expect_column_values_to_not_be_null` |
| **Unicidade** | % de valores únicos | `expect_column_values_to_be_unique` |
| **Validade** | % de valores válidos | `expect_column_values_to_be_in_set` |
| **Consistência** | % de valores consistentes | `expect_column_values_to_match_regex` |
| **Precisão** | % de valores precisos | `expect_column_values_to_be_between` |
| **Atualidade** | Freshness dos dados | `expect_column_max_to_be_between` |

### 🎓 Conceitos Avançados

#### Data Docs

```bash
# Gerar documentação
great_expectations docs build

# Abrir no navegador
great_expectations docs open
```

Data Docs incluem:
- Expectation Suites detalhadas
- Resultados de validações
- Profiling estatístico
- Histórico de validações

#### Batch Requests

```python
# Batch por data
batch_request = {
    "datasource_name": "my_datasource",
    "data_asset_name": "sales_data",
    "options": {
        "year": "2025",
        "month": "01"
    }
}

# Batch por query SQL
batch_request = {
    "datasource_name": "postgres_db",
    "data_asset_name": "sales_table",
    "options": {
        "query": "SELECT * FROM sales WHERE date >= '2025-01-01'"
    }
}
```

### 💡 Melhores Práticas

1. **Comece simples**: Valide colunas críticas primeiro
2. **Automatize**: Integre com CI/CD e orquestradores
3. **Documente**: Use Data Docs para transparência
4. **Monitore**: Configure alertas para falhas
5. **Itere**: Adicione expectativas conforme aprende sobre os dados
6. **Colabore**: Compartilhe suites entre equipes
7. **Versione**: Mantenha expectation suites no Git

### 🚨 Tratamento de Falhas

```python
# Executar checkpoint com ações customizadas
results = checkpoint.run()

if not results["success"]:
    # Enviar alerta
    send_slack_alert("Data quality validation failed!")
    
    # Logar detalhes
    for validation in results["run_results"].values():
        for result in validation["validation_result"]["results"]:
            if not result["success"]:
                print(f"Failed: {result['expectation_config']['expectation_type']}")
                print(f"Details: {result['result']}")
    
    # Parar pipeline
    raise ValueError("Data quality check failed!")
```

### 🔗 Recursos Adicionais

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Great Expectations Gallery](https://greatexpectations.io/expectations/)
- [Data Quality Patterns](https://greatexpectations.io/blog/)
- [GX Community Slack](https://greatexpectations.io/slack)

### 🎯 Próximos Passos

- [ ] Adicionar mais expectation suites (produtos, transações)
- [ ] Implementar alertas (Slack, PagerDuty)
- [ ] Criar dashboard de métricas de qualidade
- [ ] Integrar com dbt para validação de modelos
- [ ] Adicionar testes de performance
- [ ] Implementar data quality scoring

---

## 🇬🇧 Enterprise Data Quality Framework with Great Expectations

Complete and professional framework for **data quality management** using **Great Expectations**. Implements automated validations, profiling, living documentation, and integration with modern data pipelines.

### 🚀 Quick Start

```bash
# Install Great Expectations
pip install great-expectations

# Initialize project
great_expectations init

# Create expectation suite
great_expectations suite new

# Run validation
great_expectations checkpoint run my_checkpoint

# View documentation
great_expectations docs build
```

### 🎓 Key Learnings

- ✅ Create declarative data expectations
- ✅ Automate data profiling
- ✅ Generate living documentation (Data Docs)
- ✅ Integrate with Airflow and dbt
- ✅ Build custom expectations
- ✅ Implement data quality monitoring

---

**Author:** Gabriel Demetrios Lafis  
**License:** MIT  
**Last Updated:** October 2025
