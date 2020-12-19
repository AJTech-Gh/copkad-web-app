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
					messageTop: 'MEMBER POPULATION',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_assembly_data_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'MEMBER POPULATION',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4] //[0, ':visible']
					}
				},
				{
					filename: 'COP_assembly_data_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'MEMBER POPULATION',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4] //[0, ':visible']
					}
				},
				{
					filename: 'COP_assembly_data_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'MEMBER POPULATION',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4] //[0, ':visible']
					}
				},
				{
					filename: 'COP_assembly_data_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'MEMBER POPULATION',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4] //[0, ':visible']
					}
				}
			],
			responsive: true,
			pagingType: 'full_numbers',
			columnDefs: [
				
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


$(".assemblies").on("click", function(e) {
	let assembly_name = $(this).text().trim();
	$("#load_ass_data").attr("hidden", false);
	$.ajax({
		method: "POST",

		url: "/assembly_forecast/" + assembly_name.toLowerCase().replaceAll(" ", "_"),

		success: function(res) {
			$("#assembly_forecast_title").text("Assembly Forecast (" + assembly_name + ")");
			$("#no_registration").text(res.member_count + " member(s) registered");
			$("#status_active").text(res.status.active + " active");
			$("#status_inactive").text(res.status.inactive + " inactive");
			$("#status_backslider").text(res.status.backslider + " backslider");
			$("#finance_income").text(res.finance.income);
			$("#finance_expenditure").text(res.finance.expenditure);
			$("#welfare").text(res.welfare);
			$("#load_ass_data").attr("hidden", true);
},

		error: function(res, status, error) {
			$("#load_ass_data").attr("hidden", true);
			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
});

// trigger click for first assembly in assembly forecast list
$(".assemblies").first().trigger("click");


$(".assembly_ui_toggle_activate").on("click", function(e) {
	let assembly_name = $(this).attr("id");
	let activate_status = $(this).text().toLowerCase().trim();
	$("#" + assembly_name + "_spinner").attr("hidden", false);
	$.ajax({
		method: "POST",

		url: "/" + activate_status + "_assembly/" + assembly_name,

		success: function(res) {
			if (activate_status === "deactivate") {
				document.querySelector("#" + assembly_name).innerHTML = `<span class="kt-badge kt-badge--success kt-badge--inline">Activate</span>`;
				$("#edit_settings_" + assembly_name).attr("target", "");
				$("#edit_settings_" + assembly_name).attr("href", "javascript:void(0)");
			} else {
				document.querySelector("#" + assembly_name).innerHTML = `<span class="kt-badge kt-badge--danger kt-badge--inline">Deactivate</span>`;
				$("#edit_settings_" + assembly_name).attr("target", "_blank");
				$("#edit_settings_" + assembly_name).attr("href", "/edit_settings/" + assembly_name);
			}
			$("#" + assembly_name + "_spinner").attr("hidden", true);
		},

		error: function(res, status, error) {
			$("#" + assembly_name + "_spinner").attr("hidden", true);
			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
});