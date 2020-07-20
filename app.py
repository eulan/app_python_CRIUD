from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import datetime
import json



#initialization
app = Flask(__name__)


# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tecnicaltest'
mysql = MySQL(app)



#main
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes ORDER BY compras DESC LIMIT 3 ;')
    data = cur.fetchall()
    cur.execute('SELECT * FROM productos LIMIT 3;')
    data2 = cur.fetchall()
    return render_template("index.html", clientes = data, products = data2)

#clients process
@app.route("/clientes")
def all_clients():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes ORDER BY compras DESC')
    data = cur.fetchall()
    return render_template("clientes.html", clientes = data)

@app.route("/add_client", methods = ['POST'])
def add_client():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.form['foto']
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO clientes 
            (cedula, nombre, direccion, telefono, foto)
            VALUES (%s,%s,%s,%s,%s)     
        """, (cedula, nombre, direccion, telefono, foto))
        mysql.connection.commit()
        return redirect(url_for("index"))

@app.route('/edit/<string:id>')
def get_client(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE idclientes = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit_client.html', cliente = data[0])

@app.route('/update/<string:id>', methods = ['POST'])
def update_cliente(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        foto = request.form['foto']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET cedula = %s,
                nombre = %s,
                direccion = %s,
                telefono = %s,
                foto = %s
            WHERE idclientes = %s
        """, (cedula, nombre, direccion, telefono, foto,id))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE idclientes = %s', (id))
    mysql.connection.commit()
    return redirect(url_for('index'))


#products process
@app.route("/productos")
def all_products():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    return render_template("productos.html", productos = data)


@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cantidadBodega = request.form['cantidadBodega']
        foto_producto = request.form['foto_producto']
        estado = 0 if int(cantidadBodega) == 0 else 1
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO productos 
            (categoria, nombre, precio, cantidadBodega, estado, foto_producto)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (categoria, nombre, precio, cantidadBodega, estado, foto_producto))

        mysql.connection.commit()
        return redirect(url_for("index"))

@app.route('/edit_product/<string:id>')
def get_product(id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM productos WHERE idproductos = %s", (id))
    data = cur.fetchall()
    return render_template('edit_product.html', producto = data[0])

@app.route('/update_product/<string:id>', methods = ['POST'])
def update_product(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        cantidadBodega = request.form['cantidadBodega']
        foto_producto = request.form['foto_producto']
        estado = 0 if int(cantidadBodega) == 0 else 1
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET categoria = %s,
                nombre = %s,
                precio = %s,
                cantidadBodega = %s,
                estado = %s,
                foto_producto = %s
            WHERE idproductos = %s    
        """, (categoria, nombre, precio, cantidadBodega, estado, foto_producto,id))
        mysql.connection.commit()
        return redirect(url_for("index"))

@app.route('/delete_product/<string:id>')
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM productos WHERE idproductos = %s", (id))
    mysql.connection.commit()
    return redirect(url_for("index")) 


#facturation process

@app.route("/facturas")
def all_facturas():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT clientes.idClientes,
           clientes.cedula, 
           clientes.nombre,
           clientes.foto,
           clientes.compras,
           facturas.cantidadProductos,
           facturas.fecha,
           facturas.valorTotal,
           facturas.payMethod,
           facturas.compraCliente,
           facturas.idFactura
    FROM   clientes
    INNER JOIN facturas ON
            clientes.idClientes = facturas.clienteID;
    """)
    data = cur.fetchall()

    productos_facturas = []

    clientes_facturas = {}

    id_an = 0 
    id_des = 0

    for factura in data:
        id_des = factura[0]
        productos_facturas.append(
            {
            'id_factura' : factura[10],
            'cedula' : factura[1],
            'nombre' : factura[2],
            'fecha' : factura[6],
            'valorTotal' : factura[7],
            'payMethod' : factura[8],
            'compras' : json.loads(factura[9])
            }
        )

        if (id_an != id_des) :
            clientes_facturas[factura[0]] = {
                'nombre' : factura[2],
                'cedula' : factura[1],
                'foto' : factura[3],
                'compras' : factura[4],
                'facturas' : []
            }
            clientes_facturas[factura[0]]['facturas'].append(productos_facturas)
        else:
            clientes_facturas[factura[0]]['facturas'].append(productos_facturas)   

        id_an = id_des

        #clientes_facturas[factura[0]]['facturas'].append(productos_facturas)
        print(clientes_facturas[factura[0]]['facturas'])
        productos_facturas = []

    
    return render_template("facturas.html", facturas = clientes_facturas)



@app.route("/compra/<string:id>")
def get_compra_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE idclientes = {0}'.format(id))
    data = cur.fetchall()
    cur.execute('SELECT * FROM productos')
    data2 = cur.fetchall()
    payMethods = ['efectivo', 'Cheque', 'Paypal', 'PSE', 'NEQUI']
    categ = list( set( [ d[1] for d in data2] ) )
    
    print(categ)

    return render_template('compra_client.html', cliente = data[0], productos = data2, categoria = categ, lon = len(categ), paymethods = payMethods, lonpay = len(payMethods)) 

@app.route("/gen_factura/<string:id>", methods = ['POST'])
def gen_factura(id):

    #POST request
    if request.method == 'POST':

        data_obtain = request.get_data()
        data_obtain = json.loads(data_obtain.decode('utf-8'))
        data_obtain['fecha'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cantidad_productos = data_obtain['cantDeProductos']
        fecha = data_obtain['fecha']
        total_dinero = data_obtain['totalDinero']
        metodo_pago = data_obtain['metodoPago']
        productos = json.dumps(data_obtain['productos'])

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO facturas
            (clienteID, cantidadProductos, fecha, valorTotal, payMethod, compraCliente) 
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (id, cantidad_productos, fecha, total_dinero, metodo_pago, productos))

        mysql.connection.commit()

        cur.execute('SELECT COUNT(idfactura) FROM facturas WHERE clienteid = {0}'.format(id))
        compras = cur.fetchall()[0][0]
        cur.execute('UPDATE clientes SET compras = %s WHERE idclientes = %s', (compras, id))
        mysql.connection.commit()
        
        return 'OK', 200

@app.route('/delete_factura/<string:id>')
def delete_factura(id):
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM facturas WHERE idfactura = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("all_facturas"))  

