/** @odoo-module **/

import { FormRenderer } from "@web/views/form/form_renderer";
import { patch } from "@web/core/utils/patch";

patch(FormRenderer.prototype, {
    _renderTagSheet(node) {
        const $sheet = this._super(...arguments);
        const $plansContainer = $sheet.find('div[data-plan]').parent();

        if ($plansContainer.length) {
            this._reorderPlanDivs($plansContainer);
        }
        return $sheet;
    },

    _reorderPlanDivs($container) {
        const record = this.props.record.data;
        const $plans = $container.find('div[data-plan]').detach();

        const plansData = [];
        $plans.each(function() {
            const planNum = parseInt($(this).data('plan'), 10);
            const rank = record[`is_plan_${planNum}_highest`];
            plansData.push({
                plan: planNum,
                rank: rank,
                element: this
            });
        });

        plansData.sort((a, b) => a.rank - b.rank);

        plansData.forEach(data => {
            $container.append(data.element);
        });
    }
});