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

// $("#update_attendance_btn").on("click", function(e){

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