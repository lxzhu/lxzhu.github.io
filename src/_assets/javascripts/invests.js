(function () {
	"use strict";

	function renderDetailHtml(data) {
		var pairs = Object.entries(data.details || {})
			.map(function (entry) {
				return '<div class="col-12 col-md-6"><span class="fw-semibold">' + entry[0] + ":</span> " + String(entry[1]) + "</div>";
			})
			.join("");

		return (
			'<div class="row g-2">' +
			'<div class="col-12 col-md-6"><span class="fw-semibold">trade_date:</span> ' + String(data.trade_date || "") + "</div>" +
			'<div class="col-12 col-md-6"><span class="fw-semibold">name:</span> ' + String(data.name || "") + "</div>" +
			pairs +
			"</div>"
		);
	}

	function loadData(options) {
		if (options.dataUrl) {
			return fetch(options.dataUrl).then(function (response) {
				if (!response.ok) {
					throw new Error("Failed to load invests data: " + response.status);
				}
				return response.json();
			});
		}

		var dataElement = document.getElementById(options.dataElementId || "");
		if (!dataElement) {
			return Promise.resolve({ transactions: [], stocks: [] });
		}
		return Promise.resolve(JSON.parse(dataElement.textContent || "{}"));
	}

	function formatMoney(value) {
		if (value === null || value === undefined || value === "") {
			return "N/A";
		}
		var number = Number(value || 0);
		return "$" + number.toFixed(2);
	}

	function buildTransactionsTable(rows, options) {
		var dateInput = document.getElementById(options.dateInputId);
		var symbolInput = document.getElementById(options.symbolInputId);
		var resetButton = document.getElementById(options.resetButtonId);

		if (!dateInput || !symbolInput || !resetButton || typeof Tabulator === "undefined") {
			return null;
		}

		var table = new Tabulator("#" + options.gridElementId, {
			data: rows,
			layout: "fitColumns",
			placeholder: "No transactions match current filters.",
			pagination: true,
			paginationSize: 20,
			columns: [
				{ title: "Trade Date", field: "trade_date", sorter: "string", headerSort: true },
				{ title: "Name", field: "name", sorter: "string", headerSort: true },
				{ title: "Market", field: "market", sorter: "string", headerSort: true },
				{ title: "Trade", field: "trade", sorter: "string", headerSort: true },
				{ title: "Share", field: "share", sorter: "number", headerSort: true },
				{ title: "Price", field: "price", sorter: "number", headerSort: true },
				{ title: "Fee", field: "fee", sorter: "number", headerSort: true },
			],
			rowFormatter: function (row) {
				var data = row.getData();
				var rowElement = row.getElement();
				rowElement.style.cursor = "pointer";

				var detail = rowElement.querySelector(".tx-detail-panel");
				if (!detail) {
					detail = document.createElement("div");
					detail.className = "tx-detail-panel border-top mt-2 pt-2 small";
					detail.hidden = true;
					rowElement.appendChild(detail);
				}

				detail.innerHTML = renderDetailHtml(data);
			},
		});

		table.on("rowClick", function (e, row) {
			var panel = row.getElement().querySelector(".tx-detail-panel");
			if (!panel) {
				return;
			}
			panel.hidden = !panel.hidden;
		});

		function applyFilters() {
			var date = (dateInput.value || "").trim();
			var stockQuery = (symbolInput.value || "").trim();

			table.setFilter(function (rowData) {
				var dateText = String(rowData.trade_date || "");
				if (date && dateText.indexOf(date) === -1) {
					return false;
				}

				if (!stockQuery) {
					return true;
				}

				var symbolText = rowData.symbol || "";
				var nameText = rowData.name || "";
				return fuzzyContains(symbolText, stockQuery) || fuzzyContains(nameText, stockQuery);
			});
		}

		dateInput.addEventListener("input", applyFilters);
		symbolInput.addEventListener("input", applyFilters);
		resetButton.addEventListener("click", function () {
			dateInput.value = "";
			symbolInput.value = "";
			table.clearFilter(true);
		});

		return table;
	}

	function buildStocksTable(rows, options) {
		if (typeof Tabulator === "undefined") {
			return null;
		}

		return new Tabulator("#" + options.gridElementId, {
			data: rows,
			layout: "fitColumns",
			placeholder: "No stocks available.",
			pagination: true,
			paginationSize: 20,
			initialSort: [{ column: "name", dir: "asc" }],
			columns: [
				{ title: "Name", field: "name", sorter: "string", headerSort: true },
				{ title: "Share", field: "share", sorter: "number", headerSort: true },
				{ title: "Avg Cost", field: "avg_cost", sorter: "number", headerSort: true, formatter: function (cell) { return formatMoney(cell.getValue()); } },
				{ title: "Profit", field: "profit", sorter: "number", headerSort: true, formatter: function (cell) { return formatMoney(cell.getValue()); } },
			],
		});
	}

	function initInvestsPage(options) {
		return loadData(options)
			.then(function (payload) {
				var transactions = Array.isArray(payload.transactions) ? payload.transactions : [];
				var stocks = Array.isArray(payload.stocks) ? payload.stocks : [];

				var transactionsTable = buildTransactionsTable(transactions, {
					gridElementId: options.transactionsGridElementId,
					dateInputId: options.dateInputId,
					symbolInputId: options.symbolInputId,
					resetButtonId: options.resetButtonId,
				});
				var stocksTable = buildStocksTable(stocks, {
					gridElementId: options.stocksGridElementId,
				});

				function redrawTables() {
					if (transactionsTable && typeof transactionsTable.redraw === "function") {
						transactionsTable.redraw(true);
					}
					if (stocksTable && typeof stocksTable.redraw === "function") {
						stocksTable.redraw(true);
					}
				}

				var tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
				Array.prototype.forEach.call(tabButtons, function (button) {
					button.addEventListener("shown.bs.tab", redrawTables);
				});

				redrawTables();
				return { transactionsTable: transactionsTable, stocksTable: stocksTable };
			})
			.catch(function (error) {
				console.error(error);
				return null;
			});
	}

	function normalizeText(value) {
		return String(value || "").toUpperCase().replace(/\s+/g, " ").trim();
	}

	function fuzzyContains(haystack, needle) {
		if (!needle) {
			return true;
		}

		var text = normalizeText(haystack);
		var query = normalizeText(needle);
		if (!query) {
			return true;
		}

		if (text.indexOf(query) !== -1) {
			return true;
		}

		var qi = 0;
		for (var ti = 0; ti < text.length && qi < query.length; ti += 1) {
			if (text.charAt(ti) === query.charAt(qi)) {
				qi += 1;
			}
		}

		return qi === query.length;
	}
	window.initInvestsPage = initInvestsPage;
	window.initInvestsTable = initInvestsPage;
})();
