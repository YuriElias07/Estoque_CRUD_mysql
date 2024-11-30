CREATE DATABASE estoque;
USE estoque;

CREATE TABLE produtos(
	id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(30),
    descrição TEXT,
    qtde_disp INT,
    preco FLOAT
);

CREATE TABLE vendas(
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    qtde_vendida INT,
    data_venda DATETIME,
	id_produtos INT,
    FOREIGN KEY (id_produtos) REFERENCES produtos(id)
);

SELECT * FROM produtos;
SELECT * FROM vendas;
