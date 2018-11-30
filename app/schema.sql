DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Asset;
DROP TABLE IF EXISTS Covariance;
DROP TABLE IF EXISTS WeeklyAssetData;
DROP TABLE IF EXISTS WeeklyMarketData;
DROP TABLE IF EXISTS Portfolio;
DROP TABLE IF EXISTS PortfolioAsset;

CREATE TABLE User (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  risk_profile REAL
);

CREATE TABLE Asset (
  ticker TEXT PRIMARY KEY,
  average_return REAL NOT NULL,
  market_cap REAL NOT NULL,
  price REAL NOT NULL
);

CREATE TABLE Covariance (
  ticker1 TEXT NOT NULL,
  ticker2 TEXT NOT NULL,
  covariance REAL NOT NULL,
  PRIMARY KEY(ticker1, ticker2),
  FOREIGN KEY (ticker1) REFERENCES Asset(ticker),
  FOREIGN KEY (ticker2) REFERENCES Asset(ticker)
);

CREATE TABLE WeeklyAssetData (
  ticker TEXT NOT NULL,
  date_time TIMESTAMP NOT NULL,
  price REAL NOT NULL,
  market_cap REAL NOT NULL,
  PRIMARY KEY(ticker, date_time),
  FOREIGN KEY(ticker) REFERENCES Asset(ticker)
);

CREATE TABLE WeeklyMarketData (
  date_time TIMESTAMP PRIMARY KEY,
  capm REAL NOT NULL,
  small_vs_big REAL NOT NULL,
  high_vs_low REAL NOT NULL,
  risk_free_rate REAL NOT NULL
);

CREATE TABLE Portfolio (
  portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  FOREIGN KEY(user_id) REFERENCES User(user_id)
);

CREATE TABLE PortfolioAsset (
  portfolio_id INTEGER NOT NULL,
  ticker TEXT NOT NULL,
  amount REAL NOT NULL,
  PRIMARY KEY(portfolio_id, ticker),
  FOREIGN KEY(portfolio_id) REFERENCES Portfolio(portfolio_id),
  FOREIGN KEY(ticker) REFERENCES Asset(ticker)
);
