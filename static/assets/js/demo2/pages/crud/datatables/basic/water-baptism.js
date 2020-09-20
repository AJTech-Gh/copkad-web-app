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
						columns: [0, 1, 2, 3, 4, 5, 6, 7] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_bc_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7] //[0, ':visible']
					}
				},
				{
					filename: 'COP_bc_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'BAPTISM',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7] //[0, ':visible']
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
                                <button class="dropdown-item" onclick="getNotifId(this.parentElement.parentElement.parentElement.parentElement)" data-toggle="modal" data-target="#kt_modal_4"><i class="fa flaticon2-email"></i> Push Notification</button>								
                                <button class="dropdown-item" onclick="printRowData(this.parentElement.parentElement.parentElement.parentElement)" ><i class="la la-print"></i> Generate Report</button>
                            </div>
                        </span>
                        <a onclick="viewRowData(this.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="View">
                          <i class="fa 
						  flaticon-search-magnifier-interface-symbol"></i>
                        </a>`;
					},
				},
				{
					targets: 3,
					render: function(data, type, full, meta) {

						var assembly = {
							EEA: {'title': 'Emmanuel'},
							GA: {'title': 'Glory'},
							HA: {'title': 'Hope'}
						}
						
						if(typeof assembly[data] === 'undefined') {
							return data;
						}

						return assembly[data].title;
					}
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
					targets: 7,
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


// print the row data
let printRowData = (row) => {
	let colIds = ["record_id", "member_id", "full_name", "assembly", "date_of_baptism", "officiating_minister", "venue", "certificate"]
	let jsonData = {};
	let rowData = row.getElementsByTagName("td");
	for (let i = 0; i < rowData.length - 1; i++) {
		jsonData[colIds[i]] = rowData[i].textContent;
	}
	printRowDetails(jsonData);
}


let printRowDetails =  (data) => {
	// open the print window
	var print_area = window.open();
	// compose the document
	print_area.document.write("<html><head><title>User Details</title>"
								+ "<style>.kt-wizard-v1__review-content {font-size: 20;}"
								+ "</style></head>"
								+ "<body style=\"padding: 20px;\">" 
								+ "<h1 style=\"text-align: center; font-weight: bold;\">COP</h1><br><br>"
								+ "<h1 style=\"text-align: center; font-weight: bold;\">WATER BAPTISM</h1>"
								+ '<div class="kt-wizard-v1__review-content">'
								+ 'Record ID: <label>' + data.record_id + '</label>'
								+ '<br/>member_id: <label>' + data.member_id + '</label>'
								+ '<br/>Full Name: <label>' + data.full_name + '</label>'
								+ '<br/>Assembly: <label>' + data.assembly + '</label>'
								+ '<br/>Date of Baptism: <label>' + data.date_of_baptism + '</label>'
								+ '<br/>Ordination Minister: <label>' + data.officiating_minister + '</label>'
								+ '<br/>Venue: <label>' + data.venue + '</label>'
								+ '<br/>Certificate: <label>' + data.certificate + '</label>'
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


// load the notification
let getNotifId = (row) => {
	document.querySelector("#send").disabled = true;

	$("#messag_id").val("");
	$("#msg_record_id").val("");
	
	$.ajax({
		method: "POST",

		url: "/load_baptism_cert_msg_id",

		success: function(res) {
			$("#message_id").val(res.msg_id);

			let rec_id = row.getElementsByTagName("td")[0].textContent;
			document.querySelector("#msg_record_id").value = rec_id;

			document.querySelector("#send").disabled = false;
		},

		error: function(res, status, error) {
			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			}).then((result) => {
				if (result.value) {
					$("#kt_modal_4").modal("toggle");
					document.querySelector("#send").disabled = true;
				}
			});
		}
	});

}

$("#send").on("click", function(e){
	KTApp.progress($(this));

	$.ajax({
		method: "POST",

		url: "/send_baptism_cert_notif_msg",

		data: {
			message_id: $("#message_id").val(),
			msg_record_id: $("#msg_record_id").val(),
			message_body: $("#message_body").val()
		},

		success: function(res) {
			KTApp.unprogress($("#send"));

			swal.fire({
				"title": "", 
				"text": "Notification Sent Successfully!", 
				"type": "success",
				"confirmButtonClass": "btn btn-secondary"
			}).then((result) => {
				if (result.value) {
					$("#kt_modal_4").modal("toggle");
					$("#message_id").val("");
					$("#msg_record_id").val("");
					$("#message_body").val("");
					document.querySelector("#send").disabled = true;
				}
			});
		},

		error: function(res, status, error) {
			KTApp.unprogress($("#send"));

			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
});

// load the row data into the form for viewing and updating
let viewRowData = (row) => {
	let rowData = row.getElementsByTagName("td");

	$("#kt_form")[0].reset();

	$("#record_id_div").attr("hidden", false);
	
	document.querySelector("#record_id").value = rowData[0].textContent;
	document.querySelector("#member_id").value = rowData[1].textContent;

	KTUtil.scrollTop();

	$.ajax({
		method: "POST",

		url: "/load_baptism_by_id/" + rowData[1].textContent,

		success: function(res) {
			if (res.place_of_baptism) {
				let img_url = "/" + replaceAll(res.img, "\\", "/");
				document.querySelector("#certImagDisplay").src = img_url;
				document.querySelector("#kt_datetimepicker_6").value = res.date_of_baptism;
				document.querySelector("#place_of_baptism").value = res.place_of_baptism;
				document.querySelector("#officiating_minister").value = res.officiating_minister;
				document.querySelector("#district").value = res.district;
				document.querySelector("#area").value = res.area;
				document.querySelector("#country").value = res.country;
			} else {
				document.querySelector("#certImagDisplay").src = "";
				document.querySelector("#date_of_baptism").value = "";
				document.querySelector("#place_of_baptism").value = "";
				document.querySelector("#officiating_minister").value = "";
				document.querySelector("#district").value = "";
				document.querySelector("#area").value = "";
				document.querySelector("#country").value = "";
				document.querySelector("#record_id").value = "";
				$("#record_id_div").attr("hidden", true);
			}
	
			$("#member_id").trigger("change");

		},

		error: function(res, status, error) {
			$("#record_id_div").attr("hidden", true);

			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
}

//compare dates: g means date1 greater than date2, l means date1 less than date2 and date1 equal to date2
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
			let sDate = new Date(tr_data[4]);
			if (compareDates(sDate, startDate) === "e" && compareDates(sDate, endDate) === "e") {
				continue;
			}
			datatable.row(i).remove().draw(false);
			i--;
			tableRowsLength--;
		}
	} else if(datesComp === "l") {
		for(let i = 0; i < tableRowsLength; i++) {
			let tr_data = datatable.row(i).data();
			let sDate = new Date(tr_data[4]);
			if (sDate >= startDate && sDate <= endDate) {
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