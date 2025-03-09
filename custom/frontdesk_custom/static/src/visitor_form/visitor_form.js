
import { VisitorForm } from "@frontdesk/visitor_form/visitor_form";
import { Component, onMounted,useState, onWillUnmount, useRef } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { patch } from "@web/core/utils/patch";
patch(VisitorForm.prototype, {
   setup() {
//        this._super.apply(this, arguments);
        super.setup()
        this.inputPhoneRef = useRef("inputPhone");
        this.state=useState({'kam_list':[]})
        this.TotalQuantity()
        onMounted(() => {
        const phoneInput = this.inputPhoneRef.el;
        if (phoneInput) {
            phoneInput.addEventListener("input", this.formatPhoneNumber);
        }
    });

    onWillUnmount(() => {
        const phoneInput = this.inputPhoneRef.el;
        if (phoneInput) {
            phoneInput.removeEventListener("input", this.formatPhoneNumber);
        }
    });
    },
    formatPhoneNumber(event) {
    let value = event.target.value.replace(/\D/g, ""); // Remove non-numeric characters

    if (value.length > 3) {
        value = `(${value.substring(0, 3)}) ${value.substring(3, 16)}`;
    }

    event.target.value = value;
},
   async TotalQuantity(){
       let data = await rpc("/frontdesk/kam_list",{})
       this.state.kam_list = data.kam_list

   },
   async _onSubmit() {

    // Get the selected KAM ID
    const selectedKAM = document.getElementById("kam_id")?.value;
    const kam_id = selectedKAM && selectedKAM !== "" ? parseInt(selectedKAM, 10) : false;
    const station_id = this.props.stationInfo?.id || false;
    // Prepare data to send
    let visitorData = {
        name: this.inputNameRef.el.value,
        phone: this.inputPhoneRef.el?.value || false,
        email: this.inputEmailRef.el?.value || false,
        company: this.inputCompanyRef.el?.value || false,
        kam_id: kam_id,
        station_id: station_id,
    };
     this.props.setVisitorData(
            this.inputNameRef.el.value,
            this.inputPhoneRef.el?.value || false,
            this.inputEmailRef.el?.value || false,
            this.inputCompanyRef.el?.value || false
        );

    // Send data to the backend
    let response = await rpc("/frontdesk/visitor/save", {
        method: "call",
        args: [visitorData],
    });
//
    if (response.status === "success") {
        console.log("Visitor saved successfully with ID:", response.visitor_id);
        this.props.showScreen("RegisterPage");  // Redirect to next screen
    } else {
        console.error("Error saving visitor.");
    }
}

});
