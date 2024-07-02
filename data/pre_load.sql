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

DROP TABLE IF EXISTS anuncios_df;
DROP TABLE IF EXISTS anunciantes_df;

---
--- create table
---


CREATE TABLE anunciantes (
    nome VARCHAR(100) PRIMARY KEY,
    endereco VARCHAR(200) NOT NULL,
    telefone VARCHAR(14),
    saiba_mais VARCHAR(1000)
);

CREATE TABLE anuncios_df (
    anuncio_id SERIAL PRIMARY KEY,
    tipo_imovel VARCHAR(20) NOT NULL,
    valor DECIMAL NOT NULL,
    qtd_quartos INTEGER,
    qtd_vagas INTEGER,
    descricao VARCHAR(2000),
    avaliacao DECIMAL,
    endereco VARCHAR(255) NOT NULL,
    anunciante VARCHAR(100) NOT NULL,
    FOREIGN KEY (anunciante) REFERENCES anunciantes(nome)
);

---
--- alter table
---

-- ALTER TABLE 