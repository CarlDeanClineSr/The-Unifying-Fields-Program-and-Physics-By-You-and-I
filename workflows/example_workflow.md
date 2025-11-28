# Reproducible Workflow Example: Solar Wind Analysis

## Purpose
Demonstrate a reproducible workflow for analyzing archived solar wind data.

## Prerequisites
- LUFT installed and running
- At least one day of collected data

## Workflow Steps

### 1. Data Collection
```bash
# Collect data for 24 hours
python run_automation.py
```

### 2. Data Retrieval
```python
from luft.storage import DataArchiver
from datetime import datetime

# Initialize archiver
archiver = DataArchiver()

# List archives for a specific date
date = "2025-11-23"
archives = archiver.list_archives('solar_wind', date=date)

# Load and verify data
for archive_path in archives:
    package = archiver.retrieve_data(archive_path)
    if archiver.verify_integrity(package):
        print(f"Verified: {archive_path}")
        # Process data here
```

### 3. Data Analysis (Example)
```python
import json

def analyze_solar_wind(archive_package):
    """
    Example analysis of solar wind data.
    Extract and summarize key parameters.
    """
    data = archive_package['data']
    sources = data['sources']
    
    results = {
        'timestamp': data['timestamp'],
        'summary': {}
    }
    
    # Extract from each source
    for source_name, source_data in sources.items():
        if source_data['status'] == 'success':
            # Add your analysis here
            results['summary'][source_name] = {
                'records': len(source_data['data']) if isinstance(source_data['data'], list) else 1,
                'collected_at': source_data['collected_at']
            }
    
    return results

# Apply analysis
for archive_path in archives:
    package = archiver.retrieve_data(archive_path)
    results = analyze_solar_wind(package)
    print(json.dumps(results, indent=2))
```

### 4. Results Documentation
Document your findings in a structured format:
- Hypothesis
- Method
- Data sources (with checksums)
- Results
- Conclusions
- Reproducibility notes

## Reproducibility Checklist

- [ ] Record LUFT version used
- [ ] Record Python version
- [ ] Note all dependencies with versions
- [ ] Document data collection period
- [ ] Include all analysis code
- [ ] Verify data integrity checksums
- [ ] Document any filtering or preprocessing
- [ ] Share complete workflow

## Example Output Structure

```json
{
  "workflow": {
    "name": "Solar Wind Analysis",
    "version": "1.0",
    "date": "2025-11-23",
    "luft_version": "0.1.0"
  },
  "data": {
    "source": "solar_wind",
    "period": "2025-11-23",
    "archives": ["path1", "path2"],
    "checksums_verified": true
  },
  "analysis": {
    "method": "Statistical summary",
    "results": {...}
  }
}
```

## Notes

This workflow can be automated and scheduled for continuous analysis. Add your own analysis methods and share your findings with the community.
