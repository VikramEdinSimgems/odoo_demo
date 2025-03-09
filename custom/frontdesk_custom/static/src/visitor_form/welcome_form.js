
import { WelcomePage } from "@frontdesk/welcome_page/welcome_page";
import { Component, onMounted,useState, onWillUnmount, useRef } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { patch } from "@web/core/utils/patch";
patch(WelcomePage.prototype, {
   setup() {
        super.setup()
        if (this.props.stationInfo.self_check_in) {
            this._getQrCodeData();
            this.qrCodeInterval = setInterval(() => this._getQrCodeData(), 604800000); // 7 days
        }
        }
    });


