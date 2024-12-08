
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
    