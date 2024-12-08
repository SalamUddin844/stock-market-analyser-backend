import os
from mistralai import Mistral
import json
import scipy.io
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import base64
from flask import Flask, request, jsonify,render_template

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

    # Extract and purify data for MATLAB
    stocks = ["AAPL", "GOOGL", "MSFT"]
    opening_price = []
    closing_price = []
    high_price = []
    low_price = []

    # Parse the stock data directly from the original `data` for precise values
    for stock in stocks:
        stock_info = data[0][stock]
        opening_price.append(float(stock_info["1. open"]))
        closing_price.append(float(stock_info["4. close"]))
        high_price.append(float(stock_info["2. high"]))
        low_price.append(float(stock_info["3. low"]))

    # Save purified data into a MATLAB-compatible .mat file
    mat_data = {
        "stocks": stocks,
        "opening_price": opening_price,
        "closing_price": closing_price,
        "high_price": high_price,
        "low_price": low_price,
    }

    scipy.io.savemat("stock_data.mat", mat_data)
    print("Data saved to stock_data.mat for MATLAB visualization.")

    # Generate and save the graph as an image
    plt.figure(figsize=(10, 6))
    prices = [opening_price, closing_price, high_price, low_price]
    bar_width = 0.2
    x = range(len(stocks))

    for i, price_set in enumerate(prices):
        plt.bar([p + i * bar_width for p in x], price_set, width=bar_width, label=['Opening Price', 'Closing Price', 'High Price', 'Low Price'][i])

    plt.title('Stock Price Comparison')
    plt.xlabel('Stocks')
    plt.ylabel('Price')
    plt.xticks([p + 1.5 * bar_width for p in x], stocks)
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    image_path = "stock_prices_comparison.png"
    plt.savefig(image_path)
    print(f"Graph saved as {image_path}.")

    # Provide a downloadable link
    print(f"Downloadable link for the graph: [Download Graph](sandbox:/mnt/data/{image_path})")

    # MATLAB visualization script
    matlab_script = """
    % Load data from .mat file
    load('stock_data.mat');

    % Create a grouped bar chart
    prices = [opening_price; closing_price; high_price; low_price]';

    % Plot the data
    figure;
    bar(prices);
    title('Stock Price Comparison');
    xlabel('Stocks');
    ylabel('Price');
    xticks(1:3);
    xticklabels(stocks);
    legend({'Opening Price', 'Closing Price', 'High Price', 'Low Price'}, 'Location', 'NorthWest');
    grid on;
    """

    # Save MATLAB script
    with open("plot_stock_data.m", "w") as f:
        f.write(matlab_script)
    print("MATLAB script saved as plot_stock_data.m.")
    base64_encoded_image=''
    with open(image_path, "rb") as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    outPutJson={
        "data": response_content,
        "image" :base64_encoded_image,
        "message":"Sucessfully run the propmt"
    }
    return outPutJson
@app.route('/download-file/<filename>', methods=['GET'])
def download_file(filename):
    return app.send_static_file(filename)
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port,debug=True)
