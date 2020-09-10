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
					filename: 'COP_cr_csv',
					extend: 'csv',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_excel',
					extend: 'excelHtml5',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_pdf',
					extend: 'pdfHtml5',
					title: 'COP',
					messageTop: 'TRANSFERS',
					messageBottom: 'END OF DOCUMENT',
					exportOptions: {
						columns: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] //[0, ':visible']
					}
				},
				{
					filename: 'COP_cr_print',
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
                            <a onclick="printRowData(this.parentElement.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" data-toggle="dropdown" aria-expanded="true" title="Print">
                              <i class="la la-print"></i>
                            </a>
                        </span>
                        <a onclick="viewRowData(this.parentElement.parentElement)" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="View">
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
                    $('#pro_kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ");
                    let fullName = res.last_name + ", " + res.first_name;
                    if (res.other_names) {
                        fullName = fullName + " " + res.other_names;
                    }
                    document.querySelector("#pro_full_name").value = fullName;
						
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
        $('.kt-avatar__holder').attr("style", "background-image: url(" + img_url + "); background-position: center; ")
        document.querySelector("#trans_full_name").value = "";
        $(".spin").attr("hidden", true);
        $("#trans_record_id_div").attr("hidden", true);

    }
});

$("#trans_member_id").on("change", function(e) {
    $("#trans_member_id").trigger("keyup");
});