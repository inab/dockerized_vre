<?php
function getSitesInfo($type="") {
    $query = [];
    if ($type) {
        $query = ["type"=> $type];
    }
    return iterator_to_array($GLOBALS['sitesCol']->find(
        $query,
        $options=[
            "sort"=>["_id"=>1]
        ]
    ));
}