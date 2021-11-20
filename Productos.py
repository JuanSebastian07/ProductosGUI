from tkinter import *
from tkinter import ttk
import sqlite3

class producto:

    db_name = 'database.db'

    def __init__(self,window):
        self.window=window
        #title es propio de la libreria tkinter
        self.window.title('Productos')
        
        #Creando elementos
        #LabelFrame es un elemento que nos probee nuestra libreria tkinter
        #cuadro
        frame = LabelFrame(self.window, text='Registre un nuevo producto')
        #posicionamos elementos con grid
        frame.grid(row=0,column=0, columnspan=3, pady=20)


        #name input
        Label(frame,text='Name:').grid(row=1,column=0)
        self.name=Entry(frame)
        self.name.focus()
        self.name.grid(row=1,column=1)

        #Precio input
        Label(frame,text='Precio:').grid(row=2,column=0)
        self.precio=Entry(frame)
        self.precio.grid(row=2,column=1)

        #Boton agragar producto |command es para decirle al boto que tiene funcion tiene que ejecutar|
        ttk.Button(frame, text='save product', command=self.agregar_producto).grid(row=3,columnspan=2, sticky=W+E)

        #Salida de mensajes por interfaz
        self.mensaje=Label(text='',fg='red')
        self.mensaje.grid(row=3,column=0,columnspan=2, sticky=W+E)

        #Tabla
        self.tree = ttk.Treeview(height = 10, column=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Nombre',anchor=CENTER)
        self.tree.heading('#1',text='Precio',anchor=CENTER)

        #Botones
        ttk.Button(text='Eliminar',command=self.eliminar_producto).grid(row=5,column=0, sticky=W+E)
        ttk.Button(text='Editar', command=self.editar).grid(row=5,column=1, sticky=W+E)

        self.get_productos()

    #Ejecuta consulta
    def run_query(self,consulta,parametros=()):
        #sqlite.connect metodo para conectarme a nuestra base de datos
        with sqlite3.connect(self.db_name) as conn:
            cursor=conn.cursor()
            #cursos.execute nos permite ejecutar la consulta
            resultado=cursor.execute(consulta,parametros)
            #Ejecuatamos la funcion
            conn.commit()
        return resultado

    def get_productos(self):
        #get_children este es para obtener todos lodatos que esten en esta tabla
        #limpiamos la tabla si
        elementos = self.tree.get_children()
        for elemento in elementos:
            self.tree.delete(elemento)

        consulta='SELECT * FROM product ORDER BY name DESC'
        db_rows=self.run_query(consulta)
        for row in db_rows:
            #print(row)
            #los insertamos en la interfaz
            self.tree.insert('',0,text=row[1],values=row[2])            


    def agregar_producto(self):
        if self.validacion():
            consulta='INSERT INTO product VALUES(NULL,?,?)'
            parametros=(self.name.get(),self.precio.get())
            self.run_query(consulta,parametros)
            self.mensaje['text']=f' {self.name.get()} agregado con exito!!'
            self.name.delete(0,END)
            self.precio.delete(0,END)
           
        else:
            self.mensaje['text']="Verifica que los espacion 'name' y 'precio' esten llenos"
        self.get_productos()

    #validamos que el name y el precio no esten vacios
    def validacion(self):
        return len(self.name.get())!=0 and len(self.precio.get())!=0
        
    def eliminar_producto(self):
        #primero miramos si un producto de mi tabla esta seleccionador
        #Esto es por si el mensaje ya tiene otro texto limpiamos
        self.mensaje['text']=''
        try:
            print(self.tree.item(self.tree.selection())['text'][0])
            self.tree.item(self.tree.selection())['text'][0]
            
        except IndexError as e:
            self.mensaje['text']='Por favor seleccion el elemento que deseas eliminar'
            return
        self.mensaje['text']=''    
        #si try continua aqui
        #con tree.item seleccionamos y lo guarda en la variable nombre lo que ha seleccionado
        nombre=self.tree.item(self.tree.selection())['text']
        #consulta
        consulta='DELETE FROM product WHERE name=?'
        self.run_query(consulta, (nombre,))
        self.mensaje['text']=f'{nombre} a sido eliminado'
        #Para actualizar nuestra tabla volvemos a llamar la funcion get_products
        self.get_productos()

    def editar(self):
        self.mensaje['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='Por favor seleccion el elemento que deseas editar'
            return
        nombre=self.tree.item(self.tree.selection())['text']
        precio_anterior=self.tree.item(self.tree.selection())['values'][0]
        print(f'Precio anterior-->{precio_anterior}')

        #Otra ventana
        self.ventana_editar=Toplevel()
        self.ventana_editar.title='Editar Producto'

        #old name
        Label(self.ventana_editar,text='Old name: ').grid(row=0,column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar,value=nombre),state='readonly').grid(row=0,column=2)

        #New name
        Label(self.ventana_editar,text='New name: ').grid(row=1,column=1)
        new_name=Entry(self.ventana_editar)
        new_name.grid(row=1,column=2)

        #precio viejo
        Label(self.ventana_editar,text='Precio viejo: ').grid(row=2,column=1)
        Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar,value=precio_anterior),state='readonly').grid(row=2,column=2)


        #Precio nuevo
        Label(self.ventana_editar,text='Nuevo Precio: ').grid(row=3,column=1)
        nuevo_precio=Entry(self.ventana_editar)
        nuevo_precio.grid(row=3,column=2)

        Button(self.ventana_editar, text='Actulizar', command=lambda: self.editar_elemento(new_name.get(),
        nombre,nuevo_precio.get(),precio_anterior)).grid(row=4,column=2,sticky=W)

    def editar_elemento(self,new_name,nombre,nuevo_precio,old_precio):
        consulta='UPDATE product SET name= ?, precio=? WHERE name=? AND precio = ?'
        parametros=(new_name,nuevo_precio,nombre,old_precio)
        self.run_query(consulta,parametros)
        self.ventana_editar.destroy()
        self.mensaje['text']=f'{(nombre)} elemento actualizado'
        self.get_productos()     

if __name__=='__main__':
    window=Tk()
    #Creamos una instancia de la clase con atributo window
    producto(window)
    #Esto es para desplegar la ventana 
    window.mainloop()