-- CONSULTA 1
SELECT SUM(inventario.cantidad)
	FROM inventario
		INNER JOIN pelicula ON pelicula.id_pelicula = inventario.id_pelicula
		WHERE pelicula.titulo = 'SUGAR WONKA';

-- CONSULTA 2
SELECT cliente.id_cliente,cliente.nombre,cliente.apellido, SUM(renta.monto::decimal) pago_total, COUNT(renta.monto::decimal) cantidad
	FROM cliente
	INNER JOIN renta ON renta.id_cliente = cliente.id_cliente
	GROUP BY (cliente.id_cliente, cliente.nombre, cliente.apellido)
	HAVING COUNT(renta.monto::decimal) >= 40
	ORDER BY cliente.nombre;

-- CONSULTA 3
SELECT actor.id_actor,actor.nombre_actor
	FROM actor
	WHERE split_part(actor.nombre_actor,' ',2) LIKE '%son%'
	ORDER BY split_part(actor.nombre_actor,' ',1);

-- CONSULTA 4
SELECT split_part(actor.nombre_actor,' ',1) nombre_actor, split_part(actor.nombre_actor,' ',2) apellido_actor,pelicula.titulo, pelicula.descripcion, pelicula.lanzamiento 
	FROM actor 
		INNER JOIN actor_pelicula ON actor_pelicula.id_actor = actor.id_actor 
		INNER JOIN pelicula ON pelicula.id_pelicula = actor_pelicula.id_pelicula
		WHERE lower(pelicula.descripcion) LIKE '%crocodile%' and lower(pelicula.descripcion) LIKE '%shark%'
		ORDER BY split_part(actor.nombre_actor,' ',2) ASC;

-- CONSULTA 5
SELECT c.nombre AS "nombre", c.apellido AS "apellido", p.nombre AS "pais", COUNT(r.id_renta) as "renta", (COUNT(r.id_renta)*100)/(
	SELECT COUNT(r.id_renta)
		FROM renta r
			INNER JOIN cliente c ON c.id_cliente = r.id_cliente
			INNER JOIN direccion d ON d.id_direccion = c.id_direccion
			INNER JOIN ciudad ci ON ci.id_ciudad = d.id_ciudad
			INNER JOIN pais z ON z.id_pais = ci.id_pais
			WHERE z.nombre = p.nombre
			GROUP BY z.nombre, z.id_pais
) AS "porcentaje"
FROM renta r
	INNER JOIN cliente c ON r.id_cliente = c.id_cliente
	INNER JOIN direccion d ON d.id_direccion = c.id_direccion
	INNER JOIN ciudad ci ON ci.id_ciudad = d.id_ciudad
	INNER JOIN pais p ON p.id_pais = ci.id_pais
	GROUP BY (c.nombre, c.apellido, p.nombre)
	ORDER BY COUNT(r.id_cliente) DESC
	LIMIT 1;
	
-- CONSULTA 6

-- CONSULTA 7

-- CONSULTA 8
SELECT p.nombre AS pais, ct.nombre_categoria AS categoria,ROUND((COUNT(ct.id_categoria) / SUM(COUNT(ct.id_categoria)) OVER(PARTITION BY p.nombre)) * 100, 2) porcentaje
	FROM Renta r 
	INNER JOIN cliente c ON r.id_cliente = c.id_cliente
	INNER JOIN direccion d ON c.id_direccion = d.id_direccion
	INNER JOIN ciudad cd ON d.id_ciudad = cd.id_ciudad
	INNER JOIN pais p ON cd.id_pais = p.id_pais
	INNER JOIN tienda t ON t.id_tienda = r.id_tienda
	INNER JOIN inventario i ON t.id_tienda = i.id_tienda
	INNER JOIN pelicula pl ON i.id_pelicula = pl.id_pelicula
	INNER JOIN categoria_pelicula pc ON pl.id_pelicula = pc.id_pelicula
	INNER JOIN categoria ct ON pc.id_categoria = ct.id_categoria
	WHERE LOWER(ct.nombre_categoria) LIKE '%sports%'
	GROUP BY p.nombre, ct.id_categoria
	ORDER BY p.nombre
	
-- CONSULTA NO 9
SELECT pais, ciudad, no_rentas
    FROM (
        SELECT p.nombre AS pais, cd.nombre AS ciudad, 
         COUNT(r.cliente_ID) as no_rentas
            FROM Renta r
            INNER JOIN Cliente c ON r.cliente_ID = c.cliente_ID
            INNER JOIN Direccion d ON c.direccion_ID = d.direccion_ID
            INNER JOIN Ciudad cd ON  d.ciudad_ID = cd.ciudad_ID
            INNER JOIN Pais p ON cd.pais_ID = p.pais_ID
            GROUP BY p.nombre, cd.nombre
    )
    WHERE pais LIKE '%United States%'
    AND no_rentas > (SELECT COUNT(r.cliente_id) 
                        FROM Renta r
                        INNER JOIN Cliente c ON r.cliente_ID = c.cliente_ID
                        INNER JOIN Direccion d ON c.direccion_ID = d.direccion_ID
                        INNER JOIN Ciudad cd ON  d.ciudad_ID = cd.ciudad_ID
                        WHERE cd.nombre LIKE '%Dayton%')
    ORDER BY no_rentas DESC

-- CONSULTA 10
SELECT p.nombre as pais, cd.nombre AS ciudad, ct.nombre_categoria AS categoria, COUNT(ct.id_categoria) AS cantidad,
	(MAX(COUNT(ct.id_categoria)) OVER (PARTITION BY cd.nombre)) AS maxima_cantidad
	FROM renta r
		INNER JOIN cliente c ON r.id_cliente = c.id_cliente
		INNER JOIN direccion d ON c.id_direccion = d.id_direccion
		INNER JOIN ciudad cd ON d.id_ciudad = cd.id_ciudad
		INNER JOIN pais p ON cd.id_pais = p.id_pais
		INNER JOIN tienda t ON t.id_tienda = r.id_tienda
		INNER JOIN inventario i ON t.id_tienda = i.id_tienda
		INNER JOIN pelicula pl ON i.id_pelicula = pl.id_pelicula
		INNER JOIN categoria_pelicula pc ON pl.id_pelicula = pc.id_pelicula
		INNER JOIN categoria ct ON pc.id_categoria = ct.id_categoria
		WHERE ct.nombre_categoria like '%Horror%'
		GROUP BY cd.nombre, p.nombre, ct.id_categoria