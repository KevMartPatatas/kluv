DROP DATABASE kluv2;

CREATE DATABASE kluv2;
USE kluv;
\R \d>

CREATE TABLE IF NOT EXISTS `Kluv`.`Proveedor` (
  `idProveedor` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `direccion` LONGTEXT NOT NULL,
  PRIMARY KEY (`idProveedor`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`Categoria` (
  `idCategoria` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  PRIMARY KEY (`idCategoria`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`Usuario` (
  `idUsuario` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `usuario` VARCHAR(50) NOT NULL,
  `password` VARCHAR(50) NOT NULL,
  `rol` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idUsuario`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`Cliente` (
  `idCliente` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `direccion` LONGTEXT NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`idCliente`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`Venta` (
  `idVenta` INT NOT NULL,
  `fecha_hora` TIMESTAMP NOT NULL,
  `idUsuario` INT NOT NULL,
  `idCliente` INT NOT NULL,
  `total` DECIMAL(10,2) NOT NULL,
  `metodoPago` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`idVenta`, `idUsuario`),
  INDEX `fk_Venta_Usuario1_idx` (`idUsuario` ASC) VISIBLE,
  INDEX `fk_Venta_Cliente1_idx` (`idCliente` ASC) VISIBLE,
  CONSTRAINT `fk_Venta_Usuario1`
    FOREIGN KEY (`idUsuario`)
    REFERENCES `Kluv`.`Usuario` (`idUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Venta_Cliente1`
    FOREIGN KEY (`idCliente`)
    REFERENCES `Kluv`.`Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`DetalleVenta` (
  `idDetalle` INT NOT NULL,
  `idVenta` INT NOT NULL,
  `idProducto` INT NOT NULL,
  `cantidad` INT NOT NULL,
  `precioUnitario` DECIMAL(10,2) NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idDetalle`, `idVenta`, `idProducto`),
  INDEX `fk_DetalleVenta_Producto1_idx` (`idProducto` ASC) VISIBLE,
  INDEX `fk_DetalleVenta_Venta1_idx` (`idVenta` ASC) VISIBLE,
  CONSTRAINT `fk_DetalleVenta_Producto1`
    FOREIGN KEY (`idProducto`)
    REFERENCES `Kluv`.`Producto` (`idProducto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_DetalleVenta_Venta1`
    FOREIGN KEY (`idVenta`)
    REFERENCES `Kluv`.`Venta` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Kluv`.`Producto` (
  `idProducto` INT NOT NULL,
  `nombre` VARCHAR(255) NOT NULL,
  `descripcion` LONGTEXT NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `unidad` VARCHAR(50) NOT NULL,
  `stock` INT NOT NULL,
  `idCategoria` INT NOT NULL,
  `idProveedor` INT NOT NULL,
  PRIMARY KEY (`idProducto`, `idCategoria`, `idProveedor`),
  INDEX `fk_Producto_Categoria_idx` (`idCategoria` ASC) VISIBLE,
  INDEX `fk_Producto_Proveedor1_idx` (`idProveedor` ASC) VISIBLE,
  CONSTRAINT `fk_Producto_Categoria`
    FOREIGN KEY (`idCategoria`)
    REFERENCES `Kluv`.`Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Producto_Proveedor1`
    FOREIGN KEY (`idProveedor`)
    REFERENCES `Kluv`.`Proveedor` (`idProveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW TABLES;