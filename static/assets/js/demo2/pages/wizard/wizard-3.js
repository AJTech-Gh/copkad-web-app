"use strict";

// Class definition
var KTWizard3 = function () {
	// Base elements
	var wizardEl;
	var formEl;
	var validator;
	var wizard;
	
	// Private functions
	var initWizard = function () {
		// Initialize form wizard
		wizard = new KTWizard('kt_wizard_v3', {
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
			reviewDetails();
		});
	}

	var initValidation = function() {
		validator = formEl.validate({
			// Validate only visible fields
			ignore: ":hidden",

			// Validation rules
			rules: {
				//= Step 1
				church_name: {
					required: true 
				},
				assembly_name: {
					required: true
				},	   
				district_name: {
					required: true
				},	 
				area_name: {
					required: true
				},	 
				address_line_1: {
					required: true
				},	 
				region: {
					required: true
				},
				country: {
					required: true
				},	

				// Step 4
				contact: {
					required: true
				},
				email: {
					required: true
				},	
				e_password: {
					required: true
				},
			},
			
			// Display error  
			invalidHandler: function(event, validator) {	 
				KTUtil.scrollTop();

				swal.fire({
					"title": "", 
					"text": "Please complete the form.", 
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

					url: "/settings_submit",

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
							"text": "Settings saved successfully!", 
							"type": "success",
							"confirmButtonClass": "btn btn-secondary"
						}).then((result => {
							// reset the form
							location.href = "settings";
						}));
					}
				});
			}
		});
	}

	return {
		// public functions
		init: function() {
			wizardEl = KTUtil.get('kt_wizard_v3');
			formEl = $('#kt_form');

			initWizard(); 
			initValidation();
			initSubmit();
		}
	};
}();

jQuery(document).ready(function() {	
	KTWizard3.init();
});

/* Adds Element BEFORE NeighborElement */
Element.prototype.appendBefore = function (element) {
	element.parentNode.insertBefore(this, element);
}, false;

/* Adds Element AFTER NeighborElement */
Element.prototype.appendAfter = function (element) {
	element.parentNode.insertBefore(this, element.nextSibling);
}, false;


let reviewDetails = () => {
	//Start -> Detail of Assembly
    let ids_to_take = ["address_line_1", "address_line_2", "district_name", "region", "country"];

    let ids_to_fill = ["rev_address_line_1","rev_address_line_2", "rev_district_name", "rev_region", "rev_country"];

    let val;
    let values = [];

    for(let i=0; i < ids_to_take.length; i++){
		let id = ids_to_take[i];
		if (id ==="country"){
			val = document.querySelector("#" + id).selectedOptions[0].textContent;
		}
	  	val = document.querySelector("#" + id).value;
        values.push(val);
    }

    for (let i=0; i < ids_to_fill.length; i++){
        let id = ids_to_fill[i];
        document.querySelector("#"+id).textContent = values[i];
	}
	//-> Detail of Assembly

	//Start -> Review of financial structure 
	let repeaterList = document.getElementsByClassName('repeater_list');
	let nodeList = [];

	for (let i=0; i < repeaterList.length; i++){
		nodeList.push(document.getElementsByName("[" + i + "][name_of_offering]"));
		nodeList.push(document.getElementsByName("[" + i + "][type_of_offering]"));
		nodeList.push(document.getElementsByName("[" + i + "][percentage_deduction]"));
		nodeList.push(document.getElementsByName("[" + i + "][offering_code]"));

	}

	//console.log(nodeList);
	
	let nodeValues = [];

	nodeList.forEach(items =>{
		items.forEach(item =>{
			nodeValues.push(item.value);
		});
	});

	let span = document.createElement("DIV");
	for(let i=0; i < nodeValues.length; i+=4){
		if (nodeValues[i+1] && nodeValues[i+3] && nodeValues[i+2]){
			span.innerHTML += nodeValues[i+1] + " | Code: " + nodeValues[i+3] + " | " + nodeValues[i+2] +"% Deduction";
			span.innerHTML += "<br>";
		}
		else if(nodeValues[i+1] && nodeValues[i+3] && !nodeValues[i+2]){
			span.innerHTML += nodeValues[i+1] + " | Code: " + nodeValues[i+3] + " | "  +"No Deduction";
			span.innerHTML += "<br>";
		}
	}
	document.querySelector("#rev_fin_items").innerHTML = span.innerHTML;
//End -> Review of financial structure 

//Start -> Review Ministries
	let ministryRepeaterList = document.getElementsByClassName('ministry_repeater_list');
	let ministryNodeList = [];

	for (let i=0; i < ministryRepeaterList.length; i++){
		ministryNodeList.push(document.getElementsByName("[" + i + "][ministry]"));
	}

	//console.log(ministryNodeList);
	
	let ministryNodeValues = [];

	ministryNodeList.forEach(items =>{
		items.forEach(item =>{
			ministryNodeValues.push(item.value);
		});
	});

	let ministrySpan = document.createElement("DIV");
	for(let i=0; i < ministryNodeValues.length; i++){
		if (ministryNodeValues[i]){
			ministrySpan.innerHTML += ministryNodeValues[i];
			ministrySpan.innerHTML += "<br>";
		}
	}
	document.querySelector("#rev_ministries").innerHTML = ministrySpan.innerHTML;
//End -> Review Ministries
	

//Start -> Review Groups
let groupsRepeaterList = document.getElementsByClassName('group_repeater_list');
let groupsNodeList = [];

for (let i=0; i < groupsRepeaterList.length; i++){
	groupsNodeList.push(document.getElementsByName("[" + i + "][group]"));
}

//console.log(nodeList);

let groupNodeValues = [];

groupsNodeList.forEach(items =>{
	items.forEach(item =>{
		groupNodeValues.push(item.value);
	});
});

let groupSpan = document.createElement("DIV");
for(let i=0; i < groupNodeValues.length; i++){
	if (groupNodeValues[i]){
		groupSpan.innerHTML += groupNodeValues[i];
		groupSpan.innerHTML += "<br>";
	}
}
document.querySelector("#rev_groups").innerHTML = groupSpan.innerHTML;
//End -> Review Groups
let assembly_name = document.getElementById("assembly_name").value;
console.log(assembly_name);
let list = document.querySelectorAll(".dis_assembly_name");
list.forEach(e => e.textContent = assembly_name);


}//End of review

