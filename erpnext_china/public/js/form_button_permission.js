const PermissionForm = class PermissionForm extends frappe.ui.form.Form {
	add_custom_button(label, fn, group) {
		let doctype = this.doctype;
		let groups = {
			'创建':['更新项目']
		};
	
		//let labels = groups[group];
		let labels = [__('Update Items')];
		


		frappe.call({
			'method': "erpnext_china.erpnext_china.doctype.button_permission.button_permission.get_button_permission",
			'args': {'doctype':doctype
					'label':__('Update Items')
			},
			'callback': function(r){
				console.log(r.message)
			}
		
		});
		

		if (labels.includes(label)) {
		 	
			// temp! old parameter used to be icon
			if (group && group.indexOf("fa fa-") !== -1) group = null;

			let btn = this.page.add_inner_button(label, fn, group);

			if (btn) {
				// Add actions as menu item in Mobile View
				let menu_item_label = group ? `${group} > ${label}` : label;
				let menu_item = this.page.add_menu_item(menu_item_label, fn, false);
				menu_item.parent().addClass("hidden-xl");

				this.custom_buttons[label] = btn;
			}
			return btn;
		}
	}
}

frappe.ui.form.Form = PermissionForm
