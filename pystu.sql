
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `cname` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `cname` (`cname`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for score
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sid` varchar(15) DEFAULT NULL,
  `cname` varchar(15) DEFAULT NULL,
  `garde` float(4,0) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cid` (`cname`),
  KEY `sid` (`sid`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `student` (`sid`),
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`cname`) REFERENCES `course` (`cname`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `sid` varchar(15) NOT NULL,
  `name` varchar(15) DEFAULT NULL,
  `password` varchar(15) DEFAULT NULL,
  `sex` varchar(15) DEFAULT NULL,
  `bnumber` varchar(15) DEFAULT NULL,
  `birthday` varchar(15) DEFAULT NULL,
  `IdCord` varchar(15) DEFAULT NULL,
  `profession` varchar(15) DEFAULT NULL,
  `class` varchar(15) DEFAULT NULL,
  `Examinee number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
