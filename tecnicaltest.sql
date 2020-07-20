-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 20, 2020 at 11:49 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tecnicaltest`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `idClientes` int(11) NOT NULL,
  `cedula` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `foto` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `compras` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`idClientes`, `cedula`, `nombre`, `direccion`, `telefono`, `foto`, `compras`) VALUES
(3, '252125', 'Fernanada', 'Cra 25 # 37 - 88', '3647479', 'img/invitado3.jpg', 1),
(6, '252684', 'Martha Muñoz', 'cra 26 # 35 - 39', '125621', 'img/invitado3.jpg', 4),
(12, '151525696', 'Pacho Meneses', 'Av siempreviva # 03 - 03', '3122511522', 'img/invitado4.jpg', 1),
(13, '11515686', 'pepe', 'cra 25 # 33 - 25', '1252552', 'img/invitado5.jpg', 0),
(14, '11515686', 'pepe', 'cra 25 # 33 - 25', '1252552', 'img/invitado5.jpg', 0),
(15, '11515686', 'pepe Albert', 'cra 25 # 33 - 25', '1252552', 'img/invitado5.jpg', 0);

-- --------------------------------------------------------

--
-- Table structure for table `facturas`
--

CREATE TABLE `facturas` (
  `idFactura` int(11) NOT NULL,
  `clienteID` int(11) NOT NULL,
  `cantidadProductos` int(255) NOT NULL,
  `fecha` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL,
  `valorTotal` int(255) NOT NULL,
  `payMethod` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `compraCliente` longtext COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `facturas`
--

INSERT INTO `facturas` (`idFactura`, `clienteID`, `cantidadProductos`, `fecha`, `valorTotal`, `payMethod`, `compraCliente`) VALUES
(35, 6, 3, '2020-07-19 16:52:41', 87000, 'Cheque', '[{\"nombre\": \"bulma\", \"cantidad\": \"3\", \"precio\": \"29000\"}]'),
(36, 6, 1, '2020-07-19 16:53:18', 80000, 'Cheque', '[{\"nombre\": \"Github\", \"cantidad\": \"1\", \"precio\": \"80000\"}]'),
(37, 12, 3, '2020-07-19 17:04:55', 45000, 'efectivo', '[{\"nombre\": \"t-shirt Vue\", \"cantidad\": \"3\", \"precio\": \"15000\"}]'),
(38, 6, 3, '2020-07-19 18:38:28', 240000, 'PSE', '[{\"nombre\": \"Github\", \"cantidad\": \"3\", \"precio\": \"80000\"}]'),
(39, 3, 5, '2020-07-19 18:38:53', 115000, 'Cheque', '[{\"nombre\": \"t-shirt Vue\", \"cantidad\": \"3\", \"precio\": \"15000\"}, {\"nombre\": \"React\", \"cantidad\": \"2\", \"precio\": \"35000\"}]'),
(40, 3, 4, '2020-07-20 16:35:06', 296000, 'Paypal', '[{\"cantidad\": 3, \"nombre\": \"bulma\", \"precio\": 87000}, {\"cantidad\": 1, \"nombre\": \"react\", \"precio\": 35000}]');

-- --------------------------------------------------------

--
-- Table structure for table `productos`
--

CREATE TABLE `productos` (
  `idProductos` int(11) NOT NULL,
  `categoria` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` int(16) NOT NULL,
  `cantidadBodega` int(16) NOT NULL,
  `estado` int(2) NOT NULL,
  `foto_producto` varchar(25) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `productos`
--

INSERT INTO `productos` (`idProductos`, `categoria`, `nombre`, `precio`, `cantidadBodega`, `estado`, `foto_producto`) VALUES
(2, 'framework', 't-shirt vue', 22000, 17, 1, 'img/1.jpg'),
(5, 'framework', 'React', 35000, 2, 1, 'img/3.jpg'),
(7, 'control de versiones', 'Github', 80000, 28, 1, 'img/8.jpg'),
(10, 'scripting', 'typescript', 25000, 29, 1, 'img/10.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idClientes`);

--
-- Indexes for table `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`idFactura`),
  ADD KEY `clienteID` (`clienteID`);

--
-- Indexes for table `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`idProductos`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idClientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `facturas`
--
ALTER TABLE `facturas`
  MODIFY `idFactura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `productos`
--
ALTER TABLE `productos`
  MODIFY `idProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `clienteID` FOREIGN KEY (`clienteID`) REFERENCES `clientes` (`idClientes`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
