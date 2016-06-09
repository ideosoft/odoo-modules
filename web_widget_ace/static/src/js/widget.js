
openerp.web_widget_ace = function(instance) {	
	instance.web.form.FieldCode = instance.web.form.AbstractField.extend(instance.web.form.ReinitializeFieldMixin, {
		template: 'FieldCode',
		init: function() {
			this._super.apply(this, arguments);
		},
		initialize_content: function() {
			var self = this;
						
			//if (! this.get("effective_readonly")) {
				self._updating_editor = false;
				this.$textarea = this.$el.find('textarea');
				this.$textarea.val(this.get('value') || '');
				self._updating_editor = true;
				
				this.$textarea.css({
					'font-family': 'monospace',
					'white-space': 'pre',
					'background-color': '#FFFFE0',
					'width': '100%',
				});
				
				if(this.get("effective_readonly")) {
			    	this.$textarea.attr('disabled', 'disabled');
					this.$textarea.attr('readonly', true);
				}
				
				//this.$editor = this.$textarea.ace({ lang: this.node.attrs.lang })
			//}
		},
		render_value: function() {
			if (! this.get("effective_readonly")) {

				console.log("autosize: " + this.auto_sized);
				
				// if (this.auto_sized) {
					this.auto_sized = true;
					this.$textarea.autosize();
				//} else {
					this.$textarea.trigger("autosize");
				//}
				
				console.log("autosize: " + this.auto_sized);
				
				this.$editor = this.$textarea.ace({ lang: 'python' })
				
			} else {
				this.$textarea.val(this.get('value') || '');
				this.$editor = this.$textarea.ace({ lang: this.node.attrs.lang })
			}
				
		},
		commit_value: function () {
			if (! this.get("effective_readonly") && this.$textarea) {
				this.store_dom_value();
			}
			return this._super();
		},
		store_dom_value: function () {
			this.internal_set_value(instance.web.parse_value(this.$textarea.val(), this));
		},
	});


	instance.web.form.widgets.add('code', 'instance.web.form.FieldCode');
	instance.web.form.widgets.add('ace', 'instance.web.form.FieldCode');
	
};