@app.route('/edit_factura/<string:id>')
def edit_factura(id):
    cur = mysql.connection.cursor()
    cur.execute(" SELECT * FROM facturas WHERE idfactura = {0}".format(id))
    data3 = cur.fetchall()

    cliente_id = data3[0][1] 

    cur.execute('SELECT * FROM clientes WHERE idclientes = {0}'.format(cliente_id))
    data = cur.fetchall()

    cur.execute('SELECT * FROM productos')
    data2 = cur.fetchall()
    payMethods = ['efectivo', 'Cheque', 'Paypal', 'PSE', 'NEQUI']
    categ = list( set( [ d[1] for d in data2] ) )

    return render_template('edit_factura.html', cliente = data[0], productos = data2, categoria = categ, lon = len(categ), paymethods = payMethods, lonpay = len(payMethods), factura = data3[0]) 

@app.route('/update_factura/<string:id>', methods = ['POST'])
def update_factura(id):
    
    if request.method == 'POST':
        data_obtain = request.get_data()
        data_obtain = json.loads(data_obtain.decode('utf-8'))
        data_obtain['fecha'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cantidad_productos = data_obtain['cantDeProductos']
        fecha = data_obtain['fecha']
        total_dinero = data_obtain['totalDinero']
        metodo_pago = data_obtain['metodoPago']
        productos = json.dumps(data_obtain['productos'])

        cur = mysql.connection.cursor()

        
        cur.execute("""
            UPDATE facturas
            SET cantidadProductos = %s,
                fecha = %s,
                valorTotal = %s,
                payMethod = %s,
                compraCliente = %s
            WHERE idFactura = %s        
        """, (cantidad_productos, fecha, total_dinero, metodo_pago, productos, id))

        
        mysql.connection.commit()
        return redirect(url_for("all_facturas"))


#_________________api - main________________________
@app.route("/api/")
def api():

    info = {
        "cliente" : {
            "allClients" : "/api/clientes/",
            "spesificClient" : "GET : /api/cliente/<id> -- <id> del cliente espesificio, puedes verlo en '/api/clientes/'",
            "createCliente" : {
                "info" : "POST : /api/cliente/ -- Así se puede crear cliente",
                "struct" : " { 'nombre' : <nombre>, 'cedula' : <cedula>, 'direccion' : <dirreccion>, 'telefono' : <telefono>, 'foto' : <telefono>, 'compras' : <cantida de compras> }"
            }
        }
    }

    return jsonify({"message": "Instrucción de uso:", "info": info})


#___________________api_cliente_____________________

@app.route("/api/clientes/")
def api_clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes ORDER BY compras DESC')
    data = cur.fetchall()

    clientes = []

    for cliente in data:

        clientes.append({
            "id_cliente" : cliente[0],
            "nombre" : cliente[2],
            "cedula" : cliente[1],
            'direccion' : cliente[3],
            'telefono' : cliente[4],
            'foto' : cliente[5],
            'compras' : cliente[6]
        })

    return jsonify({"message": "Totalidad de los clientes", "clientes" :  clientes })


@app.route("/api/clientes/<string:id>")
def api_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE idclientes = {0}'.format(id))
    data = cur.fetchall()

    cliente = {
        "id_cliente" : data[0][0],
        "cedula" : data[0][1],
        "nombre" : data[0][2],
        "direccion" : data[0][3],
        "telefono" : data[0][4],
        "foto" : data[0][5],
        "compras": data[0][6]
    }
    print(data)

    return jsonify({"message" : "Cliente obtenido", "cliente" : cliente})

@app.route("/api/clientes/", methods = ['POST'])
def create_client_api():

    if request.method == 'POST':

        created_cliente = {
            'nombre' : request.json["nombre"],
            "cedula" : request.json["cedula"],
            "direccion" : request.json["direccion"],
            "telefono" : request.json["telefono"],
            "foto" : request.json['foto'],
            "compras" : request.json['compras']
        }
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO clientes 
            (cedula, nombre, direccion, telefono, foto)
            VALUES (%s,%s,%s,%s,%s)     
        """, (created_cliente["cedula"], created_cliente["nombre"], created_cliente["direccion"], created_cliente["telefono"], created_cliente["foto"]))

        mysql.connection.commit()

        return jsonify({"message" : "Cliente creado!", "cliente" : created_cliente})


@app.route("/api/clientes/<string:id>", methods = ['PUT'])
def update_client_api(id):
    if request.method == 'PUT':

        edited_cliente = {
            'nombre' : request.json["nombre"],
            "cedula" : request.json["cedula"],
            "direccion" : request.json["direccion"],
            "telefono" : request.json["telefono"],
            "foto" : request.json['foto'],
            "compras" : request.json['compras']
        }

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE clientes
            SET cedula = %s,
                nombre = %s,
                direccion = %s,
                telefono = %s,
                foto = %s
            WHERE idclientes = %s
        """, (edited_cliente["cedula"], edited_cliente["nombre"], edited_cliente["direccion"], edited_cliente["telefono"], edited_cliente["foto"],id))
        mysql.connection.commit()
    
        return jsonify({"message": "client updated", "cliente" : edited_cliente})


