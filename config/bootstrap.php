<?php

// set up app settings
require "/var/www/html/openVRE/config/globals.inc.php";

// import vendor libs
require "/var/www/html/openVRE/vendor/autoload.php"; 

// initialize session
require "/var/www/html/openVRE/public/phplib/session.inc";

// import local classes
foreach(glob("/var/www/html/openVRE/public/phplib/classes/*.php") as $lib){
    require $lib;
}
// import local libs
foreach(glob("/var/www/html/openVRE/public/phplib/*.php") as $lib){
    require $lib;
}

?>
