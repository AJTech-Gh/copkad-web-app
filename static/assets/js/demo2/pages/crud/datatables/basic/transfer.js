"use strict"
var KTDatatablesBasicPaginations2 = function() {

	var initTable2 = function() {
		var table = $('#kt_table_2');

		// begin first table
		// https://datatables.net/extensions/buttons/examples/html5/columns.html
		table.DataTable({
			dom: 'Bfrtip',
			buttons: [
				'colvis',
				{
					extend: 'copyHtml5',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_Transfer_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_Transfer_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_Transfer_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_Transfer_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'TRANSFERS',
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
                            <a onclick="transPrintRowData(this.parentElement.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" data-toggle="dropdown" aria-expanded="true" title="Print">
                              <i class="la la-print"></i>
                            </a>
                        </span>
                        <a onclick="transViewRowData(this.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="View">
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
			initTable2();
		},

	};

}();

jQuery(document).ready(function() {
	KTDatatablesBasicPaginations2.init();
});


// search for user's data when member id field value length is 8
$("#trans_member_id").on("keyup", function(e) {
    if ($(this).val().length === 8) {
        $(".spin").attr("hidden", false);
        $.ajax({
            method: "POST",

            url: "/load_user_by_id/trans_member_id",

            data: $(this).serialize(),

            success: function(res) {
                $(".spin").attr("hidden", true);
                if (res.first_name) {
                    let img_url = "/" + res.img.replaceAll("\\", "/");
                    if (img_url === "/") {
                        img_url = "/static/assets/media/users/thecopkadna-users.png";
                    }
                    $('#trans_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
                    }
                    document.querySelector("#trans_full_name").value = fullName;
						
                } else {
                    let img_url = "/static/assets/media/users/thecopkadna-users.png";
                    $('#trans_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    document.querySelector("#trans_full_name").value = "";
                    $(".spin").attr("hidden", true);
                    $("#trans_record_id_div").attr("hidden", true);
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
        $('#trans_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
        document.querySelector("#trans_full_name").value = "";
        $(".spin").attr("hidden", true);
        $("#trans_record_id_div").attr("hidden", true);

    }
});

$("#trans_member_id").on("change", function(e) {
    $("#trans_member_id").trigger("keyup");
});


// print the row data
let transPrintRowData = (row) => {
	let colIds = ["transfer_id", "member_id", "full_name", "age", "transfered_from", "transfered_to", "present_portfolio", "transfer_specification", 
				"transfer_date", "officiating_minister"];
	let jsonData = {};
	let rowData = row.getElementsByTagName("td");
	for (let i = 0; i < rowData.length - 1; i++) {
		jsonData[colIds[i]] = rowData[i].textContent;
	}
	transPrintDetails(jsonData);
}


//Method to load row back into form
let transViewRowData = (row) => {
	let colIds = ["trans_record_id", "trans_member_id", "trans_full_name", "trans_age", "transfered_from", "transfered_to", "trans_present_portfolio", "trans_specify_transfer", 
				"transfer_date", "trans_officiating_minister"];
	let rowData = row.getElementsByTagName("td");
	let jsonRowData = {}

	for (let i = 0; i < rowData.length - 1; i++ ){
		jsonRowData[colIds[i]] = rowData[i].textContent;
	}

	$("#pro_record_id_div").attr("hidden", false);

	// KTUtil.scrollTop();

	//console.log(jsonRowData);
	document.querySelector("#trans_record_id").value = jsonRowData.trans_record_id;
	document.querySelector("#trans_member_id").value = jsonRowData.trans_member_id;
	document.querySelector("#trans_full_name").value = jsonRowData.trans_full_name;
	document.querySelector("#trans_age").value = jsonRowData.trans_age;
	document.querySelector("#trans_transfered_from").value = jsonRowData.transfered_from;
    document.querySelector("#trans_transfered_to").value = jsonRowData.transfered_to;
	document.querySelector("#trans_present_portfolio").value = jsonRowData.trans_present_portfolio;
	document.querySelector("#trans_specify_transfer").value = jsonRowData.trans_specify_transfer;
	document.querySelector("#kt_datetimepicker_2").value = jsonRowData.transfer_date;
	document.querySelector("#trans_officiating_minister").value = jsonRowData.trans_officiating_minister;

	$.ajax({
		method: "POST",

		url: "/load_user_img/" + $("#trans_member_id").val(),

		success: function(res) {
			let img_url = "/" + res.img.replaceAll("\\", "/");
			if (img_url === "/") {
				img_url = "/static/assets/media/users/thecopkadna-users.png";
			}
			$('#trans_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
		},

		error: function(res, status, error) {
			let img_url = "/static/assets/media/users/thecopkadna-users.png";
			$('#trans_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")

			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
};


// Class definition
var KTForm2 = function () {
    // Base elements
    var transFormEl;
    var transValidator;

    var initValidation2 = function() {
		
        transValidator = transFormEl.validate({
            // Validate only visible fields
            ignore: ":hidden",

			// Validation rules
            rules: {
               	//= Step 1
				trans_member_id: {
					required: true
				},   
				trans_full_name: {
					required: true
				},	 
				trans_assembly: {
					required: true
				},
				trans_age: {
					required: true
				},
				trans_present_portfolio: {
					required: true
				},
				trans_transfered_from: {
					required: true
				},
				trans_transfered_to: {
					required: true
				},
				trans_transfer_specifics: {
					required: true
				},
				trans_ordination_minister: {
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

    var initSubmit2 = function() {
        var btn = transFormEl.find('[id="submit_transfer"]');

        btn.on('click', function(e) {
            e.preventDefault();

            if (transValidator.form()) {
                // See: src\js\framework\base\app.js
                KTApp.progress(btn);
                //KTApp.block(formEl);

                // See: http://malsup.com/jquery/form/#ajaxSubmit
                transFormEl.ajaxSubmit({

                    url: "/transfer_submit",

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
                            "text": "The data has been submitted successfully!", 
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
								transPrintDetails(res);
								// reset the form
								location.href = "promotion_and_transfer";
							} else {
								// reset the form
								location.href = "promotion_and_transfer";
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
			transFormEl = $('#transfer_form');
			
			initValidation2();
			initSubmit2();
        }
    };
}();

jQuery(document).ready(function() {    
    KTForm2.init();
});

// print the user's details
let transPrintDetails =  (data) => {
	// open the print window
	var print_area = window.open();
	// compose the document
	// print_area.document.write("<html><head><title>User Details</title>"
	// 							+ "<style>.kt-wizard-v1__review-content {font-size: 20;}"
	// 							+ "</style></head>"
	// 							+ "<body style=\"padding: 20px;\">" 
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">COP</h1><br><br>"
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">TRANSFER DETAILS</h1>"
	// 							+ '<div class="kt-wizard-v1__review-content">'
	// 							+ 'Record ID: <label>' + data.transfer_id + '</label>'
	// 							+ '<br/>Member ID: <label>' + data.member_id + '</label>'
	// 							+ '<br/>Full Name: <label>' + data.full_name + '</label>'
	// 							+ '<br/>Reason for Transfer: <label>' + data.transfer_specification + '</label>'
	// 							+ '<br/>Transfer Date: <label>' + data.transfer_date + '</label>'
	// 							+ '<br/>Age: <label>' + data.age + '</label>'
	// 							+ '<br/>Present Portfolio: <label>' + data.present_portfolio + '</label>'
	// 							+ '<br/>Transfered From: <label>' + data.transfered_from + '</label>'
	// 							+ '<br/>Transfered To: <label>' + data.transfered_to + '</label>'
	// 							+ '<br/>Officiating Minister: <label>' + data.officiating_minister + '</label>'
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
																		<h1>TRANSFER DATA</h1>
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
																	<strong>Transfer Date:</strong><br/>
																	<label>` + data.transfer_date + `</label>
																</div>
																<div class="col">
																	<strong>Fullname:</strong><br/>
																	<label>` + data.full_name + `</label>
																</div>
															</div>
															<br/>
															<div class="row">
																<div class="col">
																	<strong>Age(At Promotion):</strong><br/>
																	<label>` + data.age + `</label>
																</div>
																<div class="col">
																	<strong>Assembly:</strong><br/>
																	<label>` + data.assembly + `</label>
																</div>
																<div class="col">
																	<strong>Present Portfolio:</strong><br/>
																	<label>` + data.present_portfolio + `</label>
																</div>
															</div>
															<br/>
															<div class="row">
																<div class="col">
																	<strong>Transfered From:</strong><br/>
																	<label>` + data.transfered_from + `</label>
																</div>
																<div class="col">
																	<strong>Transfered To:</strong><br/>
																	<label>` + data.transfered_to + `</label>
																</div>
																<div class="col">
																	<strong>Officiating Minister:</strong><br/>
																	<label>` + data.officiating_minister + `</label>
																</div>
															</div>
															</br>
															<div class="row">
																<div class="col">
																	<strong>Transfered Specification:</strong><br/>
																	<label>` + data.transfer_specification + `</label>
																</div>
																<div class="col">
																</div>
																<div class="col">
																</div>
															</div>
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