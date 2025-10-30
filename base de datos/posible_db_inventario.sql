use master
go

drop database if exists INVENTARIO
go

create database INVENTARIO
go

use INVENTARIO
go


-- Tabla Usuarios
CREATE TABLE Usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    correo NVARCHAR(100) UNIQUE NOT NULL,
    contraseña NVARCHAR(255) NOT NULL,
    rol NVARCHAR(50) DEFAULT 'Usuario',
    fecha_registro DATETIME DEFAULT GETDATE(),
    activo BIT DEFAULT 1
);
IF NOT EXISTS (SELECT 1 FROM Usuarios WHERE id_usuario = 1)
BEGIN
    INSERT INTO Usuarios (nombre, correo, contraseña, rol)
    VALUES ('Usuario Sistema', 'sistema@inventario.com', 'temp123', 'Administrador')
    PRINT '✅ Usuario por defecto creado'
END
ELSE
    PRINT '✅ Usuario por defecto ya existe'
GO

CREATE TABLE Categorias (
    id_categoria INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100),
    descripcion NVARCHAR(255)
);

INSERT INTO Categorias (nombre, descripcion) VALUES
('Cereales andinos', 'Productos como quinua, kiwicha, cañihua, maíz serrano.'),
('Legumbres secas', 'Frijol, lenteja, arveja, habas en estado seco.'),
('Semillas para siembra', 'Semillas seleccionadas para cultivo agrícola.'),
('Productos frescos', 'Legumbres y cereales en estado fresco o recién cosechados.'),
('Derivados procesados', 'Harinas, hojuelas, tostados, mezclas listas para consumo.'),
('Insumos agrícolas', 'Fertilizantes orgánicos, abonos, herramientas menores.'),
('Empaques y envases', 'Sacos, bolsas, frascos utilizados para comercialización.');


CREATE TABLE Proveedores (
    id_proveedor INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100),
    telefono NVARCHAR(20),
    direccion NVARCHAR(255),
    correo NVARCHAR(100)
);

-- DBCC CHECKIDENT ('Movimientos_Inventario', RESEED, 0);

INSERT INTO Proveedores (nombre, telefono, direccion, correo) VALUES
('AgroAndes SAC', '+51 987 654 321', 'Jr. Los Incas 123, Huancayo, Junín', 'contacto@agroandes.pe'),
('Semillas del Sur', '+51 956 321 789', 'Av. Libertad 456, Ayacucho', 'ventas@semillasdelsur.com'),
('BioFert Perú', '+51 945 678 123', 'Calle Pachamama 89, Cusco', 'info@biofertperu.org'),
('Empaques Sierra Verde', '+51 923 456 789', 'Jr. Comercio 77, Huancavelica', 'servicio@sierraverde.pe'),
('Legumbres Selectas EIRL', '+51 912 345 678', 'Av. Central 101, Abancay', 'legumbres@selectas.com'),
('CerealCo Andino', '+51 999 888 777', 'Calle Quinoa 22, Cerro de Pasco', 'cereales@cerealco.pe');


CREATE TABLE Productos (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100),
    id_categoria INT FOREIGN KEY REFERENCES Categorias(id_categoria),
    id_proveedor INT FOREIGN KEY REFERENCES Proveedores(id_proveedor),
    unidad_medida NVARCHAR(50),
    stock_actual DECIMAL(10,2) DEFAULT 0,
    stock_minimo DECIMAL(10,2) DEFAULT 0,
    precio_unitario DECIMAL(10,2),
    fecha_registro DATETIME DEFAULT GETDATE(),
    estado NVARCHAR(20) DEFAULT 'Activo'
);

INSERT INTO Productos (nombre, id_categoria, id_proveedor, unidad_medida, stock_actual, stock_minimo, precio_unitario)
VALUES
-- Cereales andinos
('Quinua blanca', 1, 1, 'kg', 120.00, 30.00, 6.50),
('Kiwicha orgánica', 1, 2, 'kg', 80.00, 20.00, 7.20),
('Cañihua tostada', 1, 6, 'kg', 50.00, 15.00, 5.80),
('Maíz morado serrano', 1, 1, 'saco', 10.00, 3.00, 95.00),
('Maíz blanco tipo Cusco', 1, 3, 'qq', 5.00, 2.00, 120.00),
('Quinua roja', 1, 2, 'kg', 60.00, 10.00, 7.80),
('Cebada perlada', 1, 5, 'kg', 40.00, 10.00, 4.90),

-- Legumbres secas (solo algunos)
('Frijol serrano', 2, 5, 'kg', 70.00, 20.00, 6.00),
('Haba seca', 2, 4, 'kg', 45.00, 10.00, 5.20);

CREATE TABLE Clientes (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100),
    telefono NVARCHAR(20),
    direccion NVARCHAR(255),
    correo NVARCHAR(100)
);

CREATE TABLE Ventas (
    id_venta INT IDENTITY(1,1) PRIMARY KEY,
	id_usuario INT FOREIGN KEY REFERENCES Usuarios(id_usuario),
    id_cliente INT FOREIGN KEY REFERENCES Clientes(id_cliente),
    fecha_venta DATETIME DEFAULT GETDATE(),
    total DECIMAL(10,2),
    tipo_venta NVARCHAR(20) DEFAULT 'Venta',
    observaciones NVARCHAR(255)
);

CREATE TABLE Detalle_venta (
    id_detalle INT IDENTITY(1,1) PRIMARY KEY,
    id_venta INT FOREIGN KEY REFERENCES Ventas(id_venta),
    id_producto INT FOREIGN KEY REFERENCES Productos(id_producto),
    cantidad DECIMAL(10,2),
    precio_unitario DECIMAL(10,2),
    subtotal AS (cantidad * precio_unitario) PERSISTED
);

CREATE TABLE Cambios_Inventario (
    id_movimiento INT IDENTITY(1,1) PRIMARY KEY,
	id_usuario INT FOREIGN KEY REFERENCES Usuarios(id_usuario),
    id_producto INT FOREIGN KEY REFERENCES Productos(id_producto),
    tipo_movimiento NVARCHAR(20) CHECK (tipo_movimiento IN ('Entrada','Salida')),
    cantidad DECIMAL(10,2),
    fecha_movimiento DATETIME DEFAULT GETDATE(),
    observaciones NVARCHAR(255)
);