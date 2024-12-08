from flask import Flask, request, jsonify
import os
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route('/process-stock-data', methods=['POST'])
def process_stock_data():
    data = request.json.get('prompt')
    print("data : ",data)
    
    # Parse stock data
    advice = "Investment advice here based on stock data."  # Your logic
    stocks = list(data)
    opening_price = [float(data[stock]["1. open"]) for stock in stocks]
    closing_price = [float(data[stock]["4. close"]) for stock in stocks]
    high_price = [float(data[stock]["2. high"]) for stock in stocks]
    low_price = [float(data[stock]["3. low"]) for stock in stocks]
    
    # Save .mat file
    mat_data = {
        "stocks": stocks,
        "opening_price": opening_price,
        "closing_price": closing_price,
        "high_price": high_price,
        "low_price": low_price,
    }
    scipy.io.savemat("stock_data.mat", mat_data)
    
    # Generate graph
    fig, ax = plt.subplots()
    x = np.arange(len(stocks))
    width = 0.2
    ax.bar(x - width, opening_price, width, label='Opening Price')
    ax.bar(x, closing_price, width, label='Closing Price')
    ax.bar(x + width, high_price, width, label='High Price')
    ax.bar(x + 2 * width, low_price, width, label='Low Price')

    ax.set_xlabel("Stocks")
    ax.set_ylabel("Prices")
    ax.set_title("Stock Price Comparison")
    ax.set_xticks(x)
    ax.set_xticklabels(stocks)
    ax.legend()

    graph_path = "graph.png"
    plt.savefig(graph_path)
    plt.close()

    # Return results
    return jsonify({
        "advice": advice,
        "fileLinks": {
            "graph": f"/api/download-file/graph.png",
            "matFile": f"/api/download-file/stock_data.mat",
        }
    })

@app.route('/download-file/<filename>', methods=['GET'])
def download_file(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
