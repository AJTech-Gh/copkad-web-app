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
						// console.log(full[0] + " - " + full[7]);
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
							0: {'title': 'Incomplete', 'state': 'danger'},
							1: {'title': 'Complete', 'state': 'success'},
						};
						if (typeof status[data] === 'undefined') {
							return data;
						}
						return '<span class="kt-badge kt-badge--' + status[data].state + ' kt-badge--dot"></span>&nbsp;' +
							'<span class="kt-font-bold kt-font-' + status[data].state + '">' + status[data].title + '</span>';
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


//Method to load row back into form
let viewRowData = (row) => {
	let rowData = row.getElementsByTagName("td");
	let jsonIdStatus = {
		member_id: rowData[0].textContent,
		status: rowData[7].textContent
	};
	if (jsonIdStatus.status.toLowerCase() === "incomplete") {
		jsonIdStatus.status = "0";
	} else {
		jsonIdStatus.status = "1";
	}

	location.href = "view_member_data?id=" + jsonIdStatus.member_id + "&status=" + jsonIdStatus.status;
	// $.ajax({
	// 	method: "POST",

	// 	url: "/view_member_data/" + jsonIdStatus.member_id + ":" + jsonIdStatus.status,

	// 	success: function(res) {
	// 		var newWindow = window.open();
	// 		newWindow.document.write(res);
	// 	},

	// 	error: function(res, status, error) {
	// 		swal.fire({
	// 			"title": "",
	// 			"text": res.responseJSON.message, 
	// 			"type": "error",
	// 			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
	// 		});
	// 	}
	// });

};