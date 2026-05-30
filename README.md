
# 🔒 API Security Auditor Pro

[![PyPI version](https://badge.fury.io/py/api-security-auditor-pro.svg)](https://pypi.org/project/api-security-auditor-pro/)
[![Python Version](https://img.shields.io/pypi/pyversions/api-security-auditor-pro.svg)](https://pypi.org/project/api-security-auditor-pro/)
[![Downloads](https://img.shields.io/pypi/dm/api-security-auditor-pro.svg)](https://pypi.org/project/api-security-auditor-pro/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🎯 What is API Security Auditor Pro?

**API Security Auditor Pro** is a professional command-line tool designed to help developers and security engineers test the security of their APIs. It automatically detects common security vulnerabilities and misconfigurations.

### Key Features

- ✅ **Rate Limiting Detection** - Test if your API can handle brute force attacks
- 🔍 **Security Headers Check** - Identify missing security headers
- 🚨 **Vulnerability Scanning** - Detect common API vulnerabilities
- 📊 **Multiple Output Formats** - JSON, HTML, CSV reports
- 🐳 **Docker Support** - Run anywhere without installation
- ⚡ **Fast & Lightweight** - Minimal dependencies, maximum performance

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Commands Reference](#-commands-reference)
- [Examples](#-examples)
- [Security Checks](#-security-checks)
- [Docker Usage](#-docker-usage)
- [CI/CD Integration](#-cicd-integration)
- [Output Formats](#-output-formats)
- [FAQ](#-faq)
- [Contributing](#-contributing)

## 🚀 Installation

### From PyPI (Recommended)

```bash
pip install api-security-auditor-pro
```

### From Source

```bash
git clone https://github.com/yourusername/api-security-auditor-pro.git
cd api-security-auditor-pro
pip install -e .
```

### With Docker

```bash
docker pull yourusername/api-security-auditor-pro
docker run yourusername/api-security-auditor-pro --help
```

## 🎬 Quick Start

### 1. Scan an API Endpoint

```bash
api-auditor scan https://jsonplaceholder.typicode.com/users
```

**Output:**
```
🔍 Starting security scan on: https://jsonplaceholder.typicode.com/users

           Security Scan Results
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Check         ┃ Status        ┃ Severity ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Rate Limiting │ ⚠️ VULNERABLE │ MEDIUM   │
└───────────────┴───────────────┴──────────┘

⚠️ Found 1 vulnerabilities!
```

### 2. Test Rate Limiting

```bash
api-auditor test-rate-limit https://api.github.com/users/octocat
```

**Output:**
```
🚦 Testing rate limiting on: https://api.github.com/users/octocat

    Rate Limiting Test Results
┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Metric                ┃ Value  ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ Total Requests        │ 50     │
│ Successful (200)      │ 0      │
│ Rate Limited (429)    │ 50     │
│ Errors                │ 0      │
│ Rate Limiting Present │ ✅ Yes │
└───────────────────────┴────────┘
```

### 3. Save Results to File

```bash
api-auditor scan https://api.example.com --output report.json --format json
api-auditor report report.json --output final_report.html
```

## 📚 Commands Reference

### `scan` - Security Scan

Scan a single API endpoint for vulnerabilities.

```bash
api-auditor scan URL [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-v, --verbose` | Enable verbose output | False |
| `-o, --output` | Output file path | None |
| `-f, --format` | Output format (json/html) | json |
| `-t, --timeout` | Request timeout in seconds | 30 |

**Examples:**
```bash
# Basic scan
api-auditor scan https://api.example.com/users

# Scan with verbose output
api-auditor scan https://api.example.com/users --verbose

# Save to HTML report
api-auditor scan https://api.example.com/users --output report.html --format html

# Increase timeout for slow APIs
api-auditor scan https://slow-api.com --timeout 60
```

### `test-rate-limit` - Rate Limiting Test

Test if your API implements proper rate limiting.

```bash
api-auditor test-rate-limit URL [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-r, --requests` | Number of requests to send | 50 |
| `-c, --concurrency` | Concurrent connections | 5 |
| `-d, --delay` | Delay between requests (seconds) | 0.05 |

**Examples:**
```bash
# Standard test
api-auditor test-rate-limit https://api.example.com/login

# Aggressive test (100 requests, 10 concurrent)
api-auditor test-rate-limit https://api.example.com/login --requests 100 --concurrency 10

# Slow test (to be polite)
api-auditor test-rate-limit https://api.example.com/login --delay 0.5
```

### `report` - Generate Report

Generate a formatted report from previous scan results.

```bash
api-auditor report INPUT_FILE [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output file path | None |

**Examples:**
```bash
# Generate summary from JSON results
api-auditor report scan_result.json

# Save formatted report
api-auditor report scan_result.json --output formatted_report.json
```

## 💡 Examples

### Real-World Scenarios

#### 1. Security Audit of Your Production API

```bash
# Step 1: Test rate limiting on login endpoint
api-auditor test-rate-limit https://your-api.com/api/login --requests 100 --concurrency 20

# Step 2: Scan user endpoints
api-auditor scan https://your-api.com/api/users --output users_scan.json

# Step 3: Generate report
api-auditor report users_scan.json --output security_report.html
```

#### 2. Testing Different Environments

```bash
# Development
api-auditor scan https://dev-api.example.com --output dev_report.json

# Staging
api-auditor scan https://staging-api.example.com --output staging_report.json

# Production
api-auditor scan https://api.example.com --output prod_report.json
```

#### 3. Batch Scanning Multiple Endpoints

Create a batch script `scan_all.bat`:

```batch
@echo off
echo Scanning API Endpoints...

api-auditor scan https://api1.example.com --output report1.json
api-auditor scan https://api2.example.com --output report2.json
api-auditor scan https://api3.example.com --output report3.json

echo All scans complete!
```

#### 4. Testing Public APIs

```bash
# GitHub API (has rate limiting)
api-auditor test-rate-limit https://api.github.com/users

# JSONPlaceholder (no rate limiting)
api-auditor scan https://jsonplaceholder.typicode.com/posts

# Agify API (simple demo API)
api-auditor scan https://api.agify.io?name=michael

# Chuck Norris API
api-auditor test-rate-limit https://api.chucknorris.io/jokes/random
```

## 🛡️ Security Checks

| Check ID | Check Name | Severity | Description |
|----------|------------|----------|-------------|
| RATE001 | Missing Rate Limiting | MEDIUM | API doesn't limit request rates, vulnerable to brute force |
| HEAD001 | Missing Security Headers | LOW | Missing HSTS, CSP, X-Frame-Options headers |
| DATA001 | Sensitive Data Exposure | HIGH | API returns sensitive information in responses |
| AUTH001 | Weak Authentication | HIGH | Weak JWT secrets or missing authentication |

## 🐳 Docker Usage

### Pull and Run

```bash
# Pull the image
docker pull yourusername/api-security-auditor-pro:latest

# Run a scan
docker run yourusername/api-security-auditor-pro scan https://api.example.com

# Save output locally
docker run -v $(pwd)/output:/output yourusername/api-security-auditor-pro \
  scan https://api.example.com --output /output/report.json
```

### Build Custom Image

```bash
# Clone repository
git clone https://github.com/yourusername/api-security-auditor-pro.git
cd api-security-auditor-pro

# Build image
docker build -t api-auditor:custom .

# Run
docker run api-auditor:custom scan https://api.example.com
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: API Security Scan

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install API Auditor
        run: pip install api-security-auditor-pro
      
      - name: Run Security Scan
        run: |
          api-auditor scan https://api.example.com --output security-report.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security-report.json
```

### GitLab CI

```yaml
security-scan:
  stage: test
  script:
    - pip install api-security-auditor-pro
    - api-auditor scan https://api.example.com --output report.json
    - api-auditor report report.json
  artifacts:
    paths:
      - report.json
    reports:
      junit: report.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('API Security Scan') {
            steps {
                sh 'pip install api-security-auditor-pro'
                sh 'api-auditor scan https://api.example.com --output security-report.json'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'security-report.json'
        }
    }
}
```

## 📊 Output Formats

### JSON Format (Machine-readable)

```json
{
  "target": "https://api.example.com",
  "timestamp": "2026-05-30T05:20:57.186710",
  "vulnerabilities": [
    {
      "check": "Rate Limiting",
      "severity": "MEDIUM",
      "finding": "No rate limiting detected",
      "remediation": "Implement rate limiting to prevent brute force attacks"
    }
  ],
  "scan_summary": {
    "duration_seconds": 2.34,
    "checks_performed": 1
  }
}
```

### Console Table (Human-readable)

```
           Security Scan Results
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Check         ┃ Status        ┃ Severity ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Rate Limiting │ ⚠️ VULNERABLE │ MEDIUM   │
└───────────────┴───────────────┴──────────┘
```

## ❓ FAQ

### Q: What APIs can I test?

**A:** Any HTTP/HTTPS API - REST, GraphQL, SOAP. Public APIs, internal APIs, microservices.

### Q: Will this attack my API?

**A:** No! It only sends safe test requests. It checks for configurations and behaviors without exploiting vulnerabilities.

### Q: How many requests will it send?

**A:** Default is 30-50 requests per test. You can control this with `--requests` parameter.

### Q: Can I use it behind a corporate proxy?

**A:** Yes! Set environment variables:
```bash
set HTTP_PROXY=http://proxy.company.com:8080
set HTTPS_PROXY=https://proxy.company.com:8080
```

### Q: Does it work with authenticated APIs?

**A:** Current version supports basic scanning. Future versions will add authentication support.

### Q: How accurate are the results?

**A:** Very accurate for rate limiting detection. Other checks are being continuously improved.

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Report Bugs**: Open an issue on GitHub
2. **Suggest Features**: Tell us what you'd like to see
3. **Submit PRs**: Fix bugs or add features
4. **Improve Docs**: Help make documentation better

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/api-security-auditor-pro.git
cd api-security-auditor-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black src tests
flake8 src tests
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OWASP for API security guidelines
- The Python open-source community
- All contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/api-security-auditor-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/api-security-auditor-pro/discussions)
- **Email**: your.email@example.com

## ⭐ Star This Project

If you find this tool useful, please star it on GitHub!

```
https://github.com/yourusername/api-security-auditor-pro
```

---

**Made with ❤️ for API security**

## 🚀 Quick Command Reference Card

```bash
# Help
api-auditor --help
api-auditor scan --help

# Scan
api-auditor scan https://api.example.com
api-auditor scan https://api.example.com --verbose
api-auditor scan https://api.example.com --output report.json

# Rate Limit Test
api-auditor test-rate-limit https://api.example.com
api-auditor test-rate-limit https://api.example.com --requests 100 --concurrency 10

# Reports
api-auditor report scan_result.json
api-auditor report scan_result.json --output final.html
```

---

**Start securing your APIs today! 🎯**
