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
				$("#edit_settings_" + assembly_name).attr("href", "/edit_settings?assembly_name=" + assembly_name);
			}
			$("#" + assembly_name + "_spinner").attr("hidden", true);

			location.reload()
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


// let getRandomUpperCase = () => {

// 	return String.fromCharCode((Math.floor(Math.random() * 26) + 65));
// }

// let getRandomLowerCase = () => {
// 	return String.fromCharCode((Math.floor(Math.random() * 26) + 97));
// }

// let getRandomNumber = () => {
// 	return String.fromCharCode((Math.floor(Math.random() * 10) + 48));
// }

// let getRandomSymbol = () => {
// 	let symbol = "!@#$%^&*(){}[]=<>/,.|~?";
// 	return symbol[Math.floor(Math.random()*symbol.length)];
// }

// let genRandomPassword = () => {
// 	let password = "COP_";
// 	let funcs = [getRandomUpperCase, getRandomNumber, getRandomSymbol, getRandomLowerCase];
// 	for (let i = 0; i < 4; i++) {
// 		for (let j = 0; j < 2; j++) {
// 			password = password.concat([funcs[i]()]);
// 		}
// 	}
// 	return password;
// }

// let setRandomPassword = () => {
// 	document.querySelector("#accessibility_password").value = genRandomPassword();
// }


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
				password: {
					required: true
				},	
				assembly: {
					required: true
				}, 
				permission: {
					required: true
				},
                 
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
        var btn = formEl.find('[id="assign_accessibility"]');

        btn.on('click', function(e) {
			e.preventDefault();
			// generate the password
			// setRandomPassword();

            if (validator.form()) {
                // See: src\js\framework\base\app.js
                KTApp.progress(btn);
                //KTApp.block(formEl);

                // See: http://malsup.com/jquery/form/#ajaxSubmit
                formEl.ajaxSubmit({

                    url: "/accessibility_submit",

                    error: function(res, err) {
                        KTApp.unprogress(btn);
            
                        swal.fire({
                            "title": "Error",
                            "text": res.responseJSON.message, 
                            "type": "error",
                            "confirmButtonClass": "btn btn-brand btn-sm btn-bold"
                        });
                    },

                    success: function(res) {
                        KTApp.unprogress(btn);
						//KTApp.unblock(formEl);
						
						let img_url = "/static/assets/media/users/thecopkadna-users.png";
						$('#update_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
						document.querySelector("#accessibility_member_id").value = "";
						document.querySelector("#accessibility_assembly").value = "";
						document.querySelector("#accessibility_full_name").textContent = "";
						document.querySelector("#accessibility_email").textContent = "";
						document.querySelector("#accessibility_ministry").textContent = "";
						document.querySelector("#accessibility_group").textContent = "";
						// document.querySelector("#accessibility_permission").textContent = "";
						// document.querySelector("#accessibility_date_of_reg").textContent = "";
						$(".spin").attr("hidden", true);

                        swal.fire({
                            "title": "Success", 
                            "text": "Access granted successfully", 
                            "type": "success",
							"showCancelButton": false,
							"confirmButtonText": 'OK',
							"confirmButtonClass": "btn btn-primary"
						}).then((result) => {
							location.reload();
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
			formEl = $('#accessibility_form');
			
			initValidation();
			initSubmit();
        }
    };
}();

jQuery(document).ready(function() {    
    KTForm.init();
});


// search for user's data when member id field value length is 8
$("#accessibility_member_id").on("keyup", function(e) {
	e.stopImmediatePropagation();
    if ($(this).val().length >= 3) {
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
                    $('#update_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
					}
					document.querySelector("#accessibility_assembly").value = res.assembly;
					document.querySelector("#accessibility_full_name").textContent = fullName;
					document.querySelector("#accessibility_email").textContent = res.email;
					document.querySelector("#accessibility_ministry").textContent = res.ministry;
					document.querySelector("#accessibility_group").textContent = res.group;
					// document.querySelector("#accessibility_permission").textContent = "N/A"; //res.permission;
					// document.querySelector("#accessibility_date_of_reg").textContent = "N/A"; //res.date_of_reg;

					$(".spin").attr("hidden", true);
						
                } else {
                    let img_url = "/static/assets/media/users/thecopkadna-users.png";
                    $('#update_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
					document.querySelector("#accessibility_assembly").value = "";
					document.querySelector("#accessibility_full_name").textContent = "";
					document.querySelector("#accessibility_email").textContent = "";
					document.querySelector("#accessibility_ministry").textContent = "";
					document.querySelector("#accessibility_group").textContent = "";
					// document.querySelector("#accessibility_permission").textContent = "";
					// document.querySelector("#accessibility_date_of_reg").textContent = "";
                    $(".spin").attr("hidden", true);
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
        $('#update_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
        document.querySelector("#accessibility_assembly").value = "";
		document.querySelector("#accessibility_full_name").textContent = "";
		document.querySelector("#accessibility_email").textContent = "";
		document.querySelector("#accessibility_ministry").textContent = "";
		document.querySelector("#accessibility_group").textContent = "";
		// document.querySelector("#accessibility_permission").textContent = "";
		// document.querySelector("#accessibility_date_of_reg").textContent = "";
        $(".spin").attr("hidden", true);

    }
});

$("#accessibility_member_id").on("change", function(e) {
	e.preventDefault();
    $("#accessibility_member_id").trigger("keyup");
});

$("#upload_attendance").on('click', function(e) {
	$("#bva_modal").modal("toggle");
});


$(".accessibility_view_details").on("click", function(e) {
	let member_id = $(this).attr("name");
	clearViewAccessibility();
	$("#accessibility_details_spin").attr("hidden", false);
	$.ajax({
		method: "POST",

		url: "/view_accessibility/" + member_id,

		success: function(res) {
			$("#accessibility_details_spin").attr("hidden", true);
			
			let img_url = "/" + res.user_data.img.replaceAll("\\", "/");
			if (img_url === "/") {
				img_url = "/static/assets/media/users/thecopkadna-users.png";
			}
			$('#view_accessibility_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
			let full_name = res.user_data.last_name + ", " + res.user_data.first_name +" "+ res.user_data.other_names 
			document.querySelector("#view_accessibility_name").textContent = full_name;
			document.querySelector("#view_accessibility_member_id").textContent = res.user_data.member_id;
			document.querySelector("#view_accessibility_assembly").textContent = res.user_data.assembly;
			document.querySelector("#view_accessibility_ministry").textContent = res.user_data.ministry;
			document.querySelector("#view_accessibility_group").textContent = res.user_data.group;
			document.querySelector("#view_accessibility_email").textContent = res.user_data.email;
			document.querySelector("#view_accessibility_permission").textContent = res.view_accessibility_data.permission_edited;
		},

		error: function(res, status, error) {
			$("#accessibility_details_spin").attr("hidden", true);
			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
});


$("#delete_admin_btn").on("click", function(e) {
	let member_id = document.querySelector("#view_accessibility_member_id").textContent;
	$("#delete_accessibility_spin").attr("hidden", false);
	$.ajax({
		method: "POST",

		url: "/remove_accessibility/" + member_id,

		success: function(res) {
			$("#delete_accessibility_spin").attr("hidden", true);
			
			clearViewAccessibility();

			swal.fire({
				"title": "Success", 
				"text": res.message, 
				"type": "success",
				"showCancelButton": false,
				"confirmButtonText": 'OK',
				"confirmButtonClass": "btn btn-primary"
			}).then((result) => {
				location.reload();
			});
		},

		error: function(res, status, error) {
			$("#delete_accessibility_spin").attr("hidden", true);
			
			swal.fire({
				"title": "",
				"text": res.responseJSON.message, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
		}
	});
});

let clearViewAccessibility = () => {
	let img_url = "/static/assets/media/users/thecopkadna-users.png";
	$('#view_accessibility_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
	document.querySelector("#view_accessibility_name").textContent = "";
	document.querySelector("#view_accessibility_member_id").textContent = "";
	document.querySelector("#view_accessibility_assembly").textContent = "";
	document.querySelector("#view_accessibility_ministry").textContent = "";
	document.querySelector("#view_accessibility_group").textContent = "";
	document.querySelector("#view_accessibility_email").textContent = "";
	document.querySelector("#view_accessibility_permission").textContent = "";
};