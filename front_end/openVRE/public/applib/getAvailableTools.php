<?php

require __DIR__."/../../config/bootstrap.php";

redirectOutside();

if (!$_REQUEST) {
	//redirect($GLOBALS['URL']);
	echo "Network error, please reload the Workspace";
}

// getting data types of all the selected files
$fdt = getFiles_DataTypes($_REQUEST["fn"]);

// getting all combinations for every tool
$dt = getTools_DataTypes();

// getting all possible tools according to the given data types and tools combinations
$toolsList = getTools_ByDT($dt, $fdt);

// getting id / name pairs for all tools
$tools = getTools_ListByID($toolsList, 1);

sort($tools);

if (!empty($tools)) {
	foreach($tools as $t) { ?>
		<li>
			<a href="javascript:runTool('<?=$t['_id']?>');" class="<?=$t['_id']?>">
		<?php
			if (is_file('../tools/'.$t['_id'].'/assets/ws/icon.php')) {
				include '../tools/'.$t['_id'].'/assets/ws/icon.php';
			} else {
				include '../tools/tool_skeleton/assets/ws/icon.php';
			}
		?><?=$t['name']?></a>
		</li>
	<?php
	}
} else { ?>
	<li><a href="javascript:;" style="mouse:default;"><i class="fa fa-exclamation-triangle"></i> No tools available for this combination of files</a></li>
<?php
}