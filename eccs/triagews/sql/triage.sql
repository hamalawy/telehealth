-- phpMyAdmin SQL Dump
-- version 2.11.3deb1ubuntu1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 31, 2001 at 11:22 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.4-2ubuntu5.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- Database: `triage`
--

-- --------------------------------------------------------

--
-- Table structure for table `audit_trail`
--

CREATE TABLE IF NOT EXISTS `audit_trail` (
  `userid` int(10) unsigned NOT NULL auto_increment,
  `sql` text NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY  (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ecgdata`
--

CREATE TABLE IF NOT EXISTS `ecgdata` (
  `ecgpointid` int(10) unsigned NOT NULL auto_increment,
  `ecgtime` double NOT NULL,
  `ecgy` double NOT NULL,
  `referralid` int(10) unsigned NOT NULL,
  `dataid` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`ecgpointid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `file`
--

CREATE TABLE IF NOT EXISTS `file` (
  `fileid` varchar(100) NOT NULL default '',
  `referralid` varchar(100) NOT NULL,
  `responseid` varchar(100) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `filetype` varchar(45) NOT NULL,
  `filecontent` longblob,
  PRIMARY KEY  (`fileid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `institution`
--

CREATE TABLE IF NOT EXISTS `institution` (
  `institutionid` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(45) NOT NULL default 'DTTB',
  `contactnum` varchar(45) NOT NULL,
  `email` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  PRIMARY KEY  (`institutionid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE IF NOT EXISTS `patient` (
  `patientid` varchar(100) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `middlename` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `maidenname` varchar(45) NOT NULL,
  `sex` varchar(45) NOT NULL default 'unknown',
  `birthdate` datetime NOT NULL,
  `age` int(10) unsigned NOT NULL,
  `agevalidity` varchar(45) NOT NULL default 'known',
  `location` varchar(100) NOT NULL,
  PRIMARY KEY  (`patientid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `referral`
--

CREATE TABLE IF NOT EXISTS `referral` (
  `referralid` varchar(100) NOT NULL,
  `description` varchar(160) NOT NULL,
  `reason` varchar(45) NOT NULL default 'case',
  `patientid` varchar(100) NOT NULL,
  `timestamp` datetime NOT NULL,
  `institutionid` varchar(100) NOT NULL,
  `docname` varchar(100) NOT NULL,
  `docnum` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL default 'new',
  PRIMARY KEY  (`referralid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `response`
--

CREATE TABLE IF NOT EXISTS `response` (
  `responseid` varchar(100) NOT NULL,
  `referralid` varchar(100) NOT NULL,
  `message` varchar(320) NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY  (`responseid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `rxdata`
--

CREATE TABLE IF NOT EXISTS `rxdata` (
  `dataid` int(10) unsigned NOT NULL auto_increment,
  `referralid` int(10) unsigned NOT NULL,
  `bloodox` double NOT NULL,
  `bpressureu` double NOT NULL,
  `bpressured` double NOT NULL,
  `heartrate` double NOT NULL,
  `timestamp` datetime NOT NULL,
  PRIMARY KEY  (`dataid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `service_client`
--

CREATE TABLE IF NOT EXISTS `service_client` (
  `userid` int(10) unsigned NOT NULL auto_increment,
  `userkey` varchar(45) NOT NULL,
  `institutionid` varchar(45) NOT NULL,
  `serialnumber` varchar(45) NOT NULL,
  `permissionby` varchar(45) NOT NULL,
  `status` varchar(45) NOT NULL,
  `activationdate` datetime NOT NULL,
  `activatedby` varchar(45) NOT NULL,
  PRIMARY KEY  (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `userid` int(10) unsigned NOT NULL auto_increment,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `firstname` varchar(45) NOT NULL,
  `middlename` varchar(45) NOT NULL,
  `lastname` varchar(45) NOT NULL,
  `occupation` varchar(45) NOT NULL,
  PRIMARY KEY  (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;
