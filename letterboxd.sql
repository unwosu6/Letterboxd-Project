-- MariaDB dump 10.17  Distrib 10.4.8-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: letterboxd
-- ------------------------------------------------------
-- Server version	10.4.8-MariaDB-1:10.4.8+maria~bionic-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `all_users`
--

DROP TABLE IF EXISTS `all_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `all_users` (
  `username` varchar(255) NOT NULL,
  `average_difference` float(3,2) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `all_users`
--

LOCK TABLES `all_users` WRITE;
/*!40000 ALTER TABLE `all_users` DISABLE KEYS */;
INSERT INTO `all_users` VALUES ('bestwum',0.60),('eman2',NULL),('unwosu',0.65);
/*!40000 ALTER TABLE `all_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bestwum`
--

DROP TABLE IF EXISTS `bestwum`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bestwum` (
  `Name` text DEFAULT NULL,
  `Year` bigint(20) DEFAULT NULL,
  `Rating` double DEFAULT NULL,
  `Meter_Score` double DEFAULT NULL,
  `Difference` double DEFAULT NULL,
  `Actual_Difference` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bestwum`
--

LOCK TABLES `bestwum` WRITE;
/*!40000 ALTER TABLE `bestwum` DISABLE KEYS */;
INSERT INTO `bestwum` VALUES ('Annihilation',2018,4,4.4,0.4,-0.4),('Parasite',2019,4.5,NULL,NULL,NULL),('The Cabin in the Woods',2011,3.5,4.6,1.1,-1.1),('Event Horizon',1997,1.5,1.45,0.05,0.05),('The Lighthouse',2019,4,3.55,0.45,0.45),('Her',2013,5,NULL,NULL,NULL),('Re-Animator',1985,3,4.65,1.65,-1.65),('Django Unchained',2012,4.5,4.35,0.15,0.15),('The Matrix',1999,4,4.4,0.4,-0.4),('The Descent',2005,4,4.3,0.3,-0.3),('Inception',2010,3.5,4.35,0.85,-0.85),('Uncut Gems',2019,4.5,4.55,0.0499999999999998,-0.0499999999999998),('The Death of Stalin',2017,4,4.75,0.75,-0.75),('Twin Peaks',1989,3,NULL,NULL,NULL),('Straight Up',2019,3.5,4.65,1.15,-1.15),('Good Time',2017,3.5,4.6,1.1,-1.1),('The Lord of the Rings: The Fellowship of the Ring',2001,5,4.55,0.45,0.45),('The Lord of the Rings: The Two Towers',2002,4.5,4.75,0.25,-0.25),('The Lord of the Rings: The Return of the King',2003,5,4.65,0.35,0.35),('Palm Springs',2020,4,4.75,0.75,-0.75),('A Silent Voice',2016,3,NULL,NULL,NULL),('Your Name.',2016,4,NULL,NULL,NULL);
/*!40000 ALTER TABLE `bestwum` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `eman2`
--

DROP TABLE IF EXISTS `eman2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `eman2` (
  `Name` text DEFAULT NULL,
  `Year` bigint(20) DEFAULT NULL,
  `Rating` double DEFAULT NULL,
  `Meter_Score` double DEFAULT NULL,
  `Difference` double DEFAULT NULL,
  `Actual_Difference` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eman2`
--

LOCK TABLES `eman2` WRITE;
/*!40000 ALTER TABLE `eman2` DISABLE KEYS */;
INSERT INTO `eman2` VALUES ('In The Heights',2021,4.5,NULL,NULL,NULL);
/*!40000 ALTER TABLE `eman2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unwosu`
--

DROP TABLE IF EXISTS `unwosu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `unwosu` (
  `Name` text DEFAULT NULL,
  `Year` bigint(20) DEFAULT NULL,
  `Rating` double DEFAULT NULL,
  `Meter_Score` double DEFAULT NULL,
  `Difference` double DEFAULT NULL,
  `Actual_Difference` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unwosu`
--

LOCK TABLES `unwosu` WRITE;
/*!40000 ALTER TABLE `unwosu` DISABLE KEYS */;
INSERT INTO `unwosu` VALUES ('Straight Up',2019,5,4.65,0.35,0.35),('It\'s Such a Beautiful Day',2012,5,5,0,0),('World of Tomorrow',2015,5,5,0,0),('Eternal Sunshine of the Spotless Mind',2004,4,4.6,0.6,-0.6),('The Truman Show',1998,4,4.75,0.75,-0.75),('Eighth Grade',2018,4,4.95,0.95,-0.95),('The Half of It',2020,5,4.85,0.15,0.15),('Being John Malkovich',1999,5,4.7,0.3,0.3),('Portrait of a Lady on Fire',2019,4,NULL,NULL,NULL),('The Lorax',2012,3.5,NULL,NULL,NULL),('The One I Love',2014,4,4.1,0.0999999999999996,-0.0999999999999996),('Duck Butter',2018,5,2.85,2.15,2.15),('Lady Bird',2017,4.5,4.95,0.45,-0.45),('Everything, Everything',2017,3.5,2.25,1.25,1.25),('I\'m Thinking of Ending Things',2020,5,4.1,0.9,0.9),('Skate Kitchen',2018,5,4.45,0.55,0.55),('Kajillionaire',2020,5,4.5,0.5,0.5),('Juno',2007,4,4.7,0.7,-0.7),('Promising Young Woman',2020,5,4.5,0.5,0.5),('Little Miss Sunshine',2006,5,4.55,0.45,0.45),('Sorry to Bother You',2018,4,4.65,0.65,-0.65),('Ingrid Goes West',2017,3.5,4.3,0.8,-0.8),('Happiest Season',2020,3.5,4.1,0.6,-0.6),('Symbiopsychotaxiplasm: Take One',1968,5,4.4,0.6,0.6),('I Care a Lot',2020,3,3.9,0.9,-0.9),('Boys State',2020,3.5,4.7,1.2,-1.2),('The Social Network',2010,2.5,4.8,2.3,-2.3),('Scare Me',2020,4,4.1,0.0999999999999996,-0.0999999999999996),('The Reliant',2019,2,NULL,NULL,NULL),('Knives Out',2019,4.5,4.85,0.35,-0.35),('Bo Burnham: Inside',2021,4.5,4.7,0.2,-0.2),('Hereditary',2018,4,4.45,0.45,-0.45);
/*!40000 ALTER TABLE `unwosu` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 17:26:01
