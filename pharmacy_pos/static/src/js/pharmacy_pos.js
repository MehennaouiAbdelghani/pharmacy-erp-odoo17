/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    /**
     * Override to add pharmacy validations
     */
    async addProductToCurrentOrder(product, options = {}) {
        // Check if product is a drug and has stock
        if (product.is_drug && product.qty_available <= 0) {
            this.env.services.popup.add("ErrorPopup", {
                title: "Out of Stock",
                body: `${product.display_name} is out of stock. Cannot sell pharmaceutical products with negative stock.`,
            });
            return;
        }

        return await super.addProductToCurrentOrder(product, options);
    },
});