@app.route("/api/clientes/<string:id>", methods = ['DELETE'])
def delete_client_api(id):
    if request.method == 'DELETE':

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM clientes WHERE idClientes = {0}'.format(id))
        mysql.connection.commit()

        return jsonify({"message": "client deleted"})



#___________________api_cliente_____________________

@app.route("/api/productos/")
def api_productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()


    productos = []

    for producto in data:

        productos.append({
            "id_producto" : producto[0],
            "categoria" : producto[1],
            "nombre" : producto[2],
            'precio' : producto[3],
            'cantidadBodega' : producto[4],
            'estado' : 1 if producto[5] != 0 else 0,
            'foto' : producto[6]
        })

    return jsonify({"message" : "all products", "products" : productos})


@app.route("/api/productos/<string:id>")
def api_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE idProductos = {0}'.format(id))
    data = cur.fetchall()

    producto= {
        "id_producto" : data[0][0],
        "categoria" : data[0][1],
        "nombre" : data[0][2],
        'precio' : data[0][3],
        'cantidadBodega' : data[0][4],
        'estado' : 1 if data[0][5] != 0 else 0,
        'foto' : data[0][6]
    }
    return jsonify({"message" : "all products", "producto" : producto})

@app.route("/api/productos/", methods = ['POST'])
def create_producto_api():

    producto = {
        "categoria" : request.json['categoria'],
        "nombre" : request.json["nombre"],
        'precio' : request.json["precio"],
        'cantidadBodega' : request.json["cantidadBodega"],
        'estado' : 1 if request.json["cantidadBodega"] != 0 else 0,
        'foto' : request.json["foto"]
    }


    cur = mysql.connection.cursor()
    cur.execute("""
            INSERT INTO productos 
            (categoria, nombre, precio, cantidadBodega, estado, foto_producto)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (producto["categoria"], producto["nombre"], producto["precio"], producto["cantidadBodega"], producto["estado"], producto["foto"]))

    mysql.connection.commit()

    return jsonify({
        "message" : "product created",
        "producto" : producto
    })


@app.route("/api/productos/<string:id>", methods = ['PUT'])
def update_product_api(id):
    if request.method == "PUT":

        producto = {
            "categoria" : request.json['categoria'],
            "nombre" : request.json["nombre"],
            'precio' : request.json["precio"],
            'cantidadBodega' : request.json["cantidadBodega"],
            'estado' : 1 if request.json["cantidadBodega"] != 0 else 0,
            'foto' : request.json["foto"]
        }

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE productos
            SET categoria = %s,
                nombre = %s,
                precio = %s,
                cantidadBodega = %s,
                estado = %s,
                foto_producto = %s
            WHERE idproductos = %s    
        """, (producto["categoria"], producto["nombre"], producto["precio"], producto["cantidadBodega"], producto["estado"], producto["foto"],id))
        mysql.connection.commit()

        return jsonify({
            "message" : "producto actualizado",
            "producto" : producto
        })

