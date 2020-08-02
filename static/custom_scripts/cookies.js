"use strict";

// defines the separator to use when storing the selected church affiliation cookies
let multipleSelectSep = "|";

function writeAddUserCookies() {
  // get the for elements
  const general_ids = ["member_id", "first_name", "last_name", "other_names", "gender", "occupation", "contact_phone_1", 
  "contact_phone_2", "dob", "email", "marital_status", "kt_select2_3", "full_name", "email_readonly", "password", 
  "confirm_password", "comm_email", "comm_sms", "comm_phone", "address_line_1", "address_line_2", 
  "digital_address_code", "region", "district", "country"];
  const checkbox_ids = ["comm_email", "comm_sms", "comm_phone"];
  const multiple_select_ids = ["kt_select2_3"];
  // set all the cookies
  for(let i = 0; i < general_ids.length; i++) {
    // get the id text and the element
    let id = general_ids[i];
    let element = document.querySelector("#" + id);
    // handle checkboxes by getting a boolean for checked status
    if(checkbox_ids.includes(id)) {
      document.cookie = element.name + "=" + escape(element.checked) + ";";
      continue;
    }
    // handle multiple select boxes
    if(multiple_select_ids.includes(id)) {
      let selectedVals = "";
      let selectedOptions = element.selectedOptions;
      for(let i = 0; i < selectedOptions.length; i++) {
        selectedVals = selectedVals.concat(multipleSelectSep, [selectedOptions[i].value]);
      }
      if(selectedVals.length > 1) {
        selectedVals = selectedVals.substring(1, selectedVals.length);
      }
      document.cookie = element.name + "=" + escape(selectedVals) + ";";
      continue;
    }
    // handle other elements whose values are directly accessible by the value property
    document.cookie = element.name + "=" + escape(element.value) + ";";
  }
  // se the samesite value
  document.cookie = "SameSite=Lax;";
  // set expiry time for cookies to 30 minutes
  let now = new Date();
  now.setMinutes(now.getMinutes() + 30);
  document.cookie = "expires=" + now.toUTCString() + ";";
  // alert(document.cookie);
}


// function loadAddUserCookie()
document.addEventListener("DOMContentLoaded", function() {
  const ids = ["member_id", "first_name", "last_name", "other_names", "gender", "occupation", "contact_phone_1", 
  "contact_phone_2", "dob", "email", "marital_status", "kt_select2_3", "fullname", "email_readonly", "password", "confirm_password",
  "comm_email", "comm_sms", "comm_phone", "address_line_1", "address_line_2", "digital_address_code", "region", "district", "country"];

  const checkbox_ids = ["comm_email", "comm_sms", "comm_phone"];
  const multiple_select_ids = ["kt_select2_3"];

  let allCookies = document.cookie;

  // Obtain all the cookies pairs in an array
  let cookieList = allCookies.split(';');
  if (cookieList.length > 0) {
    // Take the name value pairs from the cokieList
    for(let i = 0; i < ids.length; i++) {
      let id = ids[i];
      let name = cookieList[i].split('=')[0];
      let value = unescape(cookieList[i].split('=')[1]);
      if (value === null) {
        value = "";
      }
      // handle checkboxes
      if (checkbox_ids.includes(id)){
        if (value === "true"){
          document.querySelector("#" + id).checked = true;
        }
        else{
          document.querySelector("#" + id).checked = false;
        }
        continue;
      }
      // handle multiple select boxes
      if(multiple_select_ids.includes(id)) {
        let selectValues = value.split("|");
        for(let i = 0; i < selectValues.length; i++) {
          // let select = document.querySelector("#" + id);
          /* Iterate options of select element */
            for (let option of document.querySelectorAll('#' + id + ' option')) {
              /* Parse value to integer */
              let val = Number.parseInt(option.value);
              /* If option value contained in values, set selected attribute */
              if (selectValues.indexOf(val) !== -1) {
                option.setAttribute('selected', 'selected');
                continue;
              }
              /* Otherwise ensure no selected attribute on option */
              else {
                option.removeAttribute('selected');
                continue;
              }
            }
          }
          continue;
        }
        document.querySelector("#" + id).value = value;
      }
  }
});