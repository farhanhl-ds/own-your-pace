-- Dijalankan otomatis saat container pertama kali buat database

-- Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Pastikan timescaledb extension aktif
SELECT timescaledb_pre_restore();
