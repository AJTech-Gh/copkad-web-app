"use strict";
var KTDatatablesBasicPaginations = function() {

	var initTable1 = function() {
		var table = $('#kt_table_1');

		// begin first table
		// https://datatables.net/extensions/buttons/examples/html5/columns.html
		table.DataTable({
			dom: 'Bfrtip',
			buttons: [
				'colvis',
				{
					extend: 'copyHtml5',
					title: 'COP',
					messageTop: 'DEATH',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_cr_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'DEATH',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'DEATH',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'DEATH',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'DEATH',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
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

// print the row data
let printRowData = (row) => {
	let col_ids = ["record_id", "member_id", "full_name", "assembly", "ministry", "date_of_birth", "aged", "date_of_dirth", "burial_date", "officiating_minister"];
	let jsonData = {};
	let row_data = row.getElementsByTagName("td");
	for (let i = 0; i < row_data.length - 1; i++) {
		jsonData[col_ids[i]] = row_data[i].textContent;
	}
	printDetails(jsonData);
}

//Method to load row back into form
let viewRowData = (row) => {
	let colIds = ["record_id", "member_id", "full_name", "assembly", "ministry", "date_of_birth", "aged", "death_date", "burial_date", "officiating_minister"];
	let rowData = row.getElementsByTagName("td");
	let jsonRowData = {}

	for (let i = 0; i < rowData.length - 1; i++ ){
		jsonRowData[colIds[i]] = rowData[i].textContent;
	}

	$("#record_id_div").attr("hidden", false);

	//console.log(jsonRowData);
	document.querySelector("#record_id").value = jsonRowData.record_id;
	document.querySelector("#member_id").value = jsonRowData.member_id;
	document.querySelector("#full_name").value = jsonRowData.full_name;
	document.querySelector("#kt_datetimepicker_c1").value = jsonRowData.date_of_birth;
	document.querySelector("#aged").value = jsonRowData.aged;
    document.querySelector("#kt_datetimepicker_c2").value = jsonRowData.death_date;
    document.querySelector("#kt_datetimepicker_c3").value = jsonRowData.burial_date;
	document.querySelector("#assembly").value = jsonRowData.assembly;
	document.querySelector("#officiating_minister").value = jsonRowData.officiating_minister;

	KTUtil.scrollTop();
};

// print the user's details
let printDetails =  (data) => {
	// open the print window
	var print_area = window.open();
	// compose the document
	print_area.document.write("<html><head><title>User Details</title>"
								+ "<style>.kt-wizard-v1__review-content {font-size: 20;}"
								+ "</style></head>"
								+ "<body style=\"padding: 20px;\">" 
								+ "<h1 style=\"text-align: center; font-weight: bold;\">COP</h1><br><br>"
								+ "<h1 style=\"text-align: center; font-weight: bold;\">RALLIES AND CONVENTIONS</h1>"
								+ '<div class="kt-wizard-v1__review-content">'
								+ 'ID: <label>' + data.cr_id + '</label>'
								+ '<br/>Type: <label>' + data.cr_type + '</label>'
								+ '<br/>Title: <label>' + data.cr_title + '</label>'
								+ '<br/>Start Date: <label>' + data.start_date_time + '</label>'
								+ '<br/>End Date: <label>' + data.end_date_time + '</label>'
								+ '<br/>Assembly: <label>' + data.assembly + '</label>'
								+ '<br/>Venue: <label>' + data.venue + '</label>'
								+ '<br/>Souls Won: <label>' + data.souls_won + '</label>'
								+ '<br/>Head Count: <label>' + data.head_count + '</label>'
								+ '<br/>Mode of Count: <label>' + data.mode_of_count + '</label>'
								+ "</div></body></html>");
	let cssPaths = ["/static/assets/css/demo2/pages/general/wizard/wizard-1.css",
					"/static/assets/vendors/global/vendors.bundle.css",
					"/static/assets/css/demo2/style.bundle.css"];

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
	print_area.print();
	print_area.close();
  }

// print table
// https://jasonday.github.io/printThis/
// $('#download_table_btn').on("click", function () {
// 	$('#kt_table_1').printThis({
// 		importCSS: true,
// 		importStyle: true,
// 		pageTitle: "COP-KAD",
// 		loadCSS: ["/static/assets/css/demo2/pages/general/wizard/wizard-1.css",
// 		"/static/assets/vendors/global/vendors.bundle.css",
// 		"/static/assets/css/demo2/style.bundle.css"],
// 		header: "<h1>Rallies and Conventions</h1>",
// 		base: location.host
// 	});
// });

// compare dates: g means date1 greater than date2, l means date1 less than date2 and date1 equal to date2
let compareDates = (date1, date2) => {
	if (date1 > date2) return ("g");
	else if (date1 < date2) return ("l");
	else return ("e"); 
}


// search by date
// https://keenthemes.com/metronic/?page=docs&section=html-components-datatable
var tableData = -1;  // keep the full table content
$("#kt_dashboard_daterangepicker").on("apply.daterangepicker", function(e, picker) {
	// let picker = document.querySelector("#kt_dashboard_daterangepicker");
	// var startDate = $(this).data('daterangepicker').startDate._d;
	// var endDate = $(this).data('daterangepicker').endDate._d;
	let startDate = new Date(picker.startDate.format('YYYY-MM-DD'));
	let endDate = new Date(picker.endDate.format('YYYY-MM-DD'));
	let datatable = $("#kt_table_1").DataTable();
	// if the table data is not set, set it
	// else reload the table data
	if(tableData === -1) {
		tableData = Object.assign({}, datatable.table().data());
	} else {
		datatable.clear();
		datatable.rows.add(tableData);
		datatable.draw(false);
	}
	let tableRowsLength = datatable.rows()[0].length;
	// handle equal dates and if startDate is less than endDate
	let datesComp = compareDates(startDate, endDate);
	if(datesComp === "e") {
		for(let i = 0; i < tableRowsLength; i++) {
			let tr_data = datatable.row(i).data();
			let sDate = new Date(tr_data[3].split(" ")[0]);
			let eDate = new Date(tr_data[4].split(" ")[0]);
			if (compareDates(sDate, startDate) === "e" && compareDates(sDate, endDate) === "e" && compareDates(eDate, startDate) === "e" && compareDates(eDate, endDate) === "e") {
				continue;
			}
			datatable.row(i).remove().draw(false);
			i--;
			tableRowsLength--;
		}
	} else if(datesComp === "l") {
		for(let i = 0; i < tableRowsLength; i++) {
			let tr_data = datatable.row(i).data();
			let sDate = new Date(tr_data[3].split(" ")[0]);
			let eDate = new Date(tr_data[4].split(" ")[0]);
			if ((sDate >= startDate && sDate <= endDate) || (eDate >= startDate && eDate <= endDate)) {
				continue;
			}
			datatable.row(i).remove().draw(false);
			i--;
			tableRowsLength--;
		}
	} else {
		swal.fire({
			"title": "",
			"text": "Invalid date range", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
	}
});