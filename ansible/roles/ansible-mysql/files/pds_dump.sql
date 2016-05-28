-- MySQL dump 10.13  Distrib 5.6.19, for osx10.7 (i386)
--
-- Host: localhost    Database: iupds_db
-- ------------------------------------------------------
-- Server version	5.5.49-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_group_permissi_permission_id_84c5c92e_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permissi_content_type_id_2f476e4b_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add profile',7,'add_profile'),(20,'Can change profile',7,'change_profile'),(21,'Can delete profile',7,'delete_profile'),(22,'Can add email track',8,'add_emailtrack'),(23,'Can change email track',8,'change_emailtrack'),(24,'Can delete email track',8,'delete_emailtrack'),(25,'Can add contact',9,'add_contact'),(26,'Can change contact',9,'change_contact'),(27,'Can delete contact',9,'delete_contact'),(28,'Can add address',10,'add_address'),(29,'Can change address',10,'change_address'),(30,'Can delete address',10,'delete_address'),(31,'Can add graph',11,'add_graph'),(32,'Can change graph',11,'change_graph'),(33,'Can delete graph',11,'delete_graph'),(34,'Can add account',12,'add_account'),(35,'Can change account',12,'change_account'),(36,'Can delete account',12,'delete_account'),(37,'Can add application',13,'add_application'),(38,'Can change application',13,'change_application'),(39,'Can delete application',13,'delete_application'),(40,'Can add grant',14,'add_grant'),(41,'Can change grant',14,'change_grant'),(42,'Can delete grant',14,'delete_grant'),(43,'Can add access token',15,'add_accesstoken'),(44,'Can change access token',15,'change_accesstoken'),(45,'Can delete access token',15,'delete_accesstoken'),(46,'Can add refresh token',16,'add_refreshtoken'),(47,'Can change refresh token',16,'change_refreshtoken'),(48,'Can delete refresh token',16,'delete_refreshtoken'),(49,'Can add cors model',17,'add_corsmodel'),(50,'Can change cors model',17,'change_corsmodel'),(51,'Can delete cors model',17,'delete_corsmodel'),(52,'Can add application',18,'add_application'),(53,'Can change application',18,'change_application'),(54,'Can delete application',18,'delete_application'),(55,'Can add grant',19,'add_grant'),(56,'Can change grant',19,'change_grant'),(57,'Can delete grant',19,'delete_grant'),(58,'Can add access token',20,'add_accesstoken'),(59,'Can change access token',20,'change_accesstoken'),(60,'Can delete access token',20,'delete_accesstoken'),(61,'Can add refresh token',21,'add_refreshtoken'),(62,'Can change refresh token',21,'change_refreshtoken'),(63,'Can delete refresh token',21,'delete_refreshtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$24000$H9069dT0dhKw$/KD2u1cvuAFTWodFqefPQP/IkfaLp8ktThpKkpxCvII=','2016-04-10 03:07:49',1,'test_user','','','admin@gmail.com',1,1,'2016-04-08 15:24:37');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `auth_user_user_perm_permission_id_1fbb5f2c_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authentication_account`
--

DROP TABLE IF EXISTS `authentication_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authentication_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `username` varchar(40) NOT NULL,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `tagline` varchar(140) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authentication_account`
--

