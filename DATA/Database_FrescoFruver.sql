-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: inventario_db
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '71bdf7d6-c0a4-11f0-81fb-7c8ae1b08832:1-188';

--
-- Table structure for table `auditoria`
--

DROP TABLE IF EXISTS `auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria` (
  `IdAuditoria` int NOT NULL AUTO_INCREMENT,
  `FechaAuditoria` date DEFAULT NULL,
  `Accion` varchar(100) DEFAULT NULL,
  `Descripcion` varchar(255) DEFAULT NULL,
  `IdUsuario` int DEFAULT NULL,
  PRIMARY KEY (`IdAuditoria`),
  KEY `IdUsuario` (`IdUsuario`),
  CONSTRAINT `auditoria_ibfk_1` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria`
--

LOCK TABLES `auditoria` WRITE;
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
INSERT INTO `auditoria` VALUES (1,'2026-03-01','Crear Producto','Se creó el producto Arroz 1kg',1),(2,'2026-03-02','Actualizar Producto','Se actualizó precio de Azúcar',2),(3,'2026-03-03','Eliminar Producto','Se eliminó producto defectuoso',3),(4,'2026-03-04','Crear Cliente','Nuevo cliente registrado',4),(5,'2026-03-05','Actualizar Cliente','Se actualizó teléfono cliente',5),(6,'2026-03-06','Crear Venta','Venta registrada FAC-001',6),(7,'2026-03-07','Cancelar Venta','Venta FAC-008 cancelada',7),(8,'2026-03-08','Actualizar Venta','Cambio en estado de venta',8),(9,'2026-03-09','Crear OrdenCompra','Orden de compra creada',9),(10,'2026-03-10','Cancelar OrdenCompra','Orden cancelada',10),(11,'2026-03-11','Actualizar Stock','Entrada de productos registrada',11),(12,'2026-03-12','Actualizar Stock','Salida por venta registrada',12),(13,'2026-03-13','Ajuste Inventario','Corrección de inventario',13),(14,'2026-03-14','Login','Inicio de sesión usuario',14),(15,'2026-03-15','Logout','Cierre de sesión usuario',15),(16,'2026-03-16','Crear Usuario','Nuevo usuario creado',16),(17,'2026-03-17','Actualizar Usuario','Cambio de rol usuario',17),(18,'2026-03-18','Eliminar Usuario','Usuario eliminado',18),(19,'2026-03-19','Crear Proveedor','Proveedor registrado',19),(20,'2026-03-20','Actualizar Proveedor','Datos proveedor actualizados',20),(21,'2026-03-21','Crear Producto','Nuevo producto agregado',21),(22,'2026-03-22','Actualizar Producto','Cambio de stock producto',22),(23,'2026-03-23','Eliminar Producto','Producto eliminado',23),(24,'2026-03-24','Crear Venta','Venta registrada FAC-015',24),(25,'2026-03-25','Cancelar Venta','Venta cancelada',25),(26,'2026-03-26','Actualizar Stock','Entrada por compra',26),(27,'2026-03-27','Ajuste Inventario','Producto dañado',27),(28,'2026-03-28','Login','Ingreso al sistema',28),(29,'2026-03-29','Logout','Salida del sistema',29),(30,'2026-03-30','Crear OrdenCompra','Nueva orden registrada',30);
/*!40000 ALTER TABLE `auditoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `IdCliente` int NOT NULL AUTO_INCREMENT,
  `NomCliente` varchar(100) DEFAULT NULL,
  `NoDocumentoCliente` varchar(50) DEFAULT NULL,
  `TelCliente` varchar(20) DEFAULT NULL,
  `CorreoCliente` varchar(100) DEFAULT NULL,
  `DireccionCliente` varchar(150) DEFAULT NULL,
  `EstadoCliente` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IdCliente`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Juan Perez','1019845632','3124587963','juan1@mail.com','Cra 45 #12-34','Activo'),(2,'Maria Gomez','52347896','3008754219','maria2@mail.com','Calle 72 #15-67','Activo'),(3,'Carlos Lopez','91234578','3189045621','carlos3@mail.com','Cra 19 #8-45','Activo'),(4,'Ana Martinez','1045789632','3017638294','ana4@mail.com','Calle 100 #23-11','Activo'),(5,'Luis Rodriguez','84573921','3208457392','luis5@mail.com','Cra 7 #45-89','Activo'),(6,'Sofia Hernandez','1093847562','3152948765','sofia6@mail.com','Calle 13 #22-56','Activo'),(7,'Pedro Ramirez','75648392','3116583942','pedro7@mail.com','Cra 68 #9-21','Activo'),(8,'Laura Torres','1073948562','3047391823','laura8@mail.com','Calle 80 #10-33','Activo'),(9,'Jorge Flores','93485721','3174829012','jorge9@mail.com','Cra 15 #60-12','Activo'),(10,'Paula Rivera','1085749236','3109582711','paula10@mail.com','Calle 50 #18-44','Activo'),(11,'Andres Diaz','82374651','3226748123','andres11@mail.com','Cra 27 #33-90','Activo'),(12,'Camila Vargas','1048392756','3138452077','camila12@mail.com','Calle 90 #14-52','Activo'),(13,'Diego Castro','76583921','3509182799','diego13@mail.com','Cra 30 #70-65','Activo'),(14,'Valentina Rojas','1123987456','3167039511','valentina14@mail.com','Calle 110 #25-78','Activo'),(15,'Fernando Ruiz','91827364','3215874012','fernando15@mail.com','Cra 10 #5-23','Activo'),(16,'Daniela Ortiz','1039485762','3149763254','daniela16@mail.com','Calle 140 #12-67','Activo'),(17,'Ricardo Medina','83475629','3182746599','ricardo17@mail.com','Cra 50 #20-10','Activo'),(18,'Natalia Vega','1092837465','3028459788','natalia18@mail.com','Calle 60 #30-45','Activo'),(19,'Sebastian Mora','74583921','3176039421','sebastian19@mail.com','Cra 24 #18-76','Activo'),(20,'Gabriela Silva','1063948572','3009158433','gabriela20@mail.com','Calle 35 #16-90','Activo'),(21,'Oscar Pineda','91837462','3117295678','oscar21@mail.com','Cra 12 #40-12','Activo'),(22,'Patricia Leon','1047852369','3154089201','patricia22@mail.com','Calle 25 #9-34','Activo'),(23,'Hugo Navarro','75649283','3206741987','hugo23@mail.com','Cra 18 #55-67','Activo'),(24,'Lucia Campos','1072849563','3019384712','lucia24@mail.com','Calle 95 #22-10','Activo'),(25,'Alberto Cruz','84562739','3185072699','alberto25@mail.com','Cra 60 #11-45','Activo'),(26,'Diana Mendoza','1083947561','3162849733','diana26@mail.com','Calle 45 #13-89','Activo'),(27,'Roberto Salas','73485921','3127594822','roberto27@mail.com','Cra 33 #27-54','Activo'),(28,'Elena Peña','91237465','3048652177','elena28@mail.com','Calle 70 #19-21','Activo'),(29,'Martin Guerrero','1073948256','3104975899','martin29@mail.com','Cra 9 #80-33','Activo'),(30,'Claudia Soto','82374659','3221587400','claudia30@mail.com','Calle 55 #14-60','Activo');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detallecompra`
--

DROP TABLE IF EXISTS `detallecompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detallecompra` (
  `IdDetalleCompra` int NOT NULL AUTO_INCREMENT,
  `Cantidad` int DEFAULT NULL,
  `PrecioCosto` double DEFAULT NULL,
  `Subtotal` double DEFAULT NULL,
  `IdOrdenCompra` int DEFAULT NULL,
  `IdProducto` int DEFAULT NULL,
  PRIMARY KEY (`IdDetalleCompra`),
  KEY `IdOrdenCompra` (`IdOrdenCompra`),
  KEY `IdProducto` (`IdProducto`),
  CONSTRAINT `detallecompra_ibfk_1` FOREIGN KEY (`IdOrdenCompra`) REFERENCES `ordencompra` (`IdOrdenCompra`),
  CONSTRAINT `detallecompra_ibfk_2` FOREIGN KEY (`IdProducto`) REFERENCES `productos` (`IdProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallecompra`
--

LOCK TABLES `detallecompra` WRITE;
/*!40000 ALTER TABLE `detallecompra` DISABLE KEYS */;
INSERT INTO `detallecompra` VALUES (1,10,2.5,25,1,1),(2,15,2,30,1,2),(3,20,0.8,16,2,3),(4,10,4.5,45,2,4),(5,25,1.2,30,3,5),(6,12,1.5,18,3,6),(7,18,3,54,4,7),(8,14,3.5,49,5,8),(9,16,1.8,28.8,5,9),(10,30,1,30,6,10),(11,22,0.9,19.8,7,11),(12,11,3.2,35.2,7,12),(13,19,0.7,13.3,8,13),(14,13,2.5,32.5,9,14),(15,17,4,68,10,15),(16,21,1.8,37.8,11,16),(17,40,0.5,20,12,17),(18,23,1.2,27.6,13,18),(19,15,2.2,33,14,19),(20,18,1.8,32.4,15,20),(21,26,1.1,28.6,16,21),(22,24,1.3,31.2,17,22),(23,12,1.5,18,18,23),(24,14,2,28,19,24),(25,16,1.2,19.2,20,25),(26,10,3.5,35,21,26),(27,35,0.9,31.5,22,27),(28,20,3,60,23,28),(29,18,2.5,45,24,29),(30,22,2,44,25,30);
/*!40000 ALTER TABLE `detallecompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `IdDetalleVenta` int NOT NULL AUTO_INCREMENT,
  `Cantidad` int DEFAULT NULL,
  `PrecioUnitario` double DEFAULT NULL,
  `Subtotal` double DEFAULT NULL,
  `IdVenta` int DEFAULT NULL,
  `IdProducto` int DEFAULT NULL,
  PRIMARY KEY (`IdDetalleVenta`),
  KEY `IdVenta` (`IdVenta`),
  KEY `IdProducto` (`IdProducto`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`IdVenta`) REFERENCES `ventas` (`IdVenta`),
  CONSTRAINT `detalleventa_ibfk_2` FOREIGN KEY (`IdProducto`) REFERENCES `productos` (`IdProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,2,3.2,6.4,1,1),(2,1,2.8,2.8,1,2),(3,3,1.2,3.6,2,3),(4,2,5.8,11.6,2,4),(5,1,1.8,1.8,3,5),(6,4,2.2,8.8,3,6),(7,2,4.2,8.4,4,7),(8,1,4.8,4.8,5,8),(9,3,2.5,7.5,5,9),(10,2,1.7,3.4,6,10),(11,1,1.5,1.5,7,11),(12,2,4.5,9,7,12),(13,3,1.2,3.6,8,13),(14,1,3.6,3.6,9,14),(15,2,5.5,11,10,15),(16,1,2.6,2.6,11,16),(17,5,1,5,12,17),(18,2,2,4,13,18),(19,3,3.1,9.3,14,19),(20,1,2.6,2.6,15,20),(21,2,1.8,3.6,16,21),(22,3,2,6,17,22),(23,1,2.3,2.3,18,23),(24,2,3,6,19,24),(25,1,2,2,20,25),(26,4,5,20,21,26),(27,2,1.5,3,22,27),(28,3,4.5,13.5,23,28),(29,2,3.8,7.6,24,29),(30,1,3.2,3.2,25,30);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientoinventario`
--

DROP TABLE IF EXISTS `movimientoinventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientoinventario` (
  `IdMovimiento` int NOT NULL AUTO_INCREMENT,
  `FechaMovimiento` date DEFAULT NULL,
  `TipoMovimiento` varchar(50) DEFAULT NULL,
  `Cantidad` int DEFAULT NULL,
  `Motivo` varchar(100) DEFAULT NULL,
  `StockResultante` int DEFAULT NULL,
  `IdProducto` int DEFAULT NULL,
  `IdUsuario` int DEFAULT NULL,
  PRIMARY KEY (`IdMovimiento`),
  KEY `IdProducto` (`IdProducto`),
  KEY `IdUsuario` (`IdUsuario`),
  CONSTRAINT `movimientoinventario_ibfk_1` FOREIGN KEY (`IdProducto`) REFERENCES `productos` (`IdProducto`),
  CONSTRAINT `movimientoinventario_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientoinventario`
--

LOCK TABLES `movimientoinventario` WRITE;
/*!40000 ALTER TABLE `movimientoinventario` DISABLE KEYS */;
INSERT INTO `movimientoinventario` VALUES (1,'2026-03-01','Entrada',50,'Compra proveedor',150,1,1),(2,'2026-03-02','Salida',10,'Venta',140,1,2),(3,'2026-03-03','Entrada',30,'Compra proveedor',110,2,3),(4,'2026-03-04','Salida',5,'Venta',105,2,4),(5,'2026-03-05','Ajuste',2,'Inventario físico',107,2,5),(6,'2026-03-06','Entrada',40,'Compra proveedor',190,3,6),(7,'2026-03-07','Salida',15,'Venta',175,3,7),(8,'2026-03-08','Entrada',20,'Compra proveedor',80,4,8),(9,'2026-03-09','Salida',8,'Venta',72,4,9),(10,'2026-03-10','Ajuste',-3,'Producto dañado',69,4,10),(11,'2026-03-11','Entrada',60,'Compra proveedor',260,5,11),(12,'2026-03-12','Salida',20,'Venta',240,5,12),(13,'2026-03-13','Entrada',25,'Compra proveedor',75,6,13),(14,'2026-03-14','Salida',10,'Venta',65,6,14),(15,'2026-03-15','Ajuste',5,'Corrección sistema',70,6,15),(16,'2026-03-16','Entrada',35,'Compra proveedor',105,7,16),(17,'2026-03-17','Salida',12,'Venta',93,7,17),(18,'2026-03-18','Entrada',45,'Compra proveedor',85,8,18),(19,'2026-03-19','Salida',15,'Venta',70,8,19),(20,'2026-03-20','Ajuste',-2,'Pérdida',68,8,20),(21,'2026-03-21','Entrada',55,'Compra proveedor',165,9,21),(22,'2026-03-22','Salida',18,'Venta',147,9,22),(23,'2026-03-23','Entrada',30,'Compra proveedor',150,10,23),(24,'2026-03-24','Salida',10,'Venta',140,10,24),(25,'2026-03-25','Ajuste',3,'Inventario físico',143,10,25),(26,'2026-03-26','Entrada',20,'Compra proveedor',130,11,26),(27,'2026-03-27','Salida',5,'Venta',125,11,27),(28,'2026-03-28','Entrada',40,'Compra proveedor',100,12,28),(29,'2026-03-29','Salida',12,'Venta',88,12,29),(30,'2026-03-30','Ajuste',-1,'Error conteo',87,12,30);
/*!40000 ALTER TABLE `movimientoinventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordencompra`
--

DROP TABLE IF EXISTS `ordencompra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordencompra` (
  `IdOrdenCompra` int NOT NULL AUTO_INCREMENT,
  `FechaOrden` date DEFAULT NULL,
  `EstadoOrden` varchar(20) DEFAULT NULL,
  `TotalOrden` double DEFAULT NULL,
  `IdProv` int DEFAULT NULL,
  `IdCliente` int DEFAULT NULL,
  PRIMARY KEY (`IdOrdenCompra`),
  KEY `IdProv` (`IdProv`),
  KEY `IdCliente` (`IdCliente`),
  CONSTRAINT `ordencompra_ibfk_1` FOREIGN KEY (`IdProv`) REFERENCES `proveedores` (`IdProv`),
  CONSTRAINT `ordencompra_ibfk_2` FOREIGN KEY (`IdCliente`) REFERENCES `cliente` (`IdCliente`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordencompra`
--

LOCK TABLES `ordencompra` WRITE;
/*!40000 ALTER TABLE `ordencompra` DISABLE KEYS */;
INSERT INTO `ordencompra` VALUES (1,'2026-02-01','Completada',500,1,1),(2,'2026-02-02','Completada',300,2,2),(3,'2026-02-03','Pendiente',450,3,3),(4,'2026-02-04','Completada',600,4,4),(5,'2026-02-05','Cancelada',200,5,5),(6,'2026-02-06','Completada',750,6,6),(7,'2026-02-07','Completada',320,7,7),(8,'2026-02-08','Pendiente',410,8,8),(9,'2026-02-09','Completada',290,9,9),(10,'2026-02-10','Completada',800,10,10),(11,'2026-02-11','Completada',520,11,11),(12,'2026-02-12','Pendiente',610,12,12),(13,'2026-02-13','Completada',430,13,13),(14,'2026-02-14','Cancelada',250,14,14),(15,'2026-02-15','Completada',700,15,15),(16,'2026-02-16','Completada',360,16,16),(17,'2026-02-17','Pendiente',480,17,17),(18,'2026-02-18','Completada',550,18,18),(19,'2026-02-19','Completada',620,19,19),(20,'2026-02-20','Completada',710,20,20),(21,'2026-02-21','Completada',330,21,21),(22,'2026-02-22','Pendiente',440,22,22),(23,'2026-02-23','Completada',390,23,23),(24,'2026-02-24','Cancelada',270,24,24),(25,'2026-02-25','Completada',680,25,25),(26,'2026-02-26','Completada',720,26,26),(27,'2026-02-27','Pendiente',510,27,27),(28,'2026-02-28','Completada',460,28,28),(29,'2026-03-01','Completada',530,29,29),(30,'2026-03-02','Completada',610,30,30);
/*!40000 ALTER TABLE `ordencompra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `IdProducto` int NOT NULL AUTO_INCREMENT,
  `NomProd` varchar(100) DEFAULT NULL,
  `PrecioCompraProd` double DEFAULT NULL,
  `PrecioVentaProd` double DEFAULT NULL,
  `StockActualProd` int DEFAULT NULL,
  `FechaVencimientoProd` date DEFAULT NULL,
  `CategoriaProd` varchar(50) DEFAULT NULL,
  `EstadoProd` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IdProducto`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Manzana Roja Kg',2000,3500,120,'2026-04-25','Frutas','Activo'),(2,'Banano Kg',1200,2200,150,'2026-04-20','Frutas','Activo'),(3,'Naranja Kg',1500,2800,180,'2026-04-28','Frutas','Activo'),(4,'Papaya Unidad',3000,5000,60,'2026-04-22','Frutas','Activo'),(5,'Piña Unidad',2800,4500,70,'2026-04-23','Frutas','Activo'),(6,'Mango Kg',2200,3800,90,'2026-04-26','Frutas','Activo'),(7,'Fresa Kg',3500,5500,50,'2026-04-19','Frutas','Activo'),(8,'Uva Kg',4000,6500,65,'2026-04-21','Frutas','Activo'),(9,'Guayaba Kg',1800,3000,100,'2026-04-24','Frutas','Activo'),(10,'Mandarina Kg',1600,2900,130,'2026-04-27','Frutas','Activo'),(11,'Papa Kg',1000,1800,200,'2026-05-10','Verduras','Activo'),(12,'Tomate Kg',1300,2400,180,'2026-04-18','Verduras','Activo'),(13,'Cebolla Kg',900,1700,160,'2026-05-15','Verduras','Activo'),(14,'Zanahoria Kg',1100,2000,140,'2026-05-12','Verduras','Activo'),(15,'Lechuga Unidad',800,1500,100,'2026-04-17','Verduras','Activo'),(16,'Pepino Unidad',700,1400,110,'2026-04-19','Verduras','Activo'),(17,'Ajo Kg',3500,5500,60,'2026-06-01','Verduras','Activo'),(18,'Pimenton Kg',2500,4200,80,'2026-04-20','Verduras','Activo'),(19,'Brocoli Unidad',1800,3200,75,'2026-04-21','Verduras','Activo'),(20,'Coliflor Unidad',2000,3500,65,'2026-04-22','Verduras','Activo'),(21,'Yuca Kg',1200,2000,130,'2026-05-05','Tuberculos','Activo'),(22,'Platano Verde Unidad',500,1000,200,'2026-04-25','Tuberculos','Activo'),(23,'Platano Maduro Unidad',600,1200,180,'2026-04-24','Tuberculos','Activo'),(24,'Arracacha Kg',2000,3500,90,'2026-05-08','Tuberculos','Activo'),(25,'Batata Kg',1500,2700,95,'2026-05-07','Tuberculos','Activo'),(26,'Cilantro Manojo',500,1200,150,'2026-04-16','Hierbas','Activo'),(27,'Perejil Manojo',600,1300,140,'2026-04-16','Hierbas','Activo'),(28,'Espinaca Manojo',700,1500,120,'2026-04-17','Hierbas','Activo'),(29,'Apio Unidad',1200,2200,85,'2026-04-20','Verduras','Activo'),(30,'Remolacha Kg',1100,2100,100,'2026-05-09','Verduras','Activo');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `IdProv` int NOT NULL AUTO_INCREMENT,
  `NomProv` varchar(100) DEFAULT NULL,
  `TelProv` varchar(20) DEFAULT NULL,
  `DirProv` varchar(150) DEFAULT NULL,
  `CorreoProv` varchar(100) DEFAULT NULL,
  `EstadoProv` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IdProv`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Distribuidora Norte','3128457392','Av 1 #20-10','prov1@mail.com','Activo'),(2,'Alimentos Global','3007642198','Av 2 #20-11','prov2@mail.com','Activo'),(3,'Comercializadora Sur','3189054731','Av 3 #20-12','prov3@mail.com','Activo'),(4,'Mayorista Central','3016724589','Av 4 #20-13','prov4@mail.com','Activo'),(5,'Proveedora Andina','3208437615','Av 5 #20-14','prov5@mail.com','Activo'),(6,'Distribuciones Vega','3152948703','Av 6 #20-15','prov6@mail.com','Activo'),(7,'Suministros Lopez','3116583927','Av 7 #20-16','prov7@mail.com','Activo'),(8,'Alimentos del Valle','3047391856','Av 8 #20-17','prov8@mail.com','Activo'),(9,'Grupo Comercial Diaz','3174829061','Av 9 #20-18','prov9@mail.com','Activo'),(10,'Distribuidora Express','3109582743','Av 10 #20-19','prov10@mail.com','Activo'),(11,'Proveedor Uno','3226748195','Av 11 #20-20','prov11@mail.com','Activo'),(12,'Proveedor Dos','3138452097','Av 12 #20-21','prov12@mail.com','Activo'),(13,'Proveedor Tres','3509182746','Av 13 #20-22','prov13@mail.com','Activo'),(14,'Proveedor Cuatro','3167039581','Av 14 #20-23','prov14@mail.com','Activo'),(15,'Proveedor Cinco','3215874092','Av 15 #20-24','prov15@mail.com','Activo'),(16,'Proveedor Seis','3149763205','Av 16 #20-25','prov16@mail.com','Activo'),(17,'Proveedor Siete','3182746509','Av 17 #20-26','prov17@mail.com','Activo'),(18,'Proveedor Ocho','3028459716','Av 18 #20-27','prov18@mail.com','Activo'),(19,'Proveedor Nueve','3176039482','Av 19 #20-28','prov19@mail.com','Activo'),(20,'Proveedor Diez','3009158476','Av 20 #20-29','prov20@mail.com','Activo'),(21,'Distribuciones Elite','3117295640','Av 21 #20-30','prov21@mail.com','Activo'),(22,'Comercial ABC','3154089273','Av 22 #20-31','prov22@mail.com','Activo'),(23,'Global Foods','3206741958','Av 23 #20-32','prov23@mail.com','Activo'),(24,'Suministros Express','3019384752','Av 24 #20-33','prov24@mail.com','Activo'),(25,'Distribuidora Max','3185072639','Av 25 #20-34','prov25@mail.com','Activo'),(26,'Alimentos Premium','3162849701','Av 26 #20-35','prov26@mail.com','Activo'),(27,'Proveedor Central','3127594806','Av 27 #20-36','prov27@mail.com','Activo'),(28,'Distribuciones Plus','3048652197','Av 28 #20-37','prov28@mail.com','Activo'),(29,'Comercial Omega','3104975823','Av 29 #20-38','prov29@mail.com','Activo'),(30,'Proveedor Final','3221587469','Av 30 #20-39','prov30@mail.com','Activo');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `IdUsuario` int NOT NULL AUTO_INCREMENT,
  `NomUsuario` varchar(100) DEFAULT NULL,
  `NoDocumentoUsuario` varchar(50) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `TelUsuario` varchar(20) DEFAULT NULL,
  `CorreoUsuario` varchar(100) DEFAULT NULL,
  `RolUsuario` varchar(50) DEFAULT NULL,
  `Estado` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`IdUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Admin Principal','1023948576','admin1','$2b$12$rfvQgLqsQwZKWC10wPWeyu5YJiOb/UkD5Qs2W3nr9zoYdJWtnTgk6','3125879432','admin1@mail.com','Administrador','Activo'),(2,'Carlos Ruiz','79845621','user2','$2b$12$93ysHooajYxkVET7dG.48eUvKngGgv5nyknoAkvykV2tZkbGw/f/W','3007642198','user2@mail.com','Vendedor','Activo'),(3,'Maria Torres','52369874','user3','$2b$12$4pkIDo.zGIjwQn.r0NPgyObeivXhZs3818tMQx/kDZ6TQ7SURafTG','3189054731','user3@mail.com','Vendedor','Activo'),(4,'Luis Gomez','91478523','user4','$2b$12$QXeHVtL9Ggrtn6A9aBlTCuYTLQeZgsXJhz112NzcGA9RPOlCscSJK','3016724589','user4@mail.com','Vendedor','Activo'),(5,'Ana Lopez','1035874692','user5','$2b$12$ayMD4sfNG46JY8p6A9M4judbZmlJSoUDYa/.xIEKRyq8Q9nVOaF3q','3208437615','user5@mail.com','Administrador','Activo'),(6,'Pedro Martinez','86745219','user6','$2b$12$szps8DEyC2cGtL667g1h6eIR.lNvCkDQzbesTdPgqHRs.Y/UCSa46','3152948703','user6@mail.com','Vendedor','Activo'),(7,'Laura Diaz','1093847562','user7','$2b$12$8f46W9.GtNHcY05UMFYi.OcUr0ZX9qxBrRWlvYORjR8jDcwS0HcEe','3116583927','user7@mail.com','Vendedor','Activo'),(8,'Jorge Castro','75482963','user8','$2b$12$ox1wnhWK3yfya.MAq4k7nOH0psfaDzCuNHIfTyUxYGPytkW2AzBse','3047391856','user8@mail.com','Administrador','Activo'),(9,'Sofia Ramirez','1123987456','user9','$2b$12$aEkS6F3rTl62swZJiUjU8uRVrEc/u1q1cHP8FzNdOWBQrJmE211tq','3174829061','user9@mail.com','Vendedor','Activo'),(10,'Diego Herrera','93284751','user10','$2b$12$cKgaFS.OrnP/VpaSusqEEODcC26XqdHshBdZtRIRLufC5XGGJ9L6y','3109582743','user10@mail.com','Vendedor','Activo'),(11,'Camila Vega','1047852369','user11','$2b$12$Q9qy0BqoVTXfCDkdoYHyievQZM75Vb2oj00PWyvCTsCxlE9p/lMe.','3226748195','user11@mail.com','Vendedor','Activo'),(12,'Andres Rojas','84573921','user12','$2b$12$KNECGQc1s/.wUoHlWJjdlu2vYwD6GPmpN0J/FzS26isup2EABQ5lK','3138452097','user12@mail.com','Vendedor','Activo'),(13,'Valentina Silva','1073948562','user13','$2b$12$JWggP5MlX2Bzg7xwf.qR/ukoL.ObRJHvPwep564Zq6hDTKPXZVjLG','3509182746','user13@mail.com','Administrador','Activo'),(14,'Fernando Ortiz','76548392','user14','$2b$12$9XuWDaKRB/Q6QZuEjahlIuZ8.DyPH3PtpToVPC3CxDDjwv6Cw./de','3167039581','user14@mail.com','Vendedor','Activo'),(15,'Daniela Cruz','1085749236','user15','$2b$12$P8B6NBcS8JmurjHqLg753eYdYEB9Da2D4PYgJVo07NdOZOf93PdL.','3215874092','user15@mail.com','Administrador','Activo'),(16,'Ricardo Mendoza','91827364','user16','$2b$12$wkPE10NvrAnKjrSxhTPgC.723BO.aTrU5b6erLTebVszd0YNlaO0K','3149763205','user16@mail.com','Vendedor','Activo'),(17,'Natalia Pineda','1092837465','user17','$2b$12$x8ZeNOWAa/1FUBHkyrGdceLuOz7lDo3RXfKFdhK3rAhLEZ3U7m1cC','3182746509','user17@mail.com','Administrador','Activo'),(18,'Sebastian Navarro','88273645','user18','$2b$12$t2jtC32uQVU7LjMB/kU5R.x/NPtN53cR04dnyjf6p8GdcT9v/Qc22','3028459716','user18@mail.com','Administrador','Activo'),(19,'Gabriela Campos','1063948572','user19','$2b$12$8556b42EkDRXip0U.to7POI2Y5FoInkWjzWKYM3FX4r6gtZ/6cuR2','3176039482','user19@mail.com','Vendedor','Activo'),(20,'Oscar Leon','73485921','user20','$2b$12$It4aPomqskerwXW.kGt/COxEV8UGwsVRIf6p0f.bbJJ3AtMOQpR0K','3009158476','user20@mail.com','Administrador','Activo'),(21,'Patricia Salas','1048392756','user21','$2b$12$SqAVbGD44J.tahKQaPePvOFwOKan3GZ9A7EHpPwjGztcwkclBGtqS','3117295640','user21@mail.com','Vendedor','Activo'),(22,'Hugo Peña','91237465','user22','$2b$12$OkfzYCXM2yug0dRDd.Pf6Ox0.uo.oA8RvftHC9y5moW8IdAgsV.B2','3154089273','user22@mail.com','Vendedor','Activo'),(23,'Lucia Guerrero','1072849563','user23','$2b$12$/l7bJOxTV5WgIicI1CUaou6lG0CdsuSmyvPSyL6bsv/1OSE0ZZxgi','3206741958','user23@mail.com','Administrador','Activo'),(24,'Alberto Soto','84562739','user24','$2b$12$4mryadpARcKTFg5H1ZzmvuRk6YZX2ORG95whXIc8017yBkqlVlX7u','3019384752','user24@mail.com','Vendedor','Activo'),(25,'Diana Vargas','1083947561','user25','$2b$12$XNI4nx4LRq7XsudYX2ycCutRr/KHAcoE1bFRz62dasFn5nI48wQM2','3185072639','user25@mail.com','Vendedor','Activo'),(26,'Roberto Medina','75649283','user26','$2b$12$3gU/o.Tviuzsw2jAxi6EB..LQJGPdNF5EHCbyRZIMAcbvttBUf5Wu','3162849701','user26@mail.com','Vendedor','Activo'),(27,'Elena Cruz','1039485762','user27','$2b$12$62aaYo/r3XeR2I/SjscgpeNlWuiI8kcmE8AwLOBhuQl2Y5DoBtKSy','3127594806','user27@mail.com','Administrador','Activo'),(28,'Martin Rojas','91837462','user28','$2b$12$/tFTSpL05paTjqtn/9YJWuzCKXZuFIUdIjqlWTPxc5gMVWYtDG2FS','3048652197','user28@mail.com','Vendedor','Activo'),(29,'Claudia Vega','1073948256','user29','$2b$12$/OCKP/2Epj7eDdkBnk6wluhGK.4YSU5.4HXmwUwOoxy7NmUlmF3W.','3104975823','user29@mail.com','Vendedor','Activo'),(30,'Juan Navarro','83475629','user30','$2b$12$mrecxXBA5JF3a3/uIz2Q8O2FwBt2Oye/nWQXS/9eGymaSpovlxO4W','3221587469','user30@mail.com','Administrador','Activo');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `IdVenta` int NOT NULL AUTO_INCREMENT,
  `NumeroFactura` varchar(50) DEFAULT NULL,
  `FechaVenta` date DEFAULT NULL,
  `TotalVenta` double DEFAULT NULL,
  `EstadoVenta` varchar(20) DEFAULT NULL,
  `CanalVenta` varchar(50) DEFAULT NULL,
  `IdCliente` int DEFAULT NULL,
  `IdUsuario` int DEFAULT NULL,
  PRIMARY KEY (`IdVenta`),
  KEY `IdCliente` (`IdCliente`),
  KEY `IdUsuario` (`IdUsuario`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`IdCliente`) REFERENCES `cliente` (`IdCliente`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,'FAC-001','2026-01-01',50,'Completada','Tienda',1,2),(2,'FAC-002','2026-01-02',75.5,'Completada','Online',2,3),(3,'FAC-003','2026-01-03',120,'Completada','Tienda',3,4),(4,'FAC-004','2026-01-04',30,'Pendiente','Tienda',4,5),(5,'FAC-005','2026-01-05',200,'Completada','Online',5,6),(6,'FAC-006','2026-01-06',15,'Completada','Tienda',6,7),(7,'FAC-007','2026-01-07',90,'Completada','Online',7,8),(8,'FAC-008','2026-01-08',45,'Cancelada','Tienda',8,9),(9,'FAC-009','2026-01-09',60,'Completada','Online',9,10),(10,'FAC-010','2026-01-10',80,'Completada','Tienda',10,11),(11,'FAC-011','2026-01-11',25,'Completada','Online',11,12),(12,'FAC-012','2026-01-12',140,'Completada','Tienda',12,13),(13,'FAC-013','2026-01-13',65,'Pendiente','Online',13,14),(14,'FAC-014','2026-01-14',95,'Completada','Tienda',14,15),(15,'FAC-015','2026-01-15',110,'Completada','Online',15,16),(16,'FAC-016','2026-01-16',40,'Completada','Tienda',16,17),(17,'FAC-017','2026-01-17',70,'Cancelada','Online',17,18),(18,'FAC-018','2026-01-18',55,'Completada','Tienda',18,19),(19,'FAC-019','2026-01-19',130,'Completada','Online',19,20),(20,'FAC-020','2026-01-20',85,'Completada','Tienda',20,21),(21,'FAC-021','2026-01-21',95,'Completada','Online',21,22),(22,'FAC-022','2026-01-22',60,'Completada','Tienda',22,23),(23,'FAC-023','2026-01-23',45,'Pendiente','Online',23,24),(24,'FAC-024','2026-01-24',150,'Completada','Tienda',24,25),(25,'FAC-025','2026-01-25',35,'Completada','Online',25,26),(26,'FAC-026','2026-01-26',20,'Cancelada','Tienda',26,27),(27,'FAC-027','2026-01-27',180,'Completada','Online',27,28),(28,'FAC-028','2026-01-28',75,'Completada','Tienda',28,29),(29,'FAC-029','2026-01-29',55,'Completada','Online',29,30),(30,'FAC-030','2026-01-30',100,'Completada','Tienda',30,1);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-19  7:42:58
