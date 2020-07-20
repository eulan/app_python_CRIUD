//global variables
var categoriesChecked = []
var factura = 0;


//Creating the class

function facturaObj (fecha, nombre, productos, cantDeProductos, totalDinero, metodoPago){
    this.fecha = fecha;
    this.nombre = nombre;
    this.productos = productos;
    this.cantDeProductos = cantDeProductos;
    this.totalDinero = totalDinero;
    this.metodoPago = metodoPago;
}

function productObj (nombre, cantidad, precio){
    this.nombre = nombre;
    this.cantidad = cantidad;
    this.precio = precio;
}

main();



function main(){
    //useful varaibles
    let burgerMenu = document.querySelector('.burmenu');
    let categories = document.querySelectorAll('.categoria');
    let obtenerTotal = document.querySelector('#total');
    let FormularioCompra = document.querySelector('#formulario_compra_cliente')
    

    //Calling listeners
    if (categories){
        categories.forEach(category => {
            category.addEventListener('click',showProduct)
        });
    }

    if (burgerMenu) {
        burgerMenu.addEventListener('click', callMenu);
    }
    
    if (obtenerTotal) {
        obtenerTotal.addEventListener('click',callTotal);
    }
    
    if (FormularioCompra) {
        FormularioCompra.addEventListener('submit', subirJson);
    }
    
}

//subir json final

function subirJson(e){
    e.preventDefault();
    actionOr = document.querySelector('form').action.split("/")
    action = actionOr[actionOr.length - 2]+"/"+actionOr[actionOr.length - 1];

    console.log(action)

        
    // POST
    fetch(`${window.origin}/${action}`, {

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify(factura)
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {
        
            window.location.href = `${window.origin}/facturas`;
            
    });


    
}

//burger menu settings
function callMenu(e){
    e.preventDefault();
    if(e.target.className === 'fas fa-hamburger'){
        document.querySelector('.barra .navegacion').style.display = 'flex';
        document.querySelector('.barra .navegacion').style.flexDirection = 'column';
        e.target.className = 'fas fa-undo-alt';
    } else {
        document.querySelector('.barra .navegacion').style.display = 'none';
        e.target.className = 'fas fa-hamburger';
    }
}

function showProduct(e){
    let category = document.querySelectorAll("#" + e.target.value)
    
    if(e.target.checked){

        for (let i = 1; i < category.length; i++) {
            const element = category[i];
            category[i].style.display = "initial"
            categoriesChecked.push(category[i].id)
        }
    } else {
        for (let i = 1; i < category.length; i++) {
            const element = category[i];
            category[i].style.display = "none" 
            categoriesChecked = categoriesChecked.filter( categorieChecked => categorieChecked != category[i].id)
        }
    }

}

function callTotal(e){
    e.preventDefault();
    categoriesChecked = [...new Set(categoriesChecked)] 
    document.querySelector('.total').style.display = 'initial';
    factura = printFactura();
    
}

function printFactura() {

    //productos
    let productos = []
    //date
    let d = new Date();

    let fecha = String(d.getDay()) + " / "+ String(d.getMonth()+1)+" / " + String(d.getFullYear()) + " " + String(d.getHours()) + ":" + String(d.getMinutes())+":"+String(d.getSeconds());

    //cliente data

    let nombreCliente = document.querySelector('.compra-clien h1 span').innerHTML;

    //data about facture
    let personalData = document.querySelector('.personal-data');

    let node = document.createElement('p');
    node.innerHTML = `<span> Fecha </span>: ${fecha}`; 
    personalData.appendChild(node);

    node = document.createElement('p');
    node.innerHTML = `<span> Cliente: </span> ${nombreCliente}`;
    personalData.appendChild(node);

    categoriesChecked.forEach(categoryChecked => {
        categoriesSelected = document.querySelectorAll("#"+categoryChecked);

        for (let i = 1; i < categoriesSelected.length; i++) {

            let categorySelected = categoriesSelected[i];
            nombreProducto = categorySelected.childNodes[3].childNodes[1].childNodes[1].innerHTML;
            precioProducto = categorySelected.childNodes[3].childNodes[5].childNodes[1].innerHTML;
            cantidadProducto = categorySelected.childNodes[3].childNodes[11].childNodes[3].value;
            let productObjeto = new productObj(nombreProducto, cantidadProducto, precioProducto);
            productos.push(productObjeto);
        }
           
    });

    //Productos, cantidad total y precio a pagar

    let totalPago = 0;
    let cantidadTotal = 0;
    let table = document.querySelector('#listado-productos tbody');


    productos.forEach( producto => {

        if(producto.cantidad != 0){
            node = document.createElement('tr');

            node.innerHTML = `
                <td>${producto.nombre}</td>
                <td>${producto.precio}</td>
                <td>${producto.cantidad}</td>
                <td>${producto.cantidad*producto.precio}</td>
            `;

            table.appendChild(node);
        }
        
        cantidadTotal += Number(producto.cantidad); 
        totalPago += Number(producto.cantidad)*Number(producto.precio);
    });

    node = document.createElement('p');
    node.innerHTML = `<p><span>Cantidad de productos: </span>${cantidadTotal}</p>`;
    document.querySelector('.final-fact').appendChild(node);


    node = document.createElement('p');
    node.innerHTML = `<p><span>Total a pagar: </span>$${totalPago}</p>`;
    document.querySelector('.final-fact').appendChild(node);

    //Metodos de pago

    let paymethods = document.querySelectorAll('.paymethods input')

    let metodoPago = "";

    paymethods.forEach(paymethod => {
        if (paymethod.checked) {
            metodoPago = paymethod.value;
        }
    });

    node = document.createElement('p');
    node.innerHTML = `<p><span> Método de pago: </span>${metodoPago}</p>`;
    document.querySelector('.final-fact').appendChild(node);


    //construyendo facturaObj

    let factura = new facturaObj (fecha, nombreCliente, productos, cantidadTotal, totalPago, metodoPago);

    return factura;
}