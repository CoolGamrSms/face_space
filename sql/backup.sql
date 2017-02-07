-- phpMyAdmin SQL Dump
-- version 3.5.5
-- http://www.phpmyadmin.net
--
-- Host: sql9.freesqldatabase.com
-- Generation Time: Feb 03, 2017 at 10:36 AM
-- Server version: 5.5.50-0ubuntu0.14.04.1
-- PHP Version: 5.3.28

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `sql9156599`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`%` PROCEDURE `get_comments`(IN `postid` BIGINT(20))
    NO SQL
SELECT cu.user_id, cu.first_name, cu.last_name, c.text, c.comment_date
FROM	tbl_users cu,
	tbl_posts p,
        tbl_comments c
WHERE   p.post_id = c.post_id
AND	c.user_id = cu.user_id
AND	p.post_id = postid
ORDER BY c.comment_date ASC$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_friends`(IN `user_id` BIGINT(20))
BEGIN
(
SELECT
       tbl_users.user_name,
       tbl_users.first_name,
       tbl_users.last_name,
       tbl_users.user_id
FROM tbl_relationships, tbl_users
WHERE tbl_relationships.friend_id = user_id
AND tbl_users.user_id = tbl_relationships.user_id
AND tbl_relationships.status = 1
)
UNION
(
SELECT
       tbl_users.user_name,
       tbl_users.first_name,
       tbl_users.last_name,
       tbl_users.user_id
FROM tbl_relationships, tbl_users
WHERE tbl_relationships.user_id = user_id
AND tbl_users.user_id = tbl_relationships.friend_id
AND tbl_relationships.status = 1
);

END$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_friendsPosts`(IN `user_id` BIGINT(20))
BEGIN
(
SELECT
       tbl_users.user_name,
       tbl_users.first_name,
       tbl_users.last_name,
       tbl_posts.post_id,
       tbl_posts.text,
       tbl_posts.post_date,
       tbl_users.user_id
FROM tbl_relationships, tbl_users, tbl_posts
WHERE tbl_relationships.friend_id = user_id
AND tbl_users.user_id = tbl_relationships.user_id
AND tbl_posts.user_id = tbl_relationships.user_id
AND tbl_relationships.status = 1
)
UNION
(
SELECT
       tbl_users.user_name,
       tbl_users.first_name,
       tbl_users.last_name,
       tbl_posts.post_id,
       tbl_posts.text,
       tbl_posts.post_date,
       tbl_users.user_id
FROM tbl_relationships, tbl_users, tbl_posts
WHERE tbl_relationships.user_id = user_id
AND tbl_users.user_id = tbl_relationships.friend_id
AND tbl_posts.user_id = tbl_relationships.friend_id
AND tbl_relationships.status = 1
)
UNION
(
SELECT
       tbl_users.user_name,
       tbl_users.first_name,
       tbl_users.last_name,
       tbl_posts.post_id,
       tbl_posts.text,
       tbl_posts.post_date,
       tbl_users.user_id
FROM tbl_users, tbl_posts
WHERE tbl_users.user_id = user_id
AND tbl_posts.user_id = user_id
)

ORDER BY post_date DESC

LIMIT 30;

END$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_pending`(IN `uid` BIGINT)
    NO SQL
SELECT
tbl_users.user_id,
tbl_users.user_name,
tbl_users.first_name,
tbl_users.last_name,
tbl_relationships.status,
tbl_relationships.action_user_id

FROM tbl_relationships, tbl_users
WHERE tbl_relationships.user_id = uid
AND `status` = 0
AND `action_user_id` != uid
AND tbl_users.user_id = tbl_relationships.friend_id

UNION

SELECT
tbl_users.user_id,
tbl_users.user_name,
tbl_users.first_name,
tbl_users.last_name,
tbl_relationships.status,
tbl_relationships.action_user_id

FROM tbl_relationships, tbl_users
WHERE tbl_relationships.friend_id = uid
AND `status` = 0
AND `action_user_id` != uid
AND tbl_users.user_id = tbl_relationships.user_id$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_posts`(IN `id` BIGINT(20))
    NO SQL
SELECT pu.user_id, pu.user_name, p.text, p.post_date, p.post_id
FROM tbl_users pu,
     tbl_posts p
WHERE pu.user_id = p.user_id
AND pu.user_id = id
ORDER by p.post_date DESC
LIMIT 30$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_comments`
--

CREATE TABLE IF NOT EXISTS `tbl_comments` (
  `comment_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `post_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `text` varchar(140) NOT NULL,
  `comment_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `tbl_comments`
--

INSERT INTO `tbl_comments` (`comment_id`, `post_id`, `user_id`, `text`, `comment_date`) VALUES
(1, 14, 14, 'HAHAHA\r\n', '2017-02-03 06:46:31'),
(2, 14, 9, 'sup bitch', '2017-02-03 06:55:32'),
(3, 14, 14, '"); DROP TABLES Shane;', '2017-02-03 06:56:47');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_posts`
--

CREATE TABLE IF NOT EXISTS `tbl_posts` (
  `post_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `text` varchar(140) NOT NULL,
  `post_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`post_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `tbl_posts`
--

