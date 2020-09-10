"use strict";
var KTDatatablesBasicPaginations1 = function() {

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
					messageTop: 'PROMOTIONS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[ 0, ':visible' ]
					}
				},
				{
					filename: 'COP_cr_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'PROMOTIONS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'PROMOTIONS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'PROMOTIONS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_print',
					extend: 'print',
					title: 'COP',
					messageTop: 'PROMOTIONS',
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
	KTDatatablesBasicPaginations1.init();
});

// search for user's data when member id field value length is 8
$("#pro_member_id").on("keyup", function(e) {
    if ($(this).val().length === 8) {
        $(".spin").attr("hidden", false);
        $.ajax({
            method: "POST",

            url: "/load_user_by_id/pro_member_id",

            data: $(this).serialize(),

            success: function(res) {
                $(".spin").attr("hidden", true);
                if (res.first_name) {
                    let img_url = "/" + res.img.replaceAll("\\", "/");
                    if (img_url === "/") {
                        img_url = "/static/assets/media/users/thecopkadna-users.png";
                    }
                    $('#pro_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
                    }
                    document.querySelector("#pro_full_name").value = fullName;
                    let assemblies = {
                        EEA: "Emmanuel",
                        GA: "Glory",
                        HA: "Hope"
                    }
				   
					document.querySelector("#pro_assembly").value = assemblies[res.assembly];
						
                } else {
                    let img_url = "/static/assets/media/users/thecopkadna-users.png";
                    $('#pro_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    document.querySelector("#pro_full_name").value = "";
                    document.querySelector("#pro_assembly").value = "";
                    $(".spin").attr("hidden", true);
                    $("#pro_record_id_div").attr("hidden", true);
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
        document.querySelector("#pro_full_name").value = "";
        document.querySelector("#pro_assembly").value = "";
        $(".spin").attr("hidden", true);
        $("#pro_record_id_div").attr("hidden", true);

    }
});

$("#pro_member_id").on("change", function(e) {
    $("#pro_member_id").trigger("keyup");
});

// Class definition
var KTForm1 = function () {
    // Base elements
    var proFormEl;
    var proValidator;

    var initValidation1 = function() {
		
        proValidator = proFormEl.validate({
            // Validate only visible fields
            ignore: ":hidden",

			// Validation rules
            rules: {
               	//= Step 1
				pro_member_id: {
					required: true
				},   
				pro_full_name: {
					required: true
				},	 
				pro_assembly: {
					required: true
				},
				age: {
					required: true
				},
				pro_present_portfolio: {
					required: true
				},
				pro_promoted_portfolio: {
					required: true
				},
				pro_specify_portfolio: {
					required: true
				},
				pro_date_of_promotion: {
					required: true
				},
				pro_ordination_minister: {
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

    var initSubmit1 = function() {
        var btn = proFormEl.find('[id="submit_promotion"]');

        btn.on('click', function(e) {
            e.preventDefault();

            if (proValidator.form()) {
                // See: src\js\framework\base\app.js
                KTApp.progress(btn);
                //KTApp.block(formEl);

                // See: http://malsup.com/jquery/form/#ajaxSubmit
                proFormEl.ajaxSubmit({

                    url: "/promotion_submit",

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
								proPrintDetails(res);
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
			proFormEl = $('#promotion_form');
			
			initValidation1();
			initSubmit1();
        }
    };
}();

jQuery(document).ready(function() {    
    KTForm1.init();
});