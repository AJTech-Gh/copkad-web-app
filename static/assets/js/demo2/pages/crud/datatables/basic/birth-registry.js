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
					messageTop: 'BIRTH REGISTRY',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_birth_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'BIRTH REGISTRY',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_birth_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'BIRTH REGISTRY',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_birth_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'DEDICBIRTH REGISTRY',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8] //[0, ':visible']
					}
				},
				{
					filename: 'COP_birth_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'BIRTH REGISTRY',
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
				{
					targets: 1,
					render: function(data, type, full, meta) {
						
						if(data.trim() == "-") {
							return "";
						}

						return data;
					}
				},
				{
					targets: 2,
					render: function(data, type, full, meta) {
						
						if(data.trim() == "-") {
							return "";
						}

						return data;
					}
				},
				// {
				// 	targets: 9,
				// 	render: function(data, type, full, meta) {
				// 		var status = {
				// 			1: {'title': 'Verified', 'state': 'success'},
				// 			2: {'title': 'Not Verified', 'state': 'primary'},
				// 		};
				// 		if (typeof status[data] === 'undefined') {
				// 			return data;
				// 		}
				// 		return '<span class="kt-badge kt-badge--' + status[data].state + ' kt-badge--dot"></span>&nbsp;' +
				// 			'<span class="kt-font-bold kt-font-' + status[data].state + '">' + status[data].title + '</span>';
				// 	},
				// },
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


// load the row data into the form for viewing and updating
let viewRowData = (row) => {
	let colIds = ["record_id", "member_id_mother", "member_id_father", "name_of_child", "child_dob", "ceremony_date", "officiating_minister", "assembly"];
	let rowData = row.getElementsByTagName("td");
	let jsonRowData = {};

	for(let i = 0; i < rowData.length - 1; i++) {
		jsonRowData[colIds[i]] = rowData[i].textContent;
	}

	$("#birth_form")[0].reset();

	$("#record_id_div").attr("hidden", false);

	//console.log(jsonRowData);
	document.querySelector("#record_id").value = jsonRowData.record_id;
	document.querySelector("#member_id_mother").value = jsonRowData.member_id_mother.split(" - ")[0];
	document.querySelector("#member_id_father").value = jsonRowData.member_id_father.split(" - ")[0];
	document.querySelector("#child_name").value = jsonRowData.name_of_child;
	document.querySelector("#child_dob").value = jsonRowData.child_dob.split(" ")[0];
	document.querySelector("#kt_datetimepicker_2").value = jsonRowData.ceremony_date;
	document.querySelector("#officiating_minister").value = jsonRowData.officiating_minister;
	let assemblies = {
		"Emmanuel": "EEA",
		"Glory": "GA",
		"Hope": "HA"
	};
	document.querySelector("#assembly").value = assemblies[jsonRowData.assembly];
	$("#kt_select2_3").trigger("change");

	KTUtil.scrollTop();

	$("#member_id_father").trigger("change");
	$("#member_id_mother").trigger("change");
}


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
								+ "<h1 style=\"text-align: center; font-weight: bold;\">BIRTH REGISTRY</h1>"
								+ '<div class="kt-wizard-v1__review-content">'
								+ 'Member ID - Name of Father: <label>' + data.member_id_father + " - " + data.father_name + '</label>'
								+ '<br/>Member ID - Name of Mother: <label>' + data.member_id_mother + " - " + data.mother_name + '</label>'
								+ '<br/>Child Name: <label>' + data.child_name + '</label>'
								+ '<br/>Child Date of Birth: <label>' + data.child_dob + '</label>'
								+ '<br/>Date of Ceremony: <label>' + data.ceremony_date + '</label>'
								+ '<br/>Officiating Minister: <label>' + data.officiating_minister + '</label>'
								+ '<br/>Assembly: <label>' + data.assembly + '</label>'
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

// compare dates: g means date1 greater than date2, l means date1 less than date2 and date1 equal to date2
let compareDates = (date1, date2) => {
	if (date1 > date2) return ("g");
	else if (date1 < date2) return ("l");
	else return ("e"); 
}