"use strict";

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
			//KTUtil.scrollTop();	

			// write form data to cookies
			// writeAddUserCookies();

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
				profile_avatar: {
					//required: true 
				},
				profile_first_name: {
					required: true
				},	   
				profile_last_name: {
					required: true
				},
				profile_phone: {
					required: true
				},	 
				profile_email: {
					required: true,
					email: true
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
							"text": "The application has been successfully submitted!", 
							"type": "success",
							"confirmButtonClass": "btn btn-secondary"
						});

						// reset the form
						location.href = "add_user";
						formEl[0].reset();
					}
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

//Receive data and print on review
	let reviewDetails = () => {

		// Name:
		// Phone:
		// Email:
		// Date of Birth:
		// Address Details
		// Address:
		// Digital Address :
		// District | Region | Country:
		// Affiliations
		// Assembly:
		// Ministry:
		// District:
		// Bible Studies Group:
		

		let ids_to_take = ["full_name_read_only", "contact_phone_1", "contact_phone_2", "email", "dob", "address_line_1", "address_line_2",
							"digital_address_code", "district", "region", "country"];
		
		let ids_to_fill = ["review_name", "review_phone", "review_mail", "review_dob", "review_address_lines", "review_digital_address", 
		"review_dis_reg_country", ];

		let values = [];

		for(let i = 0; i<ids_to_take.length; i++){
			let id = ids_to_take[i];
			let val = document.querySelector("#" + id).value;
			values.push(val);
		}

		let name = values[0];

		let phone;
		if (values[2] === ""){
			phone = values[1]
		}else{
			phone = values[1] + " , " + values[2];
		}

		let email = values[3];
		let dob = values[4];

		let address;
		if (values[6] === ""){
			address = values[5]
		}
		else{
			address = values[5] + " , " +values[6];
		} 

		let digital_address = values[7];
		let dis_reg_country = values[8] +" , "+ values[9] +" , "+ values[10];
		
		let review_list = [name, phone.trim(), email.trim(), dob, address.trim(), digital_address.trim(), dis_reg_country];

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


// display the selected photo
$("#kt_apps_contacts_add_avatar").on("change", function () {
    var acceptedImgExt = ["jpg", "jpeg", "png", "gif"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase()
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			$('.kt-avatar__holder').attr("style", "background-image: url(" + window.URL.createObjectURL(this.files[0]) + 
			"); background-position: center; ");
        } catch (error) {
            // do nothing  console.log(error)
        }
    } else {
        // $("#src-image-text").text("Unacceptable file format! Expected JPG(JPEG), PNG OR GIF");
    }
});