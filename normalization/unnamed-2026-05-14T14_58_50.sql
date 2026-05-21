
CREATE TABLE account
(
  account_id   int     NOT NULL,
  acoount_name varchar,
  brokerag     varchar,
  PRIMARY KEY (account_id)
);

CREATE TABLE asset
(
  ticker varchar NOT NULL,
  name   varchar,
  type   varchar,
  PRIMARY KEY (ticker)
);

CREATE TABLE daily_price
(
  ticker varchar NOT NULL,
  date   date    NOT NULL,
  open   double ,
  high   double ,
  low    double ,
  close  double ,
  volume bigint ,
  PRIMARY KEY (ticker, date)
);

CREATE TABLE holding
(
  ticker        varchar NOT NULL,
  account_id    int     NOT NULL,
  quantity      int    ,
  avg_buy_price double ,
  PRIMARY KEY (ticker, account_id)
);

ALTER TABLE daily_price
  ADD CONSTRAINT FK_asset_TO_daily_price
    FOREIGN KEY (ticker)
    REFERENCES asset (ticker);

ALTER TABLE holding
  ADD CONSTRAINT FK_asset_TO_holding
    FOREIGN KEY (ticker)
    REFERENCES asset (ticker);

ALTER TABLE holding
  ADD CONSTRAINT FK_account_TO_holding
    FOREIGN KEY (account_id)
    REFERENCES account (account_id);
