# Phishing URL Detector

A machine learning project that detects whether a given URL is phishing or legitimate.

## About

Phishing websites imitate genuine sites to steal sensitive information such as passwords and banking details. This project analyzes the features of a URL and uses a trained model to classify it as safe or malicious.

## Features

- Detects phishing URLs in real time
- Extracts URL-based features (length, special characters, HTTPS, IP address, subdomains, etc.)
- Uses machine learning models for classification
- Simple and easy to use

## Technologies Used

- Python
- Pandas, NumPy
- Scikit-learn
- Flask (for the web interface)



## Usage

```bash
python app.py
```

Open `http://localhost:5000` in your browser, enter a URL, and click **Check** to see whether it is phishing or legitimate.

## Dataset

The model is trained on a publicly available phishing URL dataset containing both legitimate and phishing URLs.

## Results

The model achieves good accuracy in distinguishing phishing URLs from legitimate ones.

## Future Scope

- Browser extension support
- Deep learning models for better accuracy
- Real-time updates with new phishing data
## License

This project is licensed under the MIT License.
