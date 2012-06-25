<?php

define('BASEPATH', '/var/www/bambooinvoice/bamboo_system_files/');
require_once BASEPATH . 'application/config/config.php';
require_once BASEPATH . 'libraries/Encrypt.php';

class MY_Encrypt extends CI_Encrypt {
    public function __construct() {
        $this->_mcrypt_exists = (! function_exists('mcrypt_encrypt')) ? FALSE : TRUE;
    }
}

if(count($argv)!=2) die("usage: $argv[0] password\n");

$password = $argv[1];
$encryption_key = $config['encryption_key'];

$Encrypt = new MY_Encrypt();
print $Encrypt->encode($password, $encryption_key);

?>

