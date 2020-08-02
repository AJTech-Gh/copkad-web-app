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