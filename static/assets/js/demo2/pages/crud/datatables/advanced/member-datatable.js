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
	console.log(jsonIdStatus.status.toLowerCase());
	if (jsonIdStatus.status.trim().toLowerCase() === "incomplete") {
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

// print the row data
let printRowData = (row) => {
	let colIds = ["member_id", "full_name", "gender", "marital_status", "phone", "assembly", "ministry", "status"];
	let jsonData = {};
	let rowData = row.getElementsByTagName("td");
	for (let i = 0; i < rowData.length - 1; i++) {
		jsonData[colIds[i]] = rowData[i].textContent;
	}

	printDetails(jsonData);
}

let printDetails =  (data) => {
	// open the print window
	var print_area = window.open();
	// compose the document
	// print_area.document.write("<html><head><title>User Details</title>"
	// 							+ "<style>.kt-wizard-v1__review-content {font-size: 20;}"
	// 							+ "</style></head>"
	// 							+ "<body style=\"padding: 20px;\">" 
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">COP</h1><br><br>"
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">BIRTH REGISTRY</h1>"
	// 							+ '<div class="kt-wizard-v1__review-content">'
	// 							+ 'Father\'s ID - Name of Father: <label>' + data.member_id_father + " - " + data.father_name + '</label>'
	// 							+ '<br/>Mother\'s ID - Name of Mother: <label>' + data.member_id_mother + " - " + data.mother_name + '</label>'
	// 							+ '<br/>Child Name: <label>' + data.child_name + '</label>'
	// 							+ '<br/>Child Date of Birth: <label>' + data.child_dob + '</label>'
	// 							+ '<br/>Date of Ceremony: <label>' + data.ceremony_date_time + '</label>'
	// 							+ '<br/>Officiating Minister: <label>' + data.officiating_minister + '</label>'
	// 							+ '<br/>Assembly: <label>' + data.assembly + '</label>'
	// 							+ "</div></body></html>");
	// let cssPaths = ["/static/assets/css/demo2/pages/general/wizard/wizard-1.css",
	// 				"/static/assets/vendors/global/vendors.bundle.css",
	// 				"/static/assets/css/demo2/style.bundle.css"];

	print_area.document.write("<!DOCTYPE html><html><head><style>* { font-size: 20px; }</style></head><body>" + `
	<div class="kt-content kt-grid__item kt-grid__item--fluid">
	<div class="row">
		<div class="col-lg-12">
			<div class="kt-portlet">
				<div class="kt-portlet__body kt-portlet__body--fit">
					<div class="kt-invoice-2">
						<div class="kt-invoice__wrapper">
							<div class="kt-invoice__head">
								<div class="kt-invoice__container kt-invoice__container--centered">
									<div class="kt-invoice__logo">
										<a href="#">
											<h1>MEMBER DATA SUMMARY</h1>
										</a>
										<a href="#">
											<img src="/static/assets/media/logos/thecopnsema-2.png">
										</a>
									</div>
									<span class="kt-invoice__desc">
										<span>The Church of Pentecost</span>
										<span>Kwadaso Area | Kwadaso Agric District | Nsema Assemblies</span>
										<span>Post Office Box, KW 101. </span>
										<span>Kwadaso - Kumasi</span>
										<span>Tel : +233 570 364 383</span>
										<span>Email: info@thecopkadna.com</span>
									</span>
								</div>
							</div>
							<!-- body -->
							<div class="kt-invoice__body kt-invoice__body--centered">
								<div class="row">
									<div class="col">
										<strong>Member ID:</strong><br/>
										<label>` + data.member_id + `</label>
									</div>
									<div class="col">
										<strong>Fullname:</strong><br/>
										<label>` + data.full_name + `</label>
									</div>
									<div class="col">
										<strong>Gender:</strong><br/>
										<label>` + data.gender + `</label>
									</div>
								</div>
								<br/>
								<div class="row">
									<div class="col">
										<strong>Marital Status:</strong><br/>
										<label>` + data.marital_status + `</label>
									</div>
									<div class="col">
										<strong>Assembly:</strong><br/>
										<label>` + data.assembly + `</label>
									</div>
									<div class="col">
										<strong>Phone:</strong><br/>
										<label>` + data.phone + `</label>
									</div>
								</div>
								<br/>
								<div class="row">
									<div class="col">
										<strong>Ministry:</strong><br/>
										<label>` + data.ministry + `</label>
									</div>
									<div class="col">
										<strong>Data status:</strong><br/>
										<label>` + data.status + `</label>
									</div>
									<div class="col">
									</div>
								</div>
								</br>
								
							</div>
							<!-- footer -->
							<!--<div class="kt-invoice__footer">
								<div class="kt-invoice__table  kt-invoice__table--centered table-responsive"></div>
							</div> -->
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>      
	</div>
	` + "</body></html>")

let cssPaths = ["/static/assets/css/demo2/pages/general/wizard/wizard-1.css",
"/static/assets/vendors/global/vendors.bundle.css",
"/static/assets/css/demo2/style.bundle.css",
"/static/assets/css/demo2/pages/general/invoices/invoice-2.css"];

	for (let i = 0; i < cssPaths.length; i++) {
		let style = print_area.document.createElement('link');
		style.type = "text/css";
		style.rel = "stylesheet";
		style.href = location.origin + cssPaths[i];
		style.media = "all";
		print_area.document.getElementsByTagName("head")[0].appendChild(style);
	}
	// print details and return to page
	print_area.document.close();
	print_area.focus();
	// print_area.print();
	// print_area.close();
  }