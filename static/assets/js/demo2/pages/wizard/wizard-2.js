"use strict";

// Class definition
var KTWizard2 = function () {
    // Base elements
    var wizardEl;
    var formEl;
    var validator;
    var wizard;
    
    // Private functions
    var initWizard = function () {
        // Initialize form wizard
        wizard = new KTWizard('kt_wizard_v2', {
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
            reviewBaptismDetails();  
        });
    }

    var initValidation = function() {
        validator = formEl.validate({
            // Validate only visible fields
            ignore: ":hidden",

            // Validation rules
            rules: {
               	//= Step 1
				first_name: {
					required: true 
				},
				assembly: {
					required: true
				},	   
				contacts: {
					required: true
				},	 
				email: {
					required: false,
					email: true
				},	 

				//= Step 2
				kt_datetimepicker_6: {
					required: true 
				},
				place_of_baptism: {
					required: true
				},	   
				officiating_minister: {
					required: true
                },	
                area: {
                    required: true
                },
                district: {
                    required: true
                },
				country: {
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
        var btn = formEl.find('[data-ktwizard-type="action-submit"]');

        btn.on('click', function(e) {
            e.preventDefault();

            if (validator.form()) {
                // See: src\js\framework\base\app.js
                KTApp.progress(btn);
                //KTApp.block(formEl);

                // See: http://malsup.com/jquery/form/#ajaxSubmit
                formEl.ajaxSubmit({

                    url: "/baptism_certificates_submit",

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
								printDetails(res.baptism_data);
								// reset the form
								location.href = "baptism_certificates";
							} else {
								// reset the form
								location.href = "baptism_certificates";
							}
                        });
                    }
                });
            }
        });
    }

    return {
        // public functions
        init: function() {
            wizardEl = KTUtil.get('kt_wizard_v2');
            formEl = $('#kt_form');

            initWizard(); 
            initValidation();
            initSubmit();
        }
    };
}();

jQuery(document).ready(function() {    
    KTWizard2.init();
});

function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode >= 48 && charCode <= 57) {
        return true;
    }
    return false;
}

let reviewBaptismDetails = () => {
    let ids_to_take = ["full_name", "contacts", "email", "assembly", "district", "area", 
    "kt_datetimepicker_6", "place_of_baptism", "officiating_minister"];

    let ids_to_fill = ["review_name", "review_contact", "review_email", "review_assembly", 
    "review_district", "review_area", "review_date_of_baptism", "review_place_of_baptism", "review_off_minister"];

    let val;
    let values = [];

    for(let i=0; i < ids_to_take.length; i++){
        let id = ids_to_take[i];
	  	val = document.querySelector("#" + id).value;
        values.push(val);
    }

    for (let i=0; i < ids_to_fill.length; i++){
        let id = ids_to_fill[i];
        document.querySelector("#"+id).textContent = values[i];
    }
    
}

// replace all in a string
let replaceAll = (string, search, replace) => {
    return string.split(search).join(replace);
}

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
                    let img_url = "/" + replaceAll(res.img, "\\", "/");
                    if (img_url === "/") {
                        img_url = "/static/assets/media/users/thecopkadna-users.png";
                    }
                    $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
                    }
                    document.querySelector("#full_name").value = fullName;
                    document.querySelector("#assembly").value = res.assembly;
                    let contacts = res.contact_1;
                    if (res.contact_2) {
                        contacts = contacts + ", " + res.contact_2;
                    }
                    document.querySelector("#contacts").value = contacts;
            
                    if(res.email){
                        document.querySelector("#email").value = res.email;
                    }else{
                        document.querySelector("#email").value = "";
                    }
                } else {
                    let img_url = "/static/assets/media/users/thecopkadna-users.png";
                    $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    document.querySelector("#full_name").value = "";
                    document.querySelector("#assembly").value = "";
                    document.querySelector("#contacts").value = "";
                    document.querySelector("#email").value = "";
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
        document.querySelector("#contacts").value = "";
        document.querySelector("#email").value = "";
        $(".spin").attr("hidden", true);
        $("#record_id_div").attr("hidden", true);

    }
});

$("#member_id").on("change", function(e) {
    $("#member_id").trigger("keyup");
});

// print the user's details
let printDetails =  (baptism_data) => {
	// get the content to print
	// var details = document.querySelector("#" + elementId).innerHTML;
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
														<div class="kt-invoice__head">
															<div class="kt-invoice__container kt-invoice__container--centered">
																<div class="kt-invoice__logo">
																	<a href="#">
																		<h1>BAPTISM CERTIFICATE DATA</h1>
																	</a>
																	<a href="#">
																		<img src="/static/assets/media/logos/thecopnsema-2.png">
																	</a>
																</div>
																<span class="kt-invoice__desc">
																	<span>The Church of Pentecost</span>
																	<span>Kwadaso Area | Kwadaso Agric District || Nsema Assemblies</span>
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
																	<strong>Record ID:</strong><br/>
																	<label>` + baptism_data.record_id + `</label>
																</div>
																<div class="col">
																	<strong>Member ID:</strong><br/>
																	<label>` + baptism_data.member_id + `</label>
																</div>
																<div class="col">
																	<strong>Full Name:</strong><br/>
																	<label>` + baptism_data.full_name + `</label>
																</div>
															</div>
															<br/>
															<div class="row">
																<div class="col">
																	<strong>Assembly:</strong><br/>
																	<label>` + baptism_data.date_of_baptism + `</label>
																</div>
																<div class="col">
																	<strong>Date of Baptism:</strong><br/>
																	<label>` + baptism_data.place_of_baptism + `</label>
																</div>
																<div class="col">
																	<strong>Officiating Minister:</strong><br/>
																	<label>` + baptism_data.officiating_minister + `</label>
																</div>
															</div>
															<br/>
															<div class="row">
																<div class="col">
																	<strong>District:</strong><br/>
																	<label>` + baptism_data.district + `</label>
																</div>
																<div class="col">
																	<strong>Area:</strong><br/>
																	<label>` + baptism_data.area + `</label>
																</div>
																<div class="col">
                                                                    <strong>Country:</strong><br/>
                                                                    <label>` + baptism_data.country + `</label>
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

// handle scanned file upload
// $(".custom-file-input").on("change", function() {
//     var fileName = $(this).val().split("\\").pop();
//     $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
// });

$("#certImagInput").on("change", function () {
    var acceptedImgExt = ["jpg", "jpeg", "png"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase()
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			$('#certImagDisplay').attr("src", window.URL.createObjectURL(this.files[0]));
        } catch (error) {
            // do nothing  
            // console.log(error)
        }
    } else {
        // $("#src-image-text").text("Unacceptable file format! Expected JPG(JPEG), PNG OR GIF");
    }
});