-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-05-2018 a las 07:41:59
-- Versión del servidor: 10.1.26-MariaDB
-- Versión de PHP: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `nlp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `polaridadReviews`
--

CREATE TABLE `polaridadreviews` (
  `polaridad` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `rank` int(11) NOT NULL,
  `archivoPos` varchar(30) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `polaridadReviews`
--

INSERT INTO `polaridadReviews` (`polaridad`, `rank`, `archivoPos`) VALUES
('8.425000000000002', 4, '10.review.pos'),
('21.644000000000005', 4, '100.review.pos'),
('2.928', 1, '1000.review.pos'),
('4.189', 2, '1002.review.pos'),
('9.616', 4, '1003.review.pos'),
('8.679', 1, '1005.review.pos'),
('9.323000000000002', 3, '1006.review.pos'),
('3.509', 4, '1007.review.pos'),
('8.834', 4, '1008.review.pos'),
('10.712', 3, '1009.review.pos'),
('3.4320000000000004', 4, '101.review.pos'),
('9.068000000000001', 2, '1010.review.pos'),
('7.566999999999999', 2, '1011.review.pos'),
('18.863999999999997', 3, '1012.review.pos'),
('3.9220000000000006', 2, '1013.review.pos'),
('6.131', 3, '1014.review.pos'),
('9.022', 3, '1015.review.pos'),
('3.328', 4, '1016.review.pos'),
('7.78', 3, '1017.review.pos'),
('8.625', 3, '1018.review.pos'),
('9.098000000000003', 2, '1019.review.pos'),
('5.885', 3, '102.review.pos'),
('12.376', 3, '1020.review.pos'),
('9.793000000000001', 2, '1021.review.pos'),
('18.866', 5, '1022.review.pos'),
('6.125999999999999', 4, '1023.review.pos'),
('8.126999999999999', 2, '1024.review.pos'),
('17.522999999999993', 4, '1025.review.pos'),
('1.433', 1, '1026.review.pos'),
('6.810999999999999', 4, '1028.review.pos'),
('3.549000000000001', 3, '1029.review.pos'),
('3.7410000000000005', 5, '103.review.pos'),
('9.109', 4, '1030.review.pos'),
('6.2749999999999995', 3, '1031.review.pos'),
('12.659', 4, '1032.review.pos'),
('14.741', 5, '1033.review.pos'),
('12.672000000000004', 5, '1034.review.pos'),
('9.352000000000002', 5, '1035.review.pos'),
('12.290000000000001', 5, '1036.review.pos'),
('13.042000000000002', 2, '1037.review.pos'),
('13.708', 2, '1038.review.pos'),
('19.081', 5, '1039.review.pos'),
('35.04199999999997', 5, '104.review.pos'),
('4.744', 2, '1040.review.pos'),
('28.543999999999997', 4, '1041.review.pos'),
('23.978000000000005', 2, '1042.review.pos'),
('11.636999999999999', 2, '1043.review.pos'),
('9.559', 5, '1044.review.pos'),
('6.627', 4, '1045.review.pos'),
('8.315', 5, '1046.review.pos'),
('20.944000000000003', 3, '1047.review.pos'),
('11.046000000000005', 2, '1048.review.pos'),
('10.312000000000001', 2, '1049.review.pos'),
('6.373999999999999', 2, '105.review.pos'),
('12.569', 3, '1050.review.pos'),
('9.638', 5, '1051.review.pos'),
('10.061', 3, '1052.review.pos'),
('9.614000000000003', 2, '1053.review.pos'),
('19.455', 5, '1054.review.pos'),
('7.198999999999998', 1, '1055.review.pos'),
('11.927', 1, '1056.review.pos'),
('4.092', 4, '1057.review.pos'),
('12.689000000000004', 5, '1058.review.pos'),
('2.892', 4, '1059.review.pos'),
('10.677000000000001', 3, '106.review.pos'),
('8.947000000000001', 1, '1060.review.pos'),
('24.864', 5, '1061.review.pos'),
('5.508000000000001', 3, '1062.review.pos'),
('5.418', 5, '1063.review.pos'),
('4.208', 2, '1064.review.pos'),
('6.846', 1, '1065.review.pos'),
('3.6929999999999996', 3, '1066.review.pos'),
('8.347000000000001', 5, '1067.review.pos'),
('5.775', 3, '1068.review.pos'),
('3.5370000000000004', 3, '1069.review.pos'),
('11.048000000000002', 1, '107.review.pos'),
('10.232000000000003', 2, '1070.review.pos'),
('5.628', 3, '1071.review.pos'),
('8.963999999999999', 4, '1072.review.pos'),
('14.047', 3, '1073.review.pos'),
('3.2440000000000007', 1, '1074.review.pos'),
('6.406', 3, '1075.review.pos'),
('9.424', 5, '1076.review.pos'),
('17.932999999999996', 3, '1077.review.pos'),
('4.333', 5, '1078.review.pos'),
('8.842000000000002', 4, '1079.review.pos'),
('3.3480000000000003', 3, '108.review.pos'),
('4.252999999999999', 3, '1080.review.pos'),
('2.5650000000000004', 3, '1081.review.pos'),
('14.751', 5, '1082.review.pos'),
('-1.165', 2, '1083.review.pos'),
('7.906000000000001', 3, '1084.review.pos'),
('8.543', 4, '1085.review.pos'),
('1.424', 3, '1086.review.pos'),
('13.515000000000004', 2, '1087.review.pos'),
('6.279999999999999', 2, '1088.review.pos'),
('5.498', 2, '1089.review.pos'),
('8.459999999999999', 2, '109.review.pos'),
('6.532000000000001', 4, '1090.review.pos'),
('4.100000000000001', 1, '1091.review.pos');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `polaridadReviews`
--
ALTER TABLE `polaridadReviews`
  ADD PRIMARY KEY (`archivoPos`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
