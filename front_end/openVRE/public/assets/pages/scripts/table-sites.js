var TableDatatablesSites = function () {

    var handleTable = function () {

        var table = $('#table-sites');

        var oTable = table.dataTable({

            "lengthMenu": [
                [10,  -1],
                [10, "All"] // change per page values here
            ],

            // set the initial value
            "pageLength": 10,

            "language": {
                "lengthMenu": " _MENU_ records"
            },
            "columnDefs": [{ // set default column settings
                'orderable': false,
                'targets': [1]
            }, {
                "searchable": false,
                "targets": []
            }],
            "order": [
                [0, "asc"]
            ], // set first column as a default sort by asc
        	    "initComplete": function (settings, json) {
				            $('#loading-datatable').hide();
				            $('#table-sites').show();
			           }
        });
    }

    return {

        //main function to initiate the module
        init: function () {
            handleTable();
        }

    };

}();

jQuery(document).ready(function() {
	TableDatatablesSites.init();
});