/**
 * Toggles the visibility of the email password
 */
function toggleEmailPassword() {
	let x = document.querySelector("#e_password");
	if (x.type === "password") {
		x.type = "text";
	} else {
		x.type = "password";
	}
}

$("#logo_upload").on("change", function () {
    var acceptedImgExt = ["jpg", "jpeg", "png"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase();
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			// $(this).val(window.URL.createObjectURL(this.files[0]));
        } catch (error) {
			$(this).val("Choose file");
            swal.fire({
				"title": "",
				"text": error, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
        }
    } else {
		$(this).val("Choose file");
        swal.fire({
			"title": "",
			"text": "Unacceptable file format! Expected JPG(JPEG) or PNG", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
    }
});

$("#letter_head").on("change", function () {
    var acceptedImgExt = ["jpg", "jpeg", "png"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase();
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			// $(this).val(window.URL.createObjectURL(this.files[0]));
        } catch (error) {
			$(this).val("Choose file");
            swal.fire({
				"title": "",
				"text": error, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
        }
    } else {
		$(this).val("Choose file");
        swal.fire({
			"title": "",
			"text": "Unacceptable file format! Expected JPG(JPEG) or PNG", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
    }
});

$("#baptism_cert_template").on("change", function () {
    var acceptedImgExt = ["pdf"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase();
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			// $(this).val(window.URL.createObjectURL(this.files[0]));
        } catch (error) {
			$(this).val("Choose file");
            swal.fire({
				"title": "",
				"text": error, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
        }
    } else {
		$(this).val("Choose file");
        swal.fire({
			"title": "",
			"text": "Unacceptable file format! Expected PDF", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
    }
});

$("#dedication_cert_template").on("change", function () {
    var acceptedImgExt = ["pdf"];
    var filePath = $(this).val();
    var fileName = filePath.split("\\").pop();
    var fileNameExt = fileName.split(".");
    var fileExt = fileNameExt[fileNameExt.length - 1].toLowerCase();
    if (acceptedImgExt.indexOf(fileExt) > -1) {
        try {
			// $(this).val(window.URL.createObjectURL(this.files[0]));
        } catch (error) {
			$(this).val("Choose file");
            swal.fire({
				"title": "",
				"text": error, 
				"type": "error",
				"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
			});
        }
    } else {
		$(this).val("Choose file");
        swal.fire({
			"title": "",
			"text": "Unacceptable file format! Expected PDF", 
			"type": "error",
			"confirmButtonClass": "btn btn-brand btn-sm btn-bold"
		});
    }
});