-- Script (DML) con las diferentes consultas utilizadas para realizar la carga y distribución de la información 
-- en la nueva base de datos. Debe tener el siguiente formato: [MIA]CargaDeDatos_#CARNET.sql

------------------------------------ CREANDO TABLA PAIS ------------------------------------
-- LLENANDO DATOS DE PAIS
INSERT INTO pais(nombre)
SELECT DISTINCT temporal.PAIS_CLIENTE FROM temporal
WHERE temporal.PAIS_CLIENTE != '-';

------------------------------------ CREANDO TABLA CIUDAD ------------------------------------
-- LLENANDO TABLA CIUDAD
INSERT INTO ciudad(nombre, id_pais)
SELECT DISTINCT temporal.CIUDAD_CLIENTE, pais.id_pais
FROM temporal INNER JOIN pais ON pais.nombre = temporal.PAIS_CLIENTE
WHERE temporal.CIUDAD_CLIENTE != '-';

------------------------------------ CREANDO TABLA DIRECCION ------------------------------------
-- LLENANDO TABLA DIRECCION
INSERT INTO direccion(nombre_direccion, codigo_postal, id_ciudad)
SELECT DISTINCT ON(temporal.DIRECCION_CLIENTE) temporal.DIRECCION_CLIENTE, temporal.CODIGO_POSTAL_CLIENTE, ciudad.id_ciudad
FROM temporal INNER JOIN ciudad ON ciudad.nombre = temporal.CIUDAD_CLIENTE
WHERE temporal.DIRECCION_CLIENTE != '-';

------------------------------------ CREANDO TABLA TIENDA ------------------------------------
-- LLENAR TABLA DE TIENDA
INSERT INTO tienda(nombre,id_direccion)
SELECT DISTINCT ON(temporal.NOMBRE_TIENDA) temporal.NOMBRE_TIENDA, direccion.id_direccion
FROM temporal INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_TIENDA
WHERE temporal.NOMBRE_TIENDA != '-';

------------------------------------ CREANDO TABLA EMPLEADO ------------------------------------
-- LLENANDO LA TABLA EMPLEADO
INSERT INTO empleado(nombre,apellido,correo,nombre_usuario,contrasena,estado,id_direccion,id_tienda)
SELECT DISTINCT ON(temporal.NOMBRE_EMPLEADO) split_part(temporal.NOMBRE_EMPLEADO,' ',1), split_part(temporal.NOMBRE_EMPLEADO,' ',2),temporal.CORREO_EMPLEADO,temporal.USUARIO_EMPLEADO,temporal.PASSWORD_EMPLEADO,temporal.EMPLEADO_ACTIVO,direccion.id_direccion,tienda.id_tienda 
FROM temporal 
	INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_EMPLEADO
	INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_EMPLEADO
WHERE temporal.NOMBRE_EMPLEADO != '-';

------------------------------------ CREANDO TABLA ENCARGADO_TIENDA ------------------------------------
-- LLENAR TABLA DE ENCARGADO_TIENDA
INSERT INTO encargado_tienda(id_empleado,id_tienda)
SELECT DISTINCT empleado.id_empleado, tienda.id_tienda
FROM temporal 
	INNER JOIN empleado ON empleado.nombre = split_part(temporal.ENCARGADO_TIENDA,' ',1) and empleado.apellido = split_part(temporal.ENCARGADO_TIENDA,' ',2)
	INNER JOIN tienda ON tienda.nombre = temporal.NOMBRE_TIENDA;

------------------------------------ CREANDO TABLA CLIENTE ------------------------------------
-- LLENAR TABLA CLIENTE
INSERT INTO cliente(nombre,apellido,correo,fecha_registro,estado,id_direccion,id_tienda)
SELECT DISTINCT ON(temporal.NOMBRE_CLIENTE) split_part(temporal.NOMBRE_CLIENTE,' ',1), split_part(temporal.NOMBRE_CLIENTE,' ',2),temporal.CORREO_CLIENTE,temporal.FECHA_CREACION,temporal.CLIENTE_ACTIVO,direccion.id_direccion,tienda.id_tienda 
FROM temporal 
	INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_CLIENTE
	INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_PREFERIDA
WHERE temporal.NOMBRE_CLIENTE != '-';

------------------------------------ INFORMACION CLASIFICACION ------------------------------------
-- LLENAR DATOS A LA TABLA CLASIFICACION
INSERT INTO clasificacion(nombre_clasificacion)
SELECT DISTINCT ON(temporal.CLASIFICACION) temporal.CLASIFICACION FROM temporal
WHERE temporal.CLASIFICACION != '-';

