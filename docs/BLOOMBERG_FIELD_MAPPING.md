# Bloomberg Field Mapping

## 1. Objectif et modes autorisés

Le fournisseur Bloomberg (`src/providers/bloomberg_provider.py`) permet d'adapter des données Bloomberg au format canonique commun de **MarketPulse**, afin de réutiliser les mêmes calculs analytiques (`src/analytics.py`) qu'avec Yahoo Finance.

Deux modes sont distingués :
- **`APPROVED_SAMPLE` (mode par défaut / reproductible)** : lit l'échantillon de référence approuvé (`data/sample/bloomberg_reference_sample.json`) sans nécessiter de Terminal Bloomberg. Permet de démontrer et tester le mapping et la normalisation de façon reproductible.
- **`LIVE` (environnement autorisé)** : point d'entrée prévu pour un accès à un Terminal Bloomberg autorisé. Aucune connexion réussie ne doit être simulée lorsque le mode n'est pas actif.

## 2. Identifiants AAPL / SP500

Bloomberg utilise ses propres identifiants de marché, distincts des tickers internes de MarketPulse :

| Ticker MarketPulse (`ticker`) | Identifiant Bloomberg (`provider_identifier`) | Instrument |
| --- | --- | --- |
| `AAPL` | `AAPL US Equity` | Apple Inc. (action) |
| `SP500` | `SPX Index` | S&P 500 (indice) |

Dans les observations canoniques produites par MarketPulse, la clé `ticker` doit contenir l'identifiant interne (`AAPL` ou `SP500`) et non l'identifiant Bloomberg.

Dans les fichiers JSON de référence, une série est repérée par `provider_identifier` (par exemple `"AAPL US Equity"`), même si l'observation brute de l'exemple illustratif ci-dessous contient directement `canonical_ticker`.

## 3. Correspondance des champs et types

Chaque observation normalisée doit respecter le schéma canonique suivant (7 champs) :

| Champ source Bloomberg | Champ MarketPulse | Type cible |
| --- | --- | --- |
| `observation_date` | `date` | `str` (`AAAA-MM-JJ`) |
| `canonical_ticker` | `ticker` | `str` |
| `open_value` | `open` | `float` |
| `high_value` | `high` | `float` |
| `low_value` | `low` | `float` |
| `close_value` | `close` | `float` |
| `volume_value` | `volume` | `int` |

## 4. Exemple fictif : brut → canonique

*Exemple fictif à but illustratif uniquement (ne provient pas d'une extraction Bloomberg réelle).*

Observation brute :

```json
{
  "observation_date": "2026-11-18",
  "canonical_ticker": "AAPL",
  "open_value": "100.0",
  "high_value": "112.0",
  "low_value": "99.0",
  "close_value": "110.0",
  "volume_value": "1500"
}

{
  "date": "2026-11-18",
  "ticker": "AAPL",
  "open": 100.0,
  "high": 112.0,
  "low": 99.0,
  "close": 110.0,
  "volume": 1500
}