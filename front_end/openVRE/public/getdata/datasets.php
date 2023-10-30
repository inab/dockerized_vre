<?php

require __DIR__ . "/../../config/bootstrap.php";

redirectOutside();

//Retrive communities
$sites = getSitesInfo("data");

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
              <span>From D4TH catalogue</span>
              <i class="fa fa-circle"></i>
            </li>
            <li>
              <span>Datasets</span>
            </li>
          </ul>
        </div>
        <!-- END PAGE BAR -->
        <!-- BEGIN PAGE TITLE-->
        <h1 class="page-title">
          <a href="javascript:;" target="_blank"><img src="assets/layouts/layout/img/icon.png" width=100></a>
          Available Datasets from project catalogue
        </h1>
        <!-- END PAGE TITLE-->
        <!-- END PAGE HEADER-->
	<?php

	// inject error Message
//	$_SESSION['errorData']['Info'][]="Data catalogue under construction";


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
                  <span class="caption-subject font-dark bold uppercase">Browse Datasets</span>
                </div>
              </div>
              <div class="portlet-body">
                <div id="loading-datatable">
                  <div id="loading-spinner">LOADING</div>
                </div>

                <table class="table table-striped table-hover table-bordered" id="table-repository">
                  <thead>
                    <tr>
                      <th> Id </th>
                      <th> Title </th>
                      <th> Description </th>
                      <th> Version </th>
                      <?php foreach ($sites as $site) {?>
                        <th><?=$site['_id']?></th>
                      <?php } ?>
                      <th> Materialize </th>
                    </tr>
                  </thead>

                  <tbody>
                    <!-- process and display each result row -->

			<?php
//	$ds_list =  getDatasets();
	//JL DEMO
	$ds_list = True;
	if ($ds_list) {
    $i = 1000309;
    $n = 1;
    while ($i < 1000320) {
      $data =
			['_id'=>$GLOBALS['AppPrefix'].$i,
			'name'=> $GLOBALS['AppPrefix'].'_UC1_'.$n,
			'description' => 'Some UC1 data '.$n,
			'version' => '1.0 [2023-09-30]',
      'catalogue_url' => "https://catalogue.datatools4heart.eu/dataset/?".$GLOBALS['AppPrefix'].$i
      ];
      foreach ($sites as $site) {
        $data[$site['_id']] = rand(0,100);
      }
      $datasets[] = $data;
      $i++;
      $n++;
    }

		//		foreach (getDatasets() as $obj) {
		foreach ($datasets as $obj) {
	                      ?>
             <tr>
                <td> <?= $obj["_id"]; ?> </td>
                <td> <?= $obj["name"]; ?> </td>
                <td> <?= $obj["description"]; ?> </td>
                <td> <?= $obj["version"]; ?> </td>
                <?php foreach ($sites as $site) {?>
                  <td><?= $obj[$site['_id']]?></th>
                <?php } ?>

                <td style="vertical-align:middle;">
                <?php
                  //$dataset_uri = ($obj->datalink->uri? $obj->datalink->uri:"");
			          ?>

			  <!-- Send via POST url and metadata to dataMaterialize -->

			  <form action="tools/dataMaterialize/input.php" method="post">
				  <input type="hidden" name="uploadType"        value="data-sites"/>
				  <input type="hidden" name="data_type"         value="<?= htmlspecialchars($obj->type);?>"/>
				  <input type="hidden" name="description"       value="<?= htmlspecialchars($obj->description);?>"/>
				  <input type="hidden" name="dataset_id"        value="<?= htmlspecialchars($obj->_id);?>" />
  				<button type="submit" class="btn green dropdown-toggle" value="submit">
				    <i class="fa fa-download tooltips font-white" data-original-title="Materialize datasets"></i>
	  			</button>
		    </form>
        </td>
                </tr>
        <?php
            }
          }
        ?>

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
