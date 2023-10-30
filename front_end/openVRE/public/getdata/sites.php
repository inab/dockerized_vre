<?php

require __DIR__ . "/../../config/bootstrap.php";

redirectOutside();

//Retrive sites

$sites = getSitesInfo();

$progress = ['pending', 'testing', 'active'];
$types = ['comp'=> 'Computational', 'data'=> 'Data', 'both'=>'Data & Computational'];
$status = ['inactive', 'active'];
// Print page

?>

<?php require "../htmlib/header.inc.php"; ?>

<body class="page-header-fixed page-sidebar-closed-hide-logo page-content-white page-container-bg-solid page-sidebar-fixed">
  <div class="page-wrapper">

    <?php require "../htmlib/top.inc.php"; ?>
    <?php require "../htmlib/menu.inc.php"; ?>

    <!-- BEGIN CONTENT -->
    <div class="page-content-wrapper">
      <!-- BEGIN CONTENT BODY -->
      <div class="page-content">
        <!-- BEGIN PAGE HEADER-->
        <!-- BEGIN PAGE BAR -->
        <div class="page-bar">
          <ul class="page-breadcrumb">
            <li>
              <a href="home/">Home</a>
              <i class="fa fa-circle"></i>
            </li>
            <li>
              <span>Get Data</span>
              <i class="fa fa-circle"></i>
            </li>
            <li>
              <span>From Repository</span>
              <i class="fa fa-circle"></i>
            </li>
            <li>
              <span>Repository Name</span>
            </li>
          </ul>
        </div>
        <!-- END PAGE BAR -->
        <!-- BEGIN PAGE TITLE-->
        <h1 class="page-title">
          <a href="javascript:;" target="_blank"><img src="assets/layouts/layout/img/icon.png" width=100></a>
          <?=$GLOBALS['AppPrefix']?> Network
        </h1>
        <!-- END PAGE TITLE-->
        <!-- END PAGE HEADER-->

	<?php

	// inject error Message
	//$_SESSION['errorData']['Info'][]="Data catalogue under construction";

	// print PHP ERROR MESSAGES
	if (isset($_SESSION['errorData'])) {
		foreach ($_SESSION['errorData'] as $subTitle => $txts){
			if (count($txts) == 0){
				unset($_SESSION['errorData'][$subTitle]);
			}
		}
	}
	if (isset($_SESSION['errorData']) && $_SESSION['errorData']) {
		if (isset($_SESSION['errorData']['Info'])) {
			?><div class="alert alert-info"><?php
		} else {
			?><div class="alert alert-warning"><?php
		}
		foreach ($_SESSION['errorData'] as $subTitle => $txts) {
			print "$subTitle<br/>";
			foreach ($txts as $txt) {
				print "<div style=\"margin-left:20px;\">$txt</div>";
			}
		}
		unset($_SESSION['errorData']);
		?></div><?php
	}
	?>
        <div class="row">
          <div class="col-md-12">
            <!-- BEGIN EXAMPLE TABLE PORTLET-->
            <div class="portlet light portlet-fit bordered">
              <div class="portlet-title">
                <div class="caption">
                  <i class="icon-share font-red-sunglo hide"></i>
                  <span class="caption-subject font-dark bold"><?=$GLOGALS['AppPrefix']?> sites. Status and available resources</span>
                </div>
              </div>
              <div class="portlet-body">
                <table class="table table-striped table-hover table-bordered" id="table-sites">
                  <thead>
                    <tr>
                      <th> Site Id </th>
                      <th> Full Name </th>
                      <th> Type </th>
                      <th> Progress </th>
                      <th> Status </th>
                      <th> Resources </th>
                    </tr>
                  </thead>

                  <tbody>
                    <!-- process and display each result row -->
                <?php foreach ($sites as $obj) { ?>
                    <tr>
                        <td> <?= $obj["_id"] ?> </td>
                        <td> <?= $obj["name"] ?> </td>
                        <td> <?= $types[$obj["type"]] ?> </td>
                        <td> <?= $progress[$obj["progress"]] ?> </td>
                        <td> <?= $status[$obj["status"]] ?> </td>
			                  <td>
                          CPUs: <?= $obj["cpu_count"]?> (<?=$obj['cpu_percent']?>%),
                          GPUs <?= $obj['gpu_count']?>,
                          Free RAM: <?= $obj['memory']['available']?>/<?= $obj['memory']['total']?>,
                          Conn: <?=$obj["outbound_connectivity"]?>
                        </td>
                    </tr>
                <?php } ?>

                  </tbody>
                </table>
              </div>
            </div>
            <!-- END EXAMPLE TABLE PORTLET-->
          </div>
        </div>
      </div>
      <!-- END CONTENT BODY -->
    </div>
    <!-- END CONTENT -->

<?php
require "../htmlib/footer.inc.php";
require "../htmlib/js.inc.php";

