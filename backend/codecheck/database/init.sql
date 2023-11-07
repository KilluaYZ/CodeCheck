-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主机： db
-- 生成日期： 2023-11-07 03:52:41
-- 服务器版本： 8.1.0
-- PHP 版本： 8.2.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `codecheck_db`
--
CREATE DATABASE IF NOT EXISTS `codecheck_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE `codecheck_db`;

-- --------------------------------------------------------

--
-- 表的结构 `check_code_session_key`
--

CREATE TABLE `check_code_session_key` (
  `checkCode` char(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '验证码，设定为6位随机数字',
  `sessionKey` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话，一串随机的字符，与CheckCode一一对应',
  `createTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `file_info`
--

CREATE TABLE `file_info` (
  `id` int NOT NULL,
  `fileName` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件名称。假设一条记录存储的文件是/home/checkcode/project/1/src/123.txt，那么fileName存储的就是123.txt',
  `filePath` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件路径。假设一条记录存储的文件是/home/checkcode/project/1/src/123.txt，那么filePath存储的就是src',
  `fileSuffix` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件后缀名。假设一条记录存储的文件是/home/checkcode/project/1/src/123.txt，那么fileSuffix存储的就是txt',
  `fileCategory` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件类别，我们将文件分为以下几类\r\ndirectory: 目录\r\ntext: 可阅读的文本文件\r\nbinary: 不可阅读的二进制文件\r\nspectial: 特殊文件，例如设备/dev/sda\r\n',
  `sha256` char(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '文件的sha256值，现在还用不上，但是先暂时留着',
  `projectId` int NOT NULL COMMENT '文件所属的项目ID。每一个文件都属于一个项目，不存在不属于任何项目的文件',
  `createTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `visitTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `problems`
--

CREATE TABLE `problems` (
  `problemId` int NOT NULL,
  `projectId` int DEFAULT NULL COMMENT '问题所属的项目ID。每一个问题都一定属于某个项目。',
  `filePath` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '出现问题的文件路径。\r\n假设文件/home/checkcode/project/1/src/123.txt，出问题，那么filePath存储的就是/123.txt，即相对src的相对路径',
  `problemClassName` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '问题类别名称。来自于ProblemDetail中的json数据，只不过为了方便，所以单独拿出来',
  `severity` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '问题严重程度',
  `problemDetail` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci COMMENT '扫描结果得出的完整分析结果，以JSON格式存储'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `projects`
--

CREATE TABLE `projects` (
  `id` int NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目名称',
  `isPublic` tinyint(1) DEFAULT '0' COMMENT '项目是否是公开的，如果项目是公开的，这意味着该项目可以被其他用户访问',
  `userId` int NOT NULL COMMENT '项目所属用户ID。每一个项目都一定属于某个用户',
  `createTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `tasks`
--

CREATE TABLE `tasks` (
  `taskId` int NOT NULL,
  `projectId` int DEFAULT NULL COMMENT '任务所属的项目ID',
  `status` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT 'created' COMMENT '任务的状态，支持created, unzipping, analysing, pulling, waiting, success, error几个状态',
  `createTime` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `traces`
--

CREATE TABLE `traces` (
  `traceId` int NOT NULL,
  `line` int NOT NULL,
  `file` text NOT NULL,
  `kind` text NOT NULL,
  `desc` text,
  `projectId` int NOT NULL,
  `problemId` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL COMMENT '用户的id，他是用户的唯一标识',
  `userName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名，非唯一',
  `password` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码，使用werkzeug.security加密后的字符串存储',
  `roles` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'common' COMMENT '用户角色，有admin, manager, common可选，目前没用上，默认common',
  `email` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户邮箱，用于注册，密码找回，是唯一的',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- 表的结构 `user_token`
--

CREATE TABLE `user_token` (
  `uid` int NOT NULL COMMENT '用户ID',
  `token` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '会话令牌，是一串随机字符串',
  `createTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `visitTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 转储表的索引
--

--
-- 表的索引 `file_info`
--
ALTER TABLE `file_info`
  ADD PRIMARY KEY (`id`),
  ADD KEY `file_info_projects_id_restrict` (`projectId`);

--
-- 表的索引 `problems`
--
ALTER TABLE `problems`
  ADD PRIMARY KEY (`problemId`),
  ADD KEY `problems_ibfk_1` (`projectId`);

--
-- 表的索引 `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`),
  ADD KEY `projects_ibfk_1` (`userId`);

--
-- 表的索引 `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`taskId`),
  ADD KEY `tasks_ibfk_1` (`projectId`);

--
-- 表的索引 `traces`
--
ALTER TABLE `traces`
  ADD PRIMARY KEY (`traceId`),
  ADD KEY `traces_ibfk_1` (`projectId`),
  ADD KEY `traces_ibfk_2` (`problemId`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `file_info`
--
ALTER TABLE `file_info`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `problems`
--
ALTER TABLE `problems`
  MODIFY `problemId` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `tasks`
--
ALTER TABLE `tasks`
  MODIFY `taskId` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `traces`
--
ALTER TABLE `traces`
  MODIFY `traceId` int NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT COMMENT '用户的id，他是用户的唯一标识';

--
-- 限制导出的表
--

--
-- 限制表 `file_info`
--
ALTER TABLE `file_info`
  ADD CONSTRAINT `file_info_projects_id_restrict` FOREIGN KEY (`projectId`) REFERENCES `projects` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- 限制表 `problems`
--
ALTER TABLE `problems`
  ADD CONSTRAINT `problems_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- 限制表 `projects`
--
ALTER TABLE `projects`
  ADD CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- 限制表 `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT;

--
-- 限制表 `traces`
--
ALTER TABLE `traces`
  ADD CONSTRAINT `traces_ibfk_1` FOREIGN KEY (`projectId`) REFERENCES `projects` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  ADD CONSTRAINT `traces_ibfk_2` FOREIGN KEY (`problemId`) REFERENCES `problems` (`problemId`) ON DELETE CASCADE ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
