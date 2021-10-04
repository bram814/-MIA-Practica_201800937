from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os


app = Flask(__name__)
CORS(app)

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "password"

try:
    CONECTION = psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASS,
        host = DB_HOST)
    
    cur = CONECTION.cursor()
    
    
    @app.route('/')
    def index():
        return "hola mundo"

    @app.route('/consulta1')
    def consulta1():
        try:
            TABLA = '''
            <center>
            <h1>CONSULTA 1</h1>
            '''
            CONSULTA_1 = '''
            SELECT SUM(inventario.cantidad)
                FROM inventario
                    INNER JOIN pelicula ON pelicula.id_pelicula = inventario.id_pelicula
                    WHERE LOWER(pelicula.titulo )= 'sugar wonka';
                        '''
            cur.execute(CONSULTA_1)
            rows = cur.fetchall()
            for row in rows:
                for column in row:
                    TABLA += f"Cantidad de Copias que Existen para \"Sugar Wonka\": {column}"
                    TABLA += "</center>"
                    return TABLA
        except Exception as e:
            return f"{e}"
        return "-"
    
    @app.route('/consulta2')
    def consulta2():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 2</h1>
            <p>Mostrar el nombre, apellido y pago total de todos los clientes que han rentado películas por lo menos 40 veces.</>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>id_cliente</th>
                <th>nombre</th>
                <th>apellido</th>
                <th>pago_total</th>
                <th>cantidad</th>
            </tr>
            '''
            CONSULTA_2 = '''
            SELECT cliente.id_cliente,cliente.nombre,cliente.apellido, SUM(renta.monto::decimal) pago_total, COUNT(renta.monto::decimal) cantidad
                FROM cliente
                    INNER JOIN renta ON renta.id_cliente = cliente.id_cliente
                    GROUP BY (cliente.id_cliente, cliente.nombre, cliente.apellido)
                    HAVING COUNT(renta.monto::decimal) >= 40
                    ORDER BY cliente.nombre;
            '''
            cur.execute(CONSULTA_2)
            rows = cur.fetchall()
            for row in rows:
                print(row)
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                    print(column)
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            return TABLA
        except Exception as e:
            return f"{e}"

    
    @app.route('/consulta3')
    def consulta3():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 3</h1>
            <p>Mostrar el nombre y apellido (en una sola columna) de los actores que
            contienen la palabra “SON” en su apellido, ordenados por su primer
            nombre.</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>id_actor</th>
                <th>nombre</th>
            </tr>
            '''
            CONSULTA_3 = '''
            SELECT actor.id_actor,actor.nombre_actor
                FROM actor
                WHERE split_part(actor.nombre_actor,' ',2) LIKE '%son%'
                ORDER BY split_part(actor.nombre_actor,' ',1);
            '''
            cur.execute(CONSULTA_3)
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                    # print(column)
                cont+=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
    
        
    @app.route('/consulta4')
    def consulta4():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 4</h1>
            <p>Mostrar el nombre y apellido de los actores que participaron en una
            película cuya descripción incluye la palabra “crocodile” y “shark” junto
            con el año de lanzamiento de la película, ordenados por el apellido del
            actor en forma ascendente.</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>nombre_actor</td>
                <th>apellido_actor</td>
                <th>titulo</td>
                <th>descripcion</td>
                <th>lanzamiento</td>
                
            </tr>
            '''
            CONSULTA_4 = '''
            SELECT split_part(actor.nombre_actor,' ',1) nombre_actor, split_part(actor.nombre_actor,' ',2) apellido_actor,pelicula.titulo, pelicula.descripcion, pelicula.lanzamiento 
                FROM actor 
                    INNER JOIN actor_pelicula ON actor_pelicula.id_actor = actor.id_actor 
                    INNER JOIN pelicula ON pelicula.id_pelicula = actor_pelicula.id_pelicula
                    WHERE lower(pelicula.descripcion) LIKE '%crocodile%' and lower(pelicula.descripcion) LIKE '%shark%'
                    ORDER BY split_part(actor.nombre_actor,' ',2) ASC;
            '''
            cur.execute(CONSULTA_4)
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                    # print(column)
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
    
    @app.route('/consulta5')
    def consulta5():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 5</h1>
            <p>Mostrar el país y el nombre del cliente que más películas rentó así como
            también el porcentaje que representa la cantidad de películas que rentó
            conrespecto al resto de clientes del país.</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>nombre_actor</td>
                <th>apellido_actor</td>
                <th>titulo</td>
                <th>descripcion</td>
                <th>lanzamiento</td>
                
            </tr>
            '''
            CONSULTA_5 = '''
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
                
            '''
            cur.execute(CONSULTA_5)
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                    # print(column)
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
    
    @app.route('/consulta6')
    def consulta6():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 6</h1>
            <p>Mostrar el total de clientes y porcentaje de clientes por ciudad y país. El
            ciento por ciento es el total de clientes por país. (Tip: Todos los
            porcentajes por ciudad de un país deben sumar el 100%).</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>pais</td>
                <th>ciudad</td>
                <th>promedio</td>
                
            </tr>
            '''
            CONSULTA_6 = '''
            SELECT p.nombre AS pais,ci.nombre AS ciudad,((COUNT(c.id_cliente))*100 /(
                SELECT COUNT(cl.id_cliente)
                    FROM cliente cl
                        INNER JOIN direccion d ON cl.id_direccion = d.id_direccion
                        INNER JOIN ciudad ci on d.id_ciudad = ci.id_ciudad
                        INNER JOIN pais z ON ci.id_pais = z.id_pais
                        WHERE p.nombre = z.nombre
                        GROUP BY (z.nombre)
                )) AS promedio
                FROM cliente c
                    INNER JOIN direccion d ON c.id_direccion = d.id_direccion
                    INNER JOIN ciudad ci on d.id_ciudad = ci.id_ciudad
                    INNER JOIN pais p ON ci.id_pais = p.id_pais
                    GROUP BY (p.nombre,ci.nombre)
                    ORDER BY p.nombre ASC;
            '''
            cur.execute(CONSULTA_6)
            rows = cur.fetchall()
            for row in rows:
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
     
    @app.route('/consulta7')
    def consulta7():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 7</h1>
            <p>Mostrar el nombre del país, la ciudad y el promedio de rentas por ciudad.
            Por ejemplo: si el país tiene 3 ciudades, se deben sumar todas las rentas dela ciudad y dividirlo dentro 
            de tres (número de ciudades del país).</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>pais</th>
                <th>ciudad</th>
                <th>renta</th>
                <th>promedio_renta</th>
                
            </tr>
            '''
            CONSULTA_7 = '''
            SELECT p.nombre AS "pais", ci.nombre AS ciudad,COUNT(ci.id_pais) as "renta", (COUNT(ci.id_ciudad))/(
                SELECT COUNT(r.id_renta)
                    FROM renta r
                        INNER JOIN cliente c ON c.id_cliente = r.id_cliente
                        INNER JOIN direccion d ON d.id_direccion = c.id_direccion
                        INNER JOIN ciudad cd ON cd.id_ciudad = d.id_ciudad
                        INNER JOIN pais z ON z.id_pais = cd.id_pais
                        WHERE ci.nombre = cd.nombre
                        GROUP BY ci.nombre, cd.nombre
            ) AS "promedio"
            FROM renta r
                INNER JOIN cliente c ON r.id_cliente = c.id_cliente
                INNER JOIN direccion d ON d.id_direccion = c.id_direccion
                INNER JOIN ciudad ci ON ci.id_ciudad = d.id_ciudad
                INNER JOIN pais p ON p.id_pais = ci.id_pais
                GROUP BY (p.nombre,ci.nombre)
                ORDER BY p.nombre
            '''
            cur.execute(CONSULTA_7)
            rows = cur.fetchall()
            for row in rows:
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
    
    @app.route('/consulta8')
    def consulta8():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 8</h1>
            <p>Mostrar el nombre del país y el porcentaje de rentas de películas de la
            categoría “Sports”. El porcentaje es sobre el número total de rentas de
            cada país.</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>pais</td>
                <th>categoria</td>
                <th>porcentaje</td>
                
            </tr>
            '''
            CONSULTA_8 = '''
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
            '''
            cur.execute(CONSULTA_8)
            rows = cur.fetchall()
            for row in rows:
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"  

    @app.route('/consulta9')
    def consulta9():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 9</h1>
            <p>Mostrar la lista de ciudades de Estados Unidos y el número de rentas de
            películas para las ciudades que obtuvieron más rentas que la ciudad
            "Dayton".</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>pais</td>
                <th>ciudad</td>
                <th>no. renta</td>
                
            </tr>
            '''
            CONSULTA_9 = '''
            SELECT p.nombre AS pais, cd.nombre AS ciudad, COUNT(r.id_cliente) as no_rentas
                FROM renta r
                    INNER JOIN cliente c ON r.id_cliente = c.id_cliente
                    INNER JOIN direccion d ON c.id_direccion = d.id_direccion
                    INNER JOIN ciudad cd ON  d.id_ciudad = cd.id_ciudad
                    INNER JOIN pais p ON cd.id_pais = p.id_pais
                    GROUP BY p.nombre, cd.nombre
                    HAVING p.nombre LIKE '%United States%' 
                    AND (COUNT(r.id_cliente::decimal) > (SELECT COUNT(r.id_cliente::decimal) 
                                        FROM renta r
                                        INNER JOIN cliente c ON r.id_cliente = c.id_cliente
                                        INNER JOIN direccion d ON c.id_direccion = d.id_direccion
                                        INNER JOIN ciudad cd ON  d.id_ciudad = cd.id_ciudad
                                        WHERE cd.nombre LIKE '%Dayton%'))
            '''
            cur.execute(CONSULTA_9)
            rows = cur.fetchall()
            for row in rows:
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"
    
    @app.route('/consulta10')
    def consulta10():
        try:
            cont = 1
            TABLA = '''
            <center>
            <h1>CONSULTA 10</h1>
            <p>Mostrar todas las ciudades por país en las que predomina la renta de
            películas de la categoría “Horror”. Es decir, hay más rentas que las otras
            categorías.</p>
            <h1></h1>
            <table class="default" border="1"  cellspacing="1">\n
            <tr>
                <th>No.</th>
                <th>pais</td>
                <th>ciudad</td>
                <th>categoria</td>
                <th>cantidad</td>
                <th>maxima_cantidad</td>
                
            </tr>
            '''
            CONSULTA_10 = '''
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
            '''
            cur.execute(CONSULTA_10)
            rows = cur.fetchall()
            for row in rows:
                TABLA += f'  <tr>\n  <td>{cont}</td>'
                for column in row:
                    TABLA += f'''       <td>{str(column)}</td>\n'''
                cont +=1
                TABLA += '  </tr>\n'
            TABLA+= '</table>\n</center>'
            print(TABLA)
            return TABLA
        except Exception as e:
            return f"{e}"

    @app.route('/eliminarTemporal', methods=['GET']) # ELIMINA DATOS DE LA TABLA TEMPORAL
    def delete_data_temp():
        try:
            cur.execute('DELETE FROM temporal;')
            cur.execute('DROP TABLE temporal;')
            CONECTION.commit()
        except Exception as e:
            return f"{e}"
        return "DATOS DE LA TABLA TEMPORAL ELIMINADOS!"

    @app.route('/eliminarModelo', methods=['GET']) # ELIMINA TABLA TEMPORAL
    def delete_temp():
        try:
            DELETE_MODELO = '''
            -- ELIMINAR DATOS DE LA TABLA RENTA
            DELETE FROM renta;
            -- ELIMINAR DATOS DE LA TABLA INVENTARIO
            DELETE FROM inventario;
            -- ELIMINAR DATOS DE LA TABLA ACTOR_PELICULA
            DELETE FROM actor_pelicula;
            -- ELIMINAR DATOS DE LA TABLA CATEGORIA_PELICULA
            DELETE FROM categoria_pelicula;
            -- ELIMINAR DATOS DE LA TABLA LENGUAJE_PELICULA
            DELETE FROM lenguaje_pelicula;
            -- ELIMINAR DATOS DE LA TABLA ACTOR
            DELETE FROM actor;
            -- ELIMINAR DATOS DE LA TABLA CATEGORIA
            DELETE FROM categoria;
            -- ELIMINAR DATOS DE LA TABLA LENGUAJE
            DELETE FROM lenguaje;
            -- ELIMINAR DATOS DE LA TABLA PELICULA
            DELETE FROM pelicula;
            -- ELIMINAR DATOS DE LA TABLA CLASIFICACION
            DELETE FROM clasificacion;
            -- ELIMINAR DATOS DE LA TABLA CLIENTE
            DELETE FROM cliente;
            -- ELIMINAR DATOS DE LA TABLA ENCARGADO_TIENDA
            DELETE FROM encargado_tienda;
            -- ELIMINAR DATOS DE LA TABLA EMPLEADO
            DELETE FROM empleado;
            -- ELIMINAR DATOS DE LA TABLA TIENDA
            DELETE FROM tienda;
            -- ELIMINAR DATOS DE DIRECCION
            DELETE FROM direccion;
            -- ELIMINAR DATOS CIUDAD
            DELETE FROM ciudad;
            -- ELIMINA LOS DATOS DE LA TEMPORAL
            DELETE FROM pais;
            -- ELIMINAR TABLA RENTA
            DROP TABLE renta;
            -- ELIMINAR TABLA INVENTARIO
            DROP TABLE inventario;
            -- ELIMINAR TABLA ACTOR_PELICULA
            DROP TABLE actor_pelicula;
            -- ELIMINAR TABLA CATEGORIA_PELICULA
            DROP TABLE categoria_pelicula;
            -- ELIMINAR TABLA LENGUAJE_PELICULA
            DROP TABLE lenguaje_pelicula;
            -- ELIMINAR TABLA ACTOR
            DROP TABLE actor;
            -- ELIMINAR TABLA CATEGORIA
            DROP TABLE categoria;
            -- ELIMINAR TABLA LENGUAJE
            DROP TABLE lenguaje;
            -- ELIMINAR TABLA DE LA TABLA PELICULA
            DROP TABLE pelicula;
            -- ELIMINAR TABLA CLASIFICACION
            DROP TABLE clasificacion;
            -- ELIMINAR TABLA CLIENTE
            DROP TABLE cliente;
            -- ELIMINAR TABLA ENCARGADO_TIENDA
            DROP TABLE encargado_tienda;
            -- ELIMINAR TABLA EMPLEADO
            DROP TABLE empleado;
            -- ELIMINAR TIENDA
            DROP TABLE tienda;
            -- ELMINAR TABLA DIRECCION
            DROP TABLE direccion;
            -- ELMINAR TABLA CIUDAD
            DROP TABLE ciudad;
            -- ELIMINA LA TABLA PAIS
            DROP TABLE pais;
            
            '''
            cur.execute(DELETE_MODELO)
            CONECTION.commit()
        except Exception as e:
            return f"{e}"
        return "MODELO ELIMINADO!"

    @app.route('/cargarTemporal', methods=['GET'])
    def cargar_temporal():
        try:
            # CREA LA TABLA TEMPORAL
            TABLE_TEMPORAL = '''CREATE TABLE temporal(
                NOMBRE_CLIENTE VARCHAR,
                CORREO_CLIENTE VARCHAR,
                CLIENTE_ACTIVO VARCHAR,
                FECHA_CREACION VARCHAR,
                TIENDA_PREFERIDA VARCHAR,
                DIRECCION_CLIENTE VARCHAR,
                CODIGO_POSTAL_CLIENTE VARCHAR,
                CIUDAD_CLIENTE VARCHAR,
                PAIS_CLIENTE VARCHAR,
                FECHA_RENTA VARCHAR,
                FECHA_RETORNO VARCHAR,
                MONTO_A_PAGAR VARCHAR,
                FECHA_PAGO VARCHAR,
                NOMBRE_EMPLEADO VARCHAR,
                CORREO_EMPLEADO VARCHAR,
                EMPLEADO_ACTIVO VARCHAR,
                TIENDA_EMPLEADO VARCHAR,
                USUARIO_EMPLEADO VARCHAR,
                PASSWORD_EMPLEADO VARCHAR,
                DIRECCION_EMPLEADO VARCHAR,
                CODIGO_POSTAL_EMPLEADO VARCHAR,
                CIUDAD_EMPLEADO VARCHAR,
                PAIS_EMPLEADO VARCHAR,
                NOMBRE_TIENDA VARCHAR,
                ENCARGADO_TIENDA VARCHAR,
                DIRECCION_TIENDA VARCHAR,
                CODIGO_POSTAL_TIENDA VARCHAR,
                CIUDAD_TIENDA VARCHAR,
                PAIS_TIENDA VARCHAR,
                TIENDA_PELICULA VARCHAR,
                NOMBRE_PELICULA VARCHAR,
                DESCRIPCION_PELICULA VARCHAR,
                LANZAMIENTO_YEAR VARCHAR,
                DIAS_RENTA VARCHAR,
                COSTO_RENTA	VARCHAR,
                DURACION VARCHAR,
                COSTO_POR_DAMAGE VARCHAR,
                CLASIFICACION VARCHAR,
                LENGUAJE_PELICULA VARCHAR,
                CATEGORIA_PELICULA VARCHAR,
                ACTOR_PELICULA VARCHAR);'''
            cur.execute(TABLE_TEMPORAL)
            # CARGA LOS DATOS A LA TABLA TEMPORAL
            CHARGE_MASIVE_CSV = '''COPY temporal from '/home/abraham/Escritorio/BlockbusterData.csv' USING delimiters ';' csv header encoding 'windows-1251';'''
            cur.execute(CHARGE_MASIVE_CSV)
            
            CONECTION.commit()
            # rows = cur.fetchall() # SOLO PARA SELECT
        except Exception as e:
            return f"{e}"

        return "TABLA TEMPORAL CREADA!"


    @app.route('/cargarModelo', methods=['GET'])
    def cargar_modelo():
        try:
            # ------------------------- CREA LA TABLA PAIS ------------------------- 
            TABLE_PAIS =  '''
            CREATE TABLE pais(
                id_pais INT GENERATED BY DEFAULT AS IDENTITY,
                nombre VARCHAR,
                primary key (id_pais)
            );'''
            cur.execute(TABLE_PAIS)
            # LLENA LA TABLA PAIS
            CHARGE_TABLE_PAIS = '''
            INSERT INTO pais(nombre)
                SELECT DISTINCT temporal.PAIS_CLIENTE FROM temporal
                WHERE temporal.PAIS_CLIENTE != '-';'''
            cur.execute(CHARGE_TABLE_PAIS)
            # ------------------------- CREA LA TABLA CIUDAD ------------------------- 
            TABLE_CIUDAD = '''
            CREATE TABLE ciudad(
                id_ciudad INT GENERATED BY DEFAULT AS IDENTITY,
                nombre VARCHAR,
                id_pais INT,
                primary key (id_ciudad),
                FOREIGN KEY (id_pais) REFERENCES pais(id_pais)
            );'''
            cur.execute(TABLE_CIUDAD)
            # LLENA LA TABLA CIUDAD
            CHARGE_TABLE_CIUDAD = '''
            INSERT INTO ciudad(nombre, id_pais)
                SELECT DISTINCT temporal.CIUDAD_CLIENTE, pais.id_pais
                FROM temporal INNER JOIN pais ON pais.nombre = temporal.PAIS_CLIENTE
                WHERE temporal.CIUDAD_CLIENTE != '-';'''
            cur.execute(CHARGE_TABLE_CIUDAD)
            # ------------------------- CREA LA TABLA DIRECCION ------------------------- 
            TABLE_DIRECCION = '''
            CREATE TABLE direccion(
                id_direccion INT GENERATED BY DEFAULT AS IDENTITY,
                nombre_direccion VARCHAR,
                codigo_postal VARCHAR,
                id_ciudad INT,
                primary key (id_direccion),
                FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad));'''
            cur.execute(TABLE_DIRECCION)
            # LLENA LA TABLA DIRECCION
            CHARGE_TABLE_DIRECCION = '''
            INSERT INTO direccion(nombre_direccion, codigo_postal, id_ciudad)
                SELECT DISTINCT ON(temporal.DIRECCION_CLIENTE) temporal.DIRECCION_CLIENTE, temporal.CODIGO_POSTAL_CLIENTE, ciudad.id_ciudad
                FROM temporal INNER JOIN ciudad ON ciudad.nombre = temporal.CIUDAD_CLIENTE
                WHERE temporal.DIRECCION_CLIENTE != '-';'''
            cur.execute(CHARGE_TABLE_DIRECCION)
            # ------------------------- CREA LA TABLA TIENDA ------------------------- 
            TABLE_TIENDA = '''
            CREATE TABLE tienda(
                id_tienda INT GENERATED BY DEFAULT AS IDENTITY,
                nombre VARCHAR,
                id_direccion INT,
                PRIMARY KEY(id_tienda),
                FOREIGN KEY(id_direccion) REFERENCES direccion(id_direccion)
            );'''
            cur.execute(TABLE_TIENDA)
            # LLENA LA TABLA TIENDA
            CHARGE_TABLE_TIENDA = '''
            INSERT INTO tienda(nombre,id_direccion)
                SELECT DISTINCT ON(temporal.NOMBRE_TIENDA) temporal.NOMBRE_TIENDA, direccion.id_direccion
                FROM temporal INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_TIENDA
                WHERE temporal.NOMBRE_TIENDA != '-';
            '''
            cur.execute(CHARGE_TABLE_TIENDA)
            # ------------------------- CREA LA TABLA EMPLEADO ------------------------- 
            TABLE_EMPLEADO = '''
            CREATE TABLE empleado(
                id_empleado INT GENERATED BY DEFAULT AS IDENTITY,
                nombre VARCHAR,
                apellido VARCHAR,
                correo VARCHAR,
                nombre_usuario VARCHAR,
                contrasena VARCHAR,
                estado VARCHAR,
                id_direccion INT,
                id_tienda INT,
                primary key (id_empleado),
                FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion),
                FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda)
            );'''
            cur.execute(TABLE_EMPLEADO)
            # LLENA LA TABLA EMPLEADO
            CHARGE_TABLE_EMPLEADO = '''
            INSERT INTO empleado(nombre,apellido,correo,nombre_usuario,contrasena,estado,id_direccion,id_tienda)
                SELECT DISTINCT ON(temporal.NOMBRE_EMPLEADO) split_part(temporal.NOMBRE_EMPLEADO,' ',1), split_part(temporal.NOMBRE_EMPLEADO,' ',2),temporal.CORREO_EMPLEADO,temporal.USUARIO_EMPLEADO,temporal.PASSWORD_EMPLEADO,temporal.EMPLEADO_ACTIVO,direccion.id_direccion,tienda.id_tienda 
                FROM temporal 
                    INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_EMPLEADO
                    INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_EMPLEADO
                WHERE temporal.NOMBRE_EMPLEADO != '-';
            '''
            cur.execute(CHARGE_TABLE_EMPLEADO)
            # ------------------------- CREA LA TABLA ENCARGADO_TIENDA ------------------------- 
            TABLE_ENCARGADO_TIENDA = '''
            CREATE TABLE encargado_tienda(
                id_encargado_tienda INT GENERATED BY DEFAULT AS IDENTITY,
                id_empleado INT,
                id_tienda INT,
                PRIMARY KEY (id_encargado_tienda),
                FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado),
                FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda)
            ); '''
            cur.execute(TABLE_ENCARGADO_TIENDA)
            # LLENA LA TABLA ENCARGADO_TIENDA
            CHARGE_ENCARGADO_TIENDA = '''
            INSERT INTO encargado_tienda(id_empleado,id_tienda)
                SELECT DISTINCT empleado.id_empleado, tienda.id_tienda
                FROM temporal 
                    INNER JOIN empleado ON empleado.nombre = split_part(temporal.ENCARGADO_TIENDA,' ',1) and empleado.apellido = split_part(temporal.ENCARGADO_TIENDA,' ',2)
                    INNER JOIN tienda ON tienda.nombre = temporal.NOMBRE_TIENDA
            '''
            cur.execute(CHARGE_ENCARGADO_TIENDA)
            # ------------------------- CREA LA TABLA CLIENTE ------------------------- 
            TABLE_CLIENTE ='''
            CREATE TABLE cliente(
                id_cliente INT GENERATED BY DEFAULT AS IDENTITY,
                nombre VARCHAR,
                apellido VARCHAR,
                correo VARCHAR,
                fecha_registro VARCHAR,
                estado VARCHAR,
                id_direccion INT,
                id_tienda INT,
                PRIMARY KEY (id_cliente),
                FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion),
                FOREIGN KEY (id_tienda) REFERENCES tienda(id_tienda)
            );'''
            cur.execute(TABLE_CLIENTE)
            # LLENA LA TABLA CLIENTE
            CHARGE_TABLE_CLIENTE = '''
            INSERT INTO cliente(nombre,apellido,correo,fecha_registro,estado,id_direccion,id_tienda)
                SELECT DISTINCT ON(temporal.NOMBRE_CLIENTE) split_part(temporal.NOMBRE_CLIENTE,' ',1), split_part(temporal.NOMBRE_CLIENTE,' ',2),temporal.CORREO_CLIENTE,temporal.FECHA_CREACION,temporal.CLIENTE_ACTIVO,direccion.id_direccion,tienda.id_tienda 
                FROM temporal 
                    INNER JOIN direccion ON direccion.nombre_direccion = temporal.DIRECCION_CLIENTE
                    INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_PREFERIDA
                WHERE temporal.NOMBRE_CLIENTE != '-';
            '''
            cur.execute(CHARGE_TABLE_CLIENTE)
            # ------------------------- CREA LA TABLA CLASIFICACION ------------------------- 
            TABLE_CLASIFICACION = '''
            CREATE TABLE clasificacion(
                id_clasificacion INT GENERATED BY DEFAULT AS IDENTITY,
                nombre_clasificacion VARCHAR,
                PRIMARY KEY(id_clasificacion)
            );
            '''
            cur.execute(TABLE_CLASIFICACION)
            # LLENA LA TABLA CLASIFICACION
            CHARGE_TABLE_CLASIFICACION = '''
            INSERT INTO clasificacion(nombre_clasificacion)
                SELECT DISTINCT ON(temporal.CLASIFICACION) temporal.CLASIFICACION FROM temporal
                WHERE temporal.CLASIFICACION != '-';
            ''' 
            cur.execute(CHARGE_TABLE_CLASIFICACION)
            # ------------------------- CREA LA TABLA PELICULA ------------------------- 
            TABLE_PELICULA = '''
            CREATE TABLE pelicula(
                id_pelicula INT GENERATED BY DEFAULT AS IDENTITY,
                titulo VARCHAR,
                descripcion VARCHAR,
                lanzamiento VARCHAR,
                duracion VARCHAR, 
                dias_renta VARCHAR,
                costo_renta VARCHAR,
                costo_por_damage VARCHAR,
                id_clasificacion INT,
                PRIMARY KEY(id_pelicula),
                FOREIGN KEY(id_clasificacion) REFERENCES clasificacion(id_clasificacion)
            );
            '''
            cur.execute(TABLE_PELICULA)
            # LLENA LA TABLA PELICULA
            CHARGE_TABLE_PELICULA = '''
            INSERT INTO pelicula(titulo,descripcion,lanzamiento,duracion,dias_renta,costo_renta,costo_por_damage,id_clasificacion)
                SELECT DISTINCT ON(temporal.NOMBRE_PELICULA) temporal.NOMBRE_PELICULA,temporal.DESCRIPCION_PELICULA,temporal.LANZAMIENTO_YEAR,temporal.DURACION,temporal.DIAS_RENTA,temporal.COSTO_RENTA, temporal.COSTO_POR_DAMAGE,clasificacion.id_clasificacion 
                FROM temporal
                    INNER JOIN clasificacion ON clasificacion.nombre_clasificacion = temporal.CLASIFICACION
                WHERE temporal.NOMBRE_PELICULA != '-';
            '''
            cur.execute(CHARGE_TABLE_PELICULA)
            # ------------------------- CREA LA TABLA LENGUAJE ------------------------- 
            TABLE_LENGUAJE = '''
            CREATE TABLE lenguaje(
                id_lenguaje INT GENERATED BY DEFAULT AS IDENTITY,
                nombre_lenguaje VARCHAR,
                PRIMARY KEY(id_lenguaje)
            );
            '''
            cur.execute(TABLE_LENGUAJE)
            # LLENA LA TABLA LENGUAJE
            CHARGE_TABLE_LENGUAJE = '''
            INSERT INTO lenguaje(nombre_lenguaje)
                SELECT DISTINCT ON(temporal.LENGUAJE_PELICULA) temporal.LENGUAJE_PELICULA FROM temporal
                WHERE temporal.LENGUAJE_PELICULA != '-';    
            '''
            cur.execute(CHARGE_TABLE_LENGUAJE)
            # ------------------------- CREA LA TABLA CATEGORIA ------------------------- 
            TABLE_CATEGORIA = '''
            CREATE TABLE categoria(
                id_categoria INT GENERATED BY DEFAULT AS IDENTITY,
                nombre_categoria VARCHAR,
                PRIMARY KEY(id_categoria)
            );
            '''
            cur.execute(TABLE_CATEGORIA)
            # LLENA LA TABLA CATEGORIA
            CHARGE_TABLE_CATEGORIA = '''
            INSERT INTO categoria(nombre_categoria)
                SELECT DISTINCT ON(temporal.CATEGORIA_PELICULA) temporal.CATEGORIA_PELICULA FROM temporal
                WHERE temporal.CATEGORIA_PELICULA != '-';
            '''
            cur.execute(CHARGE_TABLE_CATEGORIA)
            # ------------------------- CREA LA TABLA ACTOR ------------------------- 
            TABLE_ACTOR = '''
            CREATE TABLE actor(
                id_actor INT GENERATED BY DEFAULT AS IDENTITY,
                nombre_actor VARCHAR,
                PRIMARY KEY(id_actor)
            );
            '''
            cur.execute(TABLE_ACTOR)
            # LLENA LA TABLA ACTOR
            CHARGE_TABLE_ACTOR = '''
            INSERT INTO actor(nombre_actor)
                SELECT DISTINCT ON(temporal.ACTOR_PELICULA) temporal.ACTOR_PELICULA FROM temporal
                WHERE temporal.ACTOR_PELICULA != '-';
            '''
            cur.execute(CHARGE_TABLE_ACTOR)
            # ------------------------- CREA LA TABLA LENGUAJE_PELICULA ------------------------- 
            TABLE_LENGUAJE_PELICULA = '''
            CREATE TABLE lenguaje_pelicula(
                id_lenguaje_pelicula INT GENERATED BY DEFAULT AS IDENTITY,
                id_lenguaje INT,
                id_pelicula INT,
                PRIMARY KEY(id_lenguaje_pelicula),
                FOREIGN KEY(id_lenguaje) REFERENCES lenguaje(id_lenguaje),
                FOREIGN KEY(id_pelicula) REFERENCES pelicula(id_pelicula)
            );
            '''
            cur.execute(TABLE_LENGUAJE_PELICULA)
            # LLENA LA TABLA LENGUAJE_PELICULA
            CHARGE_TABLE_LENGUAJE_PELICULA = '''
            INSERT INTO lenguaje_pelicula(id_lenguaje,id_pelicula)
                SELECT DISTINCT lenguaje.id_lenguaje, pelicula.id_pelicula
                FROM temporal 
                    INNER JOIN lenguaje ON lenguaje.nombre_lenguaje = temporal.LENGUAJE_PELICULA
                    INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA
            '''
            cur.execute(CHARGE_TABLE_LENGUAJE_PELICULA)
            # ------------------------- CREA LA TABLA CATEGORIA_PELICULA ------------------------- 
            TABLE_CATEGORIA_PELICULA = '''
            CREATE TABLE categoria_pelicula(
                id_categoria_pelicula INT GENERATED BY DEFAULT AS IDENTITY,
                id_pelicula INT,
                id_categoria INT,
                PRIMARY KEY(id_categoria_pelicula),
                FOREIGN KEY(id_pelicula) REFERENCES pelicula(id_pelicula),
                FOREIGN KEY(id_categoria) REFERENCES categoria(id_categoria)
            );
            '''
            cur.execute(TABLE_CATEGORIA_PELICULA)
            # LLENA LA TABLA CATEGORIA_PELICULA
            CHARGE_TABLE_CATEGORIA_PELICULA = '''
            INSERT INTO categoria_pelicula(id_pelicula, id_categoria)
            SELECT DISTINCT pelicula.id_pelicula, categoria.id_categoria
            FROM temporal 
                INNER JOIN pelicula ON pelicula.titulo = temporal.NOMBRE_PELICULA
                INNER JOIN categoria ON categoria.nombre_categoria = temporal.CATEGORIA_PELICULA
            '''
            cur.execute(CHARGE_TABLE_CATEGORIA_PELICULA)
            # ------------------------- CREA LA TABLA ACTOR_PELICULA ------------------------- 
            TABLE_ACTOR_PELICULA = '''
            CREATE TABLE actor_pelicula(
                id_actor_pelicula INT GENERATED BY DEFAULT AS IDENTITY,
                id_pelicula INT,
                id_actor INT,
                PRIMARY KEY(id_actor_pelicula),
                FOREIGN KEY(id_pelicula) REFERENCES pelicula(id_pelicula),
                FOREIGN KEY(id_actor) REFERENCES actor(id_actor)
            );
            '''
            cur.execute(TABLE_ACTOR_PELICULA)
            # LLENA LA TABLA ACTOR_PELICULA
            CHARGE_TABLE_ACTOR_PELICULA = '''
            INSERT INTO actor_pelicula(id_pelicula, id_actor)
                SELECT DISTINCT pelicula.id_pelicula, actor.id_actor
                FROM temporal 
                    INNER JOIN pelicula ON pelicula.id_pelicula = (
                        SELECT id_pelicula
                        WHERE temporal.NOMBRE_PELICULA != '-'
                        AND pelicula.titulo = temporal.NOMBRE_PELICULA
                    )
                    INNER JOIN actor ON actor.id_actor = (
                        SELECT id_actor
                        WHERE temporal.ACTOR_PELICULA != '-'
                        AND actor.nombre_actor = temporal.ACTOR_PELICULA
                    );
            '''
            cur.execute(CHARGE_TABLE_ACTOR_PELICULA)
            # ------------------------- CREA LA TABLA INVENTARIO ------------------------- 
            TABLE_INVENTARIO = '''
            CREATE TABLE inventario(
                id_inventario INT GENERATED BY DEFAULT AS IDENTITY,
                id_pelicula INT,
                id_tienda INT,
	            cantidad INT,
                PRIMARY KEY(id_inventario),
                FOREIGN KEY(id_pelicula) REFERENCES pelicula(id_pelicula),
                FOREIGN KEY(id_tienda) REFERENCES tienda(id_tienda)
            );
            '''
            cur.execute(TABLE_INVENTARIO)
            # LLENA LA TABLA INVENTARIO
            CHARGE_TABLE_INVENTARIO = '''
            INSERT INTO inventario(id_pelicula, id_tienda, cantidad)
                SELECT pelicula.id_pelicula, tienda.id_tienda, COUNT(temporal.NOMBRE_PELICULA)
                    FROM temporal 
                    INNER JOIN pelicula ON pelicula.id_pelicula = (
                        SELECT id_pelicula
                            FROM pelicula
                            WHERE temporal.NOMBRE_PELICULA != '-'
                            AND pelicula.titulo = temporal.NOMBRE_PELICULA
                        )
                    INNER JOIN tienda ON tienda.id_tienda = (
                        SELECT id_tienda
                            FROM tienda
                            WHERE temporal.TIENDA_PELICULA != '-'
                            AND tienda.nombre = temporal.TIENDA_PELICULA
                        )
                WHERE temporal.NOMBRE_PELICULA != '-'
                GROUP BY pelicula.id_pelicula, tienda.id_tienda;
            '''
            cur.execute(CHARGE_TABLE_INVENTARIO)
            # ------------------------- RENTA ------------------------- 
            TABLE_RENTA = '''
            CREATE TABLE renta(
                id_renta INT GENERATED BY DEFAULT AS IDENTITY,
                monto VARCHAR,
                fecha_pago VARCHAR,
                fecha_renta VARCHAR,
                fecha_retorno VARCHAR,
                id_empleado INT,
                id_tienda INT,
                id_cliente INT,
                PRIMARY KEY(id_renta),
                FOREIGN KEY(id_empleado) REFERENCES empleado(id_empleado),
                FOREIGN KEY(id_tienda) REFERENCES tienda(id_tienda),
                FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
            );
            '''
            cur.execute(TABLE_RENTA)
            # LLENA LA TABLA RENTA
            CHARGE_TABLE_RENTA = '''
            INSERT INTO renta(monto,fecha_pago,fecha_renta,fecha_retorno,id_empleado,id_tienda,id_cliente)
            SELECT DISTINCT temporal.MONTO_A_PAGAR,temporal.FECHA_PAGO,temporal.FECHA_RENTA,temporal.FECHA_RETORNO,empleado.id_empleado,tienda.id_tienda,cliente.id_cliente
            FROM temporal
                INNER JOIN empleado ON empleado.nombre = split_part(temporal.NOMBRE_EMPLEADO,' ',1) and empleado.apellido = split_part(temporal.NOMBRE_EMPLEADO,' ',2)
                INNER JOIN tienda ON tienda.nombre = temporal.TIENDA_PELICULA
                INNER JOIN cliente ON cliente.nombre = split_part(temporal.NOMBRE_CLIENTE,' ',1) and cliente.apellido = split_part(temporal.NOMBRE_CLIENTE,' ',2)
    
            '''
            cur.execute(CHARGE_TABLE_RENTA)

            CONECTION.commit()
        except Exception as e:
            return f"{e}"
        return "SE CREÓ SUS RESPECTIVOS MODELOS Y DATOS CORRESPONDIENTES A CADA MODELO."


    if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0")        

except Exception as e:
    print(f"WARNING! - {e}")
