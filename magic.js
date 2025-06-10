const stocks = [
  { name: "AAPL", price: 150.00, change: 1.5 },
  { name: "GOOGL", price: 2800.00, change: -10.00 },
  { name: "AMZN", price: 3400.00, change: 20.00 },
  { name: "MSFT", price: 299.00, change: 5.00 },
  { name: "TSLA", price: 700.00, change: -15.00 },
];

let investorPortfolio = {
  cash: 100000,
  stocks: {},
};

function updateStockPrices() {
  stocks.forEach(stock => {
    const change = parseFloat((Math.random() * 10 - 5).toFixed(2));
    stock.price = parseFloat((stock.price + change).toFixed(2));
    stock.change = change;
  });
  render();
}

function buy() {
  const name = document.getElementById("stock-name").value.toUpperCase();
  const quantity = parseInt(document.getElementById("stock-quantity").value);

  const stock = stocks.find(s => s.name === name);
  if (!stock || isNaN(quantity) || quantity <= 0) return alert("Invalid stock or quantity.");

  const cost = stock.price * quantity;
  if (investorPortfolio.cash < cost) return alert("Insufficient cash.");

  investorPortfolio.cash -= cost;
  if (!investorPortfolio.stocks[name]) {
    investorPortfolio.stocks[name] = { quantity: 0, price: stock.price };
  }
  investorPortfolio.stocks[name].quantity += quantity;
  investorPortfolio.stocks[name].price = stock.price;

  render();
}

function sell() {
  const name = document.getElementById("stock-name").value.toUpperCase();
  const quantity = parseInt(document.getElementById("stock-quantity").value);

  const holding = investorPortfolio.stocks[name];
  if (!holding || quantity <= 0 || holding.quantity < quantity) return alert("Invalid sell.");

  const stock = stocks.find(s => s.name === name);
  investorPortfolio.cash += stock.price * quantity;
  holding.quantity -= quantity;

  if (holding.quantity === 0) delete investorPortfolio.stocks[name];

  render();
}

function render() {
  // Render stock table
  const stockTable = document.querySelector("#stocks-table tbody");
  stockTable.innerHTML = "";
  stocks.forEach(stock => {
    const row = document.createElement("tr");
    const changeClass = stock.change >= 0 ? "change-positive" : "change-negative";
    row.innerHTML = `
      <td>${stock.name}</td>
      <td>$${stock.price.toFixed(2)}</td>
      <td class="${changeClass}">${stock.change >= 0 ? "+" : ""}${stock.change.toFixed(2)}</td>
    `;
    stockTable.appendChild(row);
  });

  // Render portfolio
  document.getElementById("cash-display").textContent = `Cash: $${investorPortfolio.cash.toFixed(2)}`;
  const portfolioTable = document.querySelector("#portfolio-table tbody");
  portfolioTable.innerHTML = "";
  for (const [name, data] of Object.entries(investorPortfolio.stocks)) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${name}</td>
      <td>${data.quantity}</td>
      <td>$${data.price.toFixed(2)}</td>
    `;
    portfolioTable.appendChild(row);
  }
}

// Initial render and start simulation
render();
setInterval(updateStockPrices, 3000); // Update every 3 seconds
