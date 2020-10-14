"use strict";
var KTDatatablesBasicPaginations = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');

		// begin first table
		table.DataTable({
			dom: 'Bfrtip',
			buttons: [
				'colvis',
				{
					extend: 'copyHtml5',
					title: 'COP',
					messageTop: 'MEMBER DATATABLE',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_memb_data_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'MEMBER DATATABLE',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5] //[0, ':visible']
					}
				},
				{
					filename: 'COP_memb_data_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'MEMBER DATATABLE',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5] //[0, ':visible']
					}
				},
				{
					filename: 'COP_memb_data_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'MEMBER DATATABLE',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5] //[0, ':visible']
					}
				},
				{
					filename: 'COP_memb_data_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'MEMBER DATATABLE',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5] //[0, ':visible']
					}
				}
			],
			responsive: true,
			pagingType: 'full_numbers',
			columnDefs: [
				{
					targets: -1,
					title: 'Actions',
					orderable: false,
					render: function(data, type, full, meta) {
						return `
                        <span class="dropdown">
                            <a onclick="printRowData(this.parentElement.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" data-toggle="dropdown" aria-expanded="true" title="Print">
                              <i class="la la-print"></i>
                            </a>
                        </span>
                        <a onclick="viewRowData(this.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="View">
                          <i class="fa flaticon-search-magnifier-interface-symbol"></i>
                        </a>`;
					},
				},
				{
					targets: 7,
					render: function(data, type, full, meta) {

						var status = {
							0: `<span class="label label-inline label-light-danger" >Incomplete</span>`,
							1: `<span class="label label-inline label-light-success" >Complete</span>`,
						}
						
						if(typeof status[data] === 'undefined') {
							return data;
						}

						return status[data];
					}
				},
			],
		});
	};

	return {

		//main function to initiate the module
		init: function() {
			initTable1();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesBasicPaginations.init();
});