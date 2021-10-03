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
	
   
