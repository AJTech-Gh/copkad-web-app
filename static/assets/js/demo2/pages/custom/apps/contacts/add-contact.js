"use strict";

// https://keenthemes.com/keen/
// Class definition
var KTAppContactsAdd = function () {
	// Base elements
	var wizardEl;
	var formEl;
	var validator;
	var wizard;
	var avatar;
	
	// Private functions
	var initWizard = function () {
		// Initialize form wizard
		wizard = new KTWizard('kt_apps_contacts_add', {
			startStep: 1,
		});

		// Validation before going to next page
		wizard.on('beforeNext', function(wizardObj) {
			if (validator.form() !== true) {
				wizardObj.stop();  // don't go to the next step
			}
		})

		// Change event
		wizard.on('change', function(wizard) {
			KTUtil.scrollTop();

			// set random password
			// setRandomPassword();

			// set values for fullname in email in account settings
			showFullName();
			showEmail();

			// populate review and submit
			reviewDetails();
		});
	}

	var initValidation = function() {
		validator = formEl.validate({
			// Validate only visible fields
			ignore: ":hidden",
			// Validation rules
			rules: {
				// Step 1
				kt_apps_contacts_add_avatar: {
					required: false 
				},
				first_name: {
					required: true
				},	   
				last_name: {
					required: true
				},
				other_names: {
					required: false
				},
				gender: {
					required: true
				},
				occupation: {
					required: false
				},
				contact_phone_1: {
					required: true
				},	 
				contact_phone_2: {
					required: false
				},
				dob: {
					required: true
				},
				email: {
					required: false,
					email: false
				},
				marital_status: {
					required: true
				},
				assembly: {
					required: true
				},
				ministry: {
					required: true
				},
				assembly_groups: {
					required: false
				},
				password: {
					required: true
				},
				address_line_1: {
					required: true
				},
				address_line_2: {
					required: false
				},
				digital_address_code: {
					required: true
				},
				region: {
					required: true
				},
				district: {
					required: true
				},
				country: {
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
					"buttonStyling": false,
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			},

			// Submit valid form
			submitHandler: function (form) {
				
			}
		});   
	}

	var initSubmit = function() {
		var btn = formEl.find('[data-ktwizard-type="action-submit"]');

		btn.on('click', function(e) {
			e.preventDefault();

			if (validator.form()) {
				// See: src\js\framework\base\app.js
				KTApp.progress(btn);
				//KTApp.block(formEl);

				// See: http://malsup.com/jquery/form/#ajaxSubmit
				// Docs for ajaxSubmit: https://github.com/claviska/jquery-ajaxSubmit
				
				formEl.ajaxSubmit({

					url: "/add_user_submit",

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
						// https://sweetalert2.github.io/
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
								printDetails("review_and_submit_div", res.member_data);
								// reset the form
								location.href = "add_user";
							} else {
								// reset the form
								location.href = "add_user";
							}
						});
					},
				});
			}
		});
	}
	 
	var initAvatar = function() {
		avatar = new KTAvatar('kt_apps_contacts_add_avatar');
	}	

	return {
		// public functions
		init: function() {
			formEl = $('#kt_apps_contacts_add_form');

			initWizard(); 
			initValidation();
			initSubmit();
			initAvatar(); 
		}
	};
}();

jQuery(document).ready(function() {	
	KTAppContactsAdd.init();
});

// check if full name and contact are available
function checkNameContact() {
	let firstName = $("#first_name").val().trim();
	let lastName = $("#first_name").val().trim();
	let contact1 = $("#contact_phone_1").val().trim();
	if (firstName && lastName && contact1) {
		return true;
	}
	return false;
}

