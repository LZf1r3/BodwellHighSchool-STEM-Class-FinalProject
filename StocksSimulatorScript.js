const stocks = [
    {name: "AAPL", price: 150.00, change: 1.5},
    {name: "GOOGL", price: 2800.00, change: -10.00},
    {name: "AMZN", price: 3400.00, change: 20.00},
    {name: "MSFT", price: 299.00, change: 5.00},
    {name: "TSLA", price: 700.00, change: -15.00},
    {name: "NFLX", price: 500.00, change: 10.00},
    {name: "FB", price: 350.00, change: -5.00},
    {name: "NVDA", price: 220.00, change: 8.00},
    {name: "BRK.A", price: 420000.00, change: 1000.00},
    {name: "V", price: 230.00, change: 3.00},
    {name: "JPM", price: 160.00, change: -2.00},
    {name: "DIS", price: 180.00, change: 4.00},
    {name: "PYPL", price: 250.00, change: -8.00},
    {name: "INTC", price: 55.00, change: 1.00},
    {name: "CSCO", price: 50.00, change: 0.50},
    {name: "ADBE", price: 500.00, change: 15.00},
    {name: "CMCSA", price: 60.00, change: -1.00},
    {name: "PEP", price: 150.00, change: 2.00},
    {name: "KO", price: 55.00, change: 0.75},
    {name: "MRK", price: 80.00, change: -0.50},
    {name: "PFE", price: 40.00, change: 0.25},
    {name: "T", price: 30.00, change: -0.10},
    {name: "VZ", price: 55.00, change: 0.20},
    {name: "WMT", price: 140.00, change: 1.00},
    {name: "HD", price: 300.00, change: 5.00},
    {name: "BA", price: 220.00, change: -3.00},
    {name: "XOM", price: 60.00, change: 0.80},
    {name: "CVX", price: 110.00, change: -1.50},
    {name: "UNH", price: 400.00, change: 10.00},
    {name: "JNJ", price: 170.00, change: 2.50},
    {name: "MRNA", price: 200.00, change: 3.00},
];

let investorPortfolio = {
    cash: 100000, // Starting cash
    stocks: {}, // Stock holdings
};

const stockPrices = stocks.reduce((acc, stock) => {
    acc[stock.name] = stock.price;
    return acc;
}, {});

function updateStockPrices() {
    stocks.forEach(stock => {
        // Simulate price changes
        const change = (Math.random() * 10 - 5).toFixed(2); // Random change between -5 and +5
        stock.price = parseFloat((stock.price + parseFloat(change)).toFixed(2));
        stock.change = parseFloat(change);
    });
    
    // Update stock prices in the portfolio
    for (const stock of Object.keys(investorPortfolio.stocks)) {
        if (stockPrices[stock]) {
            investorPortfolio.stocks[stock].price = stockPrices[stock];
        }
    }
};

function buyStock(stockName, quantity) {
    const stock = stocks.find(s => s.name === stockName);
    if (!stock) {
        console.error("Stock not found:", stockName);
        return;
    }
    
    const totalCost = stock.price * quantity;
    if (investorPortfolio.cash < totalCost) {
        console.error("Insufficient cash to buy", quantity, "shares of", stockName);
        return;
    }
    
    investorPortfolio.cash -= totalCost;
    if (!investorPortfolio.stocks[stockName]) {
        investorPortfolio.stocks[stockName] = { quantity: 0, price: stock.price };
    }
    investorPortfolio.stocks[stockName].quantity += quantity;
    
    console.log(`Bought ${quantity} shares of ${stockName} at $${stock.price} each.`);
};

function sellStock(stockName, quantity) {
    const stock = investorPortfolio.stocks[stockName];
    if (!stock || stock.quantity < quantity) {
        console.error("Insufficient shares to sell", quantity, "of", stockName);
        return;
    }
    
    const totalSale = stock.price * quantity;
    investorPortfolio.cash += totalSale;
    stock.quantity -= quantity;
    
    if (stock.quantity === 0) {
        delete investorPortfolio.stocks[stockName];
    }
    
    console.log(`Sold ${quantity} shares of ${stockName} at $${stock.price} each.`);
};

function displayPortfolio() {
    console.log("Investor Portfolio:");
    console.log("Cash: $", investorPortfolio.cash.toFixed(2));
    console.log("Stocks:");
    for (const [stockName, stock] of Object.entries(investorPortfolio.stocks)) {
        console.log(`${stockName}: ${stock.quantity} shares at $${stock.price.toFixed(2)} each`);
    }
};

function displayStockPrices() {
    console.log("Current Stock Prices:");
    stocks.forEach(stock => {
        console.log(`${stock.name}: $${stock.price.toFixed(2)} (${stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)})`);
    });
};

// Example usage
updateStockPrices();
displayStockPrices();
buyStock("AAPL", 10);
displayPortfolio();
updateStockPrices();
displayStockPrices();
sellStock("AAPL", 5);
