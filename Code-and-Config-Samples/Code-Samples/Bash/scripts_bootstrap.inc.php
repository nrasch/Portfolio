<?php
/*
Utilize this file as a single-point include to get you setup with lightweight access
to resources in the CakePHP app, primarily database access
*/

try {
  Globals::$db = new Real_PDO('mysql://root:********@localhost/'.DBNAME);
} catch (Exception $e) {
  die(sprintf("Database connectivity error: %s", $e->getMessage()));
}

class Globals {
  public static $db = null;
}

class Real_PDO extends PDO {
  public $lastExecError = null;
  public $constructors = null;

  public function __construct($uri) {
    if (preg_match("/(.*?):\/\/(?:(.*?)(?:\:(.*))?\@)?(\[.*?\]|.*?)(?:\:(.*?))?(?:\/(.*))?$/", $uri, $matches)) {
      list($uri, $protocol, $username, $password, $hostname, $port, $resource) = $matches;
      $this->constructors = compact('uri', 'protocol', 'username', 'password', 'hostname', 'port', 'resource');
    } else {
      throw new Exception("Inappropriately formatted DSN URI: '$uri'");
    }
    if ($protocol == "mysql") {
      if (!$port) { $port = 3306; }
      parent::__construct("mysql:host=$hostname;port=$port;dbname=$resource", $username, $password, array(PDO::MYSQL_ATTR_USE_BUFFERED_QUERY => true));
    } else {
      throw new Exception("Unexpected protocol: '$protocol'");
    }
    return $this;
  }

  public function quote($value, $parameter_type = PDO::PARAM_STR ) {
    if (is_null($value)) return "NULL";
    return parent::quote($value, $parameter_type);
  }

  public function execParams($param1, $params) {
    if (is_string($param1)) {
      $stm = $this->prepare($param1);
    } else if (is_a($param1, 'PDOStatement')) {
      $stm = $param1;
    } else {
      throw new Exception('Bad first parameter passed in Real_PDO::execParams');
    }
    $result = false;
    $this->lastExecError = array();
    if ($stm && $stm->execute($params)) {
      $result = $stm->rowCount();
      if ($result == 0) $result = "0 but true";
      while (@$stm->fetch(PDO::FETCH_ASSOC)) {}
    } else {
      $this->lastExecError = $stm->errorInfo();
    }
    return $result;
  }

  public function quoteIdentifier($identifier) {
    // Not expecting anyone to be maniacal and using delimiters IN the identifier.
    if ($this->constructors['protocol'] == 'mysql') {
      return '`'.$identifier.'`';
    }

    // Assuming the rest of the world is ANSI
    return '"'.$identifier.'"';
  }
}
