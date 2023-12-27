<?php

require __DIR__."/../../config/bootstrap.php";
redirectOutside();

$toolsHelp = getSingleTool_Help($_REQUEST["toolID"], $_REQUEST["op"]);

$dt_list = json_decode($_REQUEST["dt_list"]);
$ft_list = json_decode($_REQUEST["ft_list"]);
$multiple = json_decode($_REQUEST["multiple"]);
$file_selected = json_decode($_REQUEST["file_selected"]);

$files_list = getGSFiles_filteredBy([
	"data_type" => ['$in' => $dt_list],
	"format" => ['$in' => $ft_list],
	"visible"   => true
]);

//$files_list = getFilesFromDT($dt_list);

$list = [];

foreach ($files_list as $file) {

	$path = getAttr_fromGSFileId($file["_id"], 'path');
	$p = explode("/", $path);

    $dt = $GLOBALS['dataTypesCol']->findOne(['_id' => $file["data_type"]]);

	$a = [
		"id" => $file["_id"],
		"execution" => $p[2],
		"file" => $p[3],
		"description" => $file["description"],
		"data_type" => $dt['name']
	];

	$proj_code = $p[1];
    $project = getProject($proj_code);

    if (isset($project['name'])) {
    	$a["project_name"]  = $project['name'];
    } else {
    	$a["project_name"]  = "Foo project";
    }

	$list[] = $a;
}

// TABLE

$html = '
<table id="workspace_st2" class="display" cellspacing="0" width="100%">
<thead>
	<tr style="background-color: #eee;padding:3px;" id="headerSearch">
		<th></th>
		<th class="inputSearch">Files</th>
		<th class="selector">Project</th>
		<th class="selector">Execution</th>
	</tr>
    <tr id="heading">
		<th></th>
      	<th>File</th>
      	<th>Project</th>
      	<th>Execution</th>
	</tr>
  </thead>
  <tbody>
';

$selectedFiles = [];

foreach ($list as $file) {

	$tr_class = "";
	$file_sel = "";

	//if($file["id"] == $file_selected) {
	if (in_array($file["id"], $file_selected)) {
		$tr_class = "input_highlighted";
		$file_sel = "checked";
		$a = [
			"fileName" => $file["file"],
			"fileID" => $file["id"],
			"filePath" => $file["project_name"]. ' / '.$file["execution"]
		];
		$selectedFiles[] = $a;
	}

	$html .= '<tr class="row-clickable '.$tr_class.'">';
	if ($multiple) {
		$html .= '
		<td>
			<label class="mt-checkbox mt-checkbox-single mt-checkbox-outline">
				<input type="checkbox" class="checkboxes" '.$file_sel.' value="'.$file["id"].'" onchange="changeCheckbox(this, \''.$file["file"].'\', \''.$file["id"].'\', \''.$file['project_name'].' / '.$file["execution"].' /\')" />
				<span></span>
			</label>
		</td>';
	} else {
		$html .= '
		<td>
			<label class="mt-radio mt-radio-outline">
				<input type="radio" name="filesRadios" '.$file_sel.' value="'.$file["id"].'" onchange="changeRadio(\''.$file["file"].'\', \''.$file["id"].'\', \''.$file['project_name'].' / '.$file["execution"].' /\')" />
				<span></span>
			</label>
		</td>';
	}
	$html .= '
		<td>'.$file["file"].' <a href="javascript:;" onmouseover="javascript:;" class="tooltips" data-trigger="hover" data-container="body"
			data-html="true" data-placement="right" data-original-title="<p align=\'left\' style=\'margin:0\'><strong>'.$file["data_type"].'</strong><br>'.$file["description"].'</p>"><i class="fa fa-info-circle"></i></a>
		<td>'.$file['project_name'].'</td>
		<td>'.$file["execution"].'</td>
	</tr>';
}

$html .= '</tbody>
</table>';

// TOOL HELP

$thelp = '
<table class="table">
	<thead>
		<tr>
			<th>Operations</th>
			<th>File(s) required</th>
			<th>File format</th>
			<th>File type</th>
		</tr>
	</thead>
	<tbody>';

$count = 0;
foreach ($toolsHelp as $th) {
	$cc = 1;
	foreach ($th["content"] as $content) {
		if ($cc == 1) {
			$trclass = "first-tr";
		} else {
			$trclass = "";
		}
		$thelp .= '<tr class="'.$trclass.'">';
		if ($cc == 1) {
			$thelp .= '<td rowspan="'.sizeof($th["content"]).'">'.$th["operation"].'</td>';
		}
		$thelp .= '
			<td>'.$content["description"].'</td>
			<td>'.implode("<br>", $content["format"]).'</td>
			<td>'.implode("<br>", $content["data_type"]).'</td>
		</tr>';

		$cc ++;
	}
}
$thelp .= '</tbody>
</table>';

echo '{
	"table":'.json_encode($html).',
	"selectedFiles":'.json_encode($selectedFiles).',
	"help": '.json_encode($thelp).'
}';
