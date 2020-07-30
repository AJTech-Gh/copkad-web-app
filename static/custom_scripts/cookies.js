"use strict";

// defines the separator to use when storing the selected church affiliation cookies
let affiliationValsSep = "|";

function writeAddUserCookies() {
  // get the for elements
  let member_id = document.querySelector("#member_id");
  let first_name = document.querySelector("#first_name");
  let last_name = document.querySelector("#last_name");
  let other_names = document.querySelector("#other_names");
  let gender = document.querySelector("#gender");
  let occupation = document.querySelector("#occupation");
  let contact_phone_1 = document.querySelector("#contact_phone_1");
  let contact_phone_2 = document.querySelector("#contact_phone_2");
  let dob = document.querySelector("#dob");
  let email = document.querySelector("#email");
  let marital_status = document.querySelector("#marital_status");
  let church_affiliation = document.querySelector("#kt_select2_3");
  let full_name = document.querySelector("#full_name");
  let email_readonly = document.querySelector("#email_readonly");
  let password = document.querySelector("#password");
  let confirm_password = document.querySelector("#confirm_password");
  let comm_email = document.querySelector("#comm_email");
  let comm_sms = document.querySelector("#comm_sms");
  let comm_phone = document.querySelector("#comm_phone");
  let address_line_1 = document.querySelector("#address_line_1");
  let address_line_2 = document.querySelector("#address_line_2");
  let digital_address_code = document.querySelector("#digital_address_code");
  let region = document.querySelector("#region");
  let district = document.querySelector("#district");
  let country = document.querySelector("#country");
  // set the cookies
  document.cookie = member_id.name + "=" + escape(member_id.value) + ";";
  document.cookie = first_name.name + "=" + escape(first_name.value) + ";";
  document.cookie = last_name.name + "=" + escape(last_name.value) + ";";
  document.cookie = other_names.name + "=" + escape(other_names.value) + ";";
  document.cookie = gender.name + "=" + escape(gender.value) + ";";
  document.cookie = occupation.name + "=" + escape(occupation.value) + ";";
  document.cookie = contact_phone_1.name + "=" + escape(contact_phone_1.value) + ";";
  document.cookie = contact_phone_2.name + "=" + escape(contact_phone_2.value) + ";";
  document.cookie = dob.name + "=" + escape(dob.value) + ";";
  document.cookie = email.name + "=" + escape(email.value) + ";";
  document.cookie = marital_status.name + "=" + escape(marital_status.value) + ";";
  let affiliationVals = "";
  let selectedOptions = church_affiliation.selectedOptions;
  for(let i = 0; i < selectedOptions.length; i++) {
    affiliationVals = affiliationVals.concat(affiliationValsSep, [selectedOptions[i].value]);
  }
  if(affiliationVals.length > 1) {
  affiliationVals = affiliationVals.substring(1, affiliationVals.length);
  }
  document.cookie = church_affiliation.name + "=" + escape(affiliationVals) + ";";
  document.cookie = full_name.name + "=" + escape(full_name.value) + ";";
  document.cookie = email_readonly.name + "=" + escape(email_readonly.value) + ";";
  document.cookie = password.name + "=" + escape(password.value) + ";";
  document.cookie = confirm_password.name + "=" + escape(confirm_password.value) + ";";
  document.cookie = comm_email.name + "=" + escape(comm_email.checked) + ";";
  document.cookie = comm_sms.name + "=" + escape(comm_sms.checked) + ";";
  document.cookie = comm_phone.name + "=" + escape(comm_phone.checked) + ";";
  document.cookie = address_line_1.name + "=" + escape(address_line_1.value) + ";";
  document.cookie = address_line_2.name + "=" + escape(address_line_2.value) + ";";
  document.cookie = digital_address_code.name + "=" + escape(digital_address_code.value) + ";";
  document.cookie = region.name + "=" + escape(region.value) + ";";
  document.cookie = district.name + "=" + escape(district.value) + ";";
  document.cookie = country.name + "=" + escape(country.value) + ";";
  document.cookie = "SameSite=Lax;";
}