@app.route("/api/productos/<string:id>", methods = ['DELETE'])
def delete_product_api(id):
    if request.method == 'DELETE':

        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM productos WHERE idProductos = {0}'.format(id))
        mysql.connection.commit()

    return jsonify({"message": "product deleted"})

#__________________facturas_______________

@app.route("/api/facturas/")
def api_facturas():
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT clientes.idClientes,
           clientes.cedula, 
           clientes.nombre,
           clientes.compras,
           facturas.cantidadProductos,
           facturas.fecha,
           facturas.valorTotal,
           facturas.payMethod,
           facturas.compraCliente,
           facturas.idFactura
    FROM   clientes
    INNER JOIN facturas ON
            clientes.idClientes = facturas.clienteID;
    """)
    data = cur.fetchall()

    facturas = []

    for factura in data:

        facturas.append({
            "id_cliente" : factura[0],
            "cedula" : factura[1],
            "nombre" : factura[2],
            'compras' : factura[3],
            'cantidadProductos' : factura[4],
            'fecha' : factura[5],
            "valorTotal" : factura[6],
            "metodoPago" : factura[7],
            "compraCliente" : json.loads(factura[8]),
            "id_factura" : factura[9]
        })

    return jsonify({"message" : "all products", "factura" : facturas})


@app.route("/api/facturas/<string:id>")
def api_factura(id):

    cur = mysql.connection.cursor()
    cur.execute(" SELECT clientes.idClientes, clientes.cedula, clientes.nombre, clientes.compras, facturas.cantidadProductos, facturas.fecha, facturas.valorTotal, facturas.payMethod, facturas.compraCliente, facturas.idFactura FROM   clientes INNER JOIN facturas ON clientes.idClientes = facturas.clienteID WHERE facturas.idFactura = {0}".format(id))

    data = cur.fetchall()

    factura = {
        "id_cliente" : data[0][0],
        "cedula" : data[0][1],
        "nombre" : data[0][2],
        'compras' : data[0][3],
        'cantidadProductos' : data[0][4],
        'fecha' : data[0][5],
        "valorTotal" : data[0][6],
        "metodoPago" : data[0][7],
        "compraCliente" : json.loads(data[0][8]),
        "id_factura" : data[0][9]
    }

    return jsonify({"message" : "factura solicitada", "factura" : factura})


@app.route("/api/facturas/<string:id>", methods = ["POST"])
def create_factura_api(id):

    if request.method == "POST":

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        factura = {
            "id_cliente" : id,
            "metodoPago" : request.json["metodoPago"],
            "compraCliente" : request.json["compraCliente"],
            "fecha" : fecha
        }

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        total_pagado = 0
        cantidad_total = 0

        for compra in factura["compraCliente"]:
            total_pagado += compra['cantidad']*compra['precio']
            cantidad_total += compra['cantidad'] 

        factura["total_pagado"] = total_pagado
        factura["cantidad_total"] = cantidad_total


        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO facturas
            (clienteID, cantidadProductos, fecha, valorTotal, payMethod, compraCliente) 
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (id, cantidad_total, fecha, total_pagado, factura["metodoPago"], json.dumps(factura["compraCliente"])))

        mysql.connection.commit()

        return jsonify({"message" : "factura insertada correctamente", "factura" : factura})


@app.route("/api/facturas/<string:id>", methods = ["PUT"])
def edit_factura_api(id):
    
    if request.method == "PUT":

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        factura = {
            "id_cliente" : id,
            "metodoPago" : request.json["metodoPago"],
            "compraCliente" : request.json["compraCliente"],
            "fecha" : fecha
        }

        fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        total_pagado = 0
        cantidad_total = 0

        for compra in factura["compraCliente"]:
            total_pagado += compra['cantidad']*compra['precio']
            cantidad_total += compra['cantidad'] 

        factura["total_pagado"] = total_pagado
        factura["cantidad_total"] = cantidad_total


        cur = mysql.connection.cursor()

        
        cur.execute("""
            UPDATE facturas
            SET cantidadProductos = %s,
                fecha = %s,
                valorTotal = %s,
                payMethod = %s,
                compraCliente = %s
            WHERE idFactura = %s        
        """, (cantidad_total, fecha, total_pagado, factura["metodoPago"], json.dumps(factura["compraCliente"]), id))

        
        mysql.connection.commit()

        return jsonify({"message" : "factura updated sucessfully", "factura" : factura})


@app.route("/api/facturas/<string:id>", methods = ["DELETE"])
def delete_factura_api(id):

    if request.method == "DELETE":
        cur = mysql.connection.cursor()
        cur.execute(" DELETE FROM facturas WHERE idfactura = {0}".format(id))
        mysql.connection.commit()
        return jsonify({"message": "factura borrada"})


if __name__== "__main__":
    app.run(port = 3000, debug = True)