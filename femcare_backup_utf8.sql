-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: femcare
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `completed_recommendations`
--

DROP TABLE IF EXISTS `completed_recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `completed_recommendations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `recommendation_id` int NOT NULL,
  `completed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_recommendation` (`user_id`,`recommendation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `completed_recommendations`
--

LOCK TABLES `completed_recommendations` WRITE;
/*!40000 ALTER TABLE `completed_recommendations` DISABLE KEYS */;
INSERT INTO `completed_recommendations` VALUES (1,2,3,'2026-08-12 06:19:04'),(2,2,4,'2026-08-12 06:21:28'),(3,2,11,'2026-08-12 06:31:58'),(4,2,15,'2026-08-12 06:33:16'),(5,2,5,'2026-08-12 06:34:50'),(6,2,14,'2026-08-12 07:07:05'),(7,1,1,'2026-08-12 07:27:29'),(8,1,2,'2026-08-12 07:27:42'),(9,4,14,'2026-08-12 08:15:09'),(10,2,9,'2026-08-12 12:39:56'),(11,3,5,'2026-08-12 16:55:43'),(12,3,6,'2026-08-12 16:55:47');
/*!40000 ALTER TABLE `completed_recommendations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `early_puberty_logs`
--

DROP TABLE IF EXISTS `early_puberty_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `early_puberty_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `puberty_signs` varchar(20) DEFAULT NULL,
  `early_breast_development` varchar(20) DEFAULT NULL,
  `early_pubic_hair` varchar(20) DEFAULT NULL,
  `early_underarm_hair` varchar(20) DEFAULT NULL,
  `body_odor` varchar(20) DEFAULT NULL,
  `acne` varchar(20) DEFAULT NULL,
  `rapid_growth` varchar(20) DEFAULT NULL,
  `vaginal_bleeding` varchar(20) DEFAULT NULL,
  `reference_result` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `early_puberty_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `early_puberty_logs`
--

LOCK TABLES `early_puberty_logs` WRITE;
/*!40000 ALTER TABLE `early_puberty_logs` DISABLE KEYS */;
INSERT INTO `early_puberty_logs` VALUES (1,4,7,'Yes','Yes','Yes','No','Yes','No','Yes','No','Several early puberty-related signs were selected for this age group.','2026-08-12 08:49:45'),(2,4,16,'Yes','Yes','Yes','No','Yes','Yes','Yes','Yes','The selected information does not show strong early-puberty reference indicators.','2026-08-12 08:55:07'),(3,1,13,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information does not show strong early-puberty reference indicators.','2026-08-12 12:35:35'),(4,1,12,'No','No','No','No','No','No','No','No','The selected information does not show strong early-puberty reference indicators.','2026-08-12 12:36:45'),(5,1,8,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','No','The selected information does not show strong early-puberty reference indicators.','2026-08-12 12:37:21'),(6,2,12,'No','No','No','No','No','No','No','No','The child is 12 years old and no puberty-related signs were selected. The current information does not show strong early-puberty reference indicators.','2026-08-12 12:43:09'),(7,2,8,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','No','The child is 8 years old and multiple puberty-related signs were selected: Puberty signs, Early breast development, Early pubic hair, Early underarm hair, Body odor, Acne, Rapid growth. The combination of recorded signs may warrant discussion with a qualified healthcare professional.','2026-08-12 12:44:55'),(8,2,8,'','','','','','','','','The child is 8 years old and no puberty-related signs were selected. The current information does not show strong early-puberty reference indicators.','2026-08-12 12:47:28'),(9,3,16,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The child is 16 years old and 8 puberty-related signs were selected: Puberty signs, Early breast development, Early pubic hair, Early underarm hair, Body odor, Acne, Rapid growth, Vaginal bleeding. The recorded information shows several puberty-related indicators. Continued monitoring may be appropriate.','2026-08-12 16:50:30');
/*!40000 ALTER TABLE `early_puberty_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `food_logs`
--

DROP TABLE IF EXISTS `food_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `log_date` date NOT NULL,
  `meals_per_day` int DEFAULT NULL,
  `fruits_servings` decimal(5,2) DEFAULT NULL,
  `vegetables_servings` decimal(5,2) DEFAULT NULL,
  `protein_servings` decimal(5,2) DEFAULT NULL,
  `water_intake_liters` decimal(5,2) DEFAULT NULL,
  `fast_food` varchar(20) DEFAULT NULL,
  `sugary_drinks` varchar(20) DEFAULT NULL,
  `breakfast` varchar(20) DEFAULT NULL,
  `dietary_preference` varchar(50) DEFAULT NULL,
  `nutrition_score` decimal(5,2) DEFAULT NULL,
  `reference_result` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `food_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `food_logs`
--

LOCK TABLES `food_logs` WRITE;
/*!40000 ALTER TABLE `food_logs` DISABLE KEYS */;
INSERT INTO `food_logs` VALUES (1,4,'2026-08-12',3,2.00,3.00,2.00,2.50,'No','No','Yes','Vegetarian',95.00,'Your selected food pattern shows strong nutrition reference indicators.','2026-08-12 10:41:24'),(2,1,'2026-08-12',3,0.00,0.00,1.00,2.00,'Yes','No','Yes','Vegetarian',48.00,'Your selected food pattern may benefit from improved nutrition habits.','2026-08-12 10:44:18'),(3,2,'2026-08-12',3,2.00,2.00,0.00,2.00,'Yes','Yes','Yes','Vegetarian',60.00,'Your selected food pattern shows moderate nutrition reference indicators.','2026-08-12 14:27:24'),(4,3,'2026-08-12',3,2.00,3.00,1.00,2.00,'Yes','No','Yes','',83.00,'Your selected food pattern shows strong nutrition reference indicators.','2026-08-12 16:52:47');
/*!40000 ALTER TABLE `food_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_logs`
--

DROP TABLE IF EXISTS `health_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `log_date` date NOT NULL,
  `sleep_hours` decimal(4,2) DEFAULT NULL,
  `water_intake_liters` decimal(4,2) DEFAULT NULL,
  `stress_score` decimal(5,2) DEFAULT NULL,
  `exercise_minutes` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_health_logs_user_date` (`user_id`,`log_date`),
  CONSTRAINT `fk_health_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_logs`
--

LOCK TABLES `health_logs` WRITE;
/*!40000 ALTER TABLE `health_logs` DISABLE KEYS */;
INSERT INTO `health_logs` VALUES (1,2,'2026-08-12',5.00,3.00,6.00,0,'2026-08-12 05:31:53'),(2,2,'2026-08-09',6.00,2.00,8.00,10,'2026-08-12 05:36:00'),(3,2,'2026-08-10',7.00,2.50,6.00,20,'2026-08-12 05:36:08'),(4,2,'2026-08-11',7.50,3.00,4.00,30,'2026-08-12 05:36:15'),(5,1,'2026-08-12',3.00,2.00,5.00,30,'2026-08-12 07:34:19'),(6,1,'2026-08-02',2.00,2.00,6.00,5,'2026-08-12 07:34:44'),(7,4,'2026-08-12',7.00,2.50,4.00,30,'2026-08-12 08:16:05'),(8,6,'2026-08-04',5.00,2.00,5.00,10,'2026-08-12 18:14:57'),(9,6,'2026-06-10',3.00,1.50,8.00,0,'2026-08-12 18:16:21'),(10,3,'2026-06-11',5.00,1.50,6.00,10,'2026-08-12 18:30:55'),(11,3,'2026-07-15',3.00,1.00,7.00,0,'2026-08-12 18:31:20');
/*!40000 ALTER TABLE `health_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `health_profiles`
--

DROP TABLE IF EXISTS `health_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `health_profiles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `bmi` decimal(5,2) DEFAULT NULL,
  `diet_quality` varchar(50) DEFAULT NULL,
  `exercise_frequency` varchar(50) DEFAULT NULL,
  `sleep_hours` decimal(4,2) DEFAULT NULL,
  `water_intake_liters` decimal(4,2) DEFAULT NULL,
  `caffeine_intake` varchar(50) DEFAULT NULL,
  `stress_score` decimal(5,2) DEFAULT NULL,
  `birth_control_use` varchar(50) DEFAULT NULL,
  `pcos_diagnosed` varchar(20) DEFAULT NULL,
  `alcohol_consumption` varchar(50) DEFAULT NULL,
  `smoking_status` varchar(50) DEFAULT NULL,
  `stress_score_baseline` decimal(5,2) DEFAULT NULL,
  `weight_gain` varchar(10) DEFAULT NULL,
  `hair_growth` varchar(10) DEFAULT NULL,
  `skin_darkening` varchar(10) DEFAULT NULL,
  `hair_loss` varchar(10) DEFAULT NULL,
  `pimples` varchar(10) DEFAULT NULL,
  `fast_food` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `health_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `health_profiles`
--

LOCK TABLES `health_profiles` WRITE;
/*!40000 ALTER TABLE `health_profiles` DISABLE KEYS */;
INSERT INTO `health_profiles` VALUES (1,1,26,25.00,'Poor','Never',5.00,NULL,'Low',NULL,'Yes','Unknown','None','Never',7.00,'No','No','Yes','Yes','Yes','Yes'),(2,2,22,20.00,'Average','Never',3.00,2.00,'Low',NULL,'Yes',NULL,'None','Never',5.00,'No','No','Yes','Yes','Yes','Yes'),(3,3,25,20.00,'Poor','Never',3.00,3.00,'Moderate',NULL,'Yes','Unknown','None','Never',5.00,'Yes','Yes','Yes','Yes','Yes','Yes'),(4,4,25,22.00,'Poor','Never',5.00,2.00,'High',NULL,'No','Unknown','Occasional','Former',5.00,'No','No','Yes','Yes','Yes','Yes'),(5,6,26,20.00,'Poor','Never',4.00,2.00,'Low',NULL,'Yes','Unknown','None','Never',5.00,'No','No','Yes','Yes','Yes','Yes');
/*!40000 ALTER TABLE `health_profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menopause_logs`
--

DROP TABLE IF EXISTS `menopause_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menopause_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `periods_stopped` varchar(20) DEFAULT NULL,
  `months_since_last_period` int DEFAULT NULL,
  `hot_flashes` varchar(20) DEFAULT NULL,
  `night_sweats` varchar(20) DEFAULT NULL,
  `mood_changes` varchar(20) DEFAULT NULL,
  `sleep_problems` varchar(20) DEFAULT NULL,
  `vaginal_dryness` varchar(20) DEFAULT NULL,
  `fatigue` varchar(20) DEFAULT NULL,
  `concentration_problems` varchar(20) DEFAULT NULL,
  `joint_pain` varchar(20) DEFAULT NULL,
  `reference_result` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `menopause_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menopause_logs`
--

LOCK TABLES `menopause_logs` WRITE;
/*!40000 ALTER TABLE `menopause_logs` DISABLE KEYS */;
INSERT INTO `menopause_logs` VALUES (1,4,50,'Yes',14,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information is consistent with a menopause-stage reference pattern.','2026-08-12 10:22:52'),(2,1,50,'No',2,'Yes','Yes','Yes','Yes','Yes','Yes','No','Yes','Several symptoms commonly associated with menopause were selected.','2026-08-12 10:27:15'),(3,1,35,'',0,'','','','','','','','','The selected information does not show strong menopause reference indicators.','2026-08-12 10:54:33'),(4,2,48,'No',0,'No','No','No','No','No','No','No','No','At age 48, no common menopause-related symptoms were selected. The current information does not show strong menopause reference indicators.','2026-08-12 12:57:11'),(5,2,52,'Yes',14,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','At age 52, the reported information shows that periods have stopped and 14 months have passed since the last period. The selected symptoms are: Hot flashes, Night sweats, Mood changes, Sleep problems, Vaginal dryness, Fatigue, Concentration problems, Joint pain. This information shows a menopause-stage reference pattern with several associated symptoms.','2026-08-12 12:57:56'),(6,2,47,'No',3,'Yes','No','Yes','No','No','Yes','No','No','At age 47, the following symptoms were selected: Hot flashes, Mood changes, Fatigue. Some menopause-related reference indicators are present. The menstrual information should be considered together with the reported symptoms.','2026-08-12 12:58:35'),(7,3,36,'No',0,'Yes','Yes','Yes','Yes','No','Yes','Yes','No','At age 36, periods have not been reported as stopped for 12 months. However, several symptoms were selected: Hot flashes, Night sweats, Mood changes, Sleep problems, Fatigue, Concentration problems. The reported information contains multiple menopause-related reference indicators, although the menstrual information does not show a 12-month period-free pattern.','2026-08-12 16:52:02');
/*!40000 ALTER TABLE `menopause_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pcos_logs`
--

DROP TABLE IF EXISTS `pcos_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pcos_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `bmi` decimal(5,2) DEFAULT NULL,
  `irregular_periods` varchar(10) DEFAULT NULL,
  `acne` varchar(10) DEFAULT NULL,
  `excess_hair_growth` varchar(10) DEFAULT NULL,
  `hair_loss` varchar(10) DEFAULT NULL,
  `weight_gain` varchar(10) DEFAULT NULL,
  `pelvic_pain` varchar(10) DEFAULT NULL,
  `pcos_result` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_pcos_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pcos_logs`
--

LOCK TABLES `pcos_logs` WRITE;
/*!40000 ALTER TABLE `pcos_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `pcos_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perimenopause_logs`
--

DROP TABLE IF EXISTS `perimenopause_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `perimenopause_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `cycle_irregularity` varchar(20) DEFAULT NULL,
  `hot_flashes` varchar(20) DEFAULT NULL,
  `night_sweats` varchar(20) DEFAULT NULL,
  `mood_changes` varchar(20) DEFAULT NULL,
  `sleep_problems` varchar(20) DEFAULT NULL,
  `vaginal_dryness` varchar(20) DEFAULT NULL,
  `fatigue` varchar(20) DEFAULT NULL,
  `headache` varchar(20) DEFAULT NULL,
  `concentration_problems` varchar(20) DEFAULT NULL,
  `reference_result` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `perimenopause_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perimenopause_logs`
--

LOCK TABLES `perimenopause_logs` WRITE;
/*!40000 ALTER TABLE `perimenopause_logs` DISABLE KEYS */;
INSERT INTO `perimenopause_logs` VALUES (1,4,45,'Yes','Yes','Yes','Yes','Yes','No','Yes','No','Yes','Several symptoms commonly associated with the perimenopause transition were selected.','2026-08-12 08:57:50'),(2,4,36,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information does not show strong perimenopause reference indicators for the selected age.','2026-08-12 09:06:56'),(3,2,48,'No','No','No','No','No','No','No','No','No','At age 48, no perimenopause-related symptoms were selected. The current information does not show strong perimenopause reference indicators.','2026-08-12 12:49:58'),(4,2,47,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','No','Yes','At age 47, several symptoms were selected that can occur during the perimenopause transition. The selected symptoms are: Cycle irregularity, Hot flashes, Night sweats, Mood changes, Sleep problems, Vaginal dryness, Fatigue, Concentration problems. The combination of these reported symptoms may warrant further discussion with a qualified healthcare professional.','2026-08-12 12:50:40'),(5,2,47,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','At age 47, several symptoms were selected that can occur during the perimenopause transition. The selected symptoms are: Cycle irregularity, Hot flashes, Night sweats, Mood changes, Sleep problems, Vaginal dryness, Fatigue, Headache, Concentration problems. The combination of these reported symptoms may warrant further discussion with a qualified healthcare professional.','2026-08-12 12:50:49'),(6,2,42,'Yes','No','No','Yes','No','No','Yes','No','No','At age 42, the following symptoms were selected: Cycle irregularity, Mood changes, Fatigue. Some perimenopause-related reference indicators are present in the information provided.','2026-08-12 12:51:34'),(7,2,42,'Yes','Yes','No','No','Yes','Yes','Yes','Yes','Yes','At age 42, multiple symptoms were selected: Cycle irregularity, Hot flashes, Sleep problems, Vaginal dryness, Fatigue, Headache, Concentration problems. These recorded symptoms may be associated with hormonal or menstrual changes and may warrant further evaluation.','2026-08-12 12:53:08'),(8,3,36,'Yes','Yes','No','Yes','Yes','No','Yes','No','Yes','At age 36, several symptoms were selected: Cycle irregularity, Hot flashes, Mood changes, Sleep problems, Fatigue, Concentration problems. Although the selected age is below the usual age range considered by this reference screening, the reported symptoms may still warrant professional evaluation.','2026-08-12 16:51:28');
/*!40000 ALTER TABLE `perimenopause_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `period_logs`
--

DROP TABLE IF EXISTS `period_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `period_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `cycle_number` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `cycle_length_days` int DEFAULT NULL,
  `prev_cycle_length` decimal(5,2) DEFAULT NULL,
  `cycle_phase` varchar(50) DEFAULT NULL,
  `flow_level` varchar(50) DEFAULT NULL,
  `pain_level` int DEFAULT NULL,
  `pms_symptoms` varchar(255) DEFAULT NULL,
  `mood_score` int DEFAULT NULL,
  `stress_score_cycle` decimal(5,2) DEFAULT NULL,
  `sleep_hours_cycle` decimal(4,2) DEFAULT NULL,
  `energy_level` int DEFAULT NULL,
  `concentration_score` int DEFAULT NULL,
  `work_hours_lost` decimal(5,2) DEFAULT NULL,
  `overall_health_score` decimal(5,2) DEFAULT NULL,
  `log_consistency_score` decimal(5,3) DEFAULT NULL,
  `prepared_before_period` tinyint DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `period_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `period_logs`
--

LOCK TABLES `period_logs` WRITE;
/*!40000 ALTER TABLE `period_logs` DISABLE KEYS */;
INSERT INTO `period_logs` VALUES (1,1,4,'2026-08-05',32,20.00,NULL,'Light',5,'cramps',5,8.00,4.90,5,4,4.80,NULL,NULL,0,'2026-08-11 15:51:16'),(3,2,2,'2026-07-07',28,35.00,NULL,'Light',6,'headache',5,6.00,4.00,5,4,5.00,NULL,NULL,0,'2026-08-11 16:40:49'),(4,2,3,'2026-08-05',28,28.00,NULL,'Medium',7,'cramps',6,6.00,3.00,5,5,3.00,NULL,NULL,0,'2026-08-11 16:41:41'),(5,1,3,'2026-07-14',20,25.00,NULL,'Heavy',9,'cramps,bloating,headache',6,8.00,2.00,3,4,3.00,NULL,NULL,1,'2026-08-11 16:45:31'),(6,3,3,'2026-08-03',28,25.00,NULL,'Medium',5,'cramps',5,6.00,6.00,4,5,4.00,NULL,NULL,1,'2026-08-11 16:49:46'),(7,3,2,'2026-07-01',25,35.00,NULL,'Medium',6,'headache',5,5.00,6.00,4,5,3.00,NULL,NULL,0,'2026-08-11 16:50:57'),(8,1,2,'2026-07-02',25,35.00,NULL,'Heavy',8,'bloating',5,7.00,3.00,4,6,3.00,NULL,NULL,0,'2026-08-11 17:42:53'),(9,1,5,'2026-08-20',30,32.00,NULL,'Light',3,'cramps',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,'2026-08-11 18:00:20'),(10,2,4,'2026-08-05',28,28.00,NULL,'Light',5,'cramps',5,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-08-12 04:13:49'),(11,1,1,'2026-01-13',35,NULL,NULL,'Heavy',6,'bloating',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,'2026-08-12 07:59:05'),(12,4,1,'2026-08-12',28,NULL,NULL,'Medium',4,'cramps',7,4.00,7.00,7,7,1.00,NULL,NULL,1,'2026-08-12 08:18:01'),(13,2,1,'2026-03-11',35,NULL,NULL,'Medium',8,'headache',5,5.00,8.00,5,6,2.00,NULL,NULL,1,'2026-08-12 14:36:57'),(14,3,1,'2026-02-06',35,NULL,NULL,'Medium',6,'cramps',6,8.00,3.00,5,4,1.00,NULL,NULL,1,'2026-08-12 16:54:06'),(15,3,4,'2026-08-04',25,28.00,NULL,'Light',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-08-12 16:54:42'),(16,6,1,'2026-06-02',35,NULL,NULL,'Medium',5,'headache',8,6.00,4.00,4,4,1.00,NULL,NULL,1,'2026-08-12 17:56:00'),(17,6,2,'2026-06-09',28,35.00,NULL,'Heavy',7,'cramps',5,5.00,4.00,NULL,NULL,NULL,NULL,NULL,0,'2026-08-12 17:56:58'),(18,6,3,'2026-08-12',NULL,28.00,NULL,NULL,NULL,NULL,NULL,5.00,7.00,NULL,NULL,NULL,NULL,NULL,NULL,'2026-08-12 18:10:06');
/*!40000 ALTER TABLE `period_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postmenopause_logs`
--

DROP TABLE IF EXISTS `postmenopause_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `postmenopause_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `years_since_menopause` decimal(5,2) DEFAULT NULL,
  `hot_flashes` varchar(20) DEFAULT NULL,
  `night_sweats` varchar(20) DEFAULT NULL,
  `vaginal_dryness` varchar(20) DEFAULT NULL,
  `sleep_problems` varchar(20) DEFAULT NULL,
  `mood_changes` varchar(20) DEFAULT NULL,
  `fatigue` varchar(20) DEFAULT NULL,
  `joint_pain` varchar(20) DEFAULT NULL,
  `urinary_symptoms` varchar(20) DEFAULT NULL,
  `bone_health_concern` varchar(20) DEFAULT NULL,
  `concentration_problems` varchar(20) DEFAULT NULL,
  `reference_result` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `postmenopause_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postmenopause_logs`
--

LOCK TABLES `postmenopause_logs` WRITE;
/*!40000 ALTER TABLE `postmenopause_logs` DISABLE KEYS */;
INSERT INTO `postmenopause_logs` VALUES (1,4,58,7.00,'Yes','Yes','Yes','Yes','No','Yes','Yes','No','Yes','No','Several symptoms commonly associated with the postmenopause stage were selected.','2026-08-12 10:32:19'),(2,1,55,5.00,'No','Yes','No','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Several symptoms commonly associated with the postmenopause stage were selected.','2026-08-12 10:34:42'),(3,2,60,8.00,'No','No','No','No','No','No','No','No','No','No','At age 60, approximately 8 year(s) since menopause were reported. No postmenopause-related symptoms were selected. The current information does not show strong symptom-related reference indicators.','2026-08-12 13:02:46'),(4,2,62,10.00,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','At age 62, the reported information indicates approximately 10 year(s) since menopause. The selected symptoms are: Hot flashes, Night sweats, Vaginal dryness, Sleep problems, Mood changes, Fatigue, Joint pain, Urinary symptoms, Bone health concern, Concentration problems. Several postmenopause-related indicators are present in the information provided.','2026-08-12 13:03:41'),(5,2,62,10.00,'','','','','','','','','','','At age 62, approximately 10 year(s) since menopause were reported. No postmenopause-related symptoms were selected. The current information does not show strong symptom-related reference indicators.','2026-08-12 13:04:56');
/*!40000 ALTER TABLE `postmenopause_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pregnancy_logs`
--

DROP TABLE IF EXISTS `pregnancy_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pregnancy_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `pregnancy_status` varchar(20) DEFAULT NULL,
  `gestational_weeks` decimal(5,2) DEFAULT NULL,
  `prenatal_visits` int DEFAULT NULL,
  `blood_pressure` varchar(30) DEFAULT NULL,
  `blood_sugar` varchar(30) DEFAULT NULL,
  `nausea` varchar(20) DEFAULT NULL,
  `vomiting` varchar(20) DEFAULT NULL,
  `fatigue` varchar(20) DEFAULT NULL,
  `swelling` varchar(20) DEFAULT NULL,
  `headache` varchar(20) DEFAULT NULL,
  `abdominal_pain` varchar(20) DEFAULT NULL,
  `bleeding` varchar(20) DEFAULT NULL,
  `reference_result` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `pregnancy_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pregnancy_logs`
--

LOCK TABLES `pregnancy_logs` WRITE;
/*!40000 ALTER TABLE `pregnancy_logs` DISABLE KEYS */;
INSERT INTO `pregnancy_logs` VALUES (1,4,28,'Yes',20.00,4,'Normal','Normal','No','No','Yes','No','No','No','No','The selected information does not show strong pregnancy-related reference indicators.','2026-08-12 10:37:32'),(2,1,20,'No',0.00,0,'Normal','Normal','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information does not indicate a current pregnancy status.','2026-08-12 10:39:48'),(3,2,18,'No',0.00,0,'','','','','','','','','','The selected information does not indicate a current pregnancy status.','2026-08-12 13:27:54'),(4,2,18,'No',0.00,0,'','','Yes','Yes','Yes','Yes','No','Yes','Yes','The selected information does not indicate a current pregnancy status.','2026-08-12 13:28:15'),(5,2,35,'Yes',5.00,2,'Normal','Normal','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Bleeding was reported during pregnancy. This symptom requires appropriate medical evaluation.','2026-08-12 13:28:42'),(6,2,35,'Yes',5.00,2,'Normal','Normal','Yes','Yes','Yes','Yes','Yes','Yes','No','Abdominal pain was reported during pregnancy and may require further medical evaluation.','2026-08-12 13:28:54'),(7,2,35,'Yes',5.00,2,'Normal','Normal','Yes','Yes','Yes','Yes','Yes','No','No','Several pregnancy-related symptoms were selected for this reference profile.','2026-08-12 13:29:02'),(8,2,35,'No',5.00,2,'Normal','Normal','Yes','Yes','Yes','Yes','Yes','No','No','The selected information does not indicate a current pregnancy status.','2026-08-12 13:29:17'),(9,2,35,'Yes',20.00,3,'Normal','Normal','No','No','No','No','No','No','No','The selected information shows a current pregnancy with recorded gestational weeks and prenatal visits, without strong additional reference indicators.','2026-08-12 13:33:58'),(10,2,35,'Yes',20.00,3,'High','Normal','No','No','No','No','No','No','No','High blood pressure was selected during pregnancy. This is a pregnancy-related reference indicator that may require further medical evaluation.','2026-08-12 13:34:13'),(11,2,35,'Yes',20.00,3,'Normal','High','No','No','No','No','No','No','No','High blood sugar was selected during pregnancy. This is a health-related reference indicator that may require further evaluation.','2026-08-12 13:34:26'),(12,2,35,'Yes',20.00,3,'Normal','High','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Both abdominal pain and bleeding were reported during pregnancy. These selected indicators may require prompt medical evaluation.','2026-08-12 13:34:59'),(13,2,35,'No',20.00,3,'Normal','High','Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information indicates that the user is not currently pregnant.','2026-08-12 13:35:12'),(14,2,20,'No',0.00,0,'','','','','','','','','','The selected information indicates that the user is not currently pregnant.','2026-08-12 13:38:23'),(15,2,20,'Yes',0.00,0,'','','','','','','','','','Pregnancy was selected, but no prenatal visits were recorded in the provided information.','2026-08-12 13:38:32');
/*!40000 ALTER TABLE `pregnancy_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recommendations`
--

DROP TABLE IF EXISTS `recommendations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recommendations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `problem` varchar(100) NOT NULL,
  `practice_type` varchar(50) NOT NULL,
  `practice_name` varchar(150) NOT NULL,
  `description` text,
  `video_url` varchar(500) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recommendations`
--

LOCK TABLES `recommendations` WRITE;
/*!40000 ALTER TABLE `recommendations` DISABLE KEYS */;
INSERT INTO `recommendations` VALUES (1,'High Stress','Yoga','Gentle Relaxation Yoga','A gentle yoga routine focused on relaxation and comfortable breathing.','https://www.youtube.com/watch?v=4b68hSez-ss','2026-08-11 16:23:41'),(2,'High Stress','Mudra','Prana Mudra','A simple hand gesture practice that can be included in a calm relaxation routine.','https://www.youtube.com/watch?v=rOoTnDN6sKQ','2026-08-11 16:23:41'),(3,'Poor Sleep','Yoga','Gentle Evening Yoga','A gentle evening movement routine suitable for relaxation before sleep.','https://www.youtube.com/watch?v=FTXTOXT3Xc0','2026-08-11 16:23:41'),(4,'Poor Sleep','Relaxation','Breathing Relaxation','A simple guided breathing and relaxation practice.','https://www.youtube.com/watch?v=o4C9MyDMb2A','2026-08-11 16:23:41'),(5,'Period Discomfort','Yoga','Gentle Period Yoga','A gentle movement routine intended for relaxation and comfort during the menstrual period.','https://www.youtube.com/watch?v=tcUtVz65t2w','2026-08-11 16:23:41'),(6,'Low Energy','Yoga','Gentle Morning Yoga','A gentle movement routine that can be used as part of a morning wellness routine.','https://www.youtube.com/watch?v=GnHTeHAZQhM','2026-08-11 16:23:41'),(7,'Low Concentration','Yoga','Gentle Focus Yoga','A gentle movement and breathing routine that can be included in a focused wellness routine.','https://www.youtube.com/watch?v=xe3D7vKvtok','2026-08-11 16:34:12'),(8,'Low Concentration','Mudra','Hakini Mudra','A simple hand gesture practice that can be included in a calm concentration routine.','https://www.youtube.com/watch?v=3_TStjm4wuo','2026-08-11 16:34:12'),(9,'PCOS Lifestyle Support','Lifestyle','Build a Consistent Daily Routine','Maintain a balanced routine with regular physical activity, adequate sleep, stress management, and nutritious meals.','https://www.youtube.com/watch?v=QG4u5AzuT1E','2026-08-12 04:24:43'),(10,'PCOS Nutrition','Nutrition','Balanced Meal Planning','Focus on balanced meals containing vegetables, whole grains, protein, and nutrient-rich foods while limiting highly processed foods.','https://www.youtube.com/watch?v=cPhf2xA1dvc','2026-08-12 04:24:43'),(11,'Physical Activity','Exercise','Regular Physical Activity','Start with manageable activities such as walking, stretching, yoga, or other exercises that you can maintain consistently.','https://www.youtube.com/watch?v=5lGS5SNzvS8','2026-08-12 04:24:43'),(12,'Weight Management','Lifestyle','Healthy Lifestyle Habits','Focus on sustainable nutrition, regular movement, adequate sleep, and consistent daily habits rather than rapid weight changes.','https://www.youtube.com/watch?v=b7eyBfhVWJk','2026-08-12 04:24:43'),(13,'Hormonal Symptom Support','Wellness','Track Symptoms Regularly','Record changes in symptoms over time and discuss persistent or concerning changes with a qualified healthcare professional.','https://www.youtube.com/results?search_query=PCOS+symptoms+education','2026-08-12 04:24:43'),(14,'Skin Health','Skin Care','Gentle Skin Care Routine','Use a simple, gentle skincare routine and seek professional advice if persistent or severe skin changes occur.','https://www.youtube.com/watch?v=ukkBNw0wgBQ','2026-08-12 04:24:43'),(15,'Hair Health','Hair Care','Hair and Scalp Care','Maintain gentle hair and scalp care and seek professional advice for persistent or significant hair changes.','https://www.youtube.com/watch?v=Ap6mQe8j71M','2026-08-12 04:24:43');
/*!40000 ALTER TABLE `recommendations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thyroid_logs`
--

DROP TABLE IF EXISTS `thyroid_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thyroid_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `tsh` decimal(6,2) DEFAULT NULL,
  `t3` decimal(6,2) DEFAULT NULL,
  `t4` decimal(6,2) DEFAULT NULL,
  `fatigue` varchar(20) DEFAULT NULL,
  `weight_change` varchar(20) DEFAULT NULL,
  `cold_sensitivity` varchar(20) DEFAULT NULL,
  `heat_sensitivity` varchar(20) DEFAULT NULL,
  `hair_changes` varchar(20) DEFAULT NULL,
  `mood_changes` varchar(20) DEFAULT NULL,
  `sleep_problems` varchar(20) DEFAULT NULL,
  `thyroid_result` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `thyroid_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thyroid_logs`
--

LOCK TABLES `thyroid_logs` WRITE;
/*!40000 ALTER TABLE `thyroid_logs` DISABLE KEYS */;
INSERT INTO `thyroid_logs` VALUES (1,4,5.20,0.70,4.80,'Yes','Yes','Yes','No','Yes','Yes','Yes','Reference indicators may be consistent with thyroid-related abnormalities.','2026-08-12 08:37:39'),(2,4,2.00,3.00,4.79,'Yes','Yes','Yes','No','Yes','Yes','Yes','Some thyroid-related indicators are present and may warrant further evaluation.','2026-08-12 08:46:11'),(3,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The selected information does not show strong thyroid-related reference indicators.','2026-08-12 12:17:33'),(4,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'The selected information does not show strong thyroid-related reference indicators.','2026-08-12 12:20:37'),(5,1,2.50,1.00,8.00,'Yes','Yes','Yes','Yes','Yes','Yes','Yes','The selected information does not show strong thyroid-related reference indicators.','2026-08-12 12:21:04'),(6,1,2.50,8.00,20.00,'Yes','Yes','No','No','Yes','Yes','Yes','The selected information does not show strong thyroid-related reference indicators.','2026-08-12 12:21:32'),(7,1,2.50,8.00,20.00,'Yes','Yes','Yes','No','Yes','No','Yes','The selected information does not show strong thyroid-related reference indicators.','2026-08-12 12:23:30'),(8,1,NULL,NULL,NULL,'Yes','Yes','No','No','Yes','No','Yes','Several thyroid-related symptoms were selected: Fatigue, Weight Change, Hair Changes, Sleep Problems. These recorded factors may warrant further evaluation if they persist.','2026-08-12 12:30:25'),(9,1,5.00,6.00,9.00,'Yes','Yes','Yes','No','Yes','No','Yes','Your current information contains one thyroid-related laboratory reference indicator and several selected symptoms. The symptoms selected include: Fatigue, Weight Change, Cold Sensitivity, Hair Changes, Sleep Problems. These recorded factors may warrant further evaluation.','2026-08-12 12:30:45'),(10,3,2.00,1.00,8.00,'Yes','Yes','Yes','No','Yes','Yes','Yes','You selected several thyroid-related symptoms: Fatigue, Weight Change, Cold Sensitivity, Hair Changes, Mood Changes, Sleep Problems. These recorded factors may warrant further evaluation, especially if the symptoms are persistent or worsening.','2026-08-12 16:49:59');
/*!40000 ALTER TABLE `thyroid_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ABC','abc@gmail.com','$2b$12$MjJ2AHQEZivnejF5WVkNOOeoCzOh1KhZBlP8aUVvYKWeNJvAGcmj6','2026-08-11 14:21:13'),(2,'Radhika','radhika@gmail.com','$2b$12$Ubg1YPvHHqK04B7P0haC2eh5fM8yqogdSpmVK0js/WJ93vaS.SzoS','2026-08-11 16:38:50'),(3,'Chaitra','chaitra@gmail.com','$2b$12$rpqhTKUX.0MiBQ798FBqgO.jIDnX85o8VMj0mQSdFR4eaaVw3q4LW','2026-08-11 16:48:04'),(4,'abcd','abcd@gmail.com','$2b$12$u5tpSFi6ZmVdArxMvyMIqupcmm3nW91NXMK8srcVfDnEcerWHznBO','2026-08-12 08:09:48'),(5,'testuser','testuser@gmail.com','$2b$12$MN5.oq4Pyjg8CQDNO5d/UOx0gpnEuYFJwM1SqIb4esX82YLWlbnJu','2026-08-12 11:02:53'),(6,'asdf','asdf@gmail.com','$2b$12$kXOkVwDTTBUr9j3N.iP.qemXWk9bY/NaWfuo/VZ8SB9GgLhWJ1iWi','2026-08-12 17:54:59');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-13  0:30:22