LOCK TABLES `authentication_account` WRITE;
/*!40000 ALTER TABLE `authentication_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `authentication_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin__content_type_id_c4bce8eb_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2016-04-08 15:29:02','1','test',1,'Added.',13,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(12,'authentication','account'),(5,'contenttypes','contenttype'),(17,'corsheaders','corsmodel'),(20,'iupdsmanager','accesstoken'),(10,'iupdsmanager','address'),(18,'iupdsmanager','application'),(9,'iupdsmanager','contact'),(8,'iupdsmanager','emailtrack'),(19,'iupdsmanager','grant'),(11,'iupdsmanager','graph'),(7,'iupdsmanager','profile'),(21,'iupdsmanager','refreshtoken'),(15,'oauth2_provider','accesstoken'),(13,'oauth2_provider','application'),(14,'oauth2_provider','grant'),(16,'oauth2_provider','refreshtoken'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-04-07 23:56:09'),(2,'auth','0001_initial','2016-04-07 23:56:10'),(3,'admin','0001_initial','2016-04-07 23:56:10'),(4,'admin','0002_logentry_remove_auto_add','2016-04-07 23:56:10'),(5,'contenttypes','0002_remove_content_type_name','2016-04-07 23:56:10'),(6,'auth','0002_alter_permission_name_max_length','2016-04-07 23:56:10'),(7,'auth','0003_alter_user_email_max_length','2016-04-07 23:56:10'),(8,'auth','0004_alter_user_username_opts','2016-04-07 23:56:10'),(9,'auth','0005_alter_user_last_login_null','2016-04-07 23:56:10'),(10,'auth','0006_require_contenttypes_0002','2016-04-07 23:56:10'),(11,'auth','0007_alter_validators_add_error_messages','2016-04-07 23:56:10'),(12,'authentication','0001_initial','2016-04-07 23:56:10'),(13,'iupdsmanager','0001_initial','2016-04-07 23:56:11'),(14,'sessions','0001_initial','2016-04-07 23:56:11'),(15,'oauth2_provider','0001_initial','2016-04-08 15:03:22'),(16,'oauth2_provider','0002_08_updates','2016-04-08 15:03:23'),(17,'iupdsmanager','0002_auto_20160409_0511','2016-04-09 02:11:41'),(18,'iupdsmanager','0003_profile_appscale_user_id','2016-04-09 03:36:21');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('8j6g6d3shgutwo08wjz1k4eqzi0ido6c','OGIyYmMyNjNhZGZjYTc3MTQ0NGI2MGY4NGZhZjJjMDFlMjE5MThlZTp7ImNsaWVudF9pZCI6ImU1ZmQzZTdhMTU5NDQxMmI2OGU2NjU5ZjA2YzQyNjc2IiwicmVkaXJlY3RfdXJpIjoiTm9uZSIsIl9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiNGU4ODNhM2M2ZmZmN2YxNGQ4ZDYwODRjNTMzYTVmNDc4MDZhNTFiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2016-04-30 20:56:19');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iupdsmanager_accesstoken`
--

DROP TABLE IF EXISTS `iupdsmanager_accesstoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_accesstoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `expires` datetime NOT NULL,
  `scope` longtext NOT NULL,
  `application_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `iupdsmanager_accesstoken_94a08da1` (`token`),
  KEY `iupdsmanager_accesstoken_6bc0a4eb` (`application_id`),
  KEY `iupdsmanager_accesstoken_e8701ad4` (`user_id`),
  CONSTRAINT `iupdsmanager_accesst_user_id_acb6bdd9_fk_iupdsmanager_profile_id` FOREIGN KEY (`user_id`) REFERENCES `iupdsmanager_profile` (`id`),
  CONSTRAINT `iupdsmana_application_id_ec7814b9_fk_iupdsmanager_application_id` FOREIGN KEY (`application_id`) REFERENCES `iupdsmanager_application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iupdsmanager_address`
--

DROP TABLE IF EXISTS `iupdsmanager_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `street` varchar(64) DEFAULT NULL,
  `city` varchar(25) DEFAULT NULL,
  `post_code` varchar(8) NOT NULL,
  `county` varchar(25) DEFAULT NULL,
  `district` varchar(25) DEFAULT NULL,
  `city_district` varchar(25) DEFAULT NULL,
  `country` varchar(25) DEFAULT NULL,
  `primary` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deletion_date` datetime DEFAULT NULL,
  `profile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iupdsmanager_address_83a0eb3f` (`profile_id`),
  CONSTRAINT `iupdsmanager_addr_profile_id_6be14141_fk_iupdsmanager_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `iupdsmanager_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iupdsmanager_application`
--

DROP TABLE IF EXISTS `iupdsmanager_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) NOT NULL,
  `redirect_uris` longtext NOT NULL,
  `client_type` varchar(32) NOT NULL,
  `authorization_grant_type` varchar(32) NOT NULL,
  `client_secret` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `skip_authorization` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `client_id_UNIQUE` (`client_id`),
  KEY `iupdsmanager_application_9d667c2b` (`client_secret`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iupdsmanager_contact`
--

DROP TABLE IF EXISTS `iupdsmanager_contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_contact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contact` varchar(64) NOT NULL,
  `contact_section` varchar(15) NOT NULL,
  `contact_type` varchar(15) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deletion_date` datetime DEFAULT NULL,
  `profile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iupdsmanager_contact_83a0eb3f` (`profile_id`),
  CONSTRAINT `iupdsmanager_cont_profile_id_c4e4e0c9_fk_iupdsmanager_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `iupdsmanager_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iupdsmanager_emailtrack`
--

DROP TABLE IF EXISTS `iupdsmanager_emailtrack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_emailtrack` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_uuid` char(32) NOT NULL,
  `email_sent` tinyint(1) NOT NULL,
  `mail_type` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iupdsmanager_emailtrack`
--

LOCK TABLES `iupdsmanager_emailtrack` WRITE;
/*!40000 ALTER TABLE `iupdsmanager_emailtrack` DISABLE KEYS */;
/*!40000 ALTER TABLE `iupdsmanager_emailtrack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iupdsmanager_grant`
--

DROP TABLE IF EXISTS `iupdsmanager_grant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_grant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) NOT NULL,
  `expires` datetime NOT NULL,
  `redirect_uri` varchar(255) NOT NULL,
  `scope` longtext NOT NULL,
  `application_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iupdsmana_application_id_935a71ee_fk_iupdsmanager_application_id` (`application_id`),
  KEY `iupdsmanager_grant_user_id_4799d7b4_fk_iupdsmanager_profile_id` (`user_id`),
  KEY `iupdsmanager_grant_c1336794` (`code`),
  CONSTRAINT `iupdsmanager_grant_user_id_4799d7b4_fk_iupdsmanager_profile_id` FOREIGN KEY (`user_id`) REFERENCES `iupdsmanager_profile` (`id`),
  CONSTRAINT `iupdsmana_application_id_935a71ee_fk_iupdsmanager_application_id` FOREIGN KEY (`application_id`) REFERENCES `iupdsmanager_application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `iupdsmanager_graph`
--

DROP TABLE IF EXISTS `iupdsmanager_graph`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_graph` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `graph` varchar(200) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `deletion_date` datetime DEFAULT NULL,
  `profile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `iupdsmanager_graph_83a0eb3f` (`profile_id`),
  CONSTRAINT `iupdsmanager_grap_profile_id_891034bd_fk_iupdsmanager_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `iupdsmanager_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iupdsmanager_graph`
--

LOCK TABLES `iupdsmanager_graph` WRITE;
/*!40000 ALTER TABLE `iupdsmanager_graph` DISABLE KEYS */;
/*!40000 ALTER TABLE `iupdsmanager_graph` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iupdsmanager_profile`
--

DROP TABLE IF EXISTS `iupdsmanager_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iupdsmanager_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) NOT NULL,
  `user_id_old` int(10) unsigned NOT NULL,
  `email` varchar(254) NOT NULL,
  `username` varchar(30) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_cloud_admin` tinyint(1) NOT NULL,
  `admin_type` varchar(20) NOT NULL,
  `appscale_user_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id_old` (`user_id_old`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `appscale_user_id` (`appscale_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8872 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iupdsmanager_profile`
--
INSERT INTO `iupdsmanager_profile` VALUES (1,9223372036854775807,0,'admin@gmail.com','','','','',0,0,'0000-00-00 00:00:00','0000-00-00 00:00:00',NULL,0,'','admin');

--
-- Table structure for table `iupdsmanager_refreshtoken`
--

DROP TABLE IF EXISTS `iupdsmanager_refreshtoken`;
CREATE TABLE `iupdsmanager_refreshtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(255) NOT NULL,
  `access_token_id` int(11) NOT NULL,
  `application_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token_id` (`access_token_id`),
  KEY `iupdsmana_application_id_1d3a9052_fk_iupdsmanager_application_id` (`application_id`),
  KEY `iupdsmanager_refresh_user_id_8fc23d23_fk_iupdsmanager_profile_id` (`user_id`),
  KEY `iupdsmanager_refreshtoken_94a08da1` (`token`),
  CONSTRAINT `iupdsmanager_refresh_user_id_8fc23d23_fk_iupdsmanager_profile_id` FOREIGN KEY (`user_id`) REFERENCES `iupdsmanager_profile` (`id`),
  CONSTRAINT `iupdsmana_application_id_1d3a9052_fk_iupdsmanager_application_id` FOREIGN KEY (`application_id`) REFERENCES `iupdsmanager_application` (`id`),
  CONSTRAINT `iupdsman_access_token_id_64e74c7d_fk_iupdsmanager_accesstoken_id` FOREIGN KEY (`access_token_id`) REFERENCES `iupdsmanager_accesstoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-05-09  1:11:17
