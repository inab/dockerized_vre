<?php


require __DIR__."/../../config/bootstrap.php";

redirectToolDevOutside();

if (checkAdmin() || in_array($_REQUEST["tool"], $_SESSION['User']['ToolsDev']) ){
    $GLOBALS['toolsCol']->updateOne(
        ['_id' => $_REQUEST["tool"]],
        ['$set'   => ['status' => intval($_REQUEST["status"])]]
    );
}
logger("Updating tool status | USER: ".$_SESSION['User']["_id"].", ID:".$_SESSION['User']["id"].", TOOL:".$_REQUEST['tool'].", STATUS:".$_REQUEST["status"]);

redirect($GLOBALS['BASEURL'].'admin/adminTools.php');
