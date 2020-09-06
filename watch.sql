-- MySQL dump 10.17  Distrib 10.3.22-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: killian_abstrackr
-- ------------------------------------------------------
-- Server version	10.3.22-MariaDB

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
-- Table structure for table `ResetPassword`
--

DROP TABLE IF EXISTS `ResetPassword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ResetPassword` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_email` varchar(80) DEFAULT NULL,
  `token` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ResetPassword`
--

LOCK TABLES `ResetPassword` WRITE;
/*!40000 ALTER TABLE `ResetPassword` DISABLE KEYS */;
/*!40000 ALTER TABLE `ResetPassword` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignments`
--

DROP TABLE IF EXISTS `assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assignments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `task_id` int(11) DEFAULT NULL,
  `done_so_far` int(11) DEFAULT NULL,
  `date_assigned` datetime DEFAULT NULL,
  `date_due` datetime DEFAULT NULL,
  `done` tinyint(1) DEFAULT NULL,
  `num_assigned` int(11) DEFAULT NULL,
  `assignment_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `user_id` (`user_id`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `assignments_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `assignments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `assignments_ibfk_3` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`done` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignments`
--

LOCK TABLES `assignments` WRITE;
/*!40000 ALTER TABLE `assignments` DISABLE KEYS */;
INSERT INTO `assignments` VALUES (4,2,2,4,22,'2020-09-05 21:45:15',NULL,0,-1,'perpetual');
/*!40000 ALTER TABLE `assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citations`
--

DROP TABLE IF EXISTS `citations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `pmid` varchar(20) DEFAULT NULL,
  `refman` varchar(20) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `abstract` varchar(10000) DEFAULT NULL,
  `authors` varchar(5000) DEFAULT NULL,
  `journal` varchar(1000) DEFAULT NULL,
  `publication_date` datetime DEFAULT NULL,
  `keywords` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `citations_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=455 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citations`
--

LOCK TABLES `citations` WRITE;
/*!40000 ALTER TABLE `citations` DISABLE KEYS */;
INSERT INTO `citations` VALUES (453,2,'31727159','31727159','Assessing the accuracy of machine-assisted abstract screening with DistillerAI: a user study.','BACKGROUND: Web applications that employ natural language processing technologies to support systematic reviewers during abstract screening have become more common. The goal of our project was to conduct a case study to explore a screening approach that temporarily replaces a human screener with a semi-automated screening tool. METHODS: We evaluated the accuracy of the approach using DistillerAI as a semi-automated screening tool. A published comparative effectiveness review served as the reference standard. Five teams of professional systematic reviewers screened the same 2472 abstracts in parallel. Each team trained DistillerAI with 300 randomly selected abstracts that the team screened dually. For all remaining abstracts, DistillerAI replaced one human screener and provided predictions about the relevance of records. A single reviewer also screened all remaining abstracts. A second human screener resolved conflicts between the single reviewer and DistillerAI. We compared the decisions of the machine-assisted approach, single-reviewer screening, and screening with DistillerAI alone against the reference standard. RESULTS: The combined sensitivity of the machine-assisted screening approach across the five screening teams was 78% (95% confidence interval [CI], 66 to 90%), and the combined specificity was 95% (95% CI, 92 to 97%). By comparison, the sensitivity of single-reviewer screening was similar (78%; 95% CI, 66 to 89%); however, the sensitivity of DistillerAI alone was substantially worse (14%; 95% CI, 0 to 31%) than that of the machine-assisted screening approach. Specificities for single-reviewer screening and DistillerAI were 94% (95% CI, 91 to 97%) and 98% (95% CI, 97 to 100%), respectively. Machine-assisted screening and single-reviewer screening had similar areas under the curve (0.87 and 0.86, respectively); by contrast, the area under the curve for DistillerAI alone was just slightly better than chance (0.56). The interrater agreement between human screeners and DistillerAI with a prevalence-adjusted kappa was 0.85 (95% CI, 0.84 to 0.86%). CONCLUSIONS: The accuracy of DistillerAI is not yet adequate to replace a human screener temporarily during abstract screening for systematic reviews. Rapid reviews, which do not require detecting the totality of the relevant evidence, may find semi-automation tools to have greater utility than traditional systematic reviews.','Gartlehner G and Wagner G and Lux L and Affengruber L and Dobrescu A and Kaminski-Hartenthaler A and Viswanathan M','Systematic reviews',NULL,'Abstracting and Indexing/classification,Humans,Information Storage and Retrieval/*methods,Internet,*Natural Language Processing,Reproducibility of Results,Sensitivity and Specificity,*Software,Systematic Reviews as Topic'),(454,2,'29714037','29714037','Effectiveness of nonpharmacological interventions to reduce procedural anxiety in children and adolescents undergoing treatment for cancer: A systematic review and meta-analysis.','OBJECTIVE: Children and young people (CYP) with cancer undergo painful and distressing procedures. We aimed to systematically review the effectiveness of nonpharmacological interventions to reduce procedural anxiety in CYP. METHODS: Extensive literature searches sought randomised controlled trials that quantified the effect of any nonpharmacological intervention for procedural anxiety in CYP with cancer aged 0 to 25. Study selection involved independent title and abstract screening and full text screening by two reviewers. Anxiety, distress, fear, and pain outcomes were extracted from included studies. Where similar intervention, comparator, and outcomes presented, meta-analysis was performed, producing pooled effect sizes (Cohen\'s d) and 95% confidence intervals (95% CI). All other data were narratively described. Quality and risk of bias appraisal was performed, based on the Cochrane risk of bias tool. RESULTS: Screening of 11 727 records yielded 56 relevant full texts. There were 15 included studies, eight trialling hypnosis, and seven nonhypnosis interventions. There were large, statistically significant reductions in anxiety and pain for hypnosis, particularly compared with treatment as usual (anxiety: d = 2.30; 95% CI, 1.30-3.30; P < .001; pain: d = 2.16; 95% CI, 1.41-2.92; P < .001). Evidence from nonhypnosis interventions was equivocal, with some promising individual studies. There was high risk of bias across included studies limiting confidence in some positive effects. CONCLUSIONS: Evidence suggests promise for hypnosis interventions to reduce procedural anxiety in CYP undergoing cancer treatment. These results largely emerge from one research group, therefore wider research is required. Promising evidence for individual nonhypnosis interventions must be evaluated through rigorously conducted randomised controlled trials.','Nunns M and Mayhew D and Ford T and Rogers M and Curle C and Logan S and Moore D','Psycho-oncology',NULL,'Adolescent,Anxiety/*therapy,Child,Humans,*Hypnosis,Neoplasms/*therapy,*Outcome Assessment, Health Care,Pain, Procedural/*psychology,*Psychotherapy');
/*!40000 ALTER TABLE `citations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citations_tasks`
--

DROP TABLE IF EXISTS `citations_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `citations_tasks` (
  `citation_id` int(11) DEFAULT NULL,
  `task_id` int(11) DEFAULT NULL,
  KEY `citation_id` (`citation_id`),
  KEY `task_id` (`task_id`),
  CONSTRAINT `citations_tasks_ibfk_1` FOREIGN KEY (`citation_id`) REFERENCES `citations` (`id`),
  CONSTRAINT `citations_tasks_ibfk_2` FOREIGN KEY (`task_id`) REFERENCES `tasks` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citations_tasks`
--

LOCK TABLES `citations_tasks` WRITE;
/*!40000 ALTER TABLE `citations_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `citations_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `encodedstatuses`
--

DROP TABLE IF EXISTS `encodedstatuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `encodedstatuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `is_encoded` tinyint(1) DEFAULT NULL,
  `labels_last_updated` datetime DEFAULT NULL,
  `base_path` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`is_encoded` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `encodedstatuses`
--

LOCK TABLES `encodedstatuses` WRITE;
/*!40000 ALTER TABLE `encodedstatuses` DISABLE KEYS */;
INSERT INTO `encodedstatuses` VALUES (2,2,0,NULL,NULL);
/*!40000 ALTER TABLE `encodedstatuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_permission`
--

DROP TABLE IF EXISTS `group_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_permission`
--

LOCK TABLES `group_permission` WRITE;
/*!40000 ALTER TABLE `group_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `group_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labeledfeatures`
--

DROP TABLE IF EXISTS `labeledfeatures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labeledfeatures` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `term` varchar(500) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `label` smallint(6) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labeledfeatures`
--

LOCK TABLES `labeledfeatures` WRITE;
/*!40000 ALTER TABLE `labeledfeatures` DISABLE KEYS */;
INSERT INTO `labeledfeatures` VALUES (3,'screening',2,2,1,'2020-09-05 22:32:19'),(4,'abstract',2,2,2,'2020-09-05 22:32:34'),(5,'clinical',2,2,-1,'2020-09-05 22:32:43'),(6,'work',2,2,-2,'2020-09-05 22:32:53');
/*!40000 ALTER TABLE `labeledfeatures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `labels`
--

DROP TABLE IF EXISTS `labels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `study_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `assignment_id` int(11) DEFAULT NULL,
  `label` smallint(6) DEFAULT NULL,
  `labeling_time` int(11) DEFAULT NULL,
  `first_labeled` datetime DEFAULT NULL,
  `label_last_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `study_id` (`study_id`),
  CONSTRAINT `labels_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `labels_ibfk_2` FOREIGN KEY (`study_id`) REFERENCES `citations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `labels`
--

LOCK TABLES `labels` WRITE;
/*!40000 ALTER TABLE `labels` DISABLE KEYS */;
INSERT INTO `labels` VALUES (6,2,16,2,4,1,1,'2020-09-05 22:28:15','2020-09-05 22:28:15'),(7,2,17,2,4,1,1,'2020-09-05 22:28:18','2020-09-05 22:28:18'),(8,2,18,2,4,1,1,'2020-09-05 22:28:20','2020-09-05 22:28:20'),(9,2,19,2,4,1,1,'2020-09-05 22:28:22','2020-09-05 22:28:22'),(10,2,20,2,4,1,1,'2020-09-05 22:28:26','2020-09-05 22:28:26'),(11,2,21,2,4,1,1,'2020-09-05 22:28:27','2020-09-05 22:28:27'),(12,2,22,2,4,1,1,'2020-09-05 22:28:29','2020-09-05 22:28:29'),(13,2,23,2,4,1,1,'2020-09-05 22:28:32','2020-09-05 22:28:32'),(14,2,24,2,4,-1,1,'2020-09-05 22:28:33','2020-09-05 22:28:33'),(15,2,25,2,4,1,1,'2020-09-05 22:28:35','2020-09-05 22:28:35'),(16,2,26,2,4,1,1,'2020-09-05 22:28:37','2020-09-05 22:28:37'),(17,2,27,2,4,1,1,'2020-09-05 22:28:39','2020-09-05 22:28:39'),(18,2,28,2,4,1,1,'2020-09-05 22:28:41','2020-09-05 22:28:41'),(19,2,29,2,4,-1,1,'2020-09-05 22:28:44','2020-09-05 22:28:44'),(20,2,30,2,4,1,1,'2020-09-05 22:28:47','2020-09-05 22:28:47'),(21,2,31,2,4,0,1,'2020-09-05 22:28:50','2020-09-05 22:28:50'),(22,2,32,2,4,0,1,'2020-09-05 22:28:53','2020-09-05 22:28:53'),(23,2,33,2,4,1,1,'2020-09-05 22:28:57','2020-09-05 22:28:57'),(24,2,34,2,4,1,1,'2020-09-05 22:28:59','2020-09-05 22:28:59'),(25,2,35,2,4,1,1,'2020-09-05 22:29:02','2020-09-05 22:29:02'),(26,2,36,2,4,1,1,'2020-09-05 22:32:47','2020-09-05 22:32:47'),(27,2,37,2,4,-1,1,'2020-09-05 22:33:00','2020-09-05 22:33:00');
/*!40000 ALTER TABLE `labels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator_id` int(11) DEFAULT NULL,
  `citation_id` int(11) DEFAULT NULL,
  `general` varchar(1000) DEFAULT NULL,
  `population` varchar(1000) DEFAULT NULL,
  `ic` varchar(1000) DEFAULT NULL,
  `outcome` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predictions`
--

DROP TABLE IF EXISTS `predictions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `predictions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `study_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `prediction` tinyint(1) DEFAULT NULL,
  `num_yes_votes` float DEFAULT NULL,
  `predicted_probability` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`prediction` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=837 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predictions`
--

LOCK TABLES `predictions` WRITE;
/*!40000 ALTER TABLE `predictions` DISABLE KEYS */;
INSERT INTO `predictions` VALUES (420,38,2,1,11,0.74644),(421,39,2,1,11,0.754196),(422,40,2,1,11,0.888136),(423,41,2,1,11,0.911285),(424,42,2,1,11,0.88957),(425,43,2,1,11,0.91114),(426,44,2,1,11,0.879157),(427,45,2,1,11,0.755098),(428,46,2,1,11,0.783396),(429,47,2,1,11,0.799499),(430,48,2,1,11,0.890108),(431,49,2,1,11,0.517383),(432,50,2,1,11,0.870954),(433,51,2,1,11,0.902487),(434,52,2,1,11,0.857383),(435,53,2,1,11,0.863331),(436,54,2,1,11,0.788387),(437,55,2,1,11,0.901354),(438,56,2,1,11,0.838929),(439,57,2,1,11,0.877312),(440,58,2,1,11,0.836004),(441,59,2,1,11,0.81443),(442,60,2,1,11,0.902319),(443,61,2,1,11,0.87684),(444,62,2,1,11,0.732309),(445,63,2,1,11,0.911716),(446,64,2,1,11,0.836726),(447,65,2,1,11,0.90136),(448,66,2,1,11,0.883085),(449,67,2,1,11,0.891711),(450,68,2,1,11,0.865979),(451,69,2,1,11,0.894325),(452,70,2,1,11,0.892764),(453,71,2,1,11,0.800958),(454,72,2,1,11,0.879044),(455,73,2,1,11,0.844943),(456,74,2,1,11,0.837045),(457,75,2,1,11,0.748038),(458,76,2,1,11,0.893107),(459,77,2,1,11,0.827495),(460,78,2,1,11,0.824582),(461,79,2,1,11,0.829148),(462,80,2,1,11,0.794264),(463,81,2,1,11,0.863955),(464,82,2,1,11,0.888949),(465,83,2,1,11,0.811911),(466,84,2,1,11,0.912337),(467,85,2,1,11,0.891874),(468,86,2,1,11,0.832522),(469,87,2,1,11,0.900296),(470,88,2,1,11,0.88176),(471,89,2,1,11,0.781942),(472,90,2,1,11,0.854618),(473,91,2,1,11,0.685889),(474,92,2,1,11,0.883743),(475,93,2,1,11,0.88943),(476,94,2,1,11,0.880751),(477,95,2,1,11,0.748511),(478,96,2,0,0,0.526121),(479,97,2,1,11,0.753578),(480,98,2,1,11,0.899952),(481,99,2,1,11,0.880572),(482,100,2,1,11,0.864444),(483,101,2,1,11,0.831627),(484,102,2,1,11,0.831878),(485,103,2,1,11,0.900101),(486,104,2,1,11,0.873058),(487,105,2,1,11,0.885304),(488,106,2,1,11,0.792677),(489,107,2,1,11,0.86735),(490,108,2,1,11,0.862155),(491,109,2,1,11,0.885636),(492,110,2,1,11,0.863392),(493,111,2,1,11,0.816039),(494,112,2,1,11,0.915721),(495,113,2,1,11,0.887066),(496,114,2,1,11,0.869667),(497,115,2,1,11,0.893573),(498,116,2,1,11,0.761632),(499,117,2,1,11,0.884533),(500,118,2,1,11,0.731044),(501,119,2,1,11,0.888112),(502,120,2,1,11,0.783657),(503,121,2,1,11,0.903237),(504,122,2,1,11,0.909741),(505,123,2,1,11,0.890514),(506,124,2,1,11,0.848288),(507,125,2,1,11,0.792236),(508,126,2,1,11,0.901224),(509,127,2,1,11,0.911194),(510,128,2,1,11,0.908282),(511,129,2,1,11,0.886194),(512,130,2,1,11,0.882085),(513,131,2,1,11,0.643643),(514,132,2,1,11,0.883451),(515,133,2,1,11,0.878245),(516,134,2,1,11,0.842973),(517,135,2,1,11,0.880303),(518,136,2,1,11,0.804487),(519,137,2,1,11,0.882898),(520,138,2,1,11,0.849557),(521,139,2,1,11,0.890663),(522,140,2,1,11,0.874681),(523,141,2,1,11,0.873598),(524,142,2,1,11,0.883305),(525,143,2,1,11,0.916622),(526,144,2,1,11,0.897847),(527,145,2,1,11,0.820229),(528,146,2,1,11,0.797448),(529,147,2,1,11,0.886669),(530,148,2,1,11,0.689384),(531,149,2,1,11,0.855687),(532,150,2,1,11,0.892877),(533,151,2,1,11,0.893793),(534,152,2,1,11,0.89468),(535,153,2,1,11,0.883717),(536,154,2,1,11,0.88774),(537,155,2,1,11,0.868081),(538,156,2,1,11,0.896536),(539,157,2,1,11,0.888779),(540,158,2,1,11,0.864856),(541,159,2,1,11,0.888998),(542,160,2,1,11,0.904672),(543,161,2,1,11,0.880253),(544,162,2,1,11,0.891712),(545,163,2,1,11,0.833957),(546,164,2,1,11,0.755302),(547,165,2,1,11,0.893597),(548,166,2,1,11,0.873109),(549,167,2,1,11,0.714748),(550,168,2,1,11,0.877739),(551,169,2,1,11,0.852722),(552,170,2,1,11,0.887247),(553,171,2,1,11,0.655128),(554,172,2,1,11,0.870588),(555,173,2,1,11,0.711082),(556,174,2,1,11,0.836933),(557,175,2,1,11,0.542387),(558,176,2,1,11,0.906004),(559,177,2,1,11,0.758848),(560,178,2,1,11,0.91161),(561,179,2,1,11,0.893312),(562,180,2,1,11,0.898405),(563,181,2,1,11,0.80135),(564,182,2,1,11,0.90713),(565,183,2,1,11,0.840966),(566,184,2,1,11,0.674602),(567,185,2,1,11,0.925241),(568,186,2,1,11,0.82801),(569,187,2,1,11,0.906376),(570,188,2,1,11,0.904033),(571,189,2,1,11,0.836928),(572,190,2,1,11,0.87858),(573,191,2,1,11,0.876394),(574,192,2,1,11,0.821423),(575,193,2,1,11,0.792867),(576,194,2,1,11,0.798474),(577,195,2,1,11,0.873417),(578,196,2,1,11,0.915085),(579,197,2,1,11,0.831428),(580,198,2,1,11,0.882152),(581,199,2,1,11,0.76917),(582,200,2,1,11,0.862724),(583,201,2,1,11,0.869125),(584,202,2,1,11,0.797986),(585,203,2,1,11,0.841619),(586,204,2,1,11,0.897917),(587,205,2,1,11,0.824598),(588,206,2,1,11,0.889938),(589,207,2,1,11,0.888665),(590,208,2,1,11,0.815155),(591,209,2,1,11,0.895024),(592,210,2,1,11,0.876318),(593,211,2,1,11,0.878887),(594,212,2,1,11,0.853542),(595,213,2,1,11,0.880853),(596,214,2,1,11,0.905579),(597,215,2,1,11,0.856669),(598,216,2,1,11,0.884279),(599,217,2,1,11,0.866147),(600,218,2,1,11,0.868827),(601,219,2,1,11,0.704579),(602,220,2,1,11,0.894702),(603,221,2,1,11,0.824931),(604,222,2,1,11,0.904889),(605,223,2,1,11,0.886716),(606,224,2,1,11,0.88515),(607,225,2,1,11,0.878965),(608,226,2,1,11,0.877852),(609,227,2,1,11,0.897588),(610,228,2,1,11,0.772661),(611,229,2,1,11,0.783141),(612,230,2,1,11,0.895914),(613,231,2,1,11,0.754993),(614,232,2,1,11,0.878407),(615,233,2,1,11,0.789533),(616,234,2,1,11,0.88835),(617,235,2,1,11,0.86087),(618,236,2,1,11,0.915551),(619,237,2,1,11,0.894724),(620,238,2,1,11,0.840537),(621,239,2,1,11,0.887968),(622,240,2,1,11,0.825665),(623,241,2,1,11,0.865247),(624,242,2,1,11,0.624278),(625,243,2,1,11,0.857986),(626,244,2,1,11,0.856419),(627,245,2,1,11,0.890956),(628,246,2,1,11,0.847029),(629,247,2,1,11,0.821491),(630,248,2,1,11,0.862879),(631,249,2,1,11,0.905458),(632,250,2,1,11,0.891064),(633,251,2,1,11,0.906663),(634,252,2,1,11,0.881509),(635,253,2,1,11,0.905558),(636,254,2,1,11,0.896085),(637,255,2,1,11,0.86951),(638,256,2,1,11,0.746257),(639,257,2,1,11,0.86249),(640,258,2,1,11,0.898355),(641,259,2,1,11,0.790865),(642,260,2,1,11,0.890624),(643,261,2,1,11,0.881562),(644,262,2,1,11,0.895862),(645,263,2,1,11,0.849964),(646,264,2,1,11,0.89832),(647,265,2,1,11,0.884215),(648,266,2,1,11,0.655959),(649,267,2,1,11,0.898275),(650,268,2,1,11,0.877965),(651,269,2,1,11,0.844827),(652,270,2,1,11,0.860475),(653,271,2,1,11,0.90148),(654,272,2,1,11,0.866916),(655,273,2,1,11,0.827176),(656,274,2,1,11,0.901687),(657,275,2,1,11,0.876728),(658,276,2,1,11,0.835164),(659,277,2,1,11,0.891695),(660,278,2,1,11,0.884223),(661,279,2,1,11,0.884008),(662,280,2,1,11,0.858892),(663,281,2,1,11,0.88731),(664,282,2,1,11,0.903484),(665,283,2,1,11,0.73278),(666,284,2,1,11,0.847531),(667,285,2,1,11,0.878466),(668,286,2,1,11,0.881975),(669,287,2,1,11,0.864482),(670,288,2,1,11,0.806037),(671,289,2,1,11,0.895417),(672,290,2,1,11,0.883479),(673,291,2,1,11,0.877655),(674,292,2,1,11,0.899558),(675,293,2,1,11,0.889651),(676,294,2,1,11,0.887016),(677,295,2,1,11,0.909404),(678,296,2,1,11,0.869525),(679,297,2,1,11,0.704961),(680,298,2,1,11,0.87637),(681,299,2,1,11,0.911782),(682,300,2,1,11,0.80598),(683,301,2,1,11,0.775854),(684,302,2,1,11,0.825042),(685,303,2,1,11,0.835626),(686,304,2,1,11,0.75879),(687,305,2,1,11,0.897655),(688,306,2,1,11,0.628115),(689,307,2,1,11,0.827199),(690,308,2,1,11,0.882548),(691,309,2,1,11,0.885216),(692,310,2,1,11,0.770265),(693,311,2,1,11,0.878062),(694,312,2,1,11,0.900468),(695,313,2,1,11,0.891553),(696,314,2,1,11,0.886936),(697,315,2,1,11,0.717493),(698,316,2,1,11,0.911597),(699,317,2,1,11,0.739078),(700,318,2,1,11,0.854681),(701,319,2,1,11,0.85078),(702,320,2,1,11,0.886699),(703,321,2,1,11,0.794007),(704,322,2,1,11,0.906213),(705,323,2,1,11,0.8914),(706,324,2,1,11,0.870059),(707,325,2,1,11,0.871564),(708,326,2,1,11,0.900182),(709,327,2,1,11,0.87125),(710,328,2,1,11,0.822878),(711,329,2,1,11,0.878941),(712,330,2,1,11,0.859099),(713,331,2,1,11,0.836423),(714,332,2,1,11,0.901428),(715,333,2,1,11,0.899395),(716,334,2,1,11,0.883608),(717,335,2,1,11,0.887724),(718,336,2,1,11,0.801381),(719,337,2,1,11,0.885684),(720,338,2,1,11,0.756947),(721,339,2,1,11,0.904206),(722,340,2,1,11,0.881944),(723,341,2,1,11,0.815898),(724,342,2,1,11,0.881576),(725,343,2,1,11,0.882149),(726,344,2,1,11,0.907928),(727,345,2,1,11,0.914934),(728,346,2,1,11,0.870798),(729,347,2,1,11,0.872719),(730,348,2,1,11,0.861418),(731,349,2,1,11,0.813394),(732,350,2,1,11,0.721617),(733,351,2,1,11,0.874352),(734,352,2,1,11,0.896125),(735,353,2,1,11,0.874214),(736,354,2,1,11,0.912153),(737,355,2,1,11,0.884039),(738,356,2,1,11,0.875883),(739,357,2,1,11,0.870223),(740,358,2,1,11,0.816888),(741,359,2,1,11,0.883992),(742,360,2,1,11,0.855551),(743,361,2,1,11,0.878877),(744,362,2,1,11,0.798696),(745,363,2,1,11,0.869886),(746,364,2,1,11,0.894796),(747,365,2,1,11,0.881093),(748,366,2,1,11,0.854714),(749,367,2,1,11,0.885754),(750,368,2,1,11,0.860748),(751,369,2,1,11,0.837487),(752,370,2,1,11,0.830665),(753,371,2,1,11,0.859242),(754,372,2,1,11,0.885956),(755,373,2,1,11,0.734515),(756,374,2,1,11,0.849243),(757,375,2,1,11,0.865247),(758,376,2,1,11,0.876554),(759,377,2,1,11,0.900366),(760,378,2,1,11,0.87367),(761,379,2,1,11,0.892948),(762,380,2,1,11,0.8834),(763,381,2,1,11,0.904513),(764,382,2,1,11,0.889962),(765,383,2,1,11,0.759305),(766,384,2,1,11,0.85092),(767,385,2,1,11,0.780013),(768,386,2,1,11,0.883257),(769,387,2,1,11,0.886519),(770,388,2,1,11,0.875295),(771,389,2,1,11,0.827594),(772,390,2,1,11,0.874082),(773,391,2,1,11,0.899618),(774,392,2,1,11,0.820918),(775,393,2,1,11,0.681432),(776,394,2,1,11,0.88789),(777,395,2,1,11,0.874717),(778,396,2,1,11,0.866387),(779,397,2,1,11,0.633195),(780,398,2,1,11,0.806139),(781,399,2,1,11,0.889808),(782,400,2,1,11,0.865706),(783,401,2,1,11,0.906259),(784,402,2,1,11,0.831297),(785,403,2,0,0,0.445966),(786,404,2,1,11,0.886039),(787,405,2,1,11,0.762923),(788,406,2,1,11,0.868186),(789,407,2,1,11,0.895235),(790,408,2,1,11,0.885284),(791,409,2,1,11,0.903055),(792,410,2,1,11,0.910043),(793,411,2,1,11,0.925429),(794,412,2,1,11,0.900543),(795,413,2,1,11,0.75651),(796,414,2,0,4,0.482488),(797,415,2,1,11,0.895401),(798,416,2,1,11,0.904399),(799,417,2,1,11,0.867738),(800,418,2,1,11,0.898055),(801,419,2,1,11,0.894038),(802,420,2,1,11,0.667881),(803,421,2,1,11,0.900119),(804,422,2,1,11,0.881781),(805,423,2,1,11,0.859212),(806,424,2,1,11,0.774083),(807,425,2,1,11,0.880021),(808,426,2,1,11,0.900547),(809,427,2,1,11,0.893823),(810,428,2,1,11,0.891749),(811,429,2,1,11,0.894524),(812,430,2,1,11,0.768454),(813,431,2,0,4,0.484054),(814,432,2,1,11,0.90755),(815,433,2,1,11,0.890878),(816,434,2,1,11,0.598756),(817,435,2,1,11,0.836501),(818,436,2,1,11,0.853506),(819,437,2,1,11,0.800863),(820,438,2,1,11,0.750908),(821,439,2,1,11,0.901219),(822,440,2,1,11,0.886177),(823,441,2,1,11,0.883956),(824,442,2,1,11,0.895983),(825,443,2,1,11,0.881192),(826,444,2,1,11,0.929171),(827,445,2,1,11,0.881523),(828,446,2,1,11,0.865034),(829,447,2,1,11,0.840336),(830,448,2,1,11,0.891291),(831,449,2,1,11,0.880397),(832,450,2,1,11,0.903484),(833,451,2,1,11,0.886409),(834,452,2,1,11,0.897785),(835,453,2,1,11,0.897625),(836,454,2,1,11,0.840281);
/*!40000 ALTER TABLE `predictions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `predictionstatuses`
--

DROP TABLE IF EXISTS `predictionstatuses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `predictionstatuses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `predictions_exist` tinyint(1) DEFAULT NULL,
  `predictions_last_made` datetime DEFAULT NULL,
  `train_set_size` int(11) DEFAULT NULL,
  `num_pos_train` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`predictions_exist` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `predictionstatuses`
--

LOCK TABLES `predictionstatuses` WRITE;
/*!40000 ALTER TABLE `predictionstatuses` DISABLE KEYS */;
INSERT INTO `predictionstatuses` VALUES (4,2,1,'2020-09-05 22:33:50',22,413);
/*!40000 ALTER TABLE `predictionstatuses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priorities`
--

DROP TABLE IF EXISTS `priorities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `priorities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `citation_id` int(11) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `num_times_labeled` int(11) DEFAULT NULL,
  `is_out` tinyint(1) DEFAULT NULL,
  `locked_by` int(11) DEFAULT NULL,
  `time_requested` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `citation_id` (`citation_id`),
  CONSTRAINT `priorities_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`),
  CONSTRAINT `priorities_ibfk_2` FOREIGN KEY (`citation_id`) REFERENCES `citations` (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`is_out` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=455 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priorities`
--

LOCK TABLES `priorities` WRITE;
/*!40000 ALTER TABLE `priorities` DISABLE KEYS */;
INSERT INTO `priorities` VALUES (16,2,16,0,1,0,NULL,'2020-09-05 22:27:47'),(17,2,17,1,1,0,NULL,'2020-09-05 22:27:48'),(18,2,18,2,1,0,NULL,'2020-09-05 22:28:15'),(19,2,19,3,1,0,NULL,'2020-09-05 22:28:18'),(20,2,20,4,1,0,NULL,'2020-09-05 22:28:20'),(21,2,21,5,1,0,NULL,'2020-09-05 22:28:22'),(22,2,22,6,1,0,NULL,'2020-09-05 22:28:26'),(23,2,23,7,1,0,NULL,'2020-09-05 22:28:27'),(24,2,24,8,1,0,NULL,'2020-09-05 22:28:29'),(25,2,25,9,1,0,NULL,'2020-09-05 22:28:32'),(26,2,26,10,1,0,NULL,'2020-09-05 22:28:33'),(27,2,27,11,1,0,NULL,'2020-09-05 22:28:35'),(28,2,28,12,1,0,NULL,'2020-09-05 22:28:37'),(29,2,29,13,1,0,NULL,'2020-09-05 22:28:39'),(30,2,30,14,1,0,NULL,'2020-09-05 22:28:41'),(31,2,31,15,1,0,NULL,'2020-09-05 22:28:44'),(32,2,32,16,1,0,NULL,'2020-09-05 22:28:47'),(33,2,33,17,1,0,NULL,'2020-09-05 22:28:50'),(34,2,34,18,1,0,NULL,'2020-09-05 22:28:53'),(35,2,35,19,1,0,NULL,'2020-09-05 22:28:57'),(36,2,36,20,1,0,NULL,'2020-09-05 22:28:59'),(37,2,37,21,1,0,NULL,'2020-09-05 22:29:02'),(38,2,38,408,0,0,NULL,NULL),(39,2,39,403,0,0,NULL,NULL),(40,2,40,148,0,0,NULL,NULL),(41,2,41,36,0,0,NULL,NULL),(42,2,42,141,0,0,NULL,NULL),(43,2,43,38,0,0,NULL,NULL),(44,2,44,214,0,0,NULL,NULL),(45,2,45,401,0,0,NULL,NULL),(46,2,46,383,0,0,NULL,NULL),(47,2,47,369,0,0,NULL,NULL),(48,2,48,136,0,0,NULL,NULL),(49,2,49,435,0,0,NULL,NULL),(50,2,50,251,0,0,NULL,NULL),(51,2,51,64,0,0,NULL,NULL),(52,2,52,293,0,0,NULL,NULL),(53,2,53,279,0,0,NULL,NULL),(54,2,54,381,0,0,NULL,NULL),(55,2,55,70,0,0,NULL,NULL),(56,2,56,320,0,0,NULL,NULL),(57,2,57,229,0,0,NULL,NULL),(58,2,58,328,0,0,NULL,NULL),(59,2,59,358,0,0,NULL,NULL),(60,2,60,65,0,0,NULL,NULL),(61,2,61,230,0,0,NULL,NULL),(62,2,62,413,0,0,NULL,NULL),(63,2,63,33,0,0,NULL,NULL),(64,2,64,325,0,0,NULL,NULL),(65,2,65,69,0,0,NULL,NULL),(66,2,66,191,0,0,NULL,NULL),(67,2,67,125,0,0,NULL,NULL),(68,2,68,269,0,0,NULL,NULL),(69,2,69,111,0,0,NULL,NULL),(70,2,70,121,0,0,NULL,NULL),(71,2,71,367,0,0,NULL,NULL),(72,2,72,215,0,0,NULL,NULL),(73,2,73,312,0,0,NULL,NULL),(74,2,74,322,0,0,NULL,NULL),(75,2,75,407,0,0,NULL,NULL),(76,2,76,118,0,0,NULL,NULL),(77,2,77,341,0,0,NULL,NULL),(78,2,78,348,0,0,NULL,NULL),(79,2,79,338,0,0,NULL,NULL),(80,2,80,374,0,0,NULL,NULL),(81,2,81,277,0,0,NULL,NULL),(82,2,82,144,0,0,NULL,NULL),(83,2,83,360,0,0,NULL,NULL),(84,2,84,30,0,0,NULL,NULL),(85,2,85,122,0,0,NULL,NULL),(86,2,86,332,0,0,NULL,NULL),(87,2,87,77,0,0,NULL,NULL),(88,2,88,200,0,0,NULL,NULL),(89,2,89,385,0,0,NULL,NULL),(90,2,90,300,0,0,NULL,NULL),(91,2,91,422,0,0,NULL,NULL),(92,2,92,183,0,0,NULL,NULL),(93,2,93,142,0,0,NULL,NULL),(94,2,94,208,0,0,NULL,NULL),(95,2,95,406,0,0,NULL,NULL),(96,2,96,434,0,0,NULL,NULL),(97,2,97,404,0,0,NULL,NULL),(98,2,98,81,0,0,NULL,NULL),(99,2,99,209,0,0,NULL,NULL),(100,2,100,276,0,0,NULL,NULL),(101,2,101,334,0,0,NULL,NULL),(102,2,102,333,0,0,NULL,NULL),(103,2,103,80,0,0,NULL,NULL),(104,2,104,247,0,0,NULL,NULL),(105,2,105,171,0,0,NULL,NULL),(106,2,106,377,0,0,NULL,NULL),(107,2,107,265,0,0,NULL,NULL),(108,2,108,283,0,0,NULL,NULL),(109,2,109,170,0,0,NULL,NULL),(110,2,110,278,0,0,NULL,NULL),(111,2,111,355,0,0,NULL,NULL),(112,2,112,26,0,0,NULL,NULL),(113,2,113,156,0,0,NULL,NULL),(114,2,114,257,0,0,NULL,NULL),(115,2,115,116,0,0,NULL,NULL),(116,2,116,394,0,0,NULL,NULL),(117,2,117,175,0,0,NULL,NULL),(118,2,118,414,0,0,NULL,NULL),(119,2,119,149,0,0,NULL,NULL),(120,2,120,382,0,0,NULL,NULL),(121,2,121,62,0,0,NULL,NULL),(122,2,122,40,0,0,NULL,NULL),(123,2,123,135,0,0,NULL,NULL),(124,2,124,309,0,0,NULL,NULL),(125,2,125,378,0,0,NULL,NULL),(126,2,126,71,0,0,NULL,NULL),(127,2,127,37,0,0,NULL,NULL),(128,2,128,42,0,0,NULL,NULL),(129,2,129,164,0,0,NULL,NULL),(130,2,130,196,0,0,NULL,NULL),(131,2,131,428,0,0,NULL,NULL),(132,2,132,187,0,0,NULL,NULL),(133,2,133,223,0,0,NULL,NULL),(134,2,134,314,0,0,NULL,NULL),(135,2,135,211,0,0,NULL,NULL),(136,2,136,364,0,0,NULL,NULL),(137,2,137,192,0,0,NULL,NULL),(138,2,138,307,0,0,NULL,NULL),(139,2,139,133,0,0,NULL,NULL),(140,2,140,239,0,0,NULL,NULL),(141,2,141,244,0,0,NULL,NULL),(142,2,142,189,0,0,NULL,NULL),(143,2,143,25,0,0,NULL,NULL),(144,2,144,91,0,0,NULL,NULL),(145,2,145,353,0,0,NULL,NULL),(146,2,146,373,0,0,NULL,NULL),(147,2,147,161,0,0,NULL,NULL),(148,2,148,421,0,0,NULL,NULL),(149,2,149,296,0,0,NULL,NULL),(150,2,150,120,0,0,NULL,NULL),(151,2,151,114,0,0,NULL,NULL),(152,2,152,109,0,0,NULL,NULL),(153,2,153,184,0,0,NULL,NULL),(154,2,154,152,0,0,NULL,NULL),(155,2,155,263,0,0,NULL,NULL),(156,2,156,96,0,0,NULL,NULL),(157,2,157,145,0,0,NULL,NULL),(158,2,158,274,0,0,NULL,NULL),(159,2,159,143,0,0,NULL,NULL),(160,2,160,55,0,0,NULL,NULL),(161,2,161,212,0,0,NULL,NULL),(162,2,162,124,0,0,NULL,NULL),(163,2,163,331,0,0,NULL,NULL),(164,2,164,400,0,0,NULL,NULL),(165,2,165,115,0,0,NULL,NULL),(166,2,166,246,0,0,NULL,NULL),(167,2,167,417,0,0,NULL,NULL),(168,2,168,227,0,0,NULL,NULL),(169,2,169,303,0,0,NULL,NULL),(170,2,170,155,0,0,NULL,NULL),(171,2,171,427,0,0,NULL,NULL),(172,2,172,253,0,0,NULL,NULL),(173,2,173,418,0,0,NULL,NULL),(174,2,174,323,0,0,NULL,NULL),(175,2,175,433,0,0,NULL,NULL),(176,2,176,50,0,0,NULL,NULL),(177,2,177,396,0,0,NULL,NULL),(178,2,178,34,0,0,NULL,NULL),(179,2,179,117,0,0,NULL,NULL),(180,2,180,85,0,0,NULL,NULL),(181,2,181,366,0,0,NULL,NULL),(182,2,182,45,0,0,NULL,NULL),(183,2,183,316,0,0,NULL,NULL),(184,2,184,424,0,0,NULL,NULL),(185,2,185,24,0,1,2,'2020-09-05 22:33:00'),(186,2,186,339,0,0,NULL,NULL),(187,2,187,47,0,0,NULL,NULL),(188,2,188,59,0,0,NULL,NULL),(189,2,189,324,0,0,NULL,NULL),(190,2,190,220,0,0,NULL,NULL),(191,2,191,233,0,0,NULL,NULL),(192,2,192,351,0,0,NULL,NULL),(193,2,193,376,0,0,NULL,NULL),(194,2,194,371,0,0,NULL,NULL),(195,2,195,245,0,0,NULL,NULL),(196,2,196,28,0,0,NULL,NULL),(197,2,197,335,0,0,NULL,NULL),(198,2,198,194,0,0,NULL,NULL),(199,2,199,391,0,0,NULL,NULL),(200,2,200,281,0,0,NULL,NULL),(201,2,201,260,0,0,NULL,NULL),(202,2,202,372,0,0,NULL,NULL),(203,2,203,315,0,0,NULL,NULL),(204,2,204,90,0,0,NULL,NULL),(205,2,205,347,0,0,NULL,NULL),(206,2,206,138,0,0,NULL,NULL),(207,2,207,146,0,0,NULL,NULL),(208,2,208,357,0,0,NULL,NULL),(209,2,209,105,0,0,NULL,NULL),(210,2,210,235,0,0,NULL,NULL),(211,2,211,218,0,0,NULL,NULL),(212,2,212,301,0,0,NULL,NULL),(213,2,213,207,0,0,NULL,NULL),(214,2,214,51,0,0,NULL,NULL),(215,2,215,294,0,0,NULL,NULL),(216,2,216,176,0,0,NULL,NULL),(217,2,217,268,0,0,NULL,NULL),(218,2,218,261,0,0,NULL,NULL),(219,2,219,420,0,0,NULL,NULL),(220,2,220,108,0,0,NULL,NULL),(221,2,221,346,0,0,NULL,NULL),(222,2,222,54,0,0,NULL,NULL),(223,2,223,159,0,0,NULL,NULL),(224,2,224,174,0,0,NULL,NULL),(225,2,225,216,0,0,NULL,NULL),(226,2,226,226,0,0,NULL,NULL),(227,2,227,95,0,0,NULL,NULL),(228,2,228,389,0,0,NULL,NULL),(229,2,229,384,0,0,NULL,NULL),(230,2,230,100,0,0,NULL,NULL),(231,2,231,402,0,0,NULL,NULL),(232,2,232,222,0,0,NULL,NULL),(233,2,233,380,0,0,NULL,NULL),(234,2,234,147,0,0,NULL,NULL),(235,2,235,285,0,0,NULL,NULL),(236,2,236,27,0,0,NULL,NULL),(237,2,237,107,0,0,NULL,NULL),(238,2,238,317,0,0,NULL,NULL),(239,2,239,150,0,0,NULL,NULL),(240,2,240,344,0,0,NULL,NULL),(241,2,241,271,0,0,NULL,NULL),(242,2,242,431,0,0,NULL,NULL),(243,2,243,292,0,0,NULL,NULL),(244,2,244,295,0,0,NULL,NULL),(245,2,245,131,0,0,NULL,NULL),(246,2,246,311,0,0,NULL,NULL),(247,2,247,350,0,0,NULL,NULL),(248,2,248,280,0,0,NULL,NULL),(249,2,249,53,0,0,NULL,NULL),(250,2,250,130,0,0,NULL,NULL),(251,2,251,46,0,0,NULL,NULL),(252,2,252,204,0,0,NULL,NULL),(253,2,253,52,0,0,NULL,NULL),(254,2,254,98,0,0,NULL,NULL),(255,2,255,259,0,0,NULL,NULL),(256,2,256,409,0,0,NULL,NULL),(257,2,257,282,0,0,NULL,NULL),(258,2,258,86,0,0,NULL,NULL),(259,2,259,379,0,0,NULL,NULL),(260,2,260,134,0,0,NULL,NULL),(261,2,261,202,0,0,NULL,NULL),(262,2,262,101,0,0,NULL,NULL),(263,2,263,306,0,0,NULL,NULL),(264,2,264,87,0,0,NULL,NULL),(265,2,265,178,0,0,NULL,NULL),(266,2,266,426,0,0,NULL,NULL),(267,2,267,88,0,0,NULL,NULL),(268,2,268,225,0,0,NULL,NULL),(269,2,269,313,0,0,NULL,NULL),(270,2,270,287,0,0,NULL,NULL),(271,2,271,67,0,0,NULL,NULL),(272,2,272,266,0,0,NULL,NULL),(273,2,273,343,0,0,NULL,NULL),(274,2,274,66,0,0,NULL,NULL),(275,2,275,231,0,0,NULL,NULL),(276,2,276,330,0,0,NULL,NULL),(277,2,277,126,0,0,NULL,NULL),(278,2,278,177,0,0,NULL,NULL),(279,2,279,180,0,0,NULL,NULL),(280,2,280,291,0,0,NULL,NULL),(281,2,281,154,0,0,NULL,NULL),(282,2,282,60,0,0,NULL,NULL),(283,2,283,412,0,0,NULL,NULL),(284,2,284,310,0,0,NULL,NULL),(285,2,285,221,0,0,NULL,NULL),(286,2,286,197,0,0,NULL,NULL),(287,2,287,275,0,0,NULL,NULL),(288,2,288,362,0,0,NULL,NULL),(289,2,289,102,0,0,NULL,NULL),(290,2,290,186,0,0,NULL,NULL),(291,2,291,228,0,0,NULL,NULL),(292,2,292,83,0,0,NULL,NULL),(293,2,293,140,0,0,NULL,NULL),(294,2,294,157,0,0,NULL,NULL),(295,2,295,41,0,0,NULL,NULL),(296,2,296,258,0,0,NULL,NULL),(297,2,297,419,0,0,NULL,NULL),(298,2,298,234,0,0,NULL,NULL),(299,2,299,32,0,0,NULL,NULL),(300,2,300,363,0,0,NULL,NULL),(301,2,301,387,0,0,NULL,NULL),(302,2,302,345,0,0,NULL,NULL),(303,2,303,329,0,0,NULL,NULL),(304,2,304,397,0,0,NULL,NULL),(305,2,305,93,0,0,NULL,NULL),(306,2,306,430,0,0,NULL,NULL),(307,2,307,342,0,0,NULL,NULL),(308,2,308,193,0,0,NULL,NULL),(309,2,309,173,0,0,NULL,NULL),(310,2,310,390,0,0,NULL,NULL),(311,2,311,224,0,0,NULL,NULL),(312,2,312,75,0,0,NULL,NULL),(313,2,313,127,0,0,NULL,NULL),(314,2,314,158,0,0,NULL,NULL),(315,2,315,416,0,0,NULL,NULL),(316,2,316,35,0,0,NULL,NULL),(317,2,317,410,0,0,NULL,NULL),(318,2,318,299,0,0,NULL,NULL),(319,2,319,305,0,0,NULL,NULL),(320,2,320,160,0,0,NULL,NULL),(321,2,321,375,0,0,NULL,NULL),(322,2,322,49,0,0,NULL,NULL),(323,2,323,128,0,0,NULL,NULL),(324,2,324,255,0,0,NULL,NULL),(325,2,325,249,0,0,NULL,NULL),(326,2,326,78,0,0,NULL,NULL),(327,2,327,250,0,0,NULL,NULL),(328,2,328,349,0,0,NULL,NULL),(329,2,329,217,0,0,NULL,NULL),(330,2,330,290,0,0,NULL,NULL),(331,2,331,327,0,0,NULL,NULL),(332,2,332,68,0,0,NULL,NULL),(333,2,333,84,0,0,NULL,NULL),(334,2,334,185,0,0,NULL,NULL),(335,2,335,153,0,0,NULL,NULL),(336,2,336,365,0,0,NULL,NULL),(337,2,337,169,0,0,NULL,NULL),(338,2,338,398,0,0,NULL,NULL),(339,2,339,58,0,0,NULL,NULL),(340,2,340,198,0,0,NULL,NULL),(341,2,341,356,0,0,NULL,NULL),(342,2,342,201,0,0,NULL,NULL),(343,2,343,195,0,0,NULL,NULL),(344,2,344,43,0,0,NULL,NULL),(345,2,345,29,0,0,NULL,NULL),(346,2,346,252,0,0,NULL,NULL),(347,2,347,248,0,0,NULL,NULL),(348,2,348,284,0,0,NULL,NULL),(349,2,349,359,0,0,NULL,NULL),(350,2,350,415,0,0,NULL,NULL),(351,2,351,240,0,0,NULL,NULL),(352,2,352,97,0,0,NULL,NULL),(353,2,353,241,0,0,NULL,NULL),(354,2,354,31,0,0,NULL,NULL),(355,2,355,179,0,0,NULL,NULL),(356,2,356,236,0,0,NULL,NULL),(357,2,357,254,0,0,NULL,NULL),(358,2,358,354,0,0,NULL,NULL),(359,2,359,181,0,0,NULL,NULL),(360,2,360,297,0,0,NULL,NULL),(361,2,361,219,0,0,NULL,NULL),(362,2,362,370,0,0,NULL,NULL),(363,2,363,256,0,0,NULL,NULL),(364,2,364,106,0,0,NULL,NULL),(365,2,365,206,0,0,NULL,NULL),(366,2,366,298,0,0,NULL,NULL),(367,2,367,168,0,0,NULL,NULL),(368,2,368,286,0,0,NULL,NULL),(369,2,369,321,0,0,NULL,NULL),(370,2,370,337,0,0,NULL,NULL),(371,2,371,288,0,0,NULL,NULL),(372,2,372,167,0,0,NULL,NULL),(373,2,373,411,0,0,NULL,NULL),(374,2,374,308,0,0,NULL,NULL),(375,2,375,272,0,0,NULL,NULL),(376,2,376,232,0,0,NULL,NULL),(377,2,377,76,0,0,NULL,NULL),(378,2,378,243,0,0,NULL,NULL),(379,2,379,119,0,0,NULL,NULL),(380,2,380,188,0,0,NULL,NULL),(381,2,381,56,0,0,NULL,NULL),(382,2,382,137,0,0,NULL,NULL),(383,2,383,395,0,0,NULL,NULL),(384,2,384,304,0,0,NULL,NULL),(385,2,385,386,0,0,NULL,NULL),(386,2,386,190,0,0,NULL,NULL),(387,2,387,162,0,0,NULL,NULL),(388,2,388,237,0,0,NULL,NULL),(389,2,389,340,0,0,NULL,NULL),(390,2,390,242,0,0,NULL,NULL),(391,2,391,82,0,0,NULL,NULL),(392,2,392,352,0,0,NULL,NULL),(393,2,393,423,0,0,NULL,NULL),(394,2,394,151,0,0,NULL,NULL),(395,2,395,238,0,0,NULL,NULL),(396,2,396,267,0,0,NULL,NULL),(397,2,397,429,0,0,NULL,NULL),(398,2,398,361,0,0,NULL,NULL),(399,2,399,139,0,0,NULL,NULL),(400,2,400,270,0,0,NULL,NULL),(401,2,401,48,0,0,NULL,NULL),(402,2,402,336,0,0,NULL,NULL),(403,2,403,438,0,0,NULL,NULL),(404,2,404,166,0,0,NULL,NULL),(405,2,405,393,0,0,NULL,NULL),(406,2,406,262,0,0,NULL,NULL),(407,2,407,104,0,0,NULL,NULL),(408,2,408,172,0,0,NULL,NULL),(409,2,409,63,0,0,NULL,NULL),(410,2,410,39,0,0,NULL,NULL),(411,2,411,23,0,1,2,'2020-09-05 22:32:47'),(412,2,412,74,0,0,NULL,NULL),(413,2,413,399,0,0,NULL,NULL),(414,2,414,437,0,0,NULL,NULL),(415,2,415,103,0,0,NULL,NULL),(416,2,416,57,0,0,NULL,NULL),(417,2,417,264,0,0,NULL,NULL),(418,2,418,89,0,0,NULL,NULL),(419,2,419,112,0,0,NULL,NULL),(420,2,420,425,0,0,NULL,NULL),(421,2,421,79,0,0,NULL,NULL),(422,2,422,199,0,0,NULL,NULL),(423,2,423,289,0,0,NULL,NULL),(424,2,424,388,0,0,NULL,NULL),(425,2,425,213,0,0,NULL,NULL),(426,2,426,73,0,0,NULL,NULL),(427,2,427,113,0,0,NULL,NULL),(428,2,428,123,0,0,NULL,NULL),(429,2,429,110,0,0,NULL,NULL),(430,2,430,392,0,0,NULL,NULL),(431,2,431,436,0,0,NULL,NULL),(432,2,432,44,0,0,NULL,NULL),(433,2,433,132,0,0,NULL,NULL),(434,2,434,432,0,0,NULL,NULL),(435,2,435,326,0,0,NULL,NULL),(436,2,436,302,0,0,NULL,NULL),(437,2,437,368,0,0,NULL,NULL),(438,2,438,405,0,0,NULL,NULL),(439,2,439,72,0,0,NULL,NULL),(440,2,440,165,0,0,NULL,NULL),(441,2,441,182,0,0,NULL,NULL),(442,2,442,99,0,0,NULL,NULL),(443,2,443,205,0,0,NULL,NULL),(444,2,444,22,0,0,NULL,NULL),(445,2,445,203,0,0,NULL,NULL),(446,2,446,273,0,0,NULL,NULL),(447,2,447,318,0,0,NULL,NULL),(448,2,448,129,0,0,NULL,NULL),(449,2,449,210,0,0,NULL,NULL),(450,2,450,61,0,0,NULL,NULL),(451,2,451,163,0,0,NULL,NULL),(452,2,452,92,0,0,NULL,NULL),(453,2,453,94,0,0,NULL,NULL),(454,2,454,319,0,0,NULL,NULL);
/*!40000 ALTER TABLE `priorities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `initial_assignment_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(10000) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `screening_mode` varchar(50) DEFAULT NULL,
  `tag_privacy` tinyint(1) DEFAULT NULL,
  `num_labels_thus_far` int(11) DEFAULT NULL,
  `sort_by` varchar(255) DEFAULT NULL,
  `initial_round_size` int(11) DEFAULT NULL,
  `min_citations` int(11) DEFAULT NULL,
  `max_citations` int(11) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `date_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_projects_code` (`code`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`tag_privacy` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (2,NULL,'thisismyprojectname','thisismyprojectdescription','VG2PLER3YF','double',0,NULL,'Most likely to be relevant',0,NULL,NULL,'2020-09-05 21:44:47',NULL);
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects_leaders`
--

DROP TABLE IF EXISTS `projects_leaders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects_leaders` (
  `user_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `projects_leaders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `projects_leaders_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects_leaders`
--

LOCK TABLES `projects_leaders` WRITE;
/*!40000 ALTER TABLE `projects_leaders` DISABLE KEYS */;
INSERT INTO `projects_leaders` VALUES (2,2);
/*!40000 ALTER TABLE `projects_leaders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_id` int(11) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `citation_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tagtypes`
--

DROP TABLE IF EXISTS `tagtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tagtypes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(500) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  `creator_id` int(11) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tagtypes`
--

LOCK TABLES `tagtypes` WRITE;
/*!40000 ALTER TABLE `tagtypes` DISABLE KEYS */;
/*!40000 ALTER TABLE `tagtypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) DEFAULT NULL,
  `task_type` varchar(50) DEFAULT NULL,
  `num_assigned` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (4,2,'perpetual',-1);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(80) DEFAULT NULL,
  `password` varchar(80) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL,
  `show_journal` tinyint(1) DEFAULT NULL,
  `show_authors` tinyint(1) DEFAULT NULL,
  `show_keywords` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`show_journal` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`show_authors` in (0,1)),
  CONSTRAINT `CONSTRAINT_3` CHECK (`show_keywords` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'killian','michael.killian@uzh.ch','f8e3af429f1bf268bf01d6283114b9142234c26007e3f6441f478ba2569b544a3b85834b781f1cb3','Michael Killian',10,1,1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_projects`
--

DROP TABLE IF EXISTS `users_projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_projects` (
  `user_id` int(11) DEFAULT NULL,
  `project_id` int(11) DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `users_projects_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `users_projects_ibfk_2` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_projects`
--

LOCK TABLES `users_projects` WRITE;
/*!40000 ALTER TABLE `users_projects` DISABLE KEYS */;
INSERT INTO `users_projects` VALUES (2,2);
/*!40000 ALTER TABLE `users_projects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-05 22:34:40