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
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_bc_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
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
                            <a href="#" class="btn btn-sm btn-clean btn-icon btn-icon-md" data-toggle="dropdown" aria-expanded="true">
                              <i class="la la-ellipsis-h"></i>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right">
                                <a class="dropdown-item" href="#" data-toggle="modal" data-target="#kt_modal_4"><i class="fa flaticon2-email"></i> Push Notification</a>
								
                                <a class="dropdown-item" href="#"><i class="
								fa flaticon2-user-1"></i> Update Status</a>
								
                                <a class="dropdown-item" href="#"><i class="la la-print"></i> Generate Report</a>
                            </div>
                        </span>
                        <a href="#" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="View">
                          <i class="fa 
						  flaticon-search-magnifier-interface-symbol"></i>
                        </a>`;
					},
				},
				// {
				// 	targets: 8,
				// 	render: function(data, type, full, meta) {
				// 		var status = {
				// 			1: {'title': 'Active', 'class': 'kt-badge--success'},
				// 			2: {'title': 'Inactive', 'class': ' kt-badge--warning'},
				// 			3: {'title': 'Backslider', 'class': ' kt-badge--danger'},
				// 		};
				// 		if (typeof status[data] === 'undefined') {
				// 			return data;
				// 		}
				// 		return '<span class="kt-badge ' + status[data].class + ' kt-badge--inline kt-badge--pill">' + status[data].title + '</span>';
				// 	},
				// },
				{
					targets: 8,
					render: function(data, type, full, meta) {
						var status = {
							1: {'title': 'Received', 'state': 'success'},
                            2: {'title': 'Pending', 'state': 'primary'},
						};
						if (typeof status[data] === 'undefined') {
							return data;
						}
						return '<span class="kt-badge kt-badge--' + status[data].state + ' kt-badge--dot"></span>&nbsp;' +
							'<span class="kt-font-bold kt-font-' + status[data].state + '">' + status[data].title + '</span>';
					},
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