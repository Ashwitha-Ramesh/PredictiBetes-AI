# Contributing to PredictiBetes

Thank you for your interest in contributing to **PredictiBetes**!

## How to Contribute

1. **Fork the Repository**: Create your own feature branch.
2. **Setup Local Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
3. **Make Your Changes**: Follow PEP8 guidelines and maintain modular code architecture.
4. **Submit a Pull Request**: Provide a clear summary of your enhancements.

## Code Standards
- Use Type Hints where applicable.
- Ensure all FastAPI routes remain backward compatible.
- Run `python app/train_model.py` before submitting ML model changes.