------------------------------------ PELICULA ------------------------------------
-- LLENAR DATOS DE LA TABLA PELICULA
INSERT INTO pelicula(titulo,descripcion,lanzamiento,duracion,dias_renta,costo_renta,costo_por_damage,id_clasificacion)
SELECT DISTINCT ON(temporal.NOMBRE_PELICULA) temporal.NOMBRE_PELICULA,temporal.DESCRIPCION_PELICULA,temporal.LANZAMIENTO_YEAR,temporal.DURACION,temporal.DIAS_RENTA,temporal.COSTO_RENTA, temporal.COSTO_POR_DAMAGE,clasificacion.id_clasificacion 
FROM temporal
	INNER JOIN clasificacion ON clasificacion.nombre_clasificacion = temporal.CLASIFICACION
WHERE temporal.NOMBRE_PELICULA != '-';

------------------------------------ LENGUAJE ------------------------------------
-- LLENAR DATOS DE LA TABLA LENGUAJE
INSERT INTO lenguaje(nombre_lenguaje)
SELECT DISTINCT ON(temporal.LENGUAJE_PELICULA) temporal.LENGUAJE_PELICULA FROM temporal
WHERE temporal.LENGUAJE_PELICULA != '-';

------------------------------------ CATEGORIA ------------------------------------
-- LLENAR DATOS DE LA TABLA CATEGORIA
INSERT INTO categoria(nombre_categoria)
SELECT DISTINCT ON(temporal.CATEGORIA_PELICULA) temporal.CATEGORIA_PELICULA FROM temporal
WHERE temporal.CATEGORIA_PELICULA != '-';

------------------------------------ ACTOR ------------------------------------
-- LLENAR DATOS DE LA TABLA ACTOR
INSERT INTO actor(nombre_actor)
SELECT DISTINCT ON(temporal.ACTOR_PELICULA) temporal.ACTOR_PELICULA FROM temporal
WHERE temporal.ACTOR_PELICULA != '-';

------------------------------------ LENGUAJE_PELICULA ------------------------------------
-- LLENAR TABLA DE LENGUAJE_PELICULA
INSERT INTO lenguaje_pelicula(id_lenguaje,id_pelicula)
SELECT DISTINCT lenguaje.id_lenguaje, pelicula.id_pelicula
FROM temporal 
	INNER JOIN lenguaje ON lenguaje.nombre_lenguaje = temporal.LENGUAJE_PELICULA
	INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA;
	
------------------------------------ CATEGORIA_PELICULA ------------------------------------
-- LLENAR TABLA DE CATEGORIA_PELICULA
INSERT INTO categoria_pelicula(id_pelicula, id_categoria)
SELECT DISTINCT pelicula.id_pelicula, categoria.id_categoria
FROM temporal 
	INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA
	INNER JOIN categoria ON categoria.nombre_categoria = temporal.CATEGORIA_PELICULA;

------------------------------------ ACTOR_PELICULA ------------------------------------
-- LLENAR TABLA DE ACTOR_PELICULA
INSERT INTO actor_pelicula(id_pelicula, id_actor)
SELECT DISTINCT pelicula.id_pelicula, actor.id_actor
FROM temporal 
	INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA
	INNER JOIN actor ON actor.nombre_actor = temporal.ACTOR_PELICULA;

------------------------------------ INVENTARIO ------------------------------------
-- LLENAR TABLA DE INVENTARIO
INSERT INTO inventario(id_pelicula, id_tienda)
SELECT DISTINCT pelicula.id_pelicula, tienda.id_tienda
FROM temporal 
	INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA
	INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_PELICULA;
;		

------------------------------------ RENTA ------------------------------------
-- LLENAR TABLA RENTA
INSERT INTO renta(monto,fecha_pago,fecha_renta,fecha_retorno,id_empleado,id_tienda,id_cliente)
SELECT DISTINCT temporal.MONTO_A_PAGAR,temporal.FECHA_PAGO,temporal.FECHA_RENTA,temporal.FECHA_RETORNO,empleado.id_empleado,tienda.id_tienda,cliente.id_cliente
FROM temporal
	INNER JOIN empleado ON empleado.nombre = split_part(temporal.NOMBRE_EMPLEADO,' ',1) and empleado.apellido = split_part(temporal.NOMBRE_EMPLEADO,' ',2)
	INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_PELICULA
	INNER JOIN cliente ON cliente.nombre = split_part(temporal.NOMBRE_CLIENTE,' ',1) and cliente.apellido = split_part(temporal.NOMBRE_CLIENTE,' ',2);
