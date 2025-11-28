# LUFT Setup and Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Internet connection for data collection

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/CarlDeanClineSr/The-Unifying-Fields-Program-and-Physics-By-You-and-I.git
cd The-Unifying-Fields-Program-and-Physics-By-You-and-I
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The default configuration is located in `config/luft_config.yml`. You can modify this file to customize:

- Data collection intervals
- Storage paths
- Logging levels
- Enable/disable specific collectors

## Running LUFT

### Run Continuous Automation

Start the automated data collection system:

```bash
python run_automation.py
```

This will continuously collect data at the configured intervals.

### Run Once

To collect data once and exit:

```bash
python run_automation.py --once
```

### Custom Configuration

Use a custom configuration file:

```bash
python run_automation.py --config path/to/custom_config.yml
```

## Data Storage

Collected data is automatically archived in the `data/archive/` directory with the following structure:

```
data/archive/
├── solar_wind/
│   └── YYYY/MM/DD/
│       └── YYYYMMDD_HHMMSS_ffffff.json
└── cosmic/
    └── YYYY/MM/DD/
        └── YYYYMMDD_HHMMSS_ffffff.json
```

Each archived file contains:
- Collected data
- Timestamp
- Source information
- Metadata
- Integrity checksum

## Logs

Application logs are stored in `logs/luft.log` by default. You can change this in the configuration file.

## Troubleshooting

### Connection Issues

If you encounter connection errors:
1. Check your internet connection
2. Verify that data source URLs are accessible
3. Check firewall settings

### Permission Issues

If you get permission errors:
```bash
chmod +x run_automation.py
```

### Missing Dependencies

If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

- Explore collected data in `data/archive/`
- Customize data sources in the collector modules
- Contribute new analysis workflows
- Share your findings with the community

For more information, see the [Contributing Guide](CONTRIBUTING.md).
