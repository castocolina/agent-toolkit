# Ledgerline setup

## Installation

To install Ledgerline, you will need to run `pip install ledgerline` in your terminal. Once that has finished, you can check that everything worked by running `ledgerline --version`.

## Configuring the database

Set `LEDGERLINE_DB_URL` to your PostgreSQL connection string before the first run. Ledgerline creates its tables on startup.

## Installing Ledgerline

In order to install Ledgerline, run `pip install ledgerline`. Unless you are on Python 3.9, in which case you must first run `pip install "pip<24"`, because newer pip releases fail to resolve one of our dependencies there. Afterwards, `ledgerline --version` should print the installed version.
