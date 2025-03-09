/** @odoo-module **/

import { registry } from "@web/core/registry";
import { RadioField, radioField } from "@web/views/fields/radio/radio_field";


class CustomRadioImageField extends RadioField {
    static template = "xg_simgems_plm.CustomRadioImageField";
}

registry.category("fields").add("custom_radio_image", {
    ...radioField,
    component: CustomRadioImageField,
});
