"use strict";

// Class definition
var KTAppUserProfile = function () {

	// Private functions
	var initAside = function () {
		// Mobile offcanvas for mobile mode
		var offcanvas = new KTOffcanvas('kt_user_profile_aside', {
            overlay: true,  
            baseClass: 'kt-app__aside',
            closeBy: 'kt_user_profile_aside_close',
            toggleBy: 'kt_subheader_mobile_toggle'
        }); 
	}

	return {
		// public functions
		init: function() {
			initAside();
		}
	};
}();

KTUtil.ready(function() {	
	KTAppUserProfile.init();
});


$("#upload_attendance").on('click', function(e) {
	$("#bva_modal").modal("toggle");
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
				attendance_file: {
					required: true
				},
            },
            
            // Display error  
            invalidHandler: function(event, validator) {     
                //KTUtil.scrollTop();

                swal.fire({
                    "title": "", 
                    "text": "No file selected!", 
                    "type": "error",
                    "confirmButtonClass": "btn btn-secondary"
                });
            },

            // Submit valid form
            // submitHandler: function (form) {
                
            // }
        });   
	}

    var initSubmit = function() {
        var btn = formEl.find('[id="upload_attendance_btn"]');

        btn.on('click', function(e) {
			e.preventDefault();
			
			KTApp.progress(btn);

			// See: http://malsup.com/jquery/form/#ajaxSubmit
			formEl.ajaxSubmit({

				url: "/upload_attendance",

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
						"confirmButtonText": 'OK',
						"confirmButtonClass": "btn btn-primary",
					}).then((result) => {
						location = "overview";
					});
				}
			});
        });
    }

    return {
        // public functions
        init: function() {
			formEl = $('#attendance_form');
			
			initValidation();
			initSubmit();
        }
    };
}();

jQuery(document).ready(function() {    
    KTForm.init();
});


// Add the following code if you want the name of the file appear on select
// $(".custom-file-input").on("change", function() {
// 	var fileName = $(this).val().split("\\").pop();
// 	$(this).siblings(".custom-file-label").addClass("selected").html(fileName);
// });


$("#reset_form").on("click", function() {
	document.querySelector("#attendance_file").value = null;
	document.querySelector("#attendance_file_label").textContent = "Choose file";
});

//$("#update_attendance_btn").on("click", function(e){
// 	$.ajax({
// 		method: "POST",

// 		url: "/upload_attendance",

// 		success: function(res) {
// 			swal.fire({
// 				"title": "", 
// 				"text": "Attendance updated Successfully!", 
// 				"type": "success",
// 				"confirmButtonClass": "btn btn-secondary"
// 			});
// 		},

// 		error: function(res, status, error) {
// 			swal.fire({
// 				"title": "",
// 				"text": res.responseJSON.message, 
// 				"type": "error",
// 				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
// 			});
// 		}
// 	});
// });


$("#kt_select2_3").select2({
	dropdownAutoWidth : true
});