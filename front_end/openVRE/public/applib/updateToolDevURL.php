<?php

require __DIR__."/../../config/bootstrap.php";

if ($_REQUEST) {

	$data = $GLOBALS['toolsDevMetaCol']->findOne(['_id' => $_REQUEST['toolid']]);

	if(!isset($data)) {
		$_SESSION['errorData']['Error'][] = "Tool id unexisting.";
		redirect($GLOBALS['BASEURL'].'admin/vmURL.php?id='.$_REQUEST['toolid']);
	}

	$GLOBALS['toolsDevMetaCol']->updateOne(
		['_id' => $_REQUEST['toolid']],
        ['$set' => [
			'last_status_date' => date('Y/m/d H:i:s'),
			'step2.date' => date('Y/m/d H:i:s'),
			'step2.status' => true,
			'step2.type' => $_REQUEST['type'],
			'step2.tool_code' => $_REQUEST['vm-code']
			]
		]
	);

	$_SESSION['errorData']['Info'][] = "Tool code path successfully saved, please go to next step (tool specification).";
	redirect($GLOBALS['BASEURL'].'admin/myNewTools.php');
}
redirect($GLOBALS['BASEURL']);
