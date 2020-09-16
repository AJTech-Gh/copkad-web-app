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
				{
					targets: 4,
					render: function(data, type, full, meta) {
						return translateMinistries(data);
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

// search for user's data when member id field value length is 8
$("#member_id").on("keyup", function(e) {
    if ($(this).val().length === 8) {
        $(".spin").attr("hidden", false);
        $.ajax({
            method: "POST",

            url: "/load_user_by_id/member_id",

            data: $(this).serialize(),

            success: function(res) {
                $(".spin").attr("hidden", true);
                if (res.first_name) {
                    let img_url = "/" + res.img.replaceAll("\\", "/");
                    if (img_url === "/") {
                        img_url = "/static/assets/media/users/thecopkadna-users.png";
                    }
                    $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
                    }
                    document.querySelector("#full_name").value = fullName;
                    let assemblies = {
                        EEA: "Emmanuel",
                        GA: "Glory",
                        HA: "Hope"
                    }
				   
					document.querySelector("#assembly").value = assemblies[res.assembly];
					document.querySelector("#ministry").value = res.ministry;
					document.querySelector("#date_of_birth").value = res.dob;
						
                } else {
                    let img_url = "/static/assets/media/users/thecopkadna-users.png";
                    $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    document.querySelector("#full_name").value = "";
                    document.querySelector("#assembly").value = "";
                    document.querySelector("#ministry").value = "";
                    $(".spin").attr("hidden", true);
                    $("#record_id_div").attr("hidden", true);
                }
            },

            error: function(res, status, error) {
				$(".spin").attr("hidden", true);
	
				swal.fire({
					"title": "",
					"text": res.responseJSON.message, 
					"type": "error",
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			}

        });

    } else {
        let img_url = "/static/assets/media/users/thecopkadna-users.png";
        $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
        document.querySelector("#full_name").value = "";
        document.querySelector("#assembly").value = "";
        document.querySelector("#ministry").value = "";
        $(".spin").attr("hidden", true);
        $("#record_id_div").attr("hidden", true);

    }
});

$("#member_id").on("change", function(e) {
    $("#member_id").trigger("keyup");
});

// print the row data
let printRowData = (row) => {
	let col_ids = ["record_id", "member_id", "full_name", "assembly", "ministry", "date_of_birth", "aged", 
	"death_date", "burial_date", "place_of_burial", "officiating_minister"];
	let jsonData = {};
	let row_data = row.getElementsByTagName("td");
	for (let i = 0; i < row_data.length - 1; i++) {
		jsonData[col_ids[i]] = row_data[i].textContent;
	}
	printDetails(jsonData);
}

let translateMinistries = (initials) => {
	let initialsArr = initials.split(",");
	let translatedMinistries = "";
	let ministries = {
		C: 'Children', 
		E: 'Evangelism', 
		P: 'Pemem', 
		W: 'Women', 
		Y: 'Youth'
	}
	for (let i = 0; i < initialsArr.length; i++) {
		translatedMinistries += ministries[initialsArr[i]] + ", ";
	}
	return translatedMinistries.substring(0, translatedMinistries.length - 2);
}

//Method to load row back into form
let viewRowData = (row) => {
	let colIds = ["record_id", "member_id", "full_name", "assembly", "ministry", "date_of_birth", "aged", "death_date", 
	"burial_date", "place_of_burial", "officiating_minister"];
	let rowData = row.getElementsByTagName("td");
	let jsonRowData = {}

	for (let i = 0; i < rowData.length - 1; i++ ){
		// if (colIds[i] === "ministry") {
		// 	jsonRowData[colIds[i]] = translateMinistries(rowData[i].textContent);
		// 	continue;
		// }
		jsonRowData[colIds[i]] = rowData[i].textContent;
	}

	$("#record_id_div").attr("hidden", false);

	KTUtil.scrollTop();

	//console.log(jsonRowData);
	document.querySelector("#record_id").value = jsonRowData.record_id;
	document.querySelector("#member_id").value = jsonRowData.member_id;
	document.querySelector("#full_name").value = jsonRowData.full_name;
	document.querySelector("#date_of_birth").value = jsonRowData.date_of_birth;
	document.querySelector("#aged").value = jsonRowData.aged;
    document.querySelector("#kt_datetimepicker_c1").value = jsonRowData.death_date;
	document.querySelector("#kt_datetimepicker_c2").value = jsonRowData.burial_date;
	document.querySelector("#place_of_burial").value = jsonRowData.place_of_burial;
	document.querySelector("#assembly").value = jsonRowData.assembly;
	document.querySelector("#ministry").value = jsonRowData.ministry;
	document.querySelector("#officiating_minister").value = jsonRowData.officiating_minister;

	$.ajax({
		method: "POST",

		url: "/load_user_img/" + $("#member_id").val(),

		success: function(res) {
			let img_url = "/" + res.img.replaceAll("\\", "/");
			if (img_url === "/") {
				img_url = "/static/assets/media/users/thecopkadna-users.png";
			}
			$('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
		},

		error: function(res, status, error) {
			let img_url = "/static/assets/media/users/thecopkadna-users.png";
			$('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")

			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
};

// calculate age from birth date and death date strings
let calcAged = (birth_date, death_date) => {
	return new Date(death_date).getYear() - new Date(birth_date).getYear();
}

// calculate the aged when the birth and death dates are set
$("#date_of_birth").on("change", function(e) {
	let birth_date = $("#date_of_birth").val();
	let death_date = $("#kt_datetimepicker_c1").val();
	let aged = calcAged(birth_date, death_date);
	if (birth_date.trim().length > 0 && death_date.trim().length > 0) {
		$("#aged").val(aged);
	}
});

$("#kt_datetimepicker_c1").on("change", function(e) {
	$("#date_of_birth").trigger("change");
});

// Class definition
var KTForm = function () {
    // Base elements
    var formEl;
    var validator;

    var initValidation = function() {
		
        validator = formEl.validate({
            // Validate only visible fields
            ignore: ":hidden",

			// Validation rules
            rules: {
               	//= Step 1
				member_id: {
					required: true
				},   
				full_name: {
					required: true
				},	 
				assembly: {
					required: true
				},	 
				ministry: {
					required: true
				},
				officiating_minister: {
					required: true
				},
				place_of_burial: {
					required: true
				},
				date_of_birth: {
					required: true
				},
				death_date: {
					required: true
				},
				aged: {
					required: true
				},
				burial_date: {
					required: true
				}
                 
            },
            
            // Display error  
            invalidHandler: function(event, validator) {     
                KTUtil.scrollTop();

                swal.fire({
                    "title": "", 
                    "text": "Your form is incomplete, Please complete it!", 
                    "type": "error",
                    "confirmButtonClass": "btn btn-secondary"
                });
            },

            // Submit valid form
            submitHandler: function (form) {
                
            }
        });   
	}

    var initSubmit = function() {
        var btn = formEl.find('[id="submit_death_btn"]');

        btn.on('click', function(e) {
            e.preventDefault();

            if (validator.form()) {
                // See: src\js\framework\base\app.js
                KTApp.progress(btn);
                //KTApp.block(formEl);

                // See: http://malsup.com/jquery/form/#ajaxSubmit
                formEl.ajaxSubmit({

                    url: "/death_submit",

                    error: function(res, err) {
                        KTApp.unprogress(btn);
            
                        swal.fire({
                            "title": "",
                            "text": res.responseJSON.message, 
                            "type": "error",
                            "confirmButtonClass": "btn btn-brand btn-sm btn-bold"
                        });
                    },

                    success: function(res) {
                        KTApp.unprogress(btn);
                        //KTApp.unblock(formEl);

                        swal.fire({
                            "title": "", 
                            "text": "The data has been successfully submitted!", 
                            "type": "success",
							"showCancelButton": true,
							"confirmButtonText": 'Print',
							"confirmButtonClass": "btn btn-primary",
							"cancelButtonText": 'Continue',
							"cancelButtonClass": 'btn btn-success',
							"reverseButtons": true
						}).then((result) => {
							if (result.value) {
								// print the member's details
								printDetails(res);
								// reset the form
								location.href = "death";
							} else {
								// reset the form
								location.href = "death";
							}
                        });
                    }
                });
            } else {
				KTUtil.scrollTop();

                swal.fire({
                    "title": "", 
                    "text": "Your form is incomplete, Please complete it!", 
                    "type": "error",
                    "confirmButtonClass": "btn btn-secondary"
                });
			}
        });
    }

    return {
        // public functions
        init: function() {
			formEl = $('#death_form');
			
			initValidation();
			initSubmit();
        }
    };
}();

jQuery(document).ready(function() {    
    KTForm.init();
});

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
								+ "<h1 style=\"text-align: center; font-weight: bold;\">DEATH DETAILS</h1>"
								+ '<div class="kt-wizard-v1__review-content">'
								+ 'Record ID: <label>' + data.record_id + '</label>'
								+ '<br/>Member ID: <label>' + data.member_id + '</label>'
								+ '<br/>Full Name: <label>' + data.full_name + '</label>'
								+ '<br/>Assembly: <label>' + data.assembly + '</label>'
								+ '<br/>Ministry: <label>' + data.ministry + '</label>'
								+ '<br/>Date of Birth: <label>' + data.date_of_birth + '</label>'
								+ '<br/>Aged: <label>' + data.aged + '</label>'
								+ '<br/>Date of Death: <label>' + data.death_date + '</label>'
								+ '<br/>Burial Date: <label>' + data.burial_date + '</label>'
								+ '<br/>Place of Burial: <label>' + data.place_of_burial + '</label>'
								+ '<br/>Officiating Minister: <label>' + data.officiating_minister + '</label>'
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
			let sDate = new Date(tr_data[7].split(" ")[0]);
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
			let sDate = new Date(tr_data[7].split(" ")[0]);
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