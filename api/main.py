import os
from mistralai import Mistral
import json
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import base64
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

api_key = "5GqlAgbTEug2mS2cjwhOQMJKuh7sLfAZ"
client = Mistral(api_key=api_key)

data = [{
    "AAPL": {
        "1. open": "224.1800",
        "2. high": "244.6300",
        "3. low": "196.0000",
        "4. close": "224.1800",
        "5. volume": "1500"
    },
    "GOOGL": {
        "1. open": "177.6900",
        "2. high": "183.6100",
        "3. low": "147.2200",
        "4. close": "177.6900",
        "5. volume": "1300"
    },
    "AMZN": {
        "1. open": "183.7500",
        "2. high": "227.1500",
        "3. low": "151.6100",
        "4. close": "183.7500",
        "5. volume": "1200"
    },
    "MSFT": {
        "1. open": "440.3700",
        "2. high": "448.3900",
        "3. low": "385.5800",
        "4. close": "440.3700",
        "5. volume": "1100"
    },
    "TSLA": {
        "1. open": "249.2300",
        "2. high": "389.4900",
        "3. low": "182.0000",
        "4. close": "249.2300",
        "5. volume": "1400"
    }
}]
@app.route('/process-stock-data', methods=['POST'])
def process_stock_data():
    # Prepare the Mistral prompt
    userPrompt = request.json.get('prompt')

    model = "codestral-latest"
    prompt = (
        'Based on the given stock data, answer the question. '
        'Do not answer anything outside the given data.\n\n'
        f'Stock Data: {data}\n\n'
        f'Question: {userPrompt} '
        'give me some data as per your answer to show them in a graph, and give those data in a array named stock_data and  so that I can easily get them from your response.'
        'Please provide the data in the following structured format: '
        '{'
        '"stock_data": ['
        '{"symbol": "AAPL", "open": value, "close": value, "high": value, "low": value}, '
        '{"symbol": "GOOGL", "open": value, "close": value, "high": value, "low": value}, '
        # Repeat for each stock in the data
        ']'
        'and stock_data should be after your actual answer. so you should have two part answer ,1) the analitical answer and 2) stock_data in a python code like ```python stock_data```,and do not write anything extra besides those two '
    )

    # Fetch response from Mistral API
    response = client.fim.complete(
        model=model,
        prompt=prompt,
        suffix="",  # No suffix needed
        temperature=0,
        top_p=1,
    )

    # Extract the response content
    response_content = response.choices[0].message.content
    print(f"API Response:\n{response_content}\n")
    match = re.search(r"stock_data\s*=\s*(\[[\s\S]*?\]|\{[\s\S]*?\})", response_content)
    base64_encoded_image = ''

    if match:
        python_code = match.group(1).strip()
        print("Extracted Python Code we get :")
        print(python_code)
        json_str = python_code.replace("'", "\"").strip()
        
        # Parse the string as a JSON object
        json_data = json.loads(json_str)
        print("json output  :")
        print(json.dumps(json_data, indent=4))
        mat_data = json_data
        # stocks = mat_data  # Convert MATLAB cell array to Python list
        # opening_price = mat_data['open']
        # closing_price = mat_data['close']
        # high_price = mat_data['high']
        # low_price = mat_data['low']
        company = []
        opening_price = []
        closing_price = []
        high_price = []
        low_price = []

        # Parse the stock data directly from the original `data` for precise values
        for stock in mat_data:
            print("stock :: ",stock)
            stock_info = stock
            company.append(float(stock_info["open"]))
            opening_price.append(float(stock_info["open"]))
            closing_price.append(float(stock_info["close"]))
            high_price.append(float(stock_info["high"]))
            low_price.append(float(stock_info["low"]))


        # Generate and save the graph as an image
        plt.figure(figsize=(10, 6))
        prices = [opening_price, closing_price, high_price, low_price]
        bar_width = 0.2
        x = range(len(mat_data))

        for i, price_set in enumerate(prices):
            plt.bar([p + i * bar_width for p in x], price_set, width=bar_width, label=['Opening Price', 'Closing Price', 'High Price', 'Low Price'][i])

        plt.title('Stock Price Comparison')
        plt.xlabel('Stocks')
        plt.ylabel('Price')
        plt.xticks([p + 1.5 * bar_width for p in x], mat_data)
        plt.legend(loc='upper left')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        image_path = "stock_prices_comparison.png"
        plt.savefig(image_path)
        print(f"Graph saved as {image_path}.")

        # Provide a downloadable link
        print(f"Downloadable link for the graph: [Download Graph](sandbox:/mnt/data/{image_path})")

        with open(image_path, "rb") as image_file:
            base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    else:
            print("No Python code found in the response.")
    outPutJson = {
        "data": response_content,
        "image": base64_encoded_image,
        "message": "Successfully run the prompt"
    }
    return outPutJson

@app.route('/download-file/<filename>', methods=['GET'])
def download_file(filename):
    return app.send_static_file(filename)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)