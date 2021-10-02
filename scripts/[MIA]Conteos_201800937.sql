-- Script (DML) con los COUNT’s de todas las tablas que utilizaron en su modelo relacional.
-- Debe tener el siguiente formato: [MIA]Conteos_#CARNET.sql


------------------------------------ COUNT ------------------------------------
SELECT COUNT(actor.nombre_actor) from actor; 									-- ACTOR 		 	 	199
SELECT COUNT(categoria.nombre_categoria) from categoria; 						-- CATEGORIA 	 	 	16
SELECT COUNT(ciudad.nombre) from ciudad; 										-- CIUDAD		 	 	600
SELECT COUNT(clasificacion.nombre_clasificacion) from clasificacion; 			-- CLASIFICACION 	 	5
SELECT COUNT(cliente.nombre) from cliente;										-- CLIENTE		 	 	599
SELECT COUNT(direccion.nombre_direccion) from direccion; 						-- DIRECCION	 	 	603
SELECT COUNT(empleado.nombre) from empleado; 									-- EMPLEADO		 	 	2
SELECT COUNT(encargado_tienda.id_empleado) from encargado_tienda;				-- ENCARGADO_TIENDA  	2
SELECT COUNT(inventario.id_inventario) from inventario; 						-- INVENTARIO		 	1521
SELECT COUNT(lenguaje.nombre_lenguaje) from lenguaje; 							-- LENGUAJE			 	6
SELECT COUNT(pais.nombre) from pais; 											-- PAIS				 	109
SELECT COUNT(pelicula.titulo) from pelicula; 									-- PELICULA			 	1000
SELECT COUNT(actor_pelicula.id_actor_pelicula) from actor_pelicula; 			-- ACTOR_PELICULA	 	5462						
SELECT COUNT(categoria_pelicula.id_categoria_pelicula) from categoria_pelicula; -- CATEGORIA_PELICULA 	1000 						
SELECT COUNT(lenguaje_pelicula.id_lenguaje_pelicula) from lenguaje_pelicula; 	-- LENGUAJE_PELICULA	1000  						
SELECT COUNT(renta.id_renta) from renta; 										-- RENTA				16045  
SELECT COUNT(tienda.nombre) from tienda; 										-- TIENDA				2