// save and continue
$("#save_continue").on('click', function(e) {
	e.preventDefault();

	KTApp.progress($("#save_continue"));

	var formEl = $('#kt_apps_contacts_add_form');

	if (checkNameContact()) {
		formEl.ajaxSubmit({

			url: "/add_user_save_continue",
	
			error: function(res, err) {
				KTApp.unprogress($("#save_continue"));
	
				swal.fire({
					"title": "",
					"text": res.responseJSON.message, 
					"type": "error",
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			},
	
			success: function(res) {
				KTApp.unprogress($("#save_continue"));
	
				swal.fire({
					"title": "", 
					"text": "Saved successfully!", 
					"type": "success",
					"confirmButtonClass": "btn btn-secondary"
				});
	
			}
		});
	} else {
		KTApp.unprogress($("#save_continue"));

		swal.fire({
			"title": "",
			"text": "Provide at least First Name, Last Name and Contact Phone 1 before saving", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
	}
});

// save and add new
$("#save_new").on('click', function(e) {
	e.preventDefault();

	KTApp.progress($("#save_new"));

	var formEl = $('#kt_apps_contacts_add_form');

	if (checkNameContact()) {
		formEl.ajaxSubmit({

			url: "/add_user_save_new",
	
			error: function(res, err) {
				KTApp.unprogress($("#save_new"));
	
				swal.fire({
					"title": "",
					"text": res.responseJSON.message, 
					"type": "error",
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			},
	
			success: function(res) {
				KTApp.unprogress($("#save_new"));
	
				swal.fire({
					"title": "", 
					"text": "Saved successfully!", 
					"type": "success",
					"confirmButtonClass": "btn btn-secondary"
				}).then((result) => {
					if (result.value) {
						// reset the form
						location.href = "add_user";
					}
				});
	
			}
		});
	} else {
		KTApp.unprogress($("#save_new"));

		swal.fire({
			"title": "",
			"text": "Provide at least First Name, Last Name and Contact Phone 1 before saving", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
	}
});


//Save and exit
$("#save_exits").on('click', function(e) {
	e.preventDefault();

	KTApp.progress($("#save_exits"));

	var formEl = $('#kt_apps_contacts_add_form');

	if (checkNameContact()) {
		formEl.ajaxSubmit({

			url: "/add_user_save_exit",
	
			error: function(res, err) {
				KTApp.unprogress($("#save_new"));
	
				swal.fire({
					"title": "",
					"text": res.responseJSON.message, 
					"type": "error",
					"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
				});
			},
	
			success: function(res) {
				KTApp.unprogress($("#save_exits"));
	
				swal.fire({
					"title": "", 
					"text": "Saved successfully!", 
					"type": "success",
					"confirmButtonClass": "btn btn-secondary"
				}).then((data) => {
					if (data.value){
						// reset the form
						location.href = "/";
					}
				});
	
			}
		});
	} else {
		KTApp.unprogress($("#save_exits"));

		swal.fire({
			"title": "",
			"text": "Provide at least First Name, Last Name and Contact Phone 1 before saving", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
	}
});

//Receive data and print on review
let reviewDetails = () => {

	let ids_to_take = ["full_name_read_only", "contact_phone_1", "contact_phone_2", "email", "dob", "address_line_1", 
	"address_line_2", "digital_address_code", "district", "region", "country", "gender", "occupation", "marital_status"];
	
	let ids_to_fill = ["review_name", "review_phone", "review_mail", "review_dob", "review_address_lines", 
	"review_digital_address", "review_dis_reg_country", "review_gender", "review_occupation", "review_marital"];

	let values = [];
	let val;
	for(let i = 0; i<ids_to_take.length; i++){
		let id = ids_to_take[i];
		if(id === "country" || id === "marital_status"){
			val = document.querySelector("#" + id).selectedOptions[0].textContent;
		}
		else{
	  		val = document.querySelector("#" + id).value;
		}
		values.push(val);
	}

	let name = values[0];

	let phone;
	if (values[2] === ""){
		phone = values[1];
	}else{
		phone = values[1] + " , " + values[2];
	}

	let email = values[3];
	let dob = values[4];

	let address;
	if (values[6] === ""){
		address = values[5];
	}
	else{
		address = values[5] + " , " +values[6];
	} 

	let digital_address = values[7];
	let dis_reg_country = values[8] +" , "+ values[9] +" , "+ values[10];

	let gender = values[11];
	let occupation = values[12];
	let marital_status = values[13];
	
	let review_list = [name, phone.trim(), email.trim(), dob, address.trim(), 
		digital_address.trim(), dis_reg_country, gender, occupation.trim(), marital_status];

	for (let i = 0; i < ids_to_fill.length; i++){
		let id = ids_to_fill[i];
		document.querySelector("#" + id).textContent = review_list[i];
	}



	//Get values from multiple selections
	let assembly = document.querySelector("#kt_select2_3").selectedOptions;
	if (assembly.length > 0) {
		assembly = assembly[0].textContent;
	} else {
		assembly = "";
	}

	let ministry = "";
	let selectedOptions = document.querySelector("#kt_select2_4").selectedOptions;
	for(let i = 0; i < selectedOptions.length; i++) {
		ministry = ministry.concat(', ', [selectedOptions[i].textContent]);
	}
	if(ministry.length > 1) {
		ministry = ministry.substring(1, ministry.length);
	}
	
	let group = document.querySelector("#kt_select2_5").selectedOptions;
	if (group.length > 0) {
		group = group[0].textContent;
	} else {
		group = "";
	}

	let affiliations = [assembly, ministry, group];
	let rev_affiliations_id = ["review_assembly", "review_ministry", "review_study_group"];

	for(let i = 0; i < affiliations.length; i++){
		let id = rev_affiliations_id[i];
		document.querySelector("#" + id).textContent = affiliations[i];
	}

}

let showFullName = () => {
	let fullName = "";
	let name_ids = ["first_name", "last_name", "other_names"];
	for(let i = 0; i < name_ids.length; i++){
		let id = name_ids[i];
		fullName = fullName + " " + document.querySelector("#" + id).value;
	}

	document.querySelector("#full_name_read_only").value = fullName.trim();
}

let showEmail = () => {
	let email = document.querySelector("#email").value.toLowerCase();
	document.querySelector("#email_readonly").value = email;
}

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
// 	document.querySelector("#password").value = genRandomPassword();
// }

// display the selected photo
$("#kt_apps_contacts_add_avatar").on("change", function () {
    var acceptedImgExt = ["jpg", "jpeg", "png"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase()
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			$('.kt-avatar__holder').attr("style", "background-image: url(" + window.URL.createObjectURL(this.files[0]) + 
			"); min-height: 200px; min-width:200px; background-position: center; ");
        } catch (error) {
            swal.fire({
				"title": "",
				"text": error, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
        }
    } else {
		swal.fire({
			"title": "",
			"text": "Unacceptable file format! Expected JPG(JPEG) or PNG", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
    }
});

// print the user's details
let printDetails =  (elementId, member_data) => {
	// get the content to print
	var details = document.querySelector("#" + elementId).innerHTML;
	// open the print window
	var print_area = window.open();
	// compose the document
	print_area.document.write("<!DOCTYPE html><html><head><style>* { font-size: 20px; }</style></head><body>" + `
				<div class="kt-content kt-grid__item kt-grid__item--fluid">
				<div class="row">
					<div class="col-lg-12">
						<div class="kt-portlet">
							<div class="kt-portlet__body kt-portlet__body--fit">
								<div class="kt-invoice-2">
									<div class="kt-invoice__wrapper">
										<div class="row kt-invoice__head">

											<div class="col">
												<h1>MEMBER DETAILS</h1>
											</div>
											
											<div class="col">
												<div class="kt-invoice__container kt-invoice__container--centered">
													<span class="kt-invoice__desc">
														<a href="#">
															<img src="/static/assets/media/logos/thecopnsema-2.png">
														</a>
														<span>The Church of Pentecost</span>
														<span>Kwadaso Area | Kwadaso Agric District || Nsema Assemblies</span>
														<span>Post Office Box, KW 101. </span>
														<span>Kwadaso - Kumasi</span>
														<span>Tel : +233 570 364 383</span>
														<span>Email: info@thecopkadna.com</span>
													</span>
												</div>
											</div>
											
										</div>
										<!-- body -->
										<div class="kt-invoice__body kt-invoice__body--centered">
											<div class="row">
												<div class="col"></div>
												<div class="col">
													<img src="/` + member_data.img.replaceAll('\\', '/') + `" style="min-width: 200px; min-height: 200px; max-width: 200px; max-height: 200px; object-fit:contain;" />
												</div>
												<div class="col"></div>
											</div>
											<br />
											<div class="row">
												<div class="col">
													<strong>Member ID:</strong><br/>
													<label>` + member_data.member_id + `</label>
												</div>
												<div class="col">
													<strong>Full name:</strong><br/>
													<label>` + member_data.last_name + ", " + member_data.first_name + " " + member_data.other_names + `</label>
												</div>
												<div class="col">
													<strong>Gender:</strong><br/>
													<label>` + member_data.gender + `</label>
												</div>
											</div>
											<br/>
											<div class="row">
												<div class="col">
													<strong>Email:</strong><br/>
													<label>` + member_data.email + `</label>
												</div>
												<div class="col">
													<strong>Date of Birth:</strong><br/>
													<label>` + member_data.dob + `</label>
												</div>
												<div class="col">
													<strong>Occupation:</strong><br/>
													<label>` + member_data.occupation + `</label>
												</div>
											</div>
											<br/>
											<div class="row">
												<div class="col">
													<strong>Marital Status:</strong><br/>
													<label>` + member_data.marital_status + `</label>
												</div>
												<div class="col">
													<strong>Address:</strong><br/>
													<label>` + member_data.address_line_1 + `</label>
													<label>` + member_data.address_line_2 + `</label>
												</div>
												<div class="col">
													<strong>Digital Address:</strong><br/>
													<label>` + member_data.digital_address_code + `</label>
												</div>
											</div>
											<br/>
											<div class="row">
												<div class="col">
													<strong>District:</strong><br/>
													<label>` + member_data.district + `</label>
												</div>
												<div class="col">
													<strong>Region:</strong><br/>
													<label>` + member_data.region + `</label>
												</div>
												<div class="col">
													<strong>Country:</strong><br/>
													<label>` + member_data.country + `</label>
												</div>
											</div>
											<br/>
											<div class="row">
												<div class="col">
													<strong>Assembly:</strong><br/>
													<label>` + member_data.assembly + `</label>
												</div>
												<div class="col">
													<strong>Ministry:</strong><br/>
													<label>` + member_data.ministry + `</label>
												</div>
												<div class="col">
													<strong>Bible Studies Group:</strong><br/>
													<label>` + member_data.group + `</label>
												</div>
											</div>
											<br/>
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
	// print_area.document.write("<html><head><title>User Details</title>"
	// 							+ "<style>.kt-wizard-v1__review-title {font-size: 25; font-weight: bold; margin-top: 20px;} "
	// 							+ ".kt-wizard-v1__review-content {font-size: 20;}"
	// 							+ "</style></head>"
	// 							+ "<body style=\"padding: 20px;\">" 
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">COP</h1><br><br>"
	// 							+ "<h1 style=\"text-align: center; font-weight: bold;\">MEMBER ID:&nbsp" + memberId + "</h1>"
	// 							+ details + "</body></html>");
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
