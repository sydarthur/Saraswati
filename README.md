# Saraswati

**Saraswati** is a scriptable literature review engine designed for researchers who seek a structured, journal-specific approach to gathering academic insights. Named after the Hindu goddess of knowledge, this tool enables curated exploration of scholarly works using the Semantic Scholar API and configurable filters.

---

## 🧠 Purpose

This tool helps automate and streamline the literature review process by:
- Allowing structured searches via a config file
- Targeting specific journals and year ranges
- Exporting results in CSV or RIS format for Zotero and citation management

---

## 📁 Project Structure

- `config/` – YAML configuration files that define search parameters
- `scripts/` – command line entry points for querying articles and running the pipeline
- `utils/` – helper modules used throughout the project
- `data/` – cached results and intermediate files
- `export/` – final exports in CSV or RIS format

## 🚀 Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the Pipeline

Once the dependencies are installed, the main pipeline can be executed with:

```bash
python scripts/run_pipeline.py --config config/search_config.yaml
```

Replace the config path if you use a different configuration file.

## 🔧 Sample Configuration

`search_config.yaml` uses YAML to define the search settings. A minimal example is shown below:

```yaml
journals:
  - name: "Nature"
    years: [2018, 2019, 2020]
keywords:
  - "machine learning"
  - "neuroscience"
limit: 50
output_format: "csv"
```

This structure can be extended with additional filters or output options depending on your requirements.

## 🛣 Roadmap

- Implement Semantic Scholar API queries
- Add advanced filtering utilities
- Provide more export formats and citation styles
- Include a user-friendly command-line interface

Contributions and suggestions are welcome as the project evolves.
