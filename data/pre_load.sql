--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;



SET default_tablespace = '';

SET default_with_oids = false;


---
--- drop tables
---

DROP TABLE IF EXISTS pilotos;
DROP TABLE IF EXISTS equipes;
DROP TABLE IF EXISTS resultados_corridas;

---
--- create table
---

CREATE TABLE equipes (
    nome VARCHAR(100) PRIMARY KEY,
    localizacao_base VARCHAR(100),
    chefe_equipe VARCHAR(100),
    chefe_tecnico VARCHAR(100),
    chassis_carro VARCHAR(50),
    unidade_potencia VARCHAR (50),
    campeonatos_mundiais NUMERIC,
    ano_estreia NUMERIC,
    bio TEXT
);

CREATE TABLE pilotos (
    nome VARCHAR(100) PRIMARY KEY,
    equipe VARCHAR(100),
    pais_origem VARCHAR(50),
    podiums NUMERIC,
    pontos_carreira NUMERIC(6, 1),
    campeonatos_mundiais NUMERIC,
    data_nascimento DATE,
    bio TEXT
);

CREATE TABLE resultados_corridas (
    grande_premio VARCHAR(100) NOT NULL,
    data_gp DATE NOT NULL,
    piloto_vencedor VARCHAR(100),
    equipe VARCHAR(100),
    voltas NUMERIC,
    tempo_total INTERVAL
);