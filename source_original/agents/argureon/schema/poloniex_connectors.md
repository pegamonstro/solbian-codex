# Poloniex Connectors (Spot + Futures) — seedrelay Integration

This document standardizes how Argureon calls Poloniex via seedrelay.

## Overview

- **Connectors**: `poloniex.spot`, `poloniex.futures`
- **Auth**: API key + HMAC signature + timestamp (exact header names and signing string per official docs).
- **Base URLs**: Fill `rest` and `ws` endpoints from the provided vendor docs.
- **Capabilities**: Read + Trade (Withdrawals disabled in v1).

## Common Conventions

- **Symbols**: `BASE-QUOTE` uppercase (e.g., `BTC-USDT`).
- **Decimals**: `decimal128` fixed-point, banker's rounding.
- **Time**: UTC, epoch ms or RFC3339.
- **Idempotency**: Use `clientOrderId` (and `Idempotency-Key` where supported).

## Public Endpoints (Spot)

- **Ping/Time**: health/time sync.
- **Markets**: list tradable symbols / filters.
- **Tickers**: latest ticker or 24h stats.
- **Order Book**: depth snapshots; optional `depth`.
- **Klines/Candles**: OHLCV with `symbol`, `interval`, optional `start`, `end`, `limit`.

## Private Endpoints (Spot)

- **Balances**: wallet/account balances.
- **Account Info**: status, limits.
- **Orders (Create)**: side, type, price/quantity, tif, clientOrderId.
- **Orders (Cancel)**: by `orderId`.
- **Open Orders**: filter by `symbol`, `limit`.
- **Order History**: time-bounded history.
- **Trades**: user trade fills (time-bounded).

## Public Endpoints (Futures)

- **Contracts**: instruments (tick size, lot size, leverage limits).
- **Tickers**: per-contract stats.
- **Order Book**: depth snapshots.
- **Klines/Candles**: futures OHLCV.
- **Funding Rates**: historical and/or upcoming funding.

## Private Endpoints (Futures)

- **Balances**: futures account balances.
- **Positions**: open positions by `symbol`.
- **Orders (Create)**: side, type, price/size, tif, reduceOnly, postOnly, leverage, stopPrice.
- **Orders (Cancel)**: by `orderId`.
- **Open Orders**: open orders per `symbol`.
- **Order History**: account order history.
- **Fills/Trades**: execution history.
- **Leverage Set**: set per-symbol leverage.
- **Margin Info**: maintenance/initial margin, risk.

## WebSocket Channels (Both)

- **Ticker**: real-time prices.
- **Trades**: public trade prints.
- **Order Book**: real-time L2/L3 (depth).
- **Funding (Futures)**: funding updates.

## Error & Retry Policy

- **Backoff**: exponential with jitter.
- **Circuit Breaking**: per-connector.
- **Rate-Limits**: global + per-order buckets.

## Compliance & Security

- **Secret storage** under `mem/secure/keys/poloniex/` (0600).
- **Redaction** of `api_secret`, signatures in logs.
- **No Withdrawals** in v1; trading only.