INSERT INTO `tbl_posts` (`post_id`, `user_id`, `text`, `post_date`) VALUES
(1, 4, 'the best post ever', '2017-02-01 21:19:31'),
(2, 4, 'bleeeeeeeh', '2017-02-01 21:51:04'),
(3, 12, 'dons post', '2017-02-02 02:37:53'),
(4, 6, 'why do dogs bark', '2017-02-02 02:38:19'),
(5, 12, 'har har', '2017-02-02 04:50:26'),
(6, 9, 'i suck', '2017-02-02 04:52:47'),
(7, 12, 'does this redirect work?', '2017-02-02 04:53:54'),
(8, 12, 'heloo', '2017-02-02 05:21:01'),
(9, 12, '', '2017-02-02 05:21:06'),
(10, 9, 'yea', '2017-02-03 00:34:33'),
(11, 9, 'let me out', '2017-02-03 02:55:57'),
(12, 9, '<a href="#">ayy lmao</a>', '2017-02-03 03:55:47'),
(13, 13, 'yo\r\n', '2017-02-03 04:36:13'),
(14, 14, 'HELLO SHANE', '2017-02-03 06:46:12');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_relationships`
--

CREATE TABLE IF NOT EXISTS `tbl_relationships` (
  `user_id` bigint(20) NOT NULL,
  `friend_id` bigint(20) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `action_user_id` bigint(20) NOT NULL,
  `friends_since` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`,`friend_id`),
  KEY `tbl_relationships_ibfk_3` (`action_user_id`),
  KEY `tbl_relationships_ibfk_2` (`friend_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_relationships`
--

INSERT INTO `tbl_relationships` (`user_id`, `friend_id`, `status`, `action_user_id`, `friends_since`) VALUES
(4, 9, 1, 9, '2017-02-03 10:07:43'),
(9, 10, 1, 9, '2017-02-03 10:00:28'),
(9, 12, 1, 9, '2017-02-03 09:40:47'),
(9, 14, 1, 9, '2017-02-03 09:40:49');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_users`
--

CREATE TABLE IF NOT EXISTS `tbl_users` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `user_name` varchar(30) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `state` varchar(30) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  `date_registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `tbl_users`
--

INSERT INTO `tbl_users` (`user_id`, `first_name`, `last_name`, `user_name`, `email`, `state`, `password`, `date_registered`) VALUES
(4, 'shane', 'schulte', 'shanesms', 'waefawiefoj', 'waeofijawef', '12345', '2017-02-01 19:10:57'),
(6, 'billy', 'billy', 'billy', 'billy', 'billy', 'sha512$b05742df52a842e68776c95', '2017-02-01 19:13:50'),
(7, 'billy', 'billy', 'bill', 'billy', 'billy', 'sha512$cff448e2febb42ce95f86af', '2017-02-01 19:15:29'),
(8, '1', '1', 'don', '1', '1', 'sha512$a9c9505d7e5a4584864079da30890c53$04ca8117585afc04ac813dbdb952e3fefc96543fbb21420bacefd043d902832d05b5e3f974572288a1c8ba9071ce022d644f5f84b6e775c7f2b47fd0681053a6', '2017-02-01 19:22:12'),
(9, 'shane', 'schulte', 'test', 'test', 'test', 'sha512$fbade052002943118a94d9b764432dcf$43f203b6529c235e9e9310f7c8f0cb155405055d3b1210da3bec70e4594da05f72ec1d12e3bd30bceccf14302dc8d51741ca560ba760eff98c9af81f8cf24cda', '2017-02-01 19:51:00'),
(10, 'a', 'a', 'abcd', 'a', 'a', 'sha512$ba649e763b3648158938ef30d153ba8b$81402143e91c40da7afbc2c44ce170b58b8d0d981948ca20bb4b3f5d74cc4cb643e0da14df02a8e590d4dcf06040bd7913984fbaf509dec1961872ffa70ac71d', '2017-02-01 20:50:11'),
(12, 'don', 'nguyen', 'donny', 'a@a', 'texas', 'sha512$4c943f303479413dbee87f4d2cf7e081$cbcdfa5a246881029d6c9f9b60071cd8d7c6cf1f429054d83a528b8d642568c9f4f9e92caa684c7f41cc6d0cd038d5cb81a071db0168750207d4eb2d7ba075a7', '2017-02-01 22:18:01'),
(13, 'yo', 'yo', 'yo', 'yo', 'yo', 'sha512$e3e1779847154f8c9ba4a968075eb564$fdf6e8f1863f49063720b781c959d31f15570b4e1e353a9a5e307a0fb655b34ff30ab6e729c2315f099348d2bd6aafcee668d8c7f440854e9e58d8e3306897c9', '2017-02-03 04:35:27'),
(14, 'Hi', 'Shane', 'hishane', 'howare@you.com', '"); DROP TABLE Users;', 'sha512$73fdc27064534689b77f5c3ca03d89ad$17e70340c4ace98256cf228419318f2532cdecc15b75d80d0366cf4ceebdc6d25de0059ea3c7f4f1666037a49f46d0ab0426fc69619d47bc81637da6e876fbd4', '2017-02-03 06:45:09');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_comments`
--
ALTER TABLE `tbl_comments`
  ADD CONSTRAINT `tbl_comments_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `tbl_posts` (`post_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `tbl_posts`
--
ALTER TABLE `tbl_posts`
  ADD CONSTRAINT `tbl_posts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `tbl_relationships`
--
ALTER TABLE `tbl_relationships`
  ADD CONSTRAINT `tbl_relationships_ibfk_3` FOREIGN KEY (`action_user_id`) REFERENCES `tbl_users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_relationships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `tbl_users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbl_relationships_ibfk_2` FOREIGN KEY (`friend_id`) REFERENCES `tbl_users` (`user_id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